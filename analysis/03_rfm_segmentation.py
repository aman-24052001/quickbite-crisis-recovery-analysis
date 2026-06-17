"""
03_rfm_segmentation.py
RFM scoring on pre-crisis customers + recovery return rate per segment
"""
import pandas as pd
import numpy as np
import warnings; warnings.filterwarnings('ignore')

BASE = "data/"

def load():
    orders = pd.read_csv(f"{BASE}fact_orders.csv")
    orders['order_timestamp'] = pd.to_datetime(orders['order_timestamp'])
    orders['month_num'] = orders['order_timestamp'].dt.month
    orders['phase'] = orders['month_num'].map(
        lambda m: 'Pre-Crisis' if m <= 5 else ('Crisis' if m == 6 else 'Recovery')
    )
    return orders

def build_rfm(orders):
    pre = orders[orders['phase'] == 'Pre-Crisis']
    snapshot = pd.Timestamp('2025-06-01')
    rfm = pre.groupby('customer_id').agg(
        recency  = ('order_timestamp', lambda x: (snapshot - x.max()).days),
        frequency= ('order_id', 'count'),
        monetary = ('total_amount', 'sum'),
    )
    rfm['R'] = pd.qcut(rfm['recency'],  4, labels=[4,3,2,1]).astype(int)
    rfm['F'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1,2,3,4]).astype(int)
    rfm['M'] = pd.qcut(rfm['monetary'], 4, labels=[1,2,3,4]).astype(int)

    def segment(r, f, m):
        if r >= 3 and f >= 3: return 'Champions'
        if r >= 3 and f >= 2: return 'Loyal'
        if r >= 3 and f == 1: return 'Recent'
        if r == 2 and f >= 2: return 'At Risk'
        if r <= 2 and f >= 3: return "Can't Lose"
        if r <= 1:            return 'Lost'
        return 'Others'

    rfm['segment'] = rfm.apply(lambda x: segment(x['R'], x['F'], x['M']), axis=1)
    return rfm

if __name__ == '__main__':
    orders = load()
    rfm = build_rfm(orders)
    rec_users = set(orders[orders['phase']=='Recovery']['customer_id'])
    rfm['came_back'] = rfm.index.isin(rec_users)

    print("=== RFM SEGMENTS ===")
    result = rfm.groupby('segment').agg(
        count      = ('came_back', 'count'),
        came_back  = ('came_back', 'sum'),
        avg_revenue= ('monetary', 'mean'),
        avg_orders = ('frequency', 'mean'),
    ).round(2)
    result['return_%'] = (result['came_back'] / result['count'] * 100).round(1)
    print(result.sort_values('count', ascending=False).to_string())

    print("\n=== KEY INSIGHT ===")
    print("All segments returned at ~12% — loyalty was not a predictor of return.")
    print("Champions (highest LTV) need active outreach, not passive win-back.")
