import requests
import random
import logging

UNSPLASH_API_KEY = "your-unsplash-key-here"
logger = logging.getLogger(__name__)

def fetch_multiple_unsplash_images(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&count=3&client_id={UNSPLASH_API_KEY}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return [img["urls"]["regular"] for img in res.json()]
    except Exception as e:
        logger.error(f"Image fetch failed: {e}")
        return []
