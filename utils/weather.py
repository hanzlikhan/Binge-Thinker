import requests
import os
from dotenv import load_dotenv
from functools import lru_cache
import streamlit as st

# load_dotenv()
# API_KEY = os.getenv("WEATHER_API_KEY")

# for deploy on the streamlit 

API_KEY = st.secrets["WEATHER_API_KEY"]


@lru_cache(maxsize=32)
def get_weather(lat, lon):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
        )
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return {"error": data.get("message", "Failed to fetch weather")}

        condition = data["weather"][0]["description"].lower()
        is_alert = any(term in condition for term in ["storm", "thunder", "typhoon", "rain", "snow"])

        return {
            "condition": condition.capitalize(),
            "temperature": round(data["main"]["temp"]),
            "wind_speed": data["wind"]["speed"],
            "is_alert": is_alert
        }
    except Exception as e:
        return {"error": str(e)}
