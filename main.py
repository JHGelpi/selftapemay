import bigquery_client
import apify_client
import data_processor

def main():
    users = bigquery_client.get_users()
    for user in users:
        raw_data = apify_client.scrape_instagram(user)
        cleaned_data = data_processor.process_data(raw_data)
        bigquery_client.insert_posts(cleaned_data)

if __name__ == "__main__":
    main()
