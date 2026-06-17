"""
01_phase_overview.py
QuickBite Express — Phase-level summary: orders, revenue, cancellations, customers
"""
import pandas as pd
import numpy as np
import warnings; warnings.filterwarnings('ignore')

BASE = "data/"  # place CSVs here

def load():
    orders = pd.read_csv(f"{BASE}fact_orders.csv")
    orders['order_timestamp'] = pd.to_datetime(orders['order_timestamp'])
    orders['month_num'] = orders['order_timestamp'].dt.month
    orders['phase'] = orders['month_num'].map(
        lambda m: 'Pre-Crisis' if m <= 5 else ('Crisis' if m == 6 else 'Recovery')
    )
    orders['cancelled'] = orders['is_cancelled'] == 'Y'
    return orders

def phase_summary(orders):
    summary = orders.groupby('phase').agg(
        total_orders      = ('order_id', 'count'),
        cancelled_orders  = ('cancelled', 'sum'),
        revenue           = ('total_amount', 'sum'),
        unique_customers  = ('customer_id', 'nunique'),
        unique_restaurants= ('restaurant_id', 'nunique'),
        avg_order_value   = ('total_amount', 'mean'),
    ).round(2)
    summary['cancel_rate_%'] = (summary['cancelled_orders'] / summary['total_orders'] * 100).round(1)
    return summary

def monthly_trend(orders):
    MONTHS = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep'}
    monthly = orders.groupby('month_num').agg(
        orders   = ('order_id', 'count'),
        revenue  = ('total_amount', 'sum'),
        customers= ('customer_id', 'nunique'),
        cancel_pct=('cancelled', 'mean'),
    ).round(2)
    monthly['month'] = monthly.index.map(MONTHS)
    monthly['cancel_pct'] = (monthly['cancel_pct'] * 100).round(2)
    return monthly

if __name__ == '__main__':
    orders = load()
    print("=== PHASE SUMMARY ===")
    print(phase_summary(orders).to_string())
    print("\n=== MONTHLY TREND ===")
    print(monthly_trend(orders).to_string())

    # Revenue gap
    monthly = monthly_trend(orders)
    avg_pre = monthly[monthly.index <= 5]['revenue'].mean()
    avg_rec = monthly[monthly.index >= 7]['revenue'].mean()
    print(f"\nPre-crisis avg monthly revenue:  ₹{avg_pre:,.0f}")
    print(f"Recovery avg monthly revenue:    ₹{avg_rec:,.0f}")
    print(f"Revenue gap:                     ₹{avg_pre - avg_rec:,.0f}  ({(avg_pre-avg_rec)/avg_pre*100:.1f}% down)")
