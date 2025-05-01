import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus  # ✅ for safe URL encoding
import streamlit as st
# load_dotenv()

GNEWS_API_KEY = st.secrets["GNEWS_API_KEY"]

def fetch_news(query: str, max_articles=3):
    try:
        if not GNEWS_API_KEY:
            return [{"title": "Missing GNEWS API key", "url": "#"}]

        clean_query = quote_plus(query.strip())
        full_query = f"{clean_query}+port+shipping+delay+strike"

        url = (
            f"https://gnews.io/api/v4/search?"
            f"q={full_query}&lang=en&country=us&max={max_articles}&token={GNEWS_API_KEY}"
        )

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])
        if not articles:
            return [{"title": "No relevant news found.", "url": "#"}]

        return [{"title": article["title"], "url": article["url"]} for article in articles]

    except Exception as e:
        return [{"title": f"News API error: {str(e)}", "url": "#"}]
