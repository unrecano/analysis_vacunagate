import json

def get_all_words():
    with open('files/words.json', 'r') as f:
        return json.load(f)

def get_all_mentions():
    with open('files/mentions.json', 'r') as f:
        return json.load(f)

def get_all_hashtags():
    with open('files/hashtags.json', 'r') as f:
        return json.load(f)

def get_all_locations():
    with open('files/locations.json', 'r') as f:
        return json.load(f)

def get_info():
    with open('files/info.json', 'r') as f:
        return json.load(f)['count']