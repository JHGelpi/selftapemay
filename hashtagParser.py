import csv
import chardet

# This is the file name for the initial input file downloaded from Apify
# it needs to match exactly the file.

# input_file = 'exampleJSON.json'
input_file = 'jsonOutput.csv'
output_file = 'jsonOutputFinal.csv'
selfTape = 'selftapemay'
selfTapeCampaign = 'selftapemaylotr'
selfTapeHashtag = ''
headerRow = ['id', 'ownerFullName', 'ownerUsername', 'type', 'url', 'hashtags', 'timestamp', 'productType',  'hashtag/0', 'hashtag/1', 'campaignFlag', '_id', '_createdDate', '_updatedDate', '_owner']

# This is the folder path where the Apify export file resides as well
# as the location of where the output csv will be
# file_path = 'D:\\consulting\\AudreyHelpsActors\\'
file_path = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'

# Determine encoding
def determine_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

# Determine the encoding type of the csv file
encoding = determine_encoding(file_path + input_file)

with open(file_path + input_file, newline='', encoding=encoding) as csvfile:
    reader = csv.reader(csvfile)
    with open(file_path + output_file, 'w', newline='', encoding=encoding) as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headerRow)
        for row in reader:
            #print(row)
            if len(row) < 2:  # Skip rows that do not have at least two elements
                continue
            hashtags = row[5].strip('[]').split(', ')
            
            for tag in hashtags:
                cleanHashtag = tag.strip("'")
                cleanHashtag = cleanHashtag.lower()
                #print(cleanHashtag)
                if cleanHashtag == selfTape and row[3] == 'Video':
                    lst = [s.strip(" '") for hashtag in hashtags for s in hashtag.strip("[]").split(",")]
                    for i in range(len(lst)):
                        if lst[i].lower() == selfTape or lst[i].lower() == selfTapeCampaign:
                            selfTapeHashtag = lst[i]
                            row.append(selfTapeHashtag)
                    
                    # write row to output file
                    writer.writerow(row)
                else:
                    continue
