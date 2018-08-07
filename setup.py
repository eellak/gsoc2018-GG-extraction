#!/usr/bin/env python3

import sqlite3
import os
import errno
from sys import argv as args, path
import platform
import zipfile
from subprocess import call
from src.util.helper import Helper

def init_db():
    if len(args) > 1:
        if args[1] == '--delete_db':
            print("Deleting SQLite db")
            DBSetup.delete_sqlite_db()
            return 
                
    print("Setting up local SQLite db")
    DBSetup.setup_sqlite_db()

class DBSetup:    
    @staticmethod
    def delete_sqlite_db():
        try:
            os.remove('src/data/default')
            print("SQLite db has been deleted")
        except FileNotFoundError as e:
            print("File has not been found")
        except PermissionError as e:
            print("File could not be deleted")


    @staticmethod
    def setup_sqlite_db():
        
        if not os.path.exists('src/data'):
            # Create data folder
            try:
                os.makedirs('src/data')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        db = sqlite3.connect('src/data/default')
        cursor = db.cursor()

        # Executes the default.sql to create default database schema
        install_sql = open('install/default.sql', 'r', encoding='utf8').read()
        cursor.executescript(install_sql)

        db.commit()
        cursor.close()
        db.close()


def init_chromedriver():
    '''Download latest chromedriver release'''
    if os.path.isfile('drivers/chromedriver'):
        print('chromedriver is already downloaded')
        return

    endpoint = 'https://chromedriver.storage.googleapis.com/' + '{version}/{file_name}'

    latest_release_link = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    latest_version = Helper.get_url_contents(latest_release_link).strip()

    if platform.system() == 'Linux':
        file = 'chromedriver_linux64.zip'
    elif platform.system() == 'Darwin':
        file = 'chromedriver_mac64.zip'
    elif platform.system() == 'Windows':
        file = 'chromedriver_win32.zip'
    else:
        print('Chromedriver is not supported on your OS.')
        return

    download_page = endpoint.format(version=latest_version, file_name=file)

    # Creates the data folder if not exists
    try:
        os.makedirs('drivers')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    if Helper.download(download_page, 'chromedriver.zip', 'drivers'):
        print('chromedriver.zip downloaded successfully')
        zip_ref = zipfile.ZipFile('drivers/chromedriver.zip', 'r')
        zip_ref.extractall('drivers')
        zip_ref.close()
        print('chromedriver extracted successfully from chromedriver.zip.')
        os.remove('drivers/chromedriver.zip')
        print('chromedriver.zip removed successfully')
        
        if platform.system() == 'Windows':
            os.chmod('drivers/chromedriver.exe', 0o755)
        else:
            os.chmod('drivers/chromedriver', 0o755)
    else:
        print('Downloading chromedriver for selenium failed.')    
    
def setup():
    init_db()
    init_chromedriver()
    call("make -C scripts", shell=True)

if __name__ == '__main__':
    setup()
