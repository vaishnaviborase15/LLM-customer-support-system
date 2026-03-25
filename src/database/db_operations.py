from .db_connection import get_connection
import pandas as pd

def insert_data(df):
    conn = get_connection()
    cursor = conn.cursor()

    # 🔥 Clear old data
    cursor.execute("DELETE FROM tickets")

    # =========================
    # ✅ FIX 1: REMOVE BAD COLUMNS
    # =========================
    df = df.loc[:, df.columns.notna()]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.columns = df.columns.str.strip()

    # =========================
    # ✅ FIX 2: CONVERT NaN → None (VERY IMPORTANT)
    # =========================
    df = df.where(pd.notnull(df), None)

    # =========================
    # ✅ FIX 3: SAFE COLUMN NAMES
    # =========================
    columns = ",".join([f"`{col}`" for col in df.columns])
    placeholders = ",".join(["%s"] * len(df.columns))
    query = f"INSERT INTO tickets ({columns}) VALUES ({placeholders})"

    # =========================
    # 🚀 BATCH INSERT
    # =========================
    batch_size = 500
    total_rows = len(df)

    for start in range(0, total_rows, batch_size):
        end = start + batch_size
        batch = df.iloc[start:end]

        # 🔥 CRITICAL FIX: convert row values safely
        data = [
            tuple(None if pd.isna(val) else val for val in row)
            for row in batch.to_numpy()
        ]

        cursor.executemany(query, data)
        conn.commit()

        print(f"Inserted rows {start} to {end}")

    cursor.close()
    conn.close()

    print("All records inserted successfully!")
