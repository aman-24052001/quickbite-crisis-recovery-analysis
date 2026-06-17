"""
04_delivery_performance.py
SLA compliance, actual vs expected delivery time, breach trends
"""
import pandas as pd
import warnings; warnings.filterwarnings('ignore')

BASE = "data/"

def load():
    orders   = pd.read_csv(f"{BASE}fact_orders.csv")
    delivery = pd.read_csv(f"{BASE}fact_delivery_performance.csv")
    orders['order_timestamp'] = pd.to_datetime(orders['order_timestamp'])
    orders['month_num'] = orders['order_timestamp'].dt.month
    orders['phase'] = orders['month_num'].map(
        lambda m: 'Pre-Crisis' if m <= 5 else ('Crisis' if m == 6 else 'Recovery')
    )
    df = delivery.merge(orders[['order_id','phase','month_num']], on='order_id')
    df['sla_breach'] = df['actual_delivery_time_mins'] > df['expected_delivery_time_mins']
    df['delay_mins'] = df['actual_delivery_time_mins'] - df['expected_delivery_time_mins']
    return df

if __name__ == '__main__':
    df = load()
    print("=== DELIVERY PERFORMANCE BY PHASE ===")
    summary = df.groupby('phase').agg(
        avg_actual    = ('actual_delivery_time_mins', 'mean'),
        avg_expected  = ('expected_delivery_time_mins', 'mean'),
        sla_breach_pct= ('sla_breach', 'mean'),
        avg_delay_late= ('delay_mins', lambda x: x[x > 0].mean()),
        orders        = ('order_id', 'count'),
    ).round(2)
    summary['sla_breach_pct'] = (summary['sla_breach_pct'] * 100).round(1)
    print(summary.to_string())

    print("\n=== MONTHLY SLA BREACH % ===")
    monthly = df.groupby('month_num')['sla_breach'].mean().mul(100).round(1)
    for m, v in monthly.items():
        bar = '█' * int(v / 5)
        print(f"  Month {m:02d}: {v:5.1f}%  {bar}")
