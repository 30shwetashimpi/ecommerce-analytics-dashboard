# 02_analysis/revenue_analysis.py

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# Add db_connect.py to Python path
# ------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../01_db_connection')))
from db_connect import create_connection  # Now import works

# ------------------------------
# Connect to database
# ------------------------------
conn = create_connection()
if conn is None:
    print("❌ Cannot proceed without DB connection")
    sys.exit(1)

# ------------------------------
# Pull Monthly Revenue Data
# ------------------------------
query = """
SELECT YEAR(o.order_date) AS year,
       MONTH(o.order_date) AS month,
       SUM(oi.item_price * oi.quantity) AS revenue
FROM orders_fact o
JOIN order_items_fact oi ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY YEAR(o.order_date), MONTH(o.order_date)
ORDER BY year, month;
"""

revenue_df = pd.read_sql(query, conn)

# Close connection after fetching data
conn.close()

# ------------------------------
# Check the data
# ------------------------------
print("Monthly Revenue Data:")
print(revenue_df)

# ------------------------------
# Plot Revenue Trend
# ------------------------------
sns.set(style="whitegrid")
plt.figure(figsize=(8,5))
sns.lineplot(data=revenue_df, x='month', y='revenue', marker='o')
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(revenue_df['month'])
plt.show()
