# get_random_word.py
import requests
import re

def get_random_word():
    r = requests.get(
        "https://random-word-api.herokuapp.com/word?number=2",
        timeout=60,
    )
    r.raise_for_status()
    json = r.json()
    words = json[0]+" "+json[1]
    return re.sub(r"[^a-z]", " ", words).lower()

if __name__ == "__main__":
    print(get_random_word())