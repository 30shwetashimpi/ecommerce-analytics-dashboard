# 02_analysis/customer_analysis.py

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# Add db_connect.py to Python path
# ------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../01_db_connection')))
from db_connect import create_connection

# ------------------------------
# Connect to database
# ------------------------------
conn = create_connection()
if conn is None:
    print("❌ Cannot proceed without DB connection")
    sys.exit(1)

# ------------------------------
# Pull Customer Metrics: CLV, Repeat Orders, AOV
# ------------------------------
query = """
SELECT c.full_name,
       COUNT(o.order_id) AS total_orders,
       SUM(o.total_amount) AS total_revenue,
       AVG(o.total_amount) AS avg_order_value
FROM customers_dim c
LEFT JOIN orders_fact o ON c.customer_id = o.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_id
ORDER BY total_revenue DESC;
"""

customer_df = pd.read_sql(query, conn)

# Close connection
conn.close()

# ------------------------------
# Check the data
# ------------------------------
print("Customer Metrics (CLV, Repeat Orders, AOV):")
print(customer_df)

# ------------------------------
# Plot: Total Revenue per Customer (CLV)
# ------------------------------
sns.set(style="whitegrid")
plt.figure(figsize=(8,5))
sns.barplot(data=customer_df, x='total_revenue', y='full_name', palette="magma")
plt.title("Customer Lifetime Value (Total Revenue)")
plt.xlabel("Total Revenue")
plt.ylabel("Customer")
plt.show()

# ------------------------------
# Plot: Average Order Value per Customer
# ------------------------------
plt.figure(figsize=(8,5))
sns.barplot(data=customer_df, x='avg_order_value', y='full_name', palette="coolwarm")
plt.title("Average Order Value (AOV) per Customer")
plt.xlabel("Average Order Value")
plt.ylabel("Customer")
plt.show()
