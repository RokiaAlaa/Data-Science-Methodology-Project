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
print("7. SUMMARY OF DATA INSPECTION")
print("====================================")

total_rows = df.shape[0]
total_cols = df.shape[1]
missing = df.isnull().sum()
duplicates = duplicate_count


print(f"✔ Total rows: {total_rows}")
print(f"✔ Total columns: {total_cols}\n")

print("✔ Missing values per column:")
for col, val in missing.items():
    print(f"   - {col}: {val}")

print(f"\n✔ Duplicate rows: {duplicates}")

# Identify columns with 100% missing
full_missing = missing[missing == total_rows].index.tolist()
if full_missing:
    print("\n⚠ Columns with 100% missing values:")
    for col in full_missing:
        print(f"   - {col}")

# Identify columns with more than 50% missing
high_missing = missing[missing > (total_rows * 0.5)].index.tolist()
if high_missing:
    print("\n⚠ Columns with >50% missing values:")
    for col in high_missing:
        print(f"   - {col}")

# Identify suspicious product names (non-mobile items)
suspicious = df[df['name'].str.contains("air|conditioner|cooler", case=False, na=False)]
print(f"\n⚠ Non-mobile suspicious items found: {suspicious.shape[0]}")



print("\n====================================")
print("✔ INSPECTION COMPLETE")
print("====================================")