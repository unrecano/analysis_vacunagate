import json
import os
from string import digits, ascii_letters, punctuation
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import regexp_tokenize
from pymongo import MongoClient

load_dotenv(verbose=True)

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/"

def get_frequencies(words, number=None):
    more_words = ["#vacunagate", "#vacunasgate", "vacunagate", "vacunasgate",
        "co", "si", "https", "vacunasvip", "vacunas", "solo", "ahora",
        "mientras", "hace", "va", "así", "hoy", "bien", "tan", "debe", "ver",
        "van", "puede", "ser", "cómo", "cada", "mas", "más", "quien", "sido",
        "quién"]
    stoplist = stopwords.words("spanish") \
        + list(digits) \
        + list(punctuation) \
        + list(ascii_letters) \
        + more_words
    tokens = [w for w in words if w not in stoplist]
    frecuencies = FreqDist(tokens)
    if number:
        return frecuencies.most_common(number)
    return frecuencies.most_common()

def get_all_words(text):
    words = regexp_tokenize(text.lower(), '\w+')
    frequencies = get_frequencies(words, 100)
    return {"labels": [t[0] for t in frequencies],
        "data": [t[1] for t in frequencies]}

def get_all_mentions(text):
    mentions = regexp_tokenize(text.lower(), '^@\w+')
    frequencies = get_frequencies(mentions, 50)
    return {"labels": [t[0] for t in frequencies],
        "data": [t[1] for t in frequencies]}

def get_all_hashtags(text):
    hashtags = regexp_tokenize(text.lower(), '^#\w+')
    frequencies = get_frequencies(hashtags, 50)
    return {"labels": [t[0] for t in frequencies],
        "data": [t[1] for t in frequencies]}

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.vacunagates

def get_tweets():
    collection = db.tweets
    return collection.find({})

def get_all_text(tweets):
    return "\n".join([t["text"] for t in tweets])

if __name__ == "__main__":
    tweets = get_tweets()
    text = get_all_text(tweets)
    words = get_all_words(text)
    hashtags = get_all_hashtags(text)
    mentions = get_all_mentions(text)

    with open('files/words.json', 'w') as f:
        json.dump(words, f, indent=2)

    with open('files/hashtags.json', 'w') as f:
        json.dump(hashtags, f, indent=2)

    with open('files/mentions.json', 'w') as f:
        json.dump(mentions, f, indent=2)
    
    with open('files/info.json', 'w') as f:
        json.dump({"count": db.tweets.count_documents({})}, f, indent=2)