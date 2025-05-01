from llm.anthropic_client import call_claude

def generate_update_message(shipment_id, route, severity, summary, action, tone="Formal"):
    prompt = f"""
Write a {tone.lower()} message to the logistics team or client based on the following shipment risk details:

- Shipment ID: {shipment_id}
- Route: {route}
- Severity: {severity}
- Risk Summary: {summary}
- Recommended Action: {action.upper()}

Structure the message in 4–6 sentences. Be clear, professional, and informative. If urgent, highlight next steps.
"""
    return call_claude(prompt)
