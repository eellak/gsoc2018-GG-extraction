#!/usr/bin/env python3

"""
Fetch Greek Government Gazette issues from 'http://www.et.gr/idocs-nph/search/fekForm.html'

Modified from:
https://github.com/eellak/gsoc2018-3gm/blob/master/scripts/fetcher.py

Original:
https://github.com/arisp8/gazette-analysis/blob/master/mmu/automations/loader.py

Usage: ./fetch.py -h
"""

import argparse
import time
from selenium import webdriver
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotVisibleException
from bs4 import BeautifulSoup
import os
import errno
import glob
import os.path
import datetime
import platform
import sys
sys.path.append('../src')
from util.helper import Helper
from main.fetcher import Fetcher 


def handle_download(download_page, params):
    """Original function"""

    global output_dir
    print(params)

    filename = archive_format(params) + ".pdf"
    volumes = {
        'Α' : 'A',
        'Β' : 'B'
    }
    vol = volumes[params['issue_type']]
    year = params['issue_date'].year

    dirs = '{}/{}/{}'.format(vol, year, filename[6:9])
    os.system('mkdir -p {}/{}'.format(output_dir, dirs))
    outfile = '{}/{}/{}'.format(output_dir, dirs, filename)

    if os.path.isfile(outfile):
       print('Already a file')
       return

    try:
        # First we get the redirect link from the download page
        html = Helper.get_url_contents(download_page)
        beautiful_soup = BeautifulSoup(html, "html.parser")
        meta = beautiful_soup.find("meta", {"http-equiv": "REFRESH"})
        download_link = meta['content'].replace("0;url=", "")

        # We do the same process twice because it involves 2 redirects.
        beautiful_soup = BeautifulSoup(
            Helper.get_url_contents(download_link), "html.parser")
        meta = beautiful_soup.find("meta", {"http-equiv": "REFRESH"})
        download_link = meta['content'].replace("0;url=", "")
    except BaseException as e:
        print(e)
        return None
    Helper.download(download_link, filename, output_dir + '/' + dirs)
    return filename

def archive_format(params):
    # Format for Internet Archive
    volumes = {
        'Α' : '01',
        'Β' : '02'
    }

    num =  params['issue_number']
    full_num = '{}{}'.format('0' * (5 - len(num)), num)
    vol = volumes[params['issue_type']]
    year = params['issue_date'].year
    archive_format = '{}{}{}'.format(year, vol, full_num)
    return archive_format


def extract_download_links(html, issue_type):
    """Original Function"""
    global specific_issues
    if specific_issues is not None and not specific_issues:
        print('No more issues in specific_issues')
        exit()
    filenames = []
    beautiful_soup = BeautifulSoup(html, "html.parser")
    result_table = beautiful_soup.find("table", {"id": "result_table"})
    rows = result_table.find_all("tr")

    if result_table.find("ul", {"id": "sitenav"}):
        start_row = 2
        end_row = -1
    else:
        start_row = 1
        end_row = len(rows)

    # We ignore the first 2 rows if there's pagination or the first row if
    # there's not and the last one

    # print(len(rows[start_row:end_row]))

    for row in rows[start_row:end_row]:
        cells = row.find_all("td")
        info_cell = cells[1].find("b")
        download_cell = cells[2].find_all("a")

        info_cell_text = info_cell.get_text()
        info_cell_text = ' '.join(info_cell_text.split())
        info_cell_parts = info_cell_text.split(" - ")

        issue_title = info_cell_text
        issue_date = info_cell_parts[1]
        issue_title_first = issue_title.split("-")[0]
        issue_number = re.search(
            pattern=r'\d+',
            string=issue_title_first).group(0)

        if specific_issues is not None:
            # print(specific_issues, type(specific_issues))
            if not specific_issues:
                # No more of the given issues to download
                print('No more issues in specific_issues to download, bye bye...')
                exit()
            elif int(issue_number) not in specific_issues:  
                # Skip any issue not in given list
                # print(int(issue_number), ' not in specific_issues list, continuing...')
                continue
            else:
                # If issue in given list: remove 
                # from remaining specified_issues
                specific_issues.remove(int(issue_number))

        date_parts = issue_date.split(".")
        issue_unix_date = datetime.datetime(
            day=int(
                date_parts[0]), month=int(
                date_parts[1]), year=int(
                date_parts[2]))

        download_path = download_cell[1]['href'] if len(
            download_cell) > 1 else download_cell[0]['href']
        download_link = "http://www.et.gr" + download_path
        params = {
            "issue_title": issue_title,
            "issue_date": issue_unix_date,
            "issue_number": issue_number,
            "issue_type": issue_type}
        print('Download Link')
        print(download_link)
        filename = handle_download(download_link, params)
        filenames.append(filename)
        if specific_issues:
            print(specific_issues, ' remaining...')

    return filenames

if __name__ == '__main__':

    # Parse Command Line Arguments
    parser = argparse.ArgumentParser(
        description='''Fetch Greek Government Gazette Issues from the ET.
        ''', 
        formatter_class=argparse.RawTextHelpFormatter)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '-date_from',
        help='Date from in DD.MM.YYYY format',
        required=True)
    required.add_argument(
        '-date_to',
        help='Date to in DD.MM.YYYY format',
        required=True)
    required.add_argument(
        '-output_dir',
        help='Output Directory',
        required=True)
    optional.add_argument(
         '--specific_issues',
        help='In [int_1, int_2, ..., int_N] format')
    optional.add_argument(
        '--chromedriver',
        help='Chrome driver executable')
    optional.add_argument(
        '--upload',
        help='Upload to database',
        action='store_true'
    )
    optional.add_argument(
        '--type',
        help="Government Gazette document type (Teychos)\nPossible types (default='Α'):\
        \n'Α', 'Β', 'Γ', 'Δ',\
        \n'Ν.Π.Δ.Δ.', 'Α.Π.Σ.', 'ΠΑΡΑΡΤΗΜΑ', 'Δ.Ε.Β.Ι.',\
        \n'Α.ΕΙ.Δ.', 'Α.Σ.Ε.Π.', 'ΑΕ-ΕΠΕ', 'Δ.Δ.Σ.',\
        \n'Ο.Π.Κ.', 'Υ.Ο.Δ.Δ.', 'Α.Α.Π.'",
        default='Α'
    )

    args = parser.parse_args()

    date_from = args.date_from
    date_to = args.date_to
    chromedriver_executable = args.chromedriver

    if not chromedriver_executable:
        print('Chrome driver not specified. Trying ../drivers/chromedriver')
        chromedriver_executable = '../drivers/chromedriver'

    global output_dir
    output_dir = args.output_dir
    Helper.make_dir(output_dir)
    
    global specific_issues
    specific_issues = list(map(int, args.specific_issues.strip('[]').split(',')))\
                      if args.specific_issues else args.specific_issues

    if specific_issues:
        try:
            assert all(isinstance(spec_issue, int) for spec_issue in specific_issues)
        except:
            print("SPECIFIC_ISSUES must be a list of [int_1, int_2, ..., int_N] format")
            exit()

    print(
        'Fetching Government Gazette Issues{}from {} to {}'.format(
            ': ' + str(specific_issues) + ' ' if specific_issues else '',
            date_from,
            date_to))

    # Initialize Driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(
            chromedriver_executable,
            chrome_options=options)
    except BaseException as e:
        print('Could not find chromedriver. Exiting')
        print(e)
        exit()

    driver.get('http://www.et.gr/idocs-nph/search/fekForm.html')

    driver.find_element_by_name("showhide").click()

    # Enter Details
    driver.find_element_by_name("fekReleaseDateTo").clear()
    driver.find_element_by_name("fekReleaseDateTo").send_keys(date_to)
    driver.find_element_by_name("fekReleaseDateFrom").clear()
    driver.find_element_by_name("fekReleaseDateFrom").send_keys(date_from)

    driver.find_element_by_name("fekEffectiveDateTo").clear()
    driver.find_element_by_name("fekEffectiveDateTo").send_keys(date_to)
    driver.find_element_by_name("fekEffectiveDateFrom").clear()
    driver.find_element_by_name("fekEffectiveDateFrom").send_keys(date_from)

    # Multiple issues support
    possible_issues = dict(zip(['Α', 'Β', 'Γ', 'Δ',
                              'Ν.Π.Δ.Δ.', 'Α.Π.Σ.', 'ΠΑΡΑΡΤΗΜΑ', 'Δ.Ε.Β.Ι.',
                              'Α.ΕΙ.Δ.', 'Α.Σ.Ε.Π.', 'ΑΕ-ΕΠΕ', 'Δ.Δ.Σ.',
                              'Ο.Π.Κ.', 'Υ.Ο.Δ.Δ.', 'Α.Α.Π.'],
                               range(1, 16)))

    type_id = possible_issues[args.type]
    # Get correct checkbox
    checkbox_id = 'chbIssue_' + str(type_id)
    issue_type = driver.find_element_by_id("label-issue-id-" + str(type_id)).text
    try:
        # Checks the box for this certain type of issues
        driver.find_element_by_name(checkbox_id).click()
    except ElementNotVisibleException as e:
        raise Exception("Issue type: '{}' is not available.".format(str(args.type)))
    driver.find_element_by_id("search").click()

    filenames = []

    try:
        # By default we'll see the first page of results, well.. first
        active_page = 1

        # Gets the pagination list items
        pages = driver.find_elements_by_class_name("pagination_field")
        # If there's no paginations then there's one page (max)
        num_pages = len(pages) if len(pages) else 1

        for current_page in range(0, num_pages):

            # Extract and handle download links.
            filenames_ = extract_download_links(driver.page_source, issue_type)

            # if args.upload:
            #     filenames.extend(filenames_)

            # We have to re-find the pagination list because the DOM has been
            # rebuilt.
            pages = driver.find_elements_by_class_name("pagination_field")
            # Loads the next page of results
            if current_page + 1 < len(pages):
                pages[current_page + 1].click()
                time.sleep(1)

    except AttributeError:
        print('Could not find results')

    finally:
        if specific_issues:
            print(specific_issues, ' not found.')
        driver.quit()

        # if args.upload:
        #     import uploader
        #     uploader.upload(filenames)