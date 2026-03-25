import pandas as pd
from config import RAW_DATA_PATH

def load_data():
    df = pd.read_csv(RAW_DATA_PATH)
    return df

"""
import pandas as pd
import os

def load_data():
    if os.path.exists("data/new_data.csv"):
        print("Loading uploaded data...")
        return pd.read_csv("data/new_data.csv")
    else:
        print("Loading default data...")
        return pd.read_csv("data/cleaned_support_tickets.csv")
"""