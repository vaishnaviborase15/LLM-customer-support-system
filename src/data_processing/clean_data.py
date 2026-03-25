import pandas as pd
import re

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text


def clean_data(df):
    # ===============================
    # 🔥 STANDARDIZE COLUMN NAMES
    # ===============================
    df.columns = df.columns.str.replace(" ", "_")

    
    # ✅ REMOVE INVALID COLUMN NAMES
    df = df.loc[:, df.columns.notna()]  # remove NaN columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # remove Unnamed columns

    # ✅ OPTIONAL: strip spaces
    df.columns = df.columns.str.strip()

    # ===============================
    # 🔥 HANDLE MISSING VALUES SAFELY
    # ===============================

    df['Resolution'] = df.get('Resolution', "").fillna("Not_Resolved_Yet")

    df['First_Response_Time'] = df.get('First_Response_Time', "0").fillna("0")
    df['Time_to_Resolution'] = df.get('Time_to_Resolution', "0").fillna("0")

    df['Customer_Satisfaction_Rating'] = df.get(
        'Customer_Satisfaction_Rating', 0
    ).fillna(0)

    # TEXT FIELDS (VERY IMPORTANT)
    df['Ticket_Subject'] = df.get('Ticket_Subject', "").fillna("")
    df['Ticket_Description'] = df.get('Ticket_Description', "").fillna("")

    # ===============================
    # 📅 DATE HANDLING
    # ===============================
    if 'Date_of_Purchase' in df.columns:
        df['Date_of_Purchase'] = pd.to_datetime(
            df['Date_of_Purchase'],
            format='%d-%m-%Y',
            errors='coerce'
        )

    # ===============================
    # 🧠 TEXT PROCESSING
    # ===============================
    df['full_text'] = df['Ticket_Subject'] + " " + df['Ticket_Description']
    df['clean_text'] = df['full_text'].apply(clean_text)

    # ===============================
    # ⚠️ PRIORITY HANDLING (FIXED)
    # ===============================
    df['Ticket_Priority'] = df.get('Ticket_Priority', "low").fillna("low").astype(str)

    df['is_high_priority'] = df['Ticket_Priority'].apply(
        lambda x: 1 if x.strip().lower() in ['high', 'critical'] else 0
    )

    return df
