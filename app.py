# SupplyShield 2.0 - Smart Shipment Guardian
# A Streamlit-based application for real-time shipment monitoring, risk detection, and contingency planning.
# Author: Muhammad Hanzla
# Contact: khangormani79@gmail.com

import streamlit as st
from dotenv import load_dotenv
from styles.layout_config import apply_layout
from llm.anthropic_client import call_claude
from logic.severity_score import assess_severity
from utils.weather import get_weather
from logic.risk_detection import detect_risks
from utils.slack import send_slack_message
from utils.history import log_risk_entry
import pandas as pd
import json
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from logic.summarizer import summarize_risk
from logic.planner import decide_action, explain_action
from logic.cost_analysis import estimate_costs, recommend_cheapest_action, explain_cost_decision
from logic.messenger import generate_update_message
import json


# Load environment variables from .env file
load_dotenv()

# Apply custom layout configurations for consistent UI styling
apply_layout()

# Sidebar navigation for user to switch between app sections
st.sidebar.markdown("## 🧭 Navigation")
section = st.sidebar.radio("Go to", [
    "📜 Instructions",
    "📊 Dashboard",
    "🚨 Risk Watch",
    "📦 Planner",
    "🧾 Reports & Input",
    "💬 Chat with Me",
    "ℹ️ About"
])

# Main app title
st.title("🚚 SupplyShield 2.0 – Smart Shipment Guardian")

# Dashboard Section: Displays shipment map, weather, risks, and cost charts
if section == "📊 Dashboard":
    import json
    import pandas as pd
    import plotly.express as px
    from utils.weather import get_weather
    from logic.severity_score import assess_severity
    from logic.cost_analysis import estimate_costs
    from logic.risk_detection import detect_risks

    # Custom CSS for shipment cards and styling
    st.markdown("""
        <style>
        .shipment-card {
            background: linear-gradient(135deg, #f9f9f9, #e9f0fa);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        }
        .shipment-title {
            font-size: 1.2rem;
            font-weight: bold;
            color: #34495e;
            margin-bottom: 0.3rem;
        }
        .weather-info {
            font-size: 0.95rem;
            color: #2c3e50;
        }
        </style>
    """, unsafe_allow_html=True)

    # Subsection header and caption for shipment tracking
    st.subheader("📍 Shipment Map & Conditions")
    st.caption("Track shipment positions, risk alerts, and weather changes.")

    # Load sample shipment data from JSON file
    with open("data/sample_shipments.json", "r") as f:
        shipments = json.load(f)

    # Initialize lists for map and chart data
    map_rows = []
    chart_rows = []

    # Process each shipment for map and chart visualization
    for ship in shipments:
        loc = ship.get("location")
        if loc and "lat" in loc and "lon" in loc:
            # Detect risks and determine risk level based on notes
            risks = detect_risks(ship)
            notes = ship.get("notes", "").lower()
            risk_level = "Low"
            if risks:
                risk_level = "High" if any(w in notes for w in ["typhoon", "strike", "fire"]) else "Medium"

            # Calculate severity and associated costs
            severity = assess_severity(ship)
            costs = estimate_costs(severity)

            # Append data for map visualization
            map_rows.append({
                "lat": loc["lat"],
                "lon": loc["lon"],
                "id": ship["id"],
                "route": ship["route"],
                "status": ship["status"],
                "risk_level": risk_level,
                "notes": ship["notes"]
            })

            # Append data for cost and severity charts
            chart_rows.append({
                "ID": ship["id"],
                "Route": ship["route"],
                "Severity": severity,
                "Penalty": costs["penalty"],
                "Expedite": costs["expedite"],
                "Reroute": costs["reroute"]
            })

    # Display warning if no valid location data is found
    if not map_rows:
        st.warning("⚠️ No location data found for shipments.")
    else:
        # Create and display shipment map using latitude and longitude
        df_map = pd.DataFrame(map_rows)
        st.map(df_map[["lat", "lon"]], zoom=1, use_container_width=True)

        # Display detailed shipment information, weather, and risks
        st.markdown("## 📦 Shipment Info + Weather + Risk")

        for row in map_rows:
            # Set status and risk badges for visual clarity
            status_icon = "🟢" if row["status"].lower() == "on schedule" else "🔴"
            risk_badge = {
                "Low": "🟩 Low",
                "Medium": "🟧 Medium",
                "High": "🟥 High"
            }[row["risk_level"]]

            # Render shipment card with status, risk, and notes
            st.markdown(f"""
                <div class="shipment-card">
                    <div class="shipment-title">{status_icon} {row['id']} – {row['route']}</div>
                    <div class="weather-info">🚚 Status: <strong>{row['status']}</strong></div>
                    <div class="weather-info">⚠️ Risk Level: <strong>{risk_badge}</strong></div>
                    <div class="weather-info">📝 Notes: <em>{row['notes']}</em></div>
            """, unsafe_allow_html=True)

            # Fetch and display weather data for shipment location
            weather = get_weather(row["lat"], row["lon"])
            if "error" in weather:
                st.markdown(f"<div class='weather-info'>⚠️ Weather unavailable: {weather['error']}</div>", unsafe_allow_html=True)
            else:
                alert_icon = "⛈️" if weather["is_alert"] else "🌤️"
                st.markdown(f"""
                    <div class="weather-info">
                    {alert_icon} <strong>Weather:</strong> {weather['condition']}<br>
                    🌡️ <strong>Temperature:</strong> {weather['temperature']}°C<br>
                    💨 <strong>Wind:</strong> {weather['wind_speed']} m/s
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    # Charts Section: Visualize severity and cost data
    st.markdown("## 📊 Risk and Cost Overview")

    df_chart = pd.DataFrame(chart_rows)

    # Allow user to filter charts by severity level
    severity_filter = st.radio("🎚️ Filter by Severity:", ["All", "High", "Medium", "Low"], horizontal=True)
    if severity_filter != "All":
        df_chart = df_chart[df_chart["Severity"] == severity_filter]

    # Chart 1: Display severity breakdown
    st.markdown("### 🛑 Shipment Severity Breakdown")
    severity_count = df_chart["Severity"].value_counts().reset_index()
    severity_count.columns = ["Severity", "Count"]
    fig1 = px.bar(severity_count, x="Severity", y="Count", color="Severity", color_discrete_map={
        "Low": "green",
        "Medium": "orange",
        "High": "red"
    })
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Display cost comparison per shipment
    st.markdown("### 💸 Cost Comparison (Per Shipment)")
    df_melted = df_chart.melt(id_vars=["ID", "Route"], value_vars=["Penalty", "Expedite", "Reroute"],
                              var_name="Cost Type", value_name="Cost")
    fig2 = px.bar(df_melted, x="ID", y="Cost", color="Cost Type", barmode="group", hover_data=["Route"], text_auto=".2s")
    st.plotly_chart(fig2, use_container_width=True)

# Instructions Section: Provides a user guide for the application
elif section == "📜 Instructions":
    st.title("📜 How to Use SupplyShield 2.0")
    st.caption("Interactive walkthrough for each major feature")

    # Detailed usage instructions with navigation and step-by-step guide
    st.markdown("""
    ## 🧭 Navigation Overview
    - **📊 Dashboard** – View live shipment positions with risk & weather
    - **🚨 Risk Watch** – Scan all notes for disruption triggers
    - **📦 Planner** – Get AI-recommended contingency actions
    - **🧾 Reports & Input** – Add or test your own shipment data
    - **💬 Chat with Me** – Talk to Claude (memory-enabled!)
    - **📜 Instructions** – You're here now 🙂
    - **ℹ️ About** – See who built this & what it's for

    ## 📌 Step-by-Step Usage

    ### 1. Add Shipment or Use Sample
    - Go to **🧾 Reports & Input**
    - Choose a sample or enter `ID`, `Route`, and `Notes`
    - Click `🚨 Analyze Shipment` to simulate disruption detection

    ### 2. Review Risk & Action
    - Use the **📦 Planner** to see the suggested action
    - Costs (Penalty / Expedite / Reroute) are shown with Claude’s advice

    ### 3. View Dashboard
    - Check the **📊 Dashboard** for map, risk icons, and charts
    - Risk levels and real-time weather are auto-highlighted

    ### 4. Export or Share
    - You can download **PDF or CSV reports**
    - Or directly **send a Slack message** with a single click

    ### 5. Chat Anytime
    - Use **💬 Chat with Me** to ask Claude anything during a session
    - Memory is retained per session, so you can ask follow-ups

    ### 🔐 Security Note
    - All your data stays local (no backend or server storage)
    - Claude calls are made securely via your own API key
    """)

# Risk Watch Section: Scans shipments for risks and displays summaries
elif section == "🚨 Risk Watch":
    st.subheader("🔍 Scan & Detect Supply Chain Risks")

    # Load sample shipment data
    with open("data/sample_shipments.json", "r") as f:
        shipments = json.load(f)

    # Handle user-input shipment from Reports & Input tab
    input_data = st.session_state.get("input_mode", {})
    if input_data and input_data.get("jump_to") == "risk":
        st.info(f"🚨 Showing risk for `{input_data['id']}` – {input_data['route']}`")

        shipment = {
            "id": input_data["id"],
            "route": input_data["route"],
            "notes": input_data["notes"]
        }
        risks = detect_risks(shipment)

        # Display risk analysis for input shipment
        if risks:
            summary = summarize_risk(shipment["notes"])
            st.error("⚠️ Risk Detected!")
            st.markdown(f"**📌 Shipment**: `{shipment['id']}`")
            st.markdown(f"**📒 Summary**: _{summary}_")
            st.markdown(f"**📍 Notes**: {shipment['notes']}")
        else:
            st.success("✅ No risks found for this shipment.")

        st.markdown("---")
        st.session_state.input_mode["jump_to"] = None  # Clear jump_to flag

    # Scan all shipments for risks
    risky_shipments = []

    for ship in shipments:
        risks = detect_risks(ship)
        if risks:
            # Summarize and assess severity for risky shipments
            summary = summarize_risk(ship["notes"])
            severity = assess_severity(ship)
            risky_shipments.append({
                "id": ship["id"],
                "route": ship["route"],
                "notes": ship["notes"],
                "summary": summary,
                "risks": risks,
                "severity": severity
            })

    # Display results for risky shipments
    if not risky_shipments:
        st.success("✅ All shipments are currently risk-free!")
    else:
        for r in risky_shipments:
            # Assign color-coded severity icon
            color = {
                "Low": "🟢",
                "Medium": "🟠",
                "High": "🔴"
            }.get(r["severity"], "⚪")

            # Display risk details
            st.error(f"{color} Risk Detected: {r['id']} | {r['route']}")
            st.markdown(f"**📌 Severity**: `{r['severity']}`")
            st.markdown(f"**📌 Summary**: {r['summary']}")
            st.markdown(f"**📒 Notes**: _{r['notes']}_")
            st.markdown("---")

# Planner Section: Generates contingency plans for risky shipments
elif section == "📦 Planner":
    st.subheader("📦 Contingency Planning Engine")

    # Handle user-input shipment from Reports & Input tab
    input_data = st.session_state.get("input_mode", {})
    if input_data and input_data.get("jump_to") == "planner":
        st.info(f"📦 Contingency Planning for `{input_data['id']}` – {input_data['route']}")
        
        shipment = {"id": input_data["id"], "route": input_data["route"], "notes": input_data["notes"]}
        summary = summarize_risk(shipment["notes"])
        severity = assess_severity(shipment)
        action = decide_action(severity)
        reason = explain_action(shipment["notes"], severity, action)
        costs = estimate_costs(severity)
        recommended = recommend_cheapest_action(costs)
        cost_reason = explain_cost_decision(costs, recommended)

        # Display contingency plan details
        st.markdown(f"**📌 Severity**: `{severity}`")
        st.markdown(f"**📒 Summary**: _{summary}_")
        st.markdown(f"**🧠 Recommended Action**: `{action.upper()}`")
        st.markdown(f"**📊 Reason**: {reason}")
        st.markdown(f"**💰 Cost Decision**: `{recommended.upper()}`")
        st.markdown(f"**🤖 Claude Reasoning**: {cost_reason}")
        
        st.markdown("---")
        st.session_state.input_mode["jump_to"] = None  # Clear jump_to flag

        st.markdown("---")

    # Load sample shipment data
    with open("data/sample_shipments.json", "r") as f:
        shipments = json.load(f)

    risky_shipments = []

    # Process each shipment for contingency planning
    for ship in shipments:
        risks = detect_risks(ship)
        if risks:
            # Generate risk summary, severity, and action plan
            summary = summarize_risk(ship["notes"])
            severity = assess_severity(ship)
            action = decide_action(severity)
            explanation = explain_action(ship["notes"], severity, action)

            # Perform cost analysis and recommend cheapest action
            costs = estimate_costs(severity)
            recommended = recommend_cheapest_action(costs)
            cost_reason = explain_cost_decision(costs, recommended)

            # Store shipment planning results
            shipment_result = {
                "id": ship["id"],
                "route": ship["route"],
                "severity": severity,
                "summary": summary,
                "action": action,
                "reason": explanation,
                "costs": costs,
                "recommended": recommended,
                "cost_reason": cost_reason
            }

            risky_shipments.append(shipment_result)

            # Log risk entry to history
            log_risk_entry({
                "id": ship["id"],
                "route": ship["route"],
                "severity": severity,
                "summary": summary,
                "action": action,
                "costs": costs,
                "recommended": recommended,
                "cost_reason": cost_reason
            })

    # Display contingency plans for risky shipments
    if not risky_shipments:
        st.success("✅ No planning actions needed — all shipments are safe.")
    else:
        for r in risky_shipments:
            # Assign action-specific icon
            icon = {
                "reroute": "🔁",
                "expedite": "⚡",
                "monitor": "👁️"
            }.get(r["action"], "📦")

            # Display shipment details and action plan
            st.markdown(f"### {icon} `{r['id']}` – {r['route']}")
            st.markdown(f"**📌 Severity**: `{r['severity']}`")
            st.markdown(f"**🧠 Action Reason**: {r['reason']}")
            st.markdown(f"**📒 Risk Summary**: _{r['summary']}_")

            # Display cost analysis in an expandable section
            with st.expander("💰 View Cost Analysis"):
                col1, col2, col3 = st.columns(3)
                col1.metric("⏱ Penalty", f"${r['costs']['penalty']}")
                col2.metric("🚀 Expedite", f"${r['costs']['expedite']}")
                col3.metric("📦 Reroute", f"${r['costs']['reroute']}")

                st.markdown(f"**✅ Best Cost Option**: `{r['recommended'].upper()}`")
                st.markdown(f"**📊 Claude’s Analysis**: {r['cost_reason']}")

            # Generate and send communication message
            with st.expander("✉️ Auto Communication Message"):
                tone = st.selectbox(f"Choose tone for {r['id']}", ["Formal", "Urgent", "Casual"], key=f"tone-{r['id']}")

                message_placeholder = st.empty()
                slack_status = st.empty()

                if st.button(f"📝 Generate Message for {r['id']}", key=f"generate-{r['id']}"):
                    # Generate message based on selected tone
                    message = generate_update_message(
                        shipment_id=r["id"],
                        route=r["route"],
                        severity=r["severity"],
                        summary=r["summary"],
                        action=r["action"],
                        tone=tone
                    )
                    message_placeholder.code(message, language="markdown")

                    if st.button(f"📬 Send to Slack", key=f"send-{r['id']}"):
                        # Send message to Slack and display status
                        sent = send_slack_message(message)
                        if sent:
                            slack_status.success("✅ Message sent to Slack successfully!")
                        else:
                            slack_status.error("❌ Failed to send message to Slack. Check webhook and logs.")

            st.markdown("---")

# Reports & Input Section: Allows users to input shipment data and generate reports
elif section == "🧾 Reports & Input":
    st.subheader("📥 Add Shipment & Export Report")

    # Initialize session state for sample selection
    if "selected_sample" not in st.session_state:
        st.session_state.selected_sample = None

    # Allow user to select a sample shipment
    st.markdown("### 📋 Select a Sample (Optional)")
    try:
        with open("data/sample_input_shipments.json", "r") as f:
            sample_data = json.load(f)
            options = [f"{s['id']} | {s['route']}" for s in sample_data]
            selected = st.selectbox("Choose one shipment", ["-- None --"] + options)

            if selected != "-- None --":
                idx = options.index(selected)
                st.session_state.selected_sample = sample_data[idx]
            else:
                st.session_state.selected_sample = None
    except Exception as e:
        st.error(f"Failed to load sample data: {e}")

    # Manual input form for shipment details
    st.markdown("### ✏️ Or Enter Manually")

    prefill = st.session_state.selected_sample or {"id": "", "route": "", "notes": ""}
    col1, col2 = st.columns(2)
    shipment_id = col1.text_input("Shipment ID", value=prefill["id"], placeholder="e.g., SHIP-011")
    route = col2.text_input("Route", value=prefill["route"], placeholder="e.g., Lahore → Gilgit")
    notes = st.text_area("Incident Notes", value=prefill["notes"], height=150, placeholder="Describe the disruption...")

    # Analyze shipment when button is clicked
    if st.button("🚨 Analyze Shipment"):
        if shipment_id and route and notes:
            # Perform risk analysis and generate contingency plan
            summary = summarize_risk(notes)
            severity = assess_severity({"notes": notes})
            action = decide_action(severity)
            reason = explain_action(notes, severity, action)
            costs = estimate_costs(severity)
            recommended = recommend_cheapest_action(costs)
            cost_reason = explain_cost_decision(costs, recommended)
            message = generate_update_message(
                shipment_id=shipment_id,
                route=route,
                severity=severity,
                summary=summary,
                action=action,
                tone="Formal"
            )

            # Store analysis results
            result = {
                "id": shipment_id,
                "route": route,
                "notes": notes,
                "summary": summary,
                "severity": severity,
                "action": action,
                "reason": reason,
                "costs": costs,
                "recommended": recommended,
                "cost_reason": cost_reason,
                "message": message
            }

            # Display analysis results
            st.success(f"✅ Risk analysis complete for `{shipment_id}`")
            st.markdown(f"**📌 Severity**: `{severity}`")
            st.markdown(f"**📒 Summary**: _{summary}_")
            st.markdown(f"**🧠 Action**: `{action.upper()}`")
            st.markdown(f"**📊 Claude:** {cost_reason}")
            st.code(message, language="markdown")

            # Option to send analysis to Slack
            from utils.slack import send_slack_message
            with st.expander("📬 Send to Slack"):
                if st.button("Send Claude Message to Slack"):
                    success, feedback = send_slack_message(message)
                    if success:
                        st.success(feedback)
                    else:
                        st.error(feedback)

            # Save analysis to history
            log_risk_entry(result)

            # Append new shipment to sample input file
            try:
                with open("data/sample_input_shipments.json", "r+") as f:
                    existing = json.load(f)
                    if not any(e["id"] == shipment_id for e in existing):
                        existing.append({"id": shipment_id, "route": route, "notes": notes})
                        f.seek(0)
                        json.dump(existing, f, indent=2)
                        f.truncate()
                        st.success("📝 Shipment added to saved inputs.")
                    else:
                        st.info("ℹ️ Shipment ID already exists in sample file.")
            except Exception as e:
                st.warning(f"⚠️ Failed to write to input sample file: {e}")

            # Generate and offer CSV export
            df_report = pd.DataFrame([{
                "Shipment": shipment_id,
                "Route": route,
                "Severity": severity,
                "Action": action,
                "Summary": summary,
                "Penalty Cost": costs["penalty"],
                "Expedite Cost": costs["expedite"],
                "Reroute Cost": costs["reroute"],
                "Recommended": recommended,
                "Claude Message": message
            }])
            st.markdown("### 📤 Export Report")

            csv = df_report.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", data=csv, file_name=f"{shipment_id}_report.csv", mime="text/csv")

            # Generate and offer PDF export
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=A4)
            width, height = A4

            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(width / 2, height - 50, f"Shipment Risk Report – {shipment_id}")

            c.setFont("Helvetica", 11)
            y = height - 100
            lines = [
                f"Shipment: {shipment_id}",
                f"Route: {route}",
                f"Severity: {severity}",
                f"Summary: {summary}",
                f"Action: {action}",
                f"Reason: {reason}",
                f"Cost Decision: {cost_reason}",
                "",
                "Claude Message:",
                message
            ]
            for line in lines:
                for wrapped_line in line.split("\n"):
                    c.drawString(40, y, wrapped_line[:120])
                    y -= 18
                    if y < 50:
                        c.showPage()
                        y = height - 50
            c.save()
            pdf_buffer.seek(0)

            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_buffer,
                file_name=f"{shipment_id}_report.pdf",
                mime="application/pdf"
            )

            # Allow navigation to Risk Watch or Planner with current input
            with st.expander("🔎 Next Actions"):
                if st.button("🧠 Show in Risk Watch"):
                    st.session_state.input_mode = {
                        "id": shipment_id,
                        "route": route,
                        "notes": notes,
                        "jump_to": "risk"
                    }
                    st.success("✅ Saved for '🚨 Risk Watch' tab. Switch manually to view.")

                if st.button("📦 Show in Planner"):
                    st.session_state.input_mode = {
                        "id": shipment_id,
                        "route": route,
                        "notes": notes,
                        "jump_to": "planner"
                    }
                    st.success("✅ Saved for '📦 Planner' tab. Switch manually to view.")
        else:
            st.warning("Please complete all fields before analyzing.")

# Chat with Me Section: Provides an interactive chat interface with Claude
elif section == "💬 Chat with Me":
    st.subheader("💬 Ask Claude Anything")

    st.markdown("Use Claude to ask supply chain, disruption, planning, or LLM-related questions.")

    user_input = st.text_input("What would you like to ask?", placeholder="e.g., What’s the best way to reroute from Karachi to Lahore?")
    if st.button("Ask Claude"):
        response = call_claude(user_input)
        st.markdown("#### 🤖 Claude Says:")
        st.success(response)



# About Section: Displays information about the application
elif section == "ℹ️ About":
    st.title("ℹ️ About SupplyShield 2.0")
    st.markdown("""
    SupplyShield 2.0 is an AI-powered shipment monitoring and risk mitigation platform designed to help logistics and supply chain teams stay proactive.

    **🔍 Key Features**
    - Real-time shipment risk analysis
    - Disruption-aware decision engine
    - Weather and event alert integration
    - Slack + PDF export and auto communication
    - Interactive charts and live map view
    - Claude LLM assistant chat (with memory)

    **🛠️ Technologies Used**
    - `Streamlit` for UI
    - `LangChain`, `LangGraph`, `Claude-3 Sonnet`
    - `Plotly`, `OpenWeatherMap`, Slack Webhook

    **🔒 Offline-Ready**
    This is a frontend-only simulation — all actions, memory, and AI are simulated or connected via secure API.

    **📘 Built for supply chain teams, field managers, AI researchers, and educators.**
    """)

# Footer with developer information
st.markdown("""<hr style='margin-top: 3rem; margin-bottom: 0.5rem'>""", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; font-size: 0.9rem; color: gray;'>
  Built with ❤️ by <strong>Muhammad Hanzla</strong><br>
  📞 0332-6400444 | 📧 khangormani79@gmail.com<br>
  🔗 <a href='https://www.linkedin.com/in/muhammad-hanzla-787081279/' target='_blank'>LinkedIn</a><br>
</div>
""", unsafe_allow_html=True)