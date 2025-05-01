# utils/history.py
# Utility module for logging and retrieving risk entries in SupplyShield 2.0.
# This module manages a JSON-based risk log, storing shipment risk analysis data with timestamps.
# Author: Muhammad Hanzla
# Contact: khangormani79@gmail.com

import json
from datetime import datetime
import os

# Path to the JSON file storing risk log entries
LOG_PATH = "data/risk_log.json"

def log_risk_entry(entry):
    """
    Logs a risk entry to the risk_log.json file with a timestamp.

    Args:
        entry (dict): A dictionary containing risk analysis data (e.g., shipment ID, severity, action).

    The function ensures the log directory exists, appends the entry with a UTC timestamp,
    and writes the updated log back to the file. If the file doesn't exist or is invalid,
    it initializes an empty log.
    """
    # Create the directory for the log file if it doesn't exist
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    # Load existing log or initialize an empty list if file is missing or invalid
    try:
        with open(LOG_PATH, "r") as f:
            log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        log = []

    # Add UTC timestamp to the entry
    entry["timestamp"] = datetime.utcnow().isoformat()

    # Append the new entry to the log
    log.append(entry)

    # Write the updated log back to the file with proper formatting
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

def load_risk_history():
    """
    Retrieves the risk log history from the risk_log.json file.

    Returns:
        list: A list of risk log entries. Returns an empty list if the file is missing or invalid.

    The function attempts to read and parse the JSON log file, handling any errors gracefully
    by returning an empty list and logging the error to the console.
    """
    try:
        # Read and parse the risk log file
        with open(LOG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        # Log error and return empty list to prevent crashes
        print(f"[ERROR loading history]: {e}")
        return []