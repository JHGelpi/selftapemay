# Data cleansing for apify data import
# Code writing assisted by ChatGPT :-)
import datetime
import subprocess

pythonInterpreter = "/usr/bin/python3"  # Replace with the actual path to the Python interpreter

# Windows filepath
folderLocation = 'D:\\github_projects\\selftapemay\\'

# Mac filepath
#folderLocation = '/Users/wegelpi/Nextcloud/Consulting/selfTapeMay/' 
#folderLocation = '/Users/wegelpi/github_repos/selftapemay/'

'''Order:
Initial file needs to be named 'dataset_instagram-api-scraper.json' and located in 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'
1) instagramJSONParser.py
2) hashtagParser.py
3) jsonOuputToCSV.py
4) urlDiffs.py'''

def execute_python_file(python_file):
    now = datetime.datetime.now()
    print(now, ": Executing ", python_file, "...")
    subprocess.run(['python', folderLocation + python_file])
    now = datetime.datetime.now()
    print(now, ": ", python_file, "Completed!")

execute_python_file('hashtagParser.py')
execute_python_file('jsonOuputToCSV.py')
execute_python_file('urlDiffs.py')