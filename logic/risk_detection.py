def detect_risks(shipment):
    risk_keywords = ["strike", "storm", "typhoon", "delay", "flood", "fire", "hurricane", "protest"]
    notes = shipment.get("notes", "").lower()
    risks = [word for word in risk_keywords if word in notes]
    return risks if risks else None
