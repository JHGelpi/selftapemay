# Data cleansing for apify data import
# Code writing assisted by ChatGPT :-)

import subprocess

pythonFile = ''
folderLocation = 'D:\\github_projects\\selftapemay\\'
'''Order:
1) instagramJSONParser.py
2) hashtagParser.py
3) jsonOuputToCSV.py'''

pythonFile = 'instagramJSONParser.py'
print("Executing " + pythonFile + "...")
subprocess.run(['python', folderLocation + pythonFile])
print(pythonFile + "Completed!")

pythonFile = 'hashtagParser.py'
print("Executing " + pythonFile + "...")
subprocess.run(['python', folderLocation + pythonFile])
print(pythonFile + "Completed!")

pythonFile = 'jsonOuputToCSV.py'
print("Executing " + pythonFile + "...")
subprocess.run(['python', folderLocation + pythonFile])
print(pythonFile + "Completed!")