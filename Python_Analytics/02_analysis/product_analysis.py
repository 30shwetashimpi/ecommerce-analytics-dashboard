# 02_analysis/product_analysis.py

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
# Pull Profit by Product
# ------------------------------
query = """
SELECT p.product_name,
       SUM((p.price - p.cost) * oi.quantity) AS profit
FROM order_items_fact oi
JOIN products_dim p ON oi.product_id = p.product_id
JOIN orders_fact o ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_name
ORDER BY profit DESC;
"""

profit_df = pd.read_sql(query, conn)

# Close connection
conn.close()

# ------------------------------
# Check the data
# ------------------------------
print("Profit by Product:")
print(profit_df)

# ------------------------------
# Plot Profit by Product
# ------------------------------
sns.set(style="whitegrid")
plt.figure(figsize=(8,5))
sns.barplot(data=profit_df, x='profit', y='product_name', palette="viridis")
plt.title("Profit by Product")
plt.xlabel("Profit")
plt.ylabel("Product")
plt.show()
