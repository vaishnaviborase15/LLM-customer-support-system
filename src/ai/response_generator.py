def generate_response(row):
    #  SAFE CONVERSION (CRITICAL FIX)
    ticket_type = str(row.get('Ticket_Type', 'other')).strip().lower()
    sentiment = str(row.get('sentiment', 'neutral')).strip().lower()
    priority = str(row.get('Ticket_Priority', 'low')).strip().lower()

    responses = {
        "technical issue": "Our technical team is working on your issue.",
        "billing inquiry": "We are checking your billing concern.",
        "product inquiry": "We will assist you with product details.",
        "cancellation request": "Your cancellation request is being processed by our team.",
        "refund request": "We are reviewing your refund request and will update you shortly.",
        "other": "Our team will assist you shortly."
    }

    # SAFE LOOKUP
    base = responses.get(ticket_type, responses["other"])

    # SENTIMENT HANDLING
    if sentiment == "negative":
        tone = "We sincerely apologize. "
    else:
        tone = ""

    # PRIORITY HANDLING
    if priority in ["high", "critical"]:
        urgency = "This is being handled urgently. "
    else:
        urgency = ""

    return tone + urgency + base


def apply_responses(df):
    df['suggested_response'] = df.apply(generate_response, axis=1)
    return df
