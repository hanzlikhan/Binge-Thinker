# logic/severity_score.py

def assess_severity(shipment):
    note = shipment.get("notes", "").lower()
    status = shipment.get("status", "").lower()

    # Rule-based severity mapping
    severity = "Low"
    if any(word in note for word in ["strike", "typhoon", "hurricane", "fire"]):
        severity = "High"
    elif any(word in note for word in ["delay", "storm", "flood"]):
        severity = "Medium"

    if "delayed" in status:
        severity = "High" if severity == "Medium" else severity

    return severity
