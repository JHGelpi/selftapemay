# selftapemay
Self Tape May code

## Purpose
This project is focused on scraping hashtag data from Instagram and summarizing it to be uploaded into a data repository to be then presented for selftapemay.com consumption.  The data is primarily used for a leaderboard as part of the "Self Tape May" project.

## Data Acquisition
This will outline how data is acquired for the leaderboard on selftapemay.com

### [Apify](https://console.apify.com/)
#### To capture Videos
The first step is to leverage the existing Apify `apify/instagram-api-scraper` web scraper.  This is done by using the Instagram API Scraper actor https://console.apify.com/actors/RB9HEZitC8hIUXAha/console.
Steps:
1) Navigate to the 'Actors' section within Apify
2) Select `Instagram API Scraper`
3) Open up Google BigQuery and run the query titled `selectInstagramHandles`
4) Export query results and copy/paste the `instagramURL` column into the `Add Instagram URLs you want to scrape (optional)` field in the Apify actor by clicking on `Bulk edit`
4) Modify the `Timeframe Newer than` value to cover the proper timeframe.
    - I will default this to 5/1/2023
5) Click `Save`
6) Click `Start`
7) After results are returned export the results to **JSON** file format and save to the local drive
8) File name should be `dataset_instagram-api-scraper.json` otherwise it won't get picked up
9) Folder path should match the `file_path` variables within the python scripts listed in [main.py](https://github.com/JHGelpi/selftapemay/blob/main/main.py)
10) Run the [main.py](https://github.com/JHGelpi/selftapemay/blob/main/main.py) python script
11) Script will output the needed columns in a file named `videoOutput.csv`.

### GCP
Once the [main.py](https://github.com/JHGelpi/selftapemay/blob/main/main.py) python script has completed successfully you will need to upload the `videoOutput.csv` file into GCP.  To do this:
1) Log into console.cloud.google.com and navigate to BigQuery
2) Upload data by using the `Local file` option
    - There is an `Add Data` button that you need to click
    - This button will give you a prompt and you need to select `Local file`
4) You will be presented with prompts:
    - `Create table from` should have the value of `Upload`
    - `Select file` should have the `videoOutput.csv` file
    - `File format` should automatically change to `csv`.  If it doesn't - change it to `csv`
    - `Project` should be `self-tape-may`
    - `Dataset` should be `self_tape_may_data`
    - `Table` should be `tblInstagramData`
    - `Table type` should be `Native table`
    - `Schema` should have `Auto detect` **checked**
    - Under `Advanced options`
      - `Write preference` should be `Overwrite Table`
    - All other values should be left to whatever they default to
    - Click `Create Table`
5) Once the data has been uploaded into `tblInstagramData` the data is available at selftapemay.com.  This is because there is a live view `view-stm-leaderboard` that presents the data to selftapemay.com.
    - Code for `view-stm-leaderboard` can be found in the file [view-stm-leaderboard.sql](https://github.com/JHGelpi/selftapemay/blob/main/view-stm-leaderboard.sql) in this repo 
#### GCP data documentation
- tblSTM2022Data
    - This has the 2022 data structured with the necessary fields for the Leaderboard
- tblInstagramData
    - This table is used to store the data that is downloaded from Instagram daily and will serve as the source for all new self tapes
- tblSTMParticipantData
    - This is the operational data store for user profiles.  This will store the data related to a person (Instagram Handle, Market, Email address, etc.)
- view-stm-leaderboard
    - This is a view and is intended to combine `tblSTM2022Data`, `tblInstagramData`, and `tblSTMParticipantData`
    - This view does a `JOIN` on instagram accounts to only show data for people from last year if and only if they participated this year
    - The results of this view should show:
        - New people who started participating for the first time this year
        - People who may have participated in the past, but did not participate last year
        - People who have participated both this year AND last year
            - In this case the data from last year will be added to their profile (so it'll show what they entered last year in terms of years participating/years achieving 16 self tapes with last year's data incrementing their history)
- viewSTMParticipantData
    - This stores the current row of data for participant data.  The Self Tape May Profile data is **APPENDED** to tblSTMParticipantData and thus this view pulls in the current record will all of the most recent data for that participant.
