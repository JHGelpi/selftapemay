import json

# Your hashtag lists
selftapemay_hashtag = ['selftapemay', 'selftapemay2024']
campaign_hashtag = ['selftapemaybridgerton']

# Save to a file
with open('/home/wesgelpi/self_tape_may/hashtags.json', 'w') as file:
    json.dump({
        'selftapemay_hashtag': selftapemay_hashtag,
        'campaign_hashtag': campaign_hashtag
    }, file)
