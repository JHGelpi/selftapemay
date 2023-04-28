# Data cleansing for apify data import
# Code writing assisted by ChatGPT :-)

import subprocess

pythonFile = ''
folderLocation = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'
'''Order:
1) instagramJSONParser.py
2) hashtagParser.py
3) jsonOutputToCSV.py'''

pythonFile = 'instagramJSONParser.py'
print("Executing instagramJSONParser.py to import raw JSON from apify actor.")
subprocess.run(['python', folderLocation + pythonFile])

pythonFile = 'hashtagParser.py'
print("Executing the process to take the initial CSV and clean/shape the data.")
subprocess.run(['python', folderLocation + pythonFile])

pythonFile = 'jsonOutputToCSV.py'
print("Executing the final process to prepare the data for GCP upload.")
subprocess.run(['python', folderLocation + pythonFile])