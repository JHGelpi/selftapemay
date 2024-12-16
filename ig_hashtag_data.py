import requests
from utils import get_config_data, configure_logging
from google.cloud import bigquery
from datetime import datetime, timezone

def init_bigquery():
    # Initialize the BigQuery client
    project_id = 'self-tape-may'
    #client = bigquery.Client(project=project_id)
    return project_id

#from google.cloud import bigquery
#from datetime import datetime, timezone

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
    config_data = get_config_data()
    user_id = config_data[3]
    access_token = config_data[8]

    table_ref = 'self-tape-may.self_tape_may_data.tbl_instagram_hashtag_data'
    client = bigquery.Client(project=project_id)

    # Query the table to check if the hashtag_id already exists
    query = f"""
        SELECT hashtag_id, COUNT(*) AS count
        FROM `{table_ref}`
        WHERE hashtag = @hashtag
        GROUP BY hashtag_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("hashtag", "STRING", config_data[4]),
        ]
    )
    
    query_job = client.query(query, job_config=job_config)
    print(f"Executing query: {query}")
    
    result_list = list(query_job.result())  # Convert result to a list once
    count = result_list[0].count if result_list else 0  # Safely check count

    if count == 0:
        # If hashtag_id does not exist, call `hashtag_id` function to create it
        print("Hashtag not found in BigQuery. Creating a new hashtag ID.")
        hashtagid = hashtag_id()
        if not hashtagid:  # Check if hashtag_id creation failed
            print("Error: Failed to create a new hashtag ID.")
            return None
    else:
        print("Hashtag already exists in BigQuery.")
        hashtagid = result_list[0].hashtag_id  # Fetch the hashtag ID

    #hashtag_id = ""
    url = f"https://graph.facebook.com/{hashtagid}/recent_media"

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
            for post in hashtag_data:  # Iterate directly over each dictionary in the list
                print("Calling post_details for post ID: ", post['id'])
                post_details(post['id'])  # Call `post_details` with the `id` from the current dictionary

            return hashtag_data[0]['id']  # Return the first hashtag's ID
        else:
            print("Error obtaining hashtag ID.")
    else:
        print(f"Error retrieving accounts: {response.status_code}, {response.text}")

    return None

def post_details(post_id, childpost=False):
    '''This function will make the API call to obtain the post details for all the
    posts that are provided as a result of the hashtag_query() function.  This function
    should check to see if the post has already been downloaded by querying GCP before
    submitting an API request for post details.  If the post has already been downloaded
    then there is no need to perform another API call.'''
    # https://graph.facebook.com/v21.0/18111483940430632?fields=id,media_type,media_url,owner,timestamp&access_token=[redacted]

    config_data = get_config_data()
    #user_id = config_data[3]
    access_token = config_data[8]
    api_version = config_data[5]
    api_fields = ['id','media_type','owner','timestamp', 'shortcode', 'caption']
    '''
    I'm going to have to leverage the children endpoint to get child data.  
    GET /{id-media-id}/children
    '''

    print ("post_id: ", post_id)
    url = f'https://graph.facebook.com/{api_version}/{post_id}'
    
    params = {
        'fields': ','.join(api_fields),
        'access_token': access_token
    }

    print(f"Making request to get post details with URL: {url} and params: {params}")
    response = requests.get(url, params=params)
    print(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    if response.status_code == 200:
        post_data = response.json()  # Get the full JSON response
        #if 'data' in post_data and len(post_data['data']) > 0:
        if post_data:
            print("Post data: ", post_data)  # Print all data returned in the response
            
            if childpost:
                # don't return to children_posts function
                return post_data
            else:
                children_posts(post_id)
                return post_data  # Return the entire response JSON
        else:
            print("No post details found in the response.")
    else:
        print(f"Error retrieving accounts: {response.status_code}, {response.text}")


    return None

def children_posts(post_id):
    '''Use this function to leverage the GET /{id-media-id}/children endpoint
    to determine if there are any children posts and the values of those children posts

    Logic should be:
    Does child post exist? Return a Y/N flag of some sort
    Return the details about the child post (id, media_type, owner, timestamp, hashtags)
    '''
    config_data = get_config_data()
    user_id = config_data[3]
    access_token = config_data[8]
    api_version = config_data[5]

    url = f'https://graph.facebook.com/{api_version}/{post_id}/children'
    params = {
        'user_id': user_id,
        'access_token': access_token
    }

    print(f"Making request to get children with URL: {url} and params: {params}")
    response = requests.get(url, params=params)
    print(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    if response.status_code == 200:
        children = response.json()
        print("children: ", children)
        if 'data' in children and len(children['data']) > 0:
            for post in children['data']:
                print("Children detected.  Passing results to post_details() ", post)
                post_details(post, True)
                
        else:
            print("No child posts.")

        return children
    else:
        print(f"Error retrieving accounts: {response.status_code}, {response.text}")

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
    #hashtag_id()
    hashtag_query()
    #get_data_and_write_to_gcp()