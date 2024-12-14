import requests
from utils import get_config_data, configure_logging
from google.cloud import bigquery
from datetime import datetime, timezone

def init_bigquery():
    # Initialize the BigQuery client
    project_id = 'self-tape-may'
    #client = bigquery.Client(project=project_id)
    return project_id

from google.cloud import bigquery
from datetime import datetime, timezone

def hashtag_id():
    '''Function to download ID of hashtags to be used.
    This should only be run once a year to obtain the IDs for the foundational hashtag
    (#selftapemay) and the campaign hashtag (e.g. #selftapemaylotr).'''
    
    config_data = get_config_data()
    user_id = config_data[3]
    q = config_data[4]
    access_token = config_data[8]
    app_id = config_data[1]

    url = 'https://graph.facebook.com/ig_hashtag_search'
    params = {
        'user_id': user_id,
        'q': q,
        'access_token': access_token,  # This needs to be the long-lived access token
        'app_id': app_id
    }

    print(f"Making request to get hashtag ID with URL: {url} and params: {params}")
    response = requests.get(url, params=params)
    print(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    if response.status_code == 200:
        hashtag_data = response.json().get('data', [])
        if len(hashtag_data) > 0:
            print("Response data retrieved! Checking for existing hashtag ID in BigQuery...")
            project_id = init_bigquery()

            table_ref = 'self-tape-may.self_tape_may_data.tbl_instagram_hashtag_data'
            client = bigquery.Client(project=project_id)

            # Query the table to check if the hashtag_id already exists
            query = f"""
                SELECT COUNT(*) AS count
                FROM `{table_ref}`
                WHERE hashtag_id = @hashtag_id
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("hashtag_id", "STRING", hashtag_data[0]['id']),
                ]
            )
            query_job = client.query(query, job_config=job_config)
            result = query_job.result()
            row = list(result)[0]  # Fetch the first row

            if row['count'] > 0:
                print(f"Hashtag ID {hashtag_data[0]['id']} already exists in the table. Skipping insertion.")
            else:
                print("Hashtag ID does not exist. Appending to BigQuery...")
                utc_now = datetime.now(timezone.utc)
                rows_to_insert = [
                    {"hashtag": q, "hashtag_id": hashtag_data[0]['id'], "effective_start_date": utc_now.isoformat()}
                ]

                # Insert the row into the table
                errors = client.insert_rows_json(table_ref, rows_to_insert)  # Make an API request
                if errors == []:
                    print("New rows have been added.")
                else:
                    print(f"Errors occurred while inserting rows: {errors}")
                
            return hashtag_data[0]['id']
        else:
            print("No data found for the requested hashtag.")
    else:
        print(f"Error retrieving hashtag ID: {response.status_code}, {response.text}")

    return None


def hashtag_query():
    '''This function will download the recent posts from the hashtag used.
    This function will need to be called every time to obtain a list of posts that are leveraging
    the foundational hashtag (#selftapemay)'''

    project_id = init_bigquery()

    table_ref = 'self-tape-may.self_tape_may_data.tbl_instagram_hashtag_data'
    client = bigquery.Client(project=project_id)

    # Query the table to check if the hashtag_id already exists
    query = f"""
        SELECT COUNT(*) AS count
        FROM `{table_ref}`
        WHERE hashtag_id = @hashtag_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("hashtag_id", "STRING", config_data[4]),
        ]
    )
    query_job = client.query(query, job_config=job_config)
    result = query_job.result()

    if len(result) == 0:
        hashtag_id()

        # Query the table to check if the hashtag_id already exists
        query = f"""
            SELECT COUNT(*) AS count
            FROM `{table_ref}`
            WHERE hashtag_id = @hashtag_id
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("hashtag_id", "STRING", config_data[4]),
            ]
        )
        query_job = client.query(query, job_config=job_config)
        result = query_job.result()

    hashtag_id = list(result)[1]  # Fetch the first row

    config_data = get_config_data()
    user_id = config_data[3]
    access_token = config_data[8]
    #hashtag_id = ""
    url = f"https://graph.facebook.com/{hashtag_id}/recent_media"

    params = {
        'user_id': user_id,
        'access_token': access_token
    }

    print(f"Making request to get recent posts with hashtag ID with URL: {url} and params: {params}")
    response = requests.get(url, params=params)
    print(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    if response.status_code == 200:
        hashtag_data = response.json().get('data', [])
        if len(hashtag_data) > 0:
            print("Recent post data: ", hashtag_data[0]['id'])
            return hashtag_data[0]['id']
        else:
            print("Error obtaining hashtag ID.")
    else:
        print(f"Error retrieving accounts: {response.status_code}, {response.text}")

    return None

def post_details():
    '''This function will make the API call to obtain the post details for all the
    posts that are provided as a result of the hashtag_query() function.  This function
    should check to see if the post has already been downloaded by querying GCP before
    submitting an API request for post details.  If the post has already been downloaded
    then there is no need to perform another API call.'''

def user_details():
    '''This function will simply return the username based on the owner id provided when
    executing the API call in post_details().'''

def get_data_and_write_to_gcp():
    '''This function will obtain the data necessary (post_details, user_details) and
    then update the necessary GCP tables with the data.  It will also maintain
    the processes necessary to keep data clean and de-duplicated'''
    hashtag_id = hashtag_id()
    print ("Completed using: ", hashtag_id)
    #hashtag_query(hashtag_id())

if __name__ == "__main__":
    # Configure logging
    configure_logging()
    hashtag_id()
    #get_data_and_write_to_gcp()