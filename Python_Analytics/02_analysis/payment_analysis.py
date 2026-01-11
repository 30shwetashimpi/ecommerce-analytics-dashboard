# 02_analysis/payment_analysis.py

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
# Pull Payment Status Metrics
# ------------------------------
query = """
SELECT o.order_status, 
       COUNT(o.order_id) AS order_count,
       SUM(p.payment_amount) AS total_payment
FROM orders_fact o
LEFT JOIN payment_fact p ON o.order_id = p.order_id
GROUP BY o.order_status;
"""

payment_df = pd.read_sql(query, conn)

# Close connection
conn.close()

# ------------------------------
# Check the data
# ------------------------------
print("Payment Status Metrics:")
print(payment_df)

payment_df['total_payment'] = payment_df['total_payment'].fillna(0)

# ------------------------------
# Plot: Orders by Payment Status
# ------------------------------
sns.set(style="whitegrid")
plt.figure(figsize=(6,4))
sns.barplot(data=payment_df, x='order_status', y='order_count', palette="pastel")
plt.title("Orders by Payment Status")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.show()

# ------------------------------
# Optional: Pie chart for total payment share
# ------------------------------
plt.figure(figsize=(6,6))
plt.pie(payment_df['total_payment'], labels=payment_df['order_status'], autopct='%1.1f%%', colors=['#8dd3c7','#fb8072'])
plt.title("Payment Share by Order Status")
plt.show()
