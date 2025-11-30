import pandas as pd
import numpy as np
import re

print("3.Data Cleaning")
# Load the dataset
df = pd.read_csv("jumia_1500_raw_fast.csv")

# Drop discount_percent and badge columns because they were empty
df = df.drop(columns=['discount_percent'])
df = df.drop(columns=['badge'])

# Remove rows where link is missing
df = df.dropna(subset=['link'])

# Define a list of realistic brands
valid_brands = [
    'Samsung', 'Apple', 'XIAOMI', 'realme', 'OPPO', 'Vivo', 'Infinix',
    'Itel', 'Motorola', 'Nokia', 'Honor', 'Redmi', 'Tecno', 'ZTE',
    'Huawei', 'Philips', 'Braun', 'Ring' ]


# Filter the dataframe to keep only valid brands
df = df[df['brand'].isin(valid_brands)].reset_index(drop=True)

# Remove duplicate image URLs
df = df.drop_duplicates(subset=['image_url']).reset_index(drop=True)




# Convert price strings into numeric float
def parse_price(price):
    if pd.isna(price):
        return np.nan
    # Remove any non-numeric character except the decimal point
    cleaned = re.sub(r'[^\d\.]', '', str(price))
    return float(cleaned) if cleaned != '' else np.nan

# Apply to price and old_price columns
df['price'] = df['price'].apply(parse_price)
df['old_price'] = df['old_price'].apply(parse_price)

# If old_price is missing assume product had no discount
df['old_price'] = df['old_price'].fillna(df['price'])

# Extract numeric rating
def parse_rating(rate):
    if pd.isna(rate):
        return np.nan
    match = re.search(r'(\d+\.?\d*)', str(rate))
    return float(match.group(1)) if match else np.nan

df['rating'] = df['rating'].apply(parse_rating)

# Fill missing ratings with median to reduce outliers effect
median_rating = df['rating'].median()
df['rating'] = df['rating'].fillna(median_rating)

# Replace missing text columns with 'Unknown'
text_cols = ['name', 'brand', 'category', 'image_url']
for col in text_cols:
        df[col] = df[col].fillna('Unknown')

# Remove duplicate rows
df = df.drop_duplicates().reset_index(drop=True)

# Extract number of reviews
def parse_num_reviews(num):
    if pd.isna(num):
        return 0
    match = re.search(r'\((\d+)\)', str(num))
    if match:
        return int(match.group(1))

    match2 = re.search(r'\d+', str(num))
    return int(match2.group(1)) if match2 else 0

df['num_reviews'] = df['num_reviews'].apply(parse_num_reviews).astype(int)

# Add discount_value, discount_percent, has_discount columns
df['discount_value'] = (df['old_price'] - df['price']).fillna(0)

df['discount_percent'] = np.where(
    df['old_price'] > 0,
    (df['discount_value'] / df['old_price']) * 100, 0)

# Binary column - 1 if discounted, 0 if not
df['has_discount'] = (df['discount_value'] > 0).astype(int)


# Remove old_price, price, discount_percent outliers within each brand using IQR
def remove_outliers_iqr(group, col):
    Q1 = group[col].quantile(0.25)
    Q3 = group[col].quantile(0.75)
    IQR = Q3 - Q1
    return group[(group[col] >= Q1 - 1.5*IQR) & (group[col] <= Q3 + 1.5*IQR)]

df = df.groupby('brand', group_keys=False).apply(lambda g: remove_outliers_iqr(g, 'old_price'))
df = df.groupby('brand', group_keys=False).apply(lambda g: remove_outliers_iqr(g, 'price'))
df = df.groupby('brand', group_keys=False).apply(lambda g: remove_outliers_iqr(g, 'discount_percent'))


# Categorize products into price ranges: Low / Medium / High
def price_category(price):
    if price <= 5000:
        return 'Low'
    elif price <= 15000:
        return 'Medium'
    else:
        return 'High'

df['price_range'] = df['price'].apply(price_category)


# Categorize discounts into Small, Medium, Large
def discount_category(discount):
    if discount <= 10:
        return 'Small'
    elif discount <= 30:
        return 'Medium'
    else:
        return 'Large'

df['discount_range'] = df['discount_percent'].apply(discount_category)


# convert date types
df['price'] = df['price'].astype(float)
df['old_price'] = df['old_price'].astype(float)
df['discount_percent'] = df['discount_percent'].astype(float)
df['has_discount'] = df['has_discount'].astype(int)
df['rating'] = df['rating'].astype(float)
df['num_reviews'] = df['num_reviews'].astype(int)

# Save the cleaned dataset to a new CSV file
df.to_csv("jumia_1500_cleaned.csv", index=False)

print(" Dataset has been cleaned and saved successfully as 'jumia_1500_cleaned.csv'\n")

print("================== DATA CLEANING & TRANSFORMATION SUMMARY =================")
print(f"Original rows: 1200, After cleaning: {len(df)}")
print(f"Dropped columns: 'discount_percent', 'badge'")
print(f"Removed duplicate rows")
print(f"Outliers removed for: 'price', 'old_price', 'discount_percent' per brand using IQR")
print("Filled missing ratings with median")
print("Filled missing text columns with 'Unknown'")
print("Created columns: 'discount_value', 'discount_percent', 'has_discount', 'price_range', 'discount_range'")
print("Converted columns to appropriate data types for analysis")
print("Cleaned dataset saved as 'jumia_1500_cleaned.csv'")
print("===========================================================================")











