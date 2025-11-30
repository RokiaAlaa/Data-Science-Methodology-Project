# inspection.py
import pandas as pd

RAW_FILE = "jumia_1500_raw_fast.csv"

print("====================================")
print("      DATA INSPECTION REPORT")
print("====================================\n")

# 1. Load the dataset
df = pd.read_csv(RAW_FILE)
print("✔ Dataset loaded successfully.\n")

# 2. Basic shape
print("====================================")
print("1. BASIC INFORMATION")
print("====================================")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}\n")

print("Column Names:")
print(df.columns.tolist())
print("\n")

# 3. General info: data types + null counts
print("====================================")
print("2. DATA TYPES")
print("====================================")
print(df.dtypes)
print("\n")

print("====================================")
print("3. MISSING VALUES PER COLUMN")
print("====================================")
print(df.isnull().sum())
print("\n")

# 4. Duplicate detection
print("====================================")
print("4. DUPLICATES CHECK")
print("====================================")
duplicate_count = df.duplicated().sum()
print(f"Number of duplicate rows: {duplicate_count}\n")

# 5. Basic stats for numeric-like columns (still strings but useful)
print("====================================")
print("5. SAMPLE STATISTICS")
print("====================================")

print("\nTop 10 brands:")
print(df['brand'].value_counts().head(10))

print("\nTop 10 product names:")
print(df['name'].value_counts().head(10))

print("\nUnique Categories:")
print(df['category'].unique())

print("\nRating Formats (first 10):")
print(df['rating'].dropna().head(10))

print("\nReviews Formats (first 10):")
print(df['num_reviews'].dropna().head(10))

print("\nPrice Formats (first 10):")
print(df['price'].dropna().head(10))

print("\n====================================")
print("✔ INSPECTION COMPLETE")
print("====================================")