import bigqueryClient
import apifyClient
import dataProcessor

def main():
    users = bigqueryClient.get_users()
    for user in users:
        raw_data = apifyClient.scrape_instagram(user)
        cleaned_data = dataProcessor.process_data(raw_data)
        bigqueryClient.insert_posts(cleaned_data)

if __name__ == "__main__":
    main()
