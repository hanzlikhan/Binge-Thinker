import os
import requests
from dotenv import load_dotenv
import streamlit as st 
# load_dotenv()

# SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# for deploy on the stramlit
SLACK_WEBHOOK_URL = st.secrets["SLACK_WEBHOOK_URL"]

def send_slack_message(message: str):
    if not SLACK_WEBHOOK_URL:
        return False, "Webhook not configured"

    payload = {"text": message}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            return True, "✅ Message sent to Slack!"
        else:
            return False, f"❌ Slack error {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"❌ Exception: {e}"
