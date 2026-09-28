import pandas as pd
import streamlit as st
from prophet import Prophet
from sklearn.cluster import KMeans
from datetime import datetime

@st.cache_data
def generate_forecast(df, periods=30):
    """Generates a sales forecast using Prophet."""
    sales = df.groupby('Order Date')['Revenue'].sum().reset_index()
    sales.columns = ['ds', 'y']
    model = Prophet()
    model.fit(sales)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast

@st.cache_data
def generate_rfm_clusters(df, n_clusters=3):
    """Generates RFM customer segmentation and K-Means clusters."""
    if 'Customer ID' not in df.columns or 'Order ID' not in df.columns:
        return None
        
    today = df['Order Date'].max()
    
 
    monetary_col = 'Revenue' if 'Revenue' in df.columns else 'Sales'
    
    rfm = df.groupby('Customer ID').agg({
        'Order Date': lambda x: (today - x.max()).days,
        'Order ID': 'nunique',
        monetary_col: 'sum'
    }).reset_index()
    
    rfm.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary']

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    rfm['Cluster'] = kmeans.fit_predict(rfm[['Recency', 'Frequency', 'Monetary']])
    
    rfm['Cluster'] = rfm['Cluster'].astype(str)
    
    return rfm
