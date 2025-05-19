import pandas as pd
import sqlite3
import os

# Set file paths
csv_file = os.path.join("data", "2024 W1 spring-Cycleways.csv")
db_file = os.path.join("data", "cycleways.db")

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Step 1: Load the CSV
try:
    df = pd.read_csv(csv_file)
    print(f"✅ Loaded {len(df)} rows from CSV.")
except FileNotFoundError:
    print(f"❌ CSV file not found at: {csv_file}")
    exit(1)
except Exception as e:
    print(f"❌ Error loading CSV: {e}")
    exit(1)

# Step 2: Connect to SQLite DB
try:
    conn = sqlite3.connect(db_file)
    print(f"✅ Connected to SQLite DB: {db_file}")
except Exception as e:
    print(f"❌ Error connecting to DB: {e}")
    exit(1)

# Step 3: Insert DataFrame into DB
try:
    df.to_sql("cycleways", conn, if_exists="replace", index=False)
    print("✅ Data loaded into 'cycleways' table.")
except Exception as e:
    print(f"❌ Error writing to DB: {e}")
    conn.close()
    exit(1)

# Step 4: Read back to verify
try:
    sample = pd.read_sql("SELECT * FROM cycleways LIMIT 5;", conn)
    print("\n🔍 Sample rows from 'cycleways':")
    print(sample)
except Exception as e:
    print(f"❌ Error reading from DB: {e}")

# Cleanup
conn.close()
print("✅ Connection closed.")
