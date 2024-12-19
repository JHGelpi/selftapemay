import requests
from utils import get_config_data, configure_logging, format_timestamp, extract_hashtags
from google.cloud import bigquery
from datetime import datetime, timezone

def init_bigquery():
    # Initialize the BigQuery client
    project_id = 'self-tape-may'
    return project_id

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

    
    if result_list:
        print("Query result fields:", result_list[0].keys())  # Check available fields
        count = result_list[0].get('count', 0)  # Use .get() to avoid KeyError
    else:
        count = 0
    
    if len(result_list) == 0:

        print("Hashtag not found in BigQuery. Creating a new hashtag ID.")
        hashtagid = hashtag_id()
        if not hashtagid:  # Check if hashtag_id creation failed
            print("Error: Failed to create a new hashtag ID.")
            return None
    else:
        print("Hashtag already exists in BigQuery.")
        hashtagid = result_list[0].hashtag_id  # Fetch the hashtag ID

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
                '''
                I need to query BigQuery table to determine if I need to call post_details().  If the post already exists in BigQuery then there is no need
                to get the data again
                '''
                query = f"SELECT id FROM `self-tape-may.self_tape_may_data.tblInstagramData` WHERE id = @id;"
                job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("id", "STRING", post['id']),
                    ]
                )
                query_job = client.query(query, job_config=job_config)
                print(f"Executing query: {query}")

                result_list = list(query_job.result())  # Convert result to a list once

                if result_list:
                    print("Query result fields:", result_list[0].keys())  # Check available fields
                    count = result_list[0].get('count', 0)  # Use .get() to avoid KeyError
                else:
                    count = 0

                if len(result_list) == 0:
                    print("Post does not exist.  Calling post_details for post ID: ", post['id'])
                    post_details(post['id'])  # Call `post_details` with the `id` from the current dictionary
                else:
                    print(f"Post {post['id']} already exists.  Exiting...")

            return hashtag_data[0]['id']  # Return the first hashtag's ID
        else:
            print("Error obtaining hashtag ID.")
    else:
        print(f"Error retrieving accounts: {response.status_code}, {response.text}")

    return None

def post_details(post_id, childpost=False, child_caption=''):
    '''This function will make the API call to obtain the post details for all the
    posts that are provided as a result of the hashtag_query() function.  This function
    should check to see if the post has already been downloaded by querying GCP before
    submitting an API request for post details.  If the post has already been downloaded
    then there is no need to perform another API call.'''
    # https://graph.facebook.com/v21.0/18111483940430632?fields=id,media_type,media_url,owner,timestamp&access_token=[redacted]

    config_data = get_config_data()
    access_token = config_data[8]
    api_version = config_data[5]
    if childpost:
        api_fields = ['id','media_type','shortcode','owner','timestamp']
    else:
        api_fields = ['id','media_type', 'shortcode', 'owner','timestamp','caption']
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

    print(f"Making request to get post details with URL: {url}")
    response = requests.get(url, params=params)
    print(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    if response.status_code == 200:
        post_data = response.json()  # Get the full JSON response
        if post_data:
            print("Post data: ", post_data)  # Print all data returned in the response
            id = post_data.get('id', '')
            owner_id = post_data.get('owner', {}).get('id', '')
            post_url = f"https://www.instagram.com/p/{post_data.get('shortcode', '')}"
            media_type = post_data.get('media_type', '')
            original_timestamp = post_data.get('timestamp', '')
            formatted_timestamp = format_timestamp(original_timestamp)
            
            caption = post_data.get('caption', '') if 'caption' in post_data else ''
            if childpost:
                # don't return to children_posts function
                print ("Child post data: ", post_data)

                get_data_and_write_to_gcp(id, post_url,media_type, formatted_timestamp, owner_id, child_caption)
                
                return post_data
            else:
                print ("Parent post data: ", post_data)

                get_data_and_write_to_gcp(id, post_url, media_type, formatted_timestamp, owner_id, caption)
                children_posts(post_id, caption)
                return post_data  # Return the entire response JSON
        else:
            print("No post details found in the response.")
    else:
        print(f"Error retrieving accounts: {response.status_code}, {response.text}")


    return None

def children_posts(post_id, caption):
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
    api_fields = ['id','media_type', 'caption']

    url = f'https://graph.facebook.com/{api_version}/{post_id}/children'
    params = {
        'user_id': user_id,
        'access_token': access_token
    }

    print(f"Making request to get children with URL: {url}")
    response = requests.get(url, params=params)
    print(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    if response.status_code == 200:
        children = response.json()
        print("children: ", children)
        if 'data' in children and len(children['data']) > 0:
            for child in children['data']:
                print("Children detected: ", child)
                # Extract the 'id' value from the child and call post_details with it
                post_details(child['id'], True, caption)
                
        else:
            print("No child posts.")

        return children
    else:
        print(f"Error retrieving accounts: {response.status_code}, {response.text}")

def user_details():
    '''This function will simply return the username based on the owner id provided when
    executing the API call in post_details().'''

def get_data_and_write_to_gcp(id, url, type, timestamp, user_id, caption, username=''):
    '''This function will obtain the data necessary (post_details, user_details) and
    then update the necessary GCP tables with the data.  It will also maintain
    the processes necessary to keep data clean and de-duplicated'''
    project_id = init_bigquery()

    table_ref = 'self-tape-may.self_tape_may_data.tblInstagramData'
    client = bigquery.Client(project=project_id)

    # Correctly extract values for insertion
    config_data = get_config_data()
    foundational_hashtag = config_data[4]
    campaign_hashtag = config_data[14]
    hashtag_0, hashtag_1 = extract_hashtags(caption, foundational_hashtag, campaign_hashtag)
    if hashtag_1 == None:
        campaign_flag = False
    else:
        campaign_flag = True

    # Prepare data for BigQuery (ensure schema compatibility)
    print (f"Preparing data for post_id: {id}")
    if type == "IMAGE":
        print (f"Not appending post {id} because it is a {type} post.")
    else:
        rows_to_insert = [{
                "id": id,
                "url": url,
                "type": type,
                "timestamp": timestamp,
                "user_id": user_id,
                "ownerUsername": username,
                "hashtags": caption,
                "hashtag_0": hashtag_0,
                "hashtag_1": hashtag_1,
                "campaignFlag": campaign_flag
            }]

        print(f"Inserting data into BigQuery: {rows_to_insert}")
        errors = client.insert_rows_json(table_ref, rows_to_insert)  # API call to append rows

        if errors == []:
            print("Data successfully appended to BigQuery.")
        else:
            print(f"Errors while appending data to BigQuery: {errors}")

if __name__ == "__main__":
    # Configure logging
    configure_logging()
    #hashtag_id()
    hashtag_query()
    #get_data_and_write_to_gcp()