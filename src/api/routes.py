from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database.connection import get_db
import pandas as pd
from src.model.predict import predict_all   # ✅ USE MODEL

router = APIRouter()

# =========================================
# 🔥 1. CREATE NEW TICKET (MODEL BASED)
# =========================================
@router.post("/new-ticket")
def create_ticket(
    customer_name: str = Form(...),
    product: str = Form(...),
    issue: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # =========================
        # 🤖 AI MODEL (FINAL)
        # =========================
        sentiment, priority, response = predict_all(issue)

        # =========================
        # 💾 DATABASE INSERT
        # =========================
        query = text("""
            INSERT INTO tickets (
                Customer_Name,
                Product_Purchased,
                Ticket_Description,
                Ticket_Type,
                Ticket_Priority,
                sentiment,
                suggested_response,
                is_high_priority
            ) VALUES (
                :customer_name,
                :product,
                :issue,
                :type,
                :priority,
                :sentiment,
                :response,
                :is_high_priority
            )
        """)

        db.execute(query, {
            "customer_name": customer_name,
            "product": product,
            "issue": issue,
            "type": "Customer Query",
            "priority": priority,
            "sentiment": sentiment,
            "response": response,
            "is_high_priority": 1 if priority == "High" else 0
        })

        db.commit()

        return {
            "message": "Ticket created successfully",
            "sentiment": sentiment,
            "priority": priority,
            "response": response
        }

    except Exception as e:
        return {"error": str(e)}


# =========================================
# 📊 2. GET ALL TICKETS
# =========================================
@router.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    df = pd.read_sql("SELECT * FROM tickets LIMIT 50", db.bind)
    return df.to_dict(orient="records")


# =========================================
# 📈 3. INSIGHTS API
# =========================================
@router.get("/insights")
def get_insights(db: Session = Depends(get_db)):
    df = pd.read_sql("SELECT * FROM tickets", db.bind)

    if 'Resolution_Hours' not in df.columns:
        df['Resolution_Hours'] = 0

    if 'Customer_Satisfaction_Rating' not in df.columns:
        df['Customer_Satisfaction_Rating'] = 0

    if 'is_high_priority' not in df.columns:
        df['is_high_priority'] = 0

    insights = {
        "total_tickets": int(len(df)),
        "high_priority": int(df['is_high_priority'].sum()),
        "avg_resolution_time": float(df['Resolution_Hours'].mean()),
        "avg_satisfaction": float(df['Customer_Satisfaction_Rating'].mean())
    }

    return insights


# =========================================
# 😊 4. SENTIMENT DISTRIBUTION
# =========================================
@router.get("/sentiment")
def sentiment_analysis(db: Session = Depends(get_db)):
    df = pd.read_sql("SELECT sentiment FROM tickets", db.bind)

    if df.empty:
        return {}

    return df['sentiment'].value_counts().to_dict()


# =========================================
# 🤖 5. RESPONSE GENERATOR
# =========================================
@router.post("/suggest-response")
def suggest_response(text: str):
    sentiment, priority, response = predict_all(text)

    return {
        "sentiment": sentiment,
        "priority": priority,
        "suggested_response": response
    }