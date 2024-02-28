
# bigquery_client.py
# Functions to connect to BigQuery, query the tblInstagramUsers table, and insert data into the tblInstagramData table.
# Use the Google Cloud Python SDK for BigQuery.

from google.cloud import bigquery

# Initialize the BigQuery client
client = bigquery.Client()

def get_users():
    # Function to retrieve user data from BigQuery

    # Retrieve user data from the BigQuery table.
    query = """
        SELECT * FROM `self-tape-may.self_tape_may_data.tblInstagramUsers`
    """
    query_job = client.query(query)  # Make an API request.
    
    try:
        users = query_job.result()  # Waits for the query to finish
        return users
    except Exception as e:
        print("Error in get_users:", e)
        return None

users = get_users()

if users is not None:
    # print("Results:")
    for user in users:
        # For every user I neeed to loop through and call the apify_client.py code
        print(user['instagramHandle'])
else:
    print("No users found or an error occurred.")

'''
def insert_posts(data):
    # Function to insert data into the BigQuery 'tblInstagramData' table
    pass
'''

