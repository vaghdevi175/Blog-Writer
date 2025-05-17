import requests
import streamlit as st
import random
import logging

logger = logging.getLogger(__name__)
UNSPLASH_API_KEY = "KYAn88o8imSvQr-6aPEO5QJ7_S2qh6RGlMeX_mTgklY"

def fetch_multiple_unsplash_images(query):
    count = random.randint(2, 5)
    url = f"https://api.unsplash.com/photos/random?query={query}&count={count}&client_id={UNSPLASH_API_KEY}"
    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        return [img["urls"]["regular"] for img in res.json() if "urls" in img]
    except Exception as e:
        st.error(f"Image error: {e}")
        logger.error(f"Unsplash error: {e}")
        return []
