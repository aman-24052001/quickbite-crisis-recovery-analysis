# Data

The raw datasets for this project are **not included** in this repository as they are the intellectual property of Codebasics.

## How to get the data

1. Visit [Codebasics Resume Project Challenge #18](https://codebasics.io/challenge/codebasics-resume-project-challenge)
2. Download `rpc_18_inputs_for_participants.zip`
3. Extract and place the 8 CSV files in this `data/` directory

## Expected files

```
data/
├── fact_orders.csv                (149,166 rows)
├── fact_order_items.csv           (342,994 rows)
├── fact_ratings.csv               (68,842 rows)
├── fact_delivery_performance.csv  (149,166 rows)
├── dim_customer.csv               (107,776 rows)
├── dim_restaurant.csv             (19,995 rows)
├── dim_delivery_partner_.csv      (15,000 rows)
└── dim_menu_item.csv              (342,671 rows)
```

## Schema overview

See `metadata.txt` (included in the Codebasics download) for full column definitions.

Star schema: `fact_orders` is the central fact table, joined to all dimension tables via their respective IDs.
