"""
05_restaurant_analysis.py
Restaurant churn by cuisine, data quality bug detection (is_active mismatch)
"""
import pandas as pd
import warnings; warnings.filterwarnings('ignore')

BASE = "data/"

def load():
    orders      = pd.read_csv(f"{BASE}fact_orders.csv")
    restaurants = pd.read_csv(f"{BASE}dim_restaurant.csv")
    orders['order_timestamp'] = pd.to_datetime(orders['order_timestamp'])
    orders['month_num'] = orders['order_timestamp'].dt.month
    orders['phase'] = orders['month_num'].map(
        lambda m: 'Pre-Crisis' if m <= 5 else ('Crisis' if m == 6 else 'Recovery')
    )
    return orders, restaurants

if __name__ == '__main__':
    orders, restaurants = load()

    pre_rest = set(orders[orders['phase']=='Pre-Crisis']['restaurant_id'])
    rec_rest = set(orders[orders['phase']=='Recovery']['restaurant_id'])
    churned  = pre_rest - rec_rest

    print(f"=== RESTAURANT ACTIVITY ===")
    print(f"Active pre-crisis:  {len(pre_rest):,}")
    print(f"Active recovery:    {len(rec_rest):,}")
    print(f"Churned:            {len(churned):,} ({len(churned)/len(pre_rest)*100:.1f}%)")

    print("\n=== CHURNED RESTAURANTS BY CUISINE ===")
    churned_info = restaurants[restaurants['restaurant_id'].isin(churned)]
    print(churned_info['cuisine_type'].value_counts().to_string())

    # DATA QUALITY BUG
    print("\n=== ⚠ DATA QUALITY BUG ===")
    active_flag_mismatch = churned_info[churned_info['is_active'] == 'Y']
    print(f"Churned restaurants still marked is_active='Y': {len(active_flag_mismatch):,}")
    print("These inflate active partner counts in management reporting.")
    print("Fix: batch job — mark is_active='N' for any restaurant with 0 orders in trailing 30 days.")
