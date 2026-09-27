# AI Based Business Analyzer

A data-driven application designed to help businesses analyze sales, customers, trends, and performance using Python, Pandas,sklearn, Matplotlib, and machine learning models.

## 🚀 Features

* Load and clean raw sales data
* Calculate Monthly Revenue Trends
* Identify top products and customers
* RFM (Recency, Frequency, Monetary) customer segmentation
* K-Means clustering for customer groups
* **Market Basket Analysis (Frequently Bought Together)**
* **Customer Churn Prediction (Random Forest)**
* Generate insights and visualizations
* **Time-Series Forecasting with Prophet (with Cross-Validation)**

## 📂 Project Structure

```
AI_Based_Business_Analyzer/
│
├── data/
│   ├── raw/
│   │   └── sample_sales.csv
│   └── processed/
|        └──cleaned_sales.csv
├── app/
│   ├── streamlit_app.py
│   └── utils.py
├──figures
│
├── notebooks/
│   ├── cleaning.ipynb
│   ├── analysis.ipynb
│   └──forecast.ipynb
│
└──README.md
```

## 🧹 Data Cleaning Steps

* Convert dates using `pd.to_datetime()`
* Remove duplicate rows
* Fill missing values for numeric columns
* Fix incorrect data types

## 📊 Analysis Included

### 1. Monthly Sales Trend

```python
df['Month'] = df['Order Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Sales'].sum()
```

### 2. RFM Customer Segmentation

```python
rfm = df.groupby('Customer ID').agg({
    'Order Date': lambda x: (today - x.max()).days,
    'Order ID': 'count',
    'Sales': 'sum'
})
```

### 3. K-Means Clustering

```python
kmeans = KMeans(n_clusters=3, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(rfm)
```

## ▶️ How to Run

1. Install required libraries:

```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:

```bash
streamlit run app/streamlit_app.py
```

## 📦 Requirements

* Python 3.10+
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Streamlit

## 💡 Future Enhancements

* Add interactive dashboards with more tabs
* Add export options (PDF/Excel)
* Connect to real SQL/Cloud Databases for live data

## 👤 Author

**K. Himash Madushanka**

