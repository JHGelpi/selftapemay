# main.py

# Import the above modules.
# Define a main function that orchestrates the whole process:
# Retrieve user data from BigQuery.
# Pass each user to the Apify scraper.
# Process the scraped data.
# Insert the cleaned data into the tblInstagramData table.

import bigquery_client
#import apifyClient
#import data_processor

def main():
    #project_id = 'self-tape-may'
    users = bigquery_client.get_users()
    #cleaned_data = data_processor.process_data()
    #for user in users:
        #raw_data = apifyClient.scrape_instagram(user)
        #cleaned_data = data_processor.process_data(raw_data)
        #bigquery_client.insert_posts(cleaned_data)

if __name__ == "__main__":
    main()
