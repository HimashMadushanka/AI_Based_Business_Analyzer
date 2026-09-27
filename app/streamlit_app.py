import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="AI-Powered Sales Insight", layout="wide")
st.title("📊 AI-Powered Sales Insight Analyzer")

# Upload CSV
uploaded_file = st.file_uploader("Upload Sales CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Check for required columns
    required_columns = ['Order Date', 'Quantity', 'Product Name']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing required columns in CSV: {', '.join(missing_columns)}")
        st.stop()
        
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    
    # If Unit Price doesn't exist but Sales does, compute Revenue from Sales
    if 'Unit Price' in df.columns:
        df['Revenue'] = df['Quantity'] * df['Unit Price'] * (1 - df.get('Discount', 0))
    elif 'Sales' in df.columns:
        df['Revenue'] = df['Sales']
    else:
        st.error("CSV must contain either 'Unit Price' or 'Sales' column.")
        st.stop()
        
    if 'Profit' not in df.columns:
        df['Profit'] = df['Revenue'] - (df.get('Cost', 0) * df['Quantity'])

    # Top Products
    st.subheader("Top 5 Products by Revenue")
    top = df.groupby('Product Name')['Revenue'].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top)

    # Monthly Revenue Trend
    st.subheader("Monthly Revenue Trend")

# Convert month to datetime or string (Fixes Period serialization)
    df['Month'] = df['Order Date'].dt.to_period('M').astype(str)

    monthly = df.groupby('Month', as_index=False)['Revenue'].sum()
    fig1 = px.line(
    monthly,
    x='Month',
    y='Revenue',
    title="Monthly Revenue Trend",
    markers=True
)

    st.plotly_chart(fig1, use_container_width=True)


    # Sales Forecast
    st.subheader("Next 30 Days Sales Forecast")
    
    from utils import generate_forecast
    forecast = generate_forecast(df, periods=30)

    fig2 = px.line(forecast, x='ds', y='yhat', title="Forecasted Revenue")
    st.plotly_chart(fig2)

    # Customer Segmentation
    st.subheader("Customer Segmentation (RFM & K-Means)")
    from utils import generate_rfm_clusters
    
    rfm_df = generate_rfm_clusters(df)
    if rfm_df is not None:
        fig3 = px.scatter_3d(
            rfm_df, x='Recency', y='Frequency', z='Monetary',
            color='Cluster', title="3D Customer Segments",
            opacity=0.7
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.dataframe(rfm_df.head(10))
    else:
        st.info("Customer ID missing. Cannot perform segmentation.")

    # Recommendation
    st.success("💡 Recommendation: Focus on top 3 products for next month!")
   


   # To Run(streamlit run app/streamlit_app.py)