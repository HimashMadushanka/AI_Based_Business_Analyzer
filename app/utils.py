import pandas as pd
from prophet import Prophet
from sklearn.cluster import KMeans
from datetime import datetime

def generate_forecast(df, periods=30):
    """Generates a sales forecast using Prophet."""
    sales = df.groupby('Order Date')['Revenue'].sum().reset_index()
    sales.columns = ['ds', 'y']
    model = Prophet()
    model.fit(sales)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast

def generate_rfm_clusters(df, n_clusters=3):
    """Generates RFM customer segmentation and K-Means clusters."""
    if 'Customer ID' not in df.columns or 'Order ID' not in df.columns:
        return None
        
    today = df['Order Date'].max()
    
    # Calculate RFM
    # Recency: days since last order
    # Frequency: count of orders
    # Monetary: sum of revenue (or sales)
    monetary_col = 'Revenue' if 'Revenue' in df.columns else 'Sales'
    
    rfm = df.groupby('Customer ID').agg({
        'Order Date': lambda x: (today - x.max()).days,
        'Order ID': 'nunique',
        monetary_col: 'sum'
    }).reset_index()
    
    rfm.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary']
    
    # K-Means Clustering
    # Scale features slightly for better clustering without full StandardScaler for simplicity
    # but using raw values for a basic demonstration (as in the README)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    rfm['Cluster'] = kmeans.fit_predict(rfm[['Recency', 'Frequency', 'Monetary']])
    
    # Map cluster to string for categorical coloring in plots
    rfm['Cluster'] = rfm['Cluster'].astype(str)
    
    return rfm
