# selftapemay
Self Tape May code

## Purpose
This project is focused on scraping hashtag data from Instagram and summarizing it to be uploaded into a data repository to be then presented for selftapemay.com consumption.  The data is primarily used for a leaderboard as part of the "Self Tape May" project.

## Data Acquisition
This will outline how data is acquired for the leaderboard on selftapemay.com

### Apify
The first step is to leverage the existing Apify Instagram web scraper.  This is done by using the Instagram Hashtag Scraper actor https://console.apify.com/actors/reGe1ST3OBgYZSsZJ.
Steps:
1) Navigate to the 'Actors' section within Apify
2) Select `Instagram Hashtag Scraper` published by zuzka (zuzka/instagram-hashtag-scraper)
3) Add the necessary Instagram hashtags to scrape
  - The value should be `selftapemaye2023`
4) Modify the `Number of posts per hashtag` value to cover all possible hashtags.
  - I will default this to 5000
5) Click `Save`
6) Click `Start`
7) After results are returned export the results to **CSV** file format and save to the local drive
8) File name should match the `input_file` variable in the [apify-data-cleansing](https://github.com/JHGelpi/selftapemay/blob/main/apify-data-cleansing) file
9) Folder path should match the `file_path` variable in the [apify-data-cleansing](https://github.com/JHGelpi/selftapemay/blob/main/apify-data-cleansing) file
