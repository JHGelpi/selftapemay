# Data cleansing for apify data import
# Code writing assisted by ChatGPT :-)
import datetime
import subprocess

pythonFile = ''
folderLocation = 'D:\\github_projects\\selftapemay\\'
'''Order:
Initial file needs to be named 'dataset_instagram-api-scraper.json' and located in 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'
1) instagramJSONParser.py
2) hashtagParser.py
3) jsonOuputToCSV.py'''

pythonFile = 'instagramJSONParser.py'
now = datetime.datetime.now()
print(now, ": Executing ", pythonFile, "...")
subprocess.run(['python', folderLocation + pythonFile])
now = datetime.datetime.now()
print(now, ": ", pythonFile, "Completed!")

pythonFile = 'hashtagParser.py'
now = datetime.datetime.now()
print(now, ": Executing ", pythonFile, "...")
subprocess.run(['python', folderLocation + pythonFile])
now = datetime.datetime.now()
print(now, ": ", pythonFile, "Completed!")

pythonFile = 'jsonOuputToCSV.py'
now = datetime.datetime.now()
print(now, ": Executing ", pythonFile, "...")
subprocess.run(['python', folderLocation + pythonFile])
now = datetime.datetime.now()
print(now, ": ", pythonFile, "Completed!")