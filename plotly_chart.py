#Plotly
from google.cloud import bigquery
from datetime import datetime
import pandas as pd
import plotly.express as px
import chart_studio
import chart_studio.plotly as py

filePath = "/home/wesgelpi/secrets/plotlySecret.txt"

with open(filePath, 'r') as file:
    fileContent = file.read().strip()

chart_studio.tools.set_credentials_file(username='wgelpi', api_key=fileContent)

def gcp_data(query):
    # Initialize the BigQuery client
    project_id = 'self-tape-may'
    client = bigquery.Client(project=project_id)

    #query = 
    query_job = client.query(query)  # Make an API request.

    try:
        # Convert query result to a DataFrame
        gcpdata = query_job.result().to_dataframe()  # Waits for the query to finish
        return gcpdata
    except Exception as e:
        print("Error in gcp_data:", e)
        return None

#df = gcpdata

def visualize_data_line(df, xaxis, yaxis, charttitle):
    if df is not None:
        #print(df.columns)  # Print the DataFrame columns to debug
        # Assuming 'timestamp' and 'id' are correct, update if necessary
        fig = px.line(df, x=xaxis, y=yaxis, title=charttitle)
        py.plot(fig, filename=charttitle, auto_open=True)
        #fig.show()

def visualize_data_col(df, xaxis, yaxis, charttitle):
    if df is not None:
        #print(df.columns)  # Print the DataFrame columns to debug
        # Assuming 'timestamp' and 'id' are correct, update if necessary
        fig = px.bar(df, x=xaxis, y=yaxis, title=charttitle)
        py.plot(fig, filename=charttitle, auto_open=True)
        #fig.show()

## Query data - Daily posts
#gcpdata = gcp_data("""
#        SELECT DATE(timestamp) AS date, COUNT(id) AS id_count FROM `self-tape-may.self_tape_may_data.tblInstagramData` GROUP BY date ORDER BY date;
#        """)

gcpdata = gcp_data("""SELECT
  date,
  id_count,
  SUM(id_count) OVER (ORDER BY date) AS cumulative_id_count,
  SUM(camp_count) OVER (ORDER BY date) AS cumulative_camp_count
FROM (
  SELECT
    DATE(timestamp) AS date,
    COUNT(id) AS id_count,
    COUNTIF(campaignFlag = True) AS camp_count
  FROM
    `self-tape-may.self_tape_may_data.tblInstagramData`
  GROUP BY
    date
  ORDER BY
    date
)
ORDER BY
  date;""")

# Visualize - Daily posts
visualize_data_line(gcpdata, 'date', 'id_count', 'Posts by Day')

# Visualize - Cumulative posts
visualize_data_line(gcpdata, 'date', 'cumulative_id_count', 'Cumulative by Day')

# Visualize - Cumulative posts
#visualize_data(gcpdata, 'date', 'cumulative_camp_count', 'Cumulative Campaign by Day')

gcpdata = gcp_data("""SELECT
  market,
  id_count,
  SUM(id_count) OVER (ORDER BY market) AS cumulative_id_count,
  SUM(camp_count) OVER (ORDER BY market) AS cumulative_camp_count
FROM (
  SELECT
    CASE
      WHEN p.market IS NULL THEN 'No Market'
      ELSE p.market
    END AS market,
    COUNT(i.id) AS id_count,
    COUNTIF(i.campaignFlag = True) AS camp_count
  FROM
    `self-tape-may.self_tape_may_data.tblInstagramData` i
  JOIN
    `self-tape-may.self_tape_may_data.tblSTMParticipantData` p ON p.Instagram = i.ownerUsername
  GROUP BY
    market
)
ORDER BY
  market;""")

# Visualize - Cumulative posts by Market
visualize_data_col(gcpdata, 'market', 'cumulative_id_count', 'Cumulative by Market')
