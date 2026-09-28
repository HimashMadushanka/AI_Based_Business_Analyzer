import pytest
import pandas as pd
from datetime import datetime, timedelta

from app.utils import generate_rfm_clusters

@pytest.fixture
def sample_sales_data():
    today = datetime.today()
    data = {
        'Customer ID': ['C1', 'C1', 'C2', 'C3', 'C3', 'C3'],
        'Order ID': ['O1', 'O2', 'O3', 'O4', 'O5', 'O6'],
        'Order Date': [
            today - timedelta(days=10),
            today - timedelta(days=5),
            today - timedelta(days=50),
            today - timedelta(days=1),
            today - timedelta(days=1),
            today - timedelta(days=2)
        ],
        'Revenue': [100, 150, 50, 200, 300, 100]
    }
    return pd.DataFrame(data)

def test_generate_rfm_clusters(sample_sales_data):
    """Test that RFM clustering returns correct dataframe structure."""
    rfm = generate_rfm_clusters(sample_sales_data, n_clusters=2)
    

    assert rfm is not None
    
    expected_cols = ['Customer ID', 'Recency', 'Frequency', 'Monetary', 'Cluster']
    for col in expected_cols:
        assert col in rfm.columns
        
    c1_data = rfm[rfm['Customer ID'] == 'C1'].iloc[0]
    assert c1_data['Frequency'] == 2  
    assert c1_data['Monetary'] == 250 
    
def test_generate_rfm_missing_cols():
    """Test behavior when required columns are missing."""
    bad_df = pd.DataFrame({'Bad Col': [1, 2]})
    assert generate_rfm_clusters(bad_df) is None
