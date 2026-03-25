import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Customer Support Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Support AI Dashboard")
st.markdown("### 🚀 Smart Ticketing & Analytics System")
st.markdown("---")

# =========================
# CUSTOMER QUERY INPUT
# =========================
st.markdown("## 🧾 Raise a Support Ticket")

with st.form("ticket_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Customer Name")
    with col2:
        product = st.text_input("💻 Product")
    issue = st.text_area("📝 Describe your issue")

    submit = st.form_submit_button("🚀 Submit Ticket")

    if submit:
        data = {
            "customer_name": name,
            "product": product,
            "issue": issue
        }
        response = requests.post(f"{API_URL}/new-ticket", data=data)

        if response.status_code == 200:
            result = response.json()
            st.success("✅ Ticket Created Successfully!")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🤖 AI Response")
                st.info(result["response"])
            with col2:
                st.markdown("### 📊 Analysis")
                st.metric("Sentiment", result["sentiment"])
                st.metric("Priority", result["priority"])

            st.cache_data.clear()
        else:
            st.error("❌ Failed to create ticket")

st.markdown("---")

# =========================
# FETCH DATA
# =========================
@st.cache_data
def get_data():
    tickets = requests.get(f"{API_URL}/tickets").json()
    insights = requests.get(f"{API_URL}/insights").json()
    sentiment = requests.get(f"{API_URL}/sentiment").json()
    return pd.DataFrame(tickets), insights, sentiment

df, insights, sentiment = get_data()

# =========================
# FILTERS SIDEBAR
# =========================
st.sidebar.header("🔍 Filters")

ticket_type = st.sidebar.selectbox(
    "📂 Ticket Type", ["All"] + list(df["Ticket_Type"].dropna().unique())
)
priority = st.sidebar.selectbox(
    "⚡ Priority", ["All"] + list(df["Ticket_Priority"].dropna().unique())
)
product = st.sidebar.selectbox(
    "💻 Product", ["All"] + list(df["Product_Purchased"].dropna().unique())
)
customer = st.sidebar.selectbox(
    "👤 Customer", ["All"] + list(df["Customer_Name"].dropna().unique())
)

# =========================
# APPLY FILTERS
# =========================
filtered_df = df.copy()
if ticket_type != "All":
    filtered_df = filtered_df[filtered_df["Ticket_Type"] == ticket_type]
if priority != "All":
    filtered_df = filtered_df[filtered_df["Ticket_Priority"] == priority]
if product != "All":
    filtered_df = filtered_df[filtered_df["Product_Purchased"] == product]
if customer != "All":
    filtered_df = filtered_df[filtered_df["Customer_Name"] == customer]

# =========================
# KPI CARDS
# =========================
st.markdown("## 📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📄 Total Tickets", len(filtered_df))
col2.metric("⚠️ High Priority", int(filtered_df['is_high_priority'].sum()))
col3.metric("⏱ Avg Resolution Time", round(filtered_df['Resolution_Hours'].mean(), 2))
col4.metric("⭐ Avg Satisfaction", round(filtered_df['Customer_Satisfaction_Rating'].mean(), 2))
st.markdown("---")

# =========================
# SENTIMENT PIE CHART
# =========================
st.subheader("😊 Sentiment Distribution")
sent_counts = filtered_df['sentiment'].value_counts()
fig1 = px.pie(
    names=sent_counts.index,
    values=sent_counts.values,
    title="Sentiment Distribution",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig1, use_container_width=True)

# =========================
# PRIORITY PIE CHART
# =========================
st.subheader("⚡ Priority Distribution")
priority_counts = filtered_df['Ticket_Priority'].value_counts()
fig2 = px.pie(
    names=priority_counts.index,
    values=priority_counts.values,
    title="Priority Distribution",
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig2, use_container_width=True)

# =========================
# TREND ANALYSIS
# =========================
st.subheader("📈 Tickets Over Time")
if 'Date_of_Purchase' in filtered_df.columns:
    df_date = filtered_df.copy()
    df_date['Date'] = pd.to_datetime(df_date['Date_of_Purchase'], errors='coerce').dt.date
    trend = df_date.groupby('Date').size().reset_index(name='Tickets')
    fig3 = px.line(trend, x='Date', y='Tickets', title="Tickets Trend Over Time", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# =========================
# DATA TABLE
# =========================
st.subheader("📋 Tickets Data")
st.dataframe(filtered_df, use_container_width=True)

# =========================
# EXTRA ANALYSIS
# =========================
st.markdown("## 🔍 Top 10 Products & Customers")
col1, col2 = st.columns(2)
with col1:
    st.subheader("📌 Tickets by Product")
    product_counts = filtered_df["Product_Purchased"].value_counts().head(10)
    fig4 = px.bar(product_counts, x=product_counts.index, y=product_counts.values,
                  color=product_counts.values, color_continuous_scale='Viridis')
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.subheader("👤 Tickets by Customer")
    customer_counts = filtered_df["Customer_Name"].value_counts().head(10)
    fig5 = px.bar(customer_counts, x=customer_counts.index, y=customer_counts.values,
                  color=customer_counts.values, color_continuous_scale='Plasma')
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.markdown("### 🤖 AI-Powered Customer Support System | Built with FastAPI + ML + Streamlit")