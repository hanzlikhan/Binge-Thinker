# SupplyShield: AI-Powered Supply Chain Resilience

SupplyShield is an AI-driven platform designed to enhance supply chain resilience by proactively detecting risks, generating contingency plans, and automating communications. By leveraging real-time data and open-source large language models (LLMs), it helps businesses mitigate disruptions, reduce costs, and maintain customer satisfaction.

---

## Problem Statement

Supply chain disruptions—such as natural disasters (e.g., typhoons, floods), geopolitical events (e.g., strikes, embargoes), shipment delays (e.g., port congestion, customs issues), and supplier shutdowns (e.g., factory closures, raw material shortages)—cost companies billions annually. Existing systems are reactive, notifying teams only after issues occur, resulting in:

- **Costly penalties**
- **Stockouts**
- **Dissatisfied customers**
- **Lost sales and reputational damage**

The absence of predictive risk detection and automated decision-making delays responses and increases operational inefficiencies.

---

## Solution: SupplyShield

SupplyShield is a proactive AI tool that serves as an early warning system for supply chain risks. It analyzes real-time data, predicts disruptions, generates actionable plans, and communicates solutions automatically. SupplyShield empowers companies to:

- **Prevent Disruptions:** Identify risks before they escalate.
- **Optimize Costs:** Compare contingency plans to minimize expenses.
- **Streamline Operations:** Automate planning and communication.
- **Protect Reputation:** Ensure timely deliveries and customer trust.

---

## Key Features

- **Real-Time Risk Detection:** Monitors shipment, weather, and news data to identify risks (e.g., typhoons, strikes).
- **Risk Summarization:** Uses LLMs to produce concise risk summaries.
- **Disruption Severity Prediction:** Classifies risks as High, Medium, or Low based on impact.
- **Auto-Generated Contingency Plans:** Suggests actions like rerouting, air freight, or delay acceptance.
- **Cost Comparison:** Evaluates plan costs (e.g., air freight vs. delay penalties).
- **Automated Communication:** Generates professional email or Slack drafts for team updates.
- **Live Dashboard:** Displays shipments, risks, and plans in real-time.
- **Risk History:** Stores past risks and outcomes for analysis.
- **Manual Override:** Allows users to modify AI recommendations.

---

## Benefits

- **Proactive Action:** Mitigate risks before they impact operations.
- **Faster Decisions:** Automated plans reduce manual analysis time.
- **Cost Efficiency:** Select cost-effective solutions.
- **Seamless Communication:** Keep teams informed effortlessly.
- **Competitive Edge:** Leverage AI for faster, more reliable supply chains.

---

## Tech Stack

| **Component**         | **Technology**                                                                 |
|------------------------|-------------------------------------------------------------------------------|
| **Frontend**           | Streamlit (responsive, rapid prototyping)                                    |
| **AI Framework**       | LangChain (prompt chaining), LangGraph (agent orchestration)                 |
| **LLM**                | Mistral-7B-Instruct-v0.1 (Hugging Face, open-source)                         |
| **Database**           | ChromaDB (vector database for risk history)                                 |
| **Embedding Model**    | SentenceTransformer (all-MiniLM-L6-v2) for vector embeddings                |
| **Data Sources**       | Mock APIs (shipment, news, weather); extensible to NewsAPI, OpenWeatherMap  |
| **Communication**      | Mock Slack/SendGrid APIs (console output); extensible to real APIs          |
| **Hosting**            | Streamlit Cloud (free tier), Render, or Railway for production              |

---

## System Architecture

```plaintext
[Data Sources: Shipment, News, Weather]
       ↓
[Risk Detection Agent] → [LLM Summarization Agent] → [Plan Generation Agent]
       ↓                          ↓                           ↓
[ChromaDB: History]       [Streamlit UI]             [Communication Agent]
       ↓                                                  ↓
[Risk History Queries]                              [Slack/Email Notifications]
```

---

## Agents

SupplyShield uses a modular agent-based architecture via LangGraph:

- **Risk Detection Agent:** Identifies risks by matching shipment locations with news/weather data.
- **Risk Summarization Agent:** Generates concise risk summaries using the LLM.
- **Plan Generation Agent:** Suggests contingency plans with cost estimates.
- **Communication Agent:** Creates email/Slack drafts for team updates.
- **History Storage Agent:** Stores risk and plan data in ChromaDB.

---

## Frontend Design

The frontend is a multi-page Streamlit application with a clean, user-friendly interface. Pages are accessible via a sidebar, and the design is responsive with a professional color scheme (blue for trust, white for clarity, red/orange for alerts).

### Pages

1. **Home Dashboard**
   - **Sections:** Risk Alerts, Shipment Status, Priority Actions.
   - **Features:** Displays risks (order ID, description, severity), shipment details (order ID, origin, destination, ETA, priority), and recommended plans with costs.
   - **UI Elements:** Color-coded tables, refresh button, metrics for risk counts.

2. **Shipment Tracker**
   - **Sections:** Shipment List, Search.
   - **Features:** Expandable shipment details, search by order ID/priority, JSON export.
   - **UI Elements:** Expanders, search bar, download button.

3. **Risk Center**
   - **Sections:** Detected Risks, Raw News/Weather Data.
   - **Features:** Shows risks with LLM summaries, collapsible raw data views.
   - **UI Elements:** Tables, expanders, markdown summaries.

4. **Plans & Recommendations**
   - **Sections:** Contingency Plans, Communication Drafts.
   - **Features:** Lists plans with costs, shows email/Slack drafts, allows plan approval.
   - **UI Elements:** Tables, expanders, download button for drafts.

5. **Risk History**
   - **Sections:** Past Risks, Search.
   - **Features:** Queries ChromaDB for historical risks, filters by date/order ID, JSON export.
   - **UI Elements:** Tables, date pickers, download button.

6. **Settings**
   - **Sections:** Manual Overrides, Threshold Settings.
   - **Features:** Modify plans, adjust risk severity thresholds (e.g., impact days).
   - **UI Elements:** Selectbox, text area, sliders, apply/reset buttons.

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Git
- Hugging Face account (for API key)

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/supplyshield.git
   cd supplyshield
   ```

2. **Install Dependencies:** Create a `requirements.txt` file:
   ```plaintext
   streamlit
   langchain
   langgraph
   transformers
   torch
   chromadb
   sentence-transformers
   python-dotenv
   ```
   Install:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Hugging Face API Key:** Create a `.env` file:
   ```plaintext
   HUGGINGFACEHUB_API_TOKEN=your_token_here
   ```
   Or set the environment variable:
   ```bash
   export HUGGINGFACEHUB_API_TOKEN='your_token_here'
   ```

4. **Run Locally:**
   ```bash
   streamlit run app.py
   ```
   Access at [http://localhost:8501](http://localhost:8501).

5. **Deploy to Streamlit Cloud:**
   - Push code to a GitHub repository.
   - Connect the repository in Streamlit Cloud.
   - Add `HUGGINGFACEHUB_API_TOKEN` to secrets.
   - Deploy the app.

---

## Usage

- **Navigate Pages:** Use the sidebar to access different pages (Home Dashboard, Shipment Tracker, etc.).
- **Monitor Risks:** View real-time risk alerts and summaries in the Risk Center.
- **Review Plans:** Check and approve contingency plans in Plans & Recommendations.
- **Access History:** Query past risks in Risk History with date or order ID filters.
- **Customize Settings:** Override plans or adjust thresholds in Settings.

---

## Sample Outputs

- **Detected Risk:** `ORD-1001: Typhoon in Shanghai (High)`
- **Contingency Plan:** Expedite `ORD-1001` via Air Freight ($5000)
- **Email Draft:**
  ```plaintext
  Subject: Shipment Risk Alert — ORD-1001
  Dear Supply Chain Team,
  A severe typhoon is forecasted for Shanghai, potentially delaying ORD-1001 by 3 days.
  We recommend expediting via air freight at $5000.
  Please review and approve.
  Best, SupplyShield Bot
  ```

---

## Future Enhancements

- **Live Data APIs:** Integrate NewsAPI, OpenWeatherMap, Slack, and SendGrid.
- **React Frontend:** Migrate to React + TailwindCSS for a polished UI.
- **Advanced Agents:** Implement multi-agent collaboration or tool-calling.
- **Scalable Database:** Use hosted ChromaDB or PostgreSQL for production.
- **User Authentication:** Add login functionality via Streamlit or Firebase.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit changes:
   ```bash
   git commit -m 'Add your feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or feedback, open an issue on GitHub or contact `khangormani79@gmail.com` `ayeshasaleem853@gmail.com`
