# main.py

# Import the above modules.
# Define a main function that orchestrates the whole process:
# Retrieve user data from BigQuery.
# Pass each user to the Apify scraper.
# Process the scraped data.
# Insert the cleaned data into the tblInstagramData table.

import bigquery_client
import plotly_chart
#import datetime
#import subprocess

def main():
    #project_id = 'self-tape-may'
    users = bigquery_client.get_users()
    plotly_chart.plotly_main()

#def gen_plotly():
#    python_file = 'plotly_chart.py'
#    folderLocation = '/home/wesgelpi/github/selftapemay/'
#    subprocess.run(['python', folderLocation + python_file])

if __name__ == "__main__":
    main()