# main.py

# Import the above modules.
# Define a main function that orchestrates the whole process:
# Retrieve user data from BigQuery.
# Pass each user to the Apify scraper.
# Process the scraped data.
# Insert the cleaned data into the tblInstagramData table.

import bigquery_client
import plotly_chart
from datetime import datetime

def main():
    users = bigquery_client.get_users()
    print("Completed bigquery_client.get_users() at: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "running plotly_chart...")
    plotly_chart.plotly_main()
    print("plotly_chart completed at: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()