# 🚚 SupplyShield 2.0 – Smart Shipment Risk and AI Dashboard

> **AI-powered logistics guardian** that prevents delays, predicts disruptions, and recommends smart decisions in real time.

![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-orange?logo=streamlit)
![LangChain](https://img.shields.io/badge/langchain-enabled-blueviolet?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🧩 Real World Problem

> In global supply chains, even a **single day of port disruption** can cause millions in losses.  
> Most logistics systems lack **real time intelligence, summaries, and predictive cost logic.**

### ⚠️ Common Challenges:

| Problem | Impact |
|--------|--------|
| ❌ Delay due to weather or strikes | Missed deliveries, huge_penalties |
| ❌ No centralized risk summarizer | Teams lose time decoding reports |
| ❌ Manual decision making | Slower, inconsistent responses |
| ❌ Lack of automation | Poor communication and lost revenue |
| ❌ No historical memory | Lessons from past mistakes are lost |

---

## ✅ Our Solution – SupplyShield 2.0

| Feature | Benefit |
|--------|---------|
| 🤖 AI Risk Summarizer | Instantly explains disruption causes using Claude LLM |
| 🚨 Risk Detection Engine | Flags delays, port strikes, storms, and keywords |
| 💡 Cost Decision Engine | Simulates reroute vs penalty vs expedite costs |
| 📦 Smart Planner | Chooses best action and explains the logic |
| 💬 Auto Messaging | Sends stakeholder updates via email/Slack |
| 📊 Export Reports | PDF and CSV of risk response with just 1 click |
| 🌦 Weather + News Feed | Adds real-time context to each shipment |
| 📜 Memory Logs | Stores past risks and results for learning |

---

## 📦 Overview

SupplyShield is a full-stack AI dashboard for **live shipment tracking, risk management, and automated decision-making**.

> Claude LLM (via Anthropic API) is used to explain disruptions, recommend routes, and even write human-like update messages.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🌍 **Live Map** | Track real-time shipment locations + weather |
| 🚨 **Risk Detection** | Auto-detect delays, strikes, and more |
| 💡 **LLM Insight** | Claude generates summaries + next steps |
| 💸 **Cost Comparison** | See penalty vs reroute vs expedite logic |
| ✉️ **Auto Messages** | Generate & send Slack updates |
| 📊 **Report Export** | One-click CSV + PDF exports |
| 🧠 **Memory History** | Tracks what worked for past risks |
| 💬 **Built-in Chatbot** | Ask Claude anything from the app |
| 🔄 **Streamlit UI** | Mobile-ready, responsive dashboards |

---

## 🧪 Tech Stack

- 🧠 LLM: [Claude 3 Sonnet – Anthropic API](https://www.anthropic.com)
- 🧩 LangChain + LangGraph for decision logic
- 📊 Streamlit + Plotly for charts + UI
- 🌦️ OpenWeatherMap for weather alerts
- 📰 News API for real-time headlines
- 💬 Slack Webhooks for stakeholder comms
- 📦 ChromaDB or JSON for memory
- 📄 PDF Reports via ReportLab

---

## 🚨 Live Use Case Example

> A shipment from Karachi to Islamabad is delayed due to rain + protests.  
> SupplyShield detects “roadblock” in notes, fetches weather, flags high severity, and recommends reroute with justification + Slack alert in 4 seconds.

---

## 📸 Screenshots

> (Drop in here any screenshots like dashboard, map, planner)

---

## 🚀 Run Locally

### ✅ 1. Clone the Repo

```bash
git clone https://github.com/hanzlikhan/Binge-Thinker.git
cd Binge-Thinker
```

### ✅ 2. Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
```
### ✅ 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### ✅ 4. Add Secrets (for API keys)
- Create .streamlit/secrets.toml:

  ``` bash
       AIML_API_KEY = "your-anthropic-key"
       SLACK_WEBHOOK_URL = "https://hooks.slack.com/..."
       GNEWS_API_KEY = "your-gnews-key"
       WEATHER_API_KEY = "your-weather-key"
  ```

  ### Meet Team Members:
  ### Muhammad Hanzla
  
