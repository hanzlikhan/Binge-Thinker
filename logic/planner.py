from llm.anthropic_client import call_claude

def decide_action(severity: str) -> str:
    """
    Rule-based contingency recommendation.
    """
    if severity == "High":
        return "reroute"
    elif severity == "Medium":
        return "expedite"
    else:
        return "monitor"

def explain_action(note: str, severity: str, action: str) -> str:
    """
    Prompt Claude to explain why the action was chosen.
    """
    prompt = f"""
You are a supply chain strategist.

A shipment risk note has been detected:
\"\"\"{note}\"\"\"

Severity: {severity}
Recommended Action: {action.upper()}

Please explain in 4-6 lines why this action is optimal. Be professional and consider cost, timing, and safety.
"""
    return call_claude(prompt)
