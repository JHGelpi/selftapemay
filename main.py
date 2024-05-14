# main.py

# Import the above modules.
# Define a main function that orchestrates the whole process:
# Retrieve user data from BigQuery.
# Pass each user to the Apify scraper.
# Process the scraped data.
# Insert the cleaned data into the tblInstagramData table.

import bigquery_client
import plotly_chart
import datetime
#import subprocess

def main():
    #project_id = 'self-tape-may'
    print("starting to run bigquery_client.get_users() at: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    users = bigquery_client.get_users()
    print("Completed bigquery_client.get_users() at: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "running plotly_chart...")
    plotly_chart.plotly_main()
    print("plotly_chart completed at: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#def gen_plotly():
#    python_file = 'plotly_chart.py'
#    folderLocation = '/home/wesgelpi/github/selftapemay/'
#    subprocess.run(['python', folderLocation + python_file])

if __name__ == "__main__":
    main()