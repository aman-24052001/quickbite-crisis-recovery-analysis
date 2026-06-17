"""
02_customer_retention.py
Cohort retention: who returned from pre-crisis through crisis and into recovery
"""
import pandas as pd
import warnings; warnings.filterwarnings('ignore')

BASE = "data/"

def load():
    orders = pd.read_csv(f"{BASE}fact_orders.csv")
    orders['order_timestamp'] = pd.to_datetime(orders['order_timestamp'])
    orders['month_num'] = orders['order_timestamp'].dt.month
    orders['phase'] = orders['month_num'].map(
        lambda m: 'Pre-Crisis' if m <= 5 else ('Crisis' if m == 6 else 'Recovery')
    )
    customers = pd.read_csv(f"{BASE}dim_customer.csv")
    return orders, customers

if __name__ == '__main__':
    orders, customers = load()

    pre   = set(orders[orders['phase']=='Pre-Crisis']['customer_id'])
    crisis= set(orders[orders['phase']=='Crisis']['customer_id'])
    rec   = set(orders[orders['phase']=='Recovery']['customer_id'])

    print("=== CUSTOMER COHORT FLOW ===")
    print(f"Pre-Crisis unique customers:        {len(pre):>8,}")
    print(f"Crisis unique customers:            {len(crisis):>8,}")
    print(f"Recovery unique customers:          {len(rec):>8,}")
    print(f"\nPre → Crisis retained:              {len(pre & crisis):>8,}  ({len(pre & crisis)/len(pre)*100:.1f}%)")
    print(f"Pre → Recovery retained:            {len(pre & rec):>8,}  ({len(pre & rec)/len(pre)*100:.1f}%)")
    print(f"New in Recovery (no pre history):   {len(rec - pre):>8,}")
    print(f"Lost (pre-crisis, gone in recovery):{len(pre - rec):>8,}  ({len(pre - rec)/len(pre)*100:.1f}%)")

    # Acquisition channel of new recovery customers
    new_rec = customers[customers['customer_id'].isin(rec - pre)]
    print("\n=== NEW RECOVERY CUSTOMERS BY ACQUISITION CHANNEL ===")
    print(new_rec['acquisition_channel'].value_counts().to_string())
