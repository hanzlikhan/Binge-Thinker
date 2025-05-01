# llm/anthropic_client.py
from anthropic import Anthropic
import streamlit as st
# Load API key securely from env
import os
client = Anthropic(
    base_url="https://api.aimlapi.com/",
    # auth_token=os.getenv("AIML_API_KEY"),
    auth_token=st.secrets["AIML_API_KEY"],
)

def call_claude(prompt: str, system_prompt: str = "You are an AI assistant who knows everything.") -> str:
    try:
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=3048,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text  # Handles response list structure
    except Exception as e:
        return f"[Error from Claude]: {str(e)}"
