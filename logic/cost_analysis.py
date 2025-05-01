from llm.anthropic_client import call_claude

def estimate_costs(severity: str, delay_days: int = 2):
    """
    Simulate basic cost formulas (adjust as needed).
    """
    costs = {
        "penalty": delay_days * 500,         # $500 per delay day
        "reroute": 1800,                      # Fixed cost
        "expedite": 1200                      # Fixed cost
    }

    if severity == "Low":
        costs["penalty"] = 0

    return costs

def recommend_cheapest_action(costs: dict) -> str:
    best = min(costs, key=costs.get)
    return best

def explain_cost_decision(costs: dict, recommended: str):
    prompt = f"""
You are a logistics analyst. Below are the estimated costs for different options in response to a shipment disruption:

- Penalty: ${costs['penalty']}
- Reroute: ${costs['reroute']}
- Expedite: ${costs['expedite']}

Which option is most cost-effective and why? The system recommends: **{recommended.upper()}**.

Write a 4–6 line justification.
"""
    return call_claude(prompt)
