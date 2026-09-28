import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI-Powered Sales Insight", layout="wide")

def check_password():
    """Returns `True` if the user had a correct password."""
    def password_entered():
        if st.session_state["password"] == "admin123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter Password to Access Dashboard (Hint: admin123)", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter Password to Access Dashboard (Hint: admin123)", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()  

st.title("📊 AI-Powered Sales Insight Analyzer")

uploaded_file = st.file_uploader("Upload Sales CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    st.sidebar.header("🗺️ Map Your Columns")
    st.sidebar.write("Please map your dataset columns so the dashboard knows what to analyze.")
    cols = df.columns.tolist()
    
    def get_idx(guess_list):
        for g in guess_list:
            if g in cols:
                return cols.index(g)
        return 0
        
    order_date_col = st.sidebar.selectbox("Order Date Column", options=cols, index=get_idx(['Order Date', 'Date', 'InvoiceDate', 'date']))
    product_name_col = st.sidebar.selectbox("Product Name Column", options=cols, index=get_idx(['Product Name', 'Description', 'Product', 'Item']))
    sales_col = st.sidebar.selectbox("Revenue/Sales Column", options=cols, index=get_idx(['Sales', 'Revenue', 'Total', 'Amount', 'Price']))
    
    st.sidebar.subheader("Optional (For Customer Segments)")
    customer_id_col = st.sidebar.selectbox("Customer ID Column", options=['None'] + cols, index=0)
    order_id_col = st.sidebar.selectbox("Order ID / Invoice Column", options=['None'] + cols, index=0)

    rename_dict = {
        order_date_col: 'Order Date',
        product_name_col: 'Product Name',
        sales_col: 'Revenue'
    }
    if customer_id_col != 'None':
        rename_dict[customer_id_col] = 'Customer ID'
    if order_id_col != 'None':
        rename_dict[order_id_col] = 'Order ID'
        
    df = df.rename(columns=rename_dict)
    
    try:
        df['Order Date'] = pd.to_datetime(df['Order Date'])
    except Exception as e:
        st.error("❌ Could not parse the selected Order Date. Please ensure it is a valid date column.")
        st.stop()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🤖 Automatic AI Data Profiling", "📊 Business Overview", "📈 Forecasting", "👥 Customer Segments", "📥 Data Export"])

    with tab1:
        st.subheader("🤖 Universal Automatic Analysis")
        st.write("Upload ANY dataset, and the engine will automatically detect all features, distributions, correlations, and warnings without any manual column mapping!")
        
        if st.button("Generate Basic Data Overview"):
            with st.spinner("Analyzing your dataset..."):
                st.subheader("Data Summary")
                st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
                st.dataframe(df.describe(include='all').fillna(""))
                
                st.subheader("Missing Values")
                st.dataframe(df.isnull().sum().reset_index().rename(columns={'index': 'Column', 0: 'Missing Count'}))
                
                st.subheader("Numeric Distributions")
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                for col in numeric_cols:
                    if col not in ['Order ID', 'Customer ID']: 
                        fig = px.histogram(df, x=col, title=f"Distribution of {col}")
                        st.plotly_chart(fig, width="stretch")

    with tab2:
        if 'Revenue' in df.columns:
            st.subheader("Key Performance Indicators")
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Revenue", f"${df['Revenue'].sum():,.2f}")
            if 'Quantity' in df.columns:
                m2.metric("Total Items Sold", f"{df['Quantity'].sum():,.0f}")
            else:
                m2.metric("Total Records", f"{len(df):,}")
                
            if 'Order ID' in df.columns:
                m3.metric("Total Orders", f"{df['Order ID'].nunique():,}")
            else:
                m3.metric("Avg Revenue / Row", f"${df['Revenue'].mean():,.2f}")
            
            st.markdown("---")

        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("🏆 Top 5 Products")
            if 'Product Name' in df.columns and 'Revenue' in df.columns:
                top = df.groupby('Product Name')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False).head(5)
                fig_bar = px.bar(
                    top, x='Revenue', y='Product Name', orientation='h', 
                    title="Revenue by Top Products", 
                    color='Revenue', color_continuous_scale='Blues'
                )
                fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
                st.plotly_chart(fig_bar, width="stretch")
            else:
                st.warning("Please map 'Product Name' and 'Revenue' in the sidebar to see this chart.")

        with col_right:
            st.subheader("📈 Monthly Trend")
            if 'Order Date' in df.columns and 'Revenue' in df.columns:

                df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
                monthly = df.groupby('Month', as_index=False)['Revenue'].sum()
                fig1 = px.line(
                    monthly, x='Month', y='Revenue', 
                    title="Revenue Trend over Time", 
                    markers=True, line_shape='spline'
                )
                fig1.update_traces(line_color='#1f77b4', line_width=3, marker=dict(size=8))
                st.plotly_chart(fig1, width="stretch")
            else:
                st.warning("Please map 'Order Date' and 'Revenue' to see the trend.")
                
        st.success("💡 Recommendation: Focus marketing campaigns on your top-performing products and analyze historical high-revenue months to replicate success!")

    with tab3:
        st.subheader("Next 30 Days Sales Forecast")
        if 'Order Date' in df.columns and 'Revenue' in df.columns:
            from utils import generate_forecast
            forecast = generate_forecast(df, periods=30)
            fig2 = px.line(forecast, x='ds', y='yhat', title="Forecasted Revenue")
            st.plotly_chart(fig2, width="stretch")
        else:
            st.warning("Please map 'Order Date' and 'Revenue' to see the forecast.")

    with tab4:
        st.subheader("Customer Segmentation (RFM & K-Means)")
        from utils import generate_rfm_clusters
        
        if 'Customer ID' in df.columns and 'Order ID' in df.columns:
            rfm_df = generate_rfm_clusters(df)
            if rfm_df is not None:
                fig3 = px.scatter_3d(
                    rfm_df, x='Recency', y='Frequency', z='Monetary',
                    color='Cluster', title="3D Customer Segments",
                    opacity=0.7
                )
                st.plotly_chart(fig3, width="stretch")
                st.dataframe(rfm_df.head(10))
            else:
                st.info("Customer ID missing. Cannot perform segmentation.")
        else:
            st.info("Please map 'Customer ID' and 'Order ID' in the sidebar to perform segmentation.")

    with tab5:
        st.subheader("Export Data")
        st.write("Download the processed data or customer segments for further analysis.")
        
        csv_sales = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Data (CSV)",
            data=csv_sales,
            file_name='processed_data.csv',
            mime='text/csv',
        )
        
        if 'Customer ID' in df.columns and 'Order ID' in df.columns:
            rfm_df = generate_rfm_clusters(df)
            if rfm_df is not None:
                csv_rfm = rfm_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Customer Segments (CSV)",
                    data=csv_rfm,
                    file_name='customer_segments.csv',
                    mime='text/csv',
                )
   


   # To Run(streamlit run app/streamlit_app.py)