#!/usr/bin/env python3

"""
Convert all pdfs of a given dir to txt with pdfminer.six's pdf2txt.py

Modified from: 
https://github.com/eellak/gsoc2018-3gm/blob/master/scripts/converter.py

Usage: ./convert.py -h
"""

import os
import multiprocessing
import argparse
import logging
import glob
import sys
sys.path.append('../src')
from main.parser import Parser
from util.helper import Helper

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def job(x):
    global pdf2txt
    global output_dir
    global count
    # global upload
    y = x.replace('.pdf', '.txt')
    if output_dir:

        y = output_dir + y.split('/')[-1]
    if not os.path.isfile(y):
        if output_dir:
            os.system('{} {} > {}'.format(pdf2txt, x, y))
            Parser().get_pdf_text(x, y)
        else:
            os.system('{} {}'.format(pdf2txt, x))

        logging.info('{} Done'.format(x))
    else:
        logging.info('{} already a converted file'.format(x))

    count.value += 1
    logging.info('Complete {} out of {}'.format(int(count.value), total))

    return y


def list_files(input_dir, suffix, recursive=True):
    if recursive:
        result = []
        
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith(suffix):
                    result.append(os.path.join(root, file))
    else:
        result = glob.glob('{}*{}'.format(input_dir, suffix))
        print(input_dir, result)
    
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Convert pdfs to txts.
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-pdf2txt', help='pdf2txt.py Executable')
    required.add_argument('-input_dir', help='Input Directory')
    optional.add_argument('-output_dir', help='Output Directory (if omitted output goes to stdout)')
    optional.add_argument(
        '--njobs',
        help='Number of parallel jobs (default = 1)',
        type=int,
        default=1)
    optional.add_argument(
        '--tmp',
        help='Temporary files directory (default /var/tmp)',
        default='/var/tmp/')
    # optional.add_argument(
    #     '--resolution',
    #     help='Resolution of Images in DPI (default 300 dpi)',
    #     type=int,
    #     default=300)

    optional.add_argument(
        '--recursive',
        dest='recursive',
        help='Recursive option (default true)',
        action='store_true')

    # optional.add_argument(
    #     '--upload',
    #     dest='upload',
    #     help='Upload to database',
    #     action='store_true')

    args = parser.parse_args()

    global input_dir
    global output_dir
    global pdf2txt
    global tmp
    global resolution
    input_dir = args.input_dir
    output_dir = args.output_dir
    pdf2txt = args.pdf2txt
    tmp = args.tmp
    # resolution = args.resolution
    recursive = args.recursive
    # upload = args.upload

    njobs = args.njobs
    if output_dir:
        Helper.make_dir(output_dir)
        if not output_dir.endswith('/'): output_dir = output_dir + '/'

    pdfs = list_files(input_dir, '.pdf', recursive=recursive)
    txts = list_files(input_dir, '.txt', recursive=recursive)

    global total
    total = len(pdfs)
    global count
    count = multiprocessing.Value('d', 0)
    # use multiprocessing for multiple jobs
    pool = multiprocessing.Pool(int(njobs))
    results = pool.map(job, pdfs)
    
    # if upload:
    #     print('Batch upload to database')
    #     uploader.upload(results)