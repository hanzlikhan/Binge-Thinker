from llm.anthropic_client import call_claude

def summarize_risk(note_text):
    prompt = f"Summarize this shipment risk note in one sentence:\n\n{note_text}"
    return call_claude(prompt)
