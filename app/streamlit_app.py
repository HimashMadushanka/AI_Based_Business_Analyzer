import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet

st.set_page_config(page_title="AI-Powered Sales Insight", layout="wide")
st.title("📊 AI-Powered Sales Insight Analyzer")

# Upload CSV
uploaded_file = st.file_uploader("Upload Sales CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Revenue'] = df['Quantity'] * df['Unit Price'] * (1 - df.get('Discount', 0))
    df['Profit'] = df['Revenue'] - (df.get('Cost', 0) * df['Quantity'])

    # Top Products
    st.subheader("Top 5 Products by Revenue")
    top = df.groupby('Product Name')['Revenue'].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top)

    # Monthly Revenue Trend
    st.subheader("Monthly Revenue Trend")
    df['Month'] = df['Order Date'].dt.to_period('M')
    monthly = df.groupby('Month')['Revenue'].sum().reset_index()
    fig1 = px.line(monthly, x='Month', y='Revenue', title="Monthly Revenue Trend")
    st.plotly_chart(fig1)

    # Sales Forecast
    st.subheader("Next 30 Days Sales Forecast")
    sales = df.groupby('Order Date')['Revenue'].sum().reset_index()
    sales.columns = ['ds', 'y']
    model = Prophet()
    model.fit(sales)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    fig2 = px.line(forecast, x='ds', y='yhat', title="Forecasted Revenue")
    st.plotly_chart(fig2)

    # Recommendation
    st.success("💡 Recommendation: Focus on top 3 products for next month!")
