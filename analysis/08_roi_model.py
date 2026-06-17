"""
08_roi_model.py
Recovery investment model — pillar-by-pillar ROI, revenue projection scenarios
"""
import pandas as pd
import warnings; warnings.filterwarnings('ignore')

BASE = "data/"

# ── Model inputs (from analysis) ─────────────────────────────────────────────
SEGMENTS = {
    'Champions':  {'size': 24783, 'avg_monthly_spend': 118},
    'At Risk':    {'size': 15864, 'avg_monthly_spend':  89},
    "Can't Lose": {'size':  8301, 'avg_monthly_spend':  82},
    'VIP':        {'size':  3823, 'avg_monthly_spend': 226},
}

PILLARS = [
    {'name': 'VIP Win-Back',             'invest_low': 8,  'invest_high': 10,
     'segment': 'VIP',         'return_rate': 0.25, 'timeline_mo': 2},
    {'name': 'Champion Reactivation',    'invest_low': 15, 'invest_high': 20,
     'segment': 'Champions',   'return_rate': 0.25, 'timeline_mo': 3},
    {'name': 'Delivery Infrastructure',  'invest_low': 25, 'invest_high': 30,
     'segment': None,          'return_rate': None, 'timeline_mo': 6},
    {'name': 'Restaurant Re-onboarding', 'invest_low': 10, 'invest_high': 15,
     'segment': None,          'return_rate': None, 'timeline_mo': 5},
    {'name': 'Food Safety Certification','invest_low':  8, 'invest_high': 12,
     'segment': None,          'return_rate': None, 'timeline_mo': 3},
]

if __name__ == '__main__':
    print("=== PILLAR ROI MODEL ===")
    total_invest_low = total_invest_high = 0
    total_monthly_recovery = 0

    for p in PILLARS:
        total_invest_low  += p['invest_low']
        total_invest_high += p['invest_high']
        if p['segment'] and p['return_rate']:
            seg = SEGMENTS[p['segment']]
            customers_recovered = int(seg['size'] * p['return_rate'])
            monthly_rev = customers_recovered * seg['avg_monthly_spend']
            total_monthly_recovery += monthly_rev
            print(f"\n{p['name']}")
            print(f"  Investment:          ₹{p['invest_low']}–{p['invest_high']}L")
            print(f"  Customers recovered: {customers_recovered:,}  ({p['return_rate']*100:.0f}% of {seg['size']:,})")
            print(f"  Monthly revenue:     ₹{monthly_rev/100000:.2f}L")
            print(f"  6-month revenue:     ₹{monthly_rev*6/100000:.1f}L")
        else:
            print(f"\n{p['name']}")
            print(f"  Investment:  ₹{p['invest_low']}–{p['invest_high']}L")
            print(f"  Output:      Operational improvement (enabler)")

    print(f"\n{'='*50}")
    print(f"Total investment range:   ₹{total_invest_low}–{total_invest_high}L")
    print(f"Direct monthly recovery:  ₹{total_monthly_recovery/100000:.2f}L/month")
    print(f"12-month revenue return:  ₹{total_monthly_recovery*12/100000:.0f}L")
    roi = (total_monthly_recovery * 9) / ((total_invest_low + total_invest_high) / 2 * 100000)
    print(f"Estimated 9-month ROI:    {roi:.1f}×")

    print("\n=== REACTIVATION SCENARIOS (all segments) ===")
    print(f"{'Scenario':<12} {'Return%':<10} {'Customers':<12} {'Monthly Revenue'}")
    for label, rate in [('Conservative', 0.15), ('Base Case', 0.25), ('Optimistic', 0.40)]:
        total_cust = sum(int(s['size'] * rate) for s in SEGMENTS.values())
        total_rev  = sum(int(s['size'] * rate) * s['avg_monthly_spend'] for s in SEGMENTS.values())
        print(f"  {label:<12} {rate*100:.0f}%       {total_cust:>8,}     ₹{total_rev/100000:.2f}L/month")
