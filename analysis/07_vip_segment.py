"""
07_vip_segment.py
Top 5% customer analysis — spend, orders, return rate, monthly revenue contribution
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

if __name__ == '__main__':
    orders = load()

    cust_spend = orders[orders['phase']=='Pre-Crisis'].groupby('customer_id').agg(
        total_spend  = ('total_amount', 'sum'),
        order_count  = ('order_id', 'count'),
        avg_order    = ('total_amount', 'mean'),
    )
    threshold = cust_spend['total_spend'].quantile(0.95)
    vip = cust_spend[cust_spend['total_spend'] >= threshold]

    rec_users = set(orders[orders['phase']=='Recovery']['customer_id'])
    vip['came_back'] = vip.index.isin(rec_users)

    print(f"=== VIP SEGMENT (top 5% by pre-crisis spend) ===")
    print(f"Spend threshold:        ₹{threshold:,.0f}")
    print(f"VIP customer count:     {len(vip):,}")
    print(f"Avg total spend:        ₹{vip['total_spend'].mean():,.0f}")
    print(f"Avg monthly spend:      ₹{vip['total_spend'].mean()/5:,.0f}")
    print(f"Avg order count:        {vip['order_count'].mean():.1f}")
    print(f"Avg order value:        ₹{vip['avg_order'].mean():.0f}")
    print(f"VIP returned:           {vip['came_back'].sum():,} ({vip['came_back'].mean()*100:.1f}%)")
    print(f"VIP lost:               {(~vip['came_back']).sum():,}")

    lost_vip_monthly = vip[~vip['came_back']]['total_spend'].sum() / 5
    print(f"\nLost VIP monthly revenue at risk: ₹{lost_vip_monthly:,.0f}")

    print("\n=== VIP MONTHLY ORDER VOLUME ===")
    vip_orders = orders[orders['customer_id'].isin(vip.index)]
    print(vip_orders.groupby('month_num').agg(
        orders  = ('order_id', 'count'),
        revenue = ('total_amount', 'sum'),
    ).round(0).to_string())

    print("\n=== REACTIVATION SCENARIOS ===")
    print(f"{'Return Rate':<15} {'Customers':<12} {'Monthly Revenue'}")
    avg_monthly = vip['total_spend'].mean() / 5
    for pct in [10, 15, 20, 25, 30, 40, 50]:
        n = int((~vip['came_back']).sum() * pct / 100)
        rev = n * avg_monthly
        print(f"  {pct}%          {n:>6,}       ₹{rev:>8,.0f}/month")
