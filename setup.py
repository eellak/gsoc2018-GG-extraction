import os
import errno
import sys
import platform
import zipfile
from subprocess import call 
from src.utilities.helper import Helper

# , ... 
DEPENDENCIES = ['selenium', "pdfminer.six"]

# class DBInitializer:
#   ...

def download_latest_chromedriver_release():
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

def install_dependencies():
    # Check if pip is installed 
    try:
        import pip
    except ImportError as e:
        raise e
    
    
    if(len(DEPENDENCIES)>1):
        with open('requirements.txt', "w") as out_file:
            out_file.write("\n".join(DEPENDENCIES))
        
        # Make install cmd        
        cmd = 'pip install -r requirements.txt'
        
        # pip install 
        call(cmd, shell=True)

        # Remove requirements.txt
        rmv_reqs_cmd = 'rm -f requirements.txt'
        call(rmv_reqs_cmd, shell=True)

    else:
        # Make install cmd        
        cmd = "pip install {}".format(DEPENDENCIES)
        
        # pip install 
        call(cmd, shell=True)
    
    
def setup():
    install_dependencies()
    # db init ...
    download_latest_chromedriver_release()

if __name__ == '__main__':
    setup()