import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
api_key = os.getenv("LASTFM_API_KEY")
base_url = "http://ws.audioscrobbler.com/2.0"


def weekly_track_chart(username):
    url_suffix = f"/?method=user.getweeklytrackchart&user={username}&api_key={api_key}&format=json"
    res = requests.get(base_url + url_suffix)
    return json.loads(res.text)
