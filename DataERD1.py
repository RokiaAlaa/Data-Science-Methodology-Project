import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

df = pd.read_csv("C:\\Users\\HP\\Downloads\\jumia_1500_cleaned.csv")

#==============================================================================
# STEP 1: DATASET OVERVIEW & DESCRIPTIVE STATISTICS
#==============================================================================
print("="*80)
print("STEP 1: DATASET OVERVIEW & DESCRIPTIVE STATISTICS")
print("="*80)

print(f"\nDataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\nColumns & Data Types:\n{df.dtypes}")

numerical_cols = ['price', 'old_price', 'rating', 'num_reviews', 'discount_value', 'discount_percent']
categorical_cols = ['brand', 'category', 'price_range', 'discount_range']

print("\nNUMERICAL STATISTICS:")
for col in numerical_cols:
    print(f"\n{col.upper()}:")
    print(f"  Mean: {df[col].mean():.2f} | Median: {df[col].median():.2f} | Mode: {df[col].mode().values[0]:.2f}")
    print(f"  Std: {df[col].std():.2f} | Min: {df[col].min():.2f} | Max: {df[col].max():.2f}")
    print(f"  Q1: {df[col].quantile(0.25):.2f} | Q3: {df[col].quantile(0.75):.2f}")

print(f"\n{df[numerical_cols].describe()}")

print("\nCATEGORICAL STATISTICS:")
for col in categorical_cols:
    print(f"\n{col}: {df[col].nunique()} unique values")
    print(df[col].value_counts().head(5))

#==============================================================================
# STEP 2: UNIVARIATE ANALYSIS - NUMERICAL
#==============================================================================
print("\n" + "="*80)
print("STEP 2: UNIVARIATE ANALYSIS - NUMERICAL")
print("="*80)

# Histograms
fig, axes = plt.subplots(3, 2, figsize=(14, 10))
fig.suptitle('Histograms - Numerical Features', fontsize=14, fontweight='bold')
for idx, col in enumerate(numerical_cols):
    ax = axes[idx // 2, idx % 2]
    ax.hist(df[col], bins=30, color='magenta', edgecolor='black', alpha=0.7)
    ax.set_title(col.replace("_", " ").title())
    ax.set_xlabel(col)
    ax.set_ylabel('Frequency')
plt.tight_layout()
plt.savefig('histograms_numerical.png', dpi=300, bbox_inches='tight')
plt.show()

# Box Plots
fig, axes = plt.subplots(3, 2, figsize=(14, 10))
fig.suptitle('Box Plots - Numerical Features', fontsize=14, fontweight='bold')
for idx, col in enumerate(numerical_cols):
    ax = axes[idx // 2, idx % 2]
    ax.boxplot(df[col], vert=True, patch_artist=True, boxprops=dict(facecolor='cyan', alpha=0.7))
    ax.set_title(col.replace("_", " ").title())
    ax.set_ylabel(col)
plt.tight_layout()
plt.savefig('boxplots_numerical.png', dpi=300, bbox_inches='tight')
plt.show()

# Density Plots
fig, axes = plt.subplots(3, 2, figsize=(14, 10))
fig.suptitle('Density Plots - Numerical Features', fontsize=14, fontweight='bold')
for idx, col in enumerate(numerical_cols):
    ax = axes[idx // 2, idx % 2]
    df[col].plot(kind='density', ax=ax, color='purple', linewidth=2)
    ax.set_title(col.replace("_", " ").title())
    ax.set_xlabel(col)
plt.tight_layout()
plt.savefig('density_plots_numerical.png', dpi=300, bbox_inches='tight')
plt.show()

#==============================================================================
# STEP 3: BIVARIATE ANALYSIS - NUMERICAL × NUMERICAL
#==============================================================================
print("\n" + "="*80)
print("STEP 3: BIVARIATE ANALYSIS - NUMERICAL × NUMERICAL")
print("="*80)

correlation_matrix = df[numerical_cols].corr()
print(f"\n{correlation_matrix.round(3)}")

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0, square=True)
plt.title('Correlation Heatmap', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

scatter_pairs = [('price', 'rating'), ('num_reviews', 'rating'), ('discount_percent', 'rating'), ('price', 'num_reviews'), ('old_price', 'price'), ('discount_value', 'num_reviews')]

fig, axes = plt.subplots(3, 2, figsize=(14, 10))
fig.suptitle('Scatter Plots - Key Relationships', fontsize=14, fontweight='bold')
for idx, (x_col, y_col) in enumerate(scatter_pairs):
    ax = axes[idx // 2, idx % 2]
    ax.scatter(df[x_col], df[y_col], alpha=0.4, s=20, color='darkred')
    ax.set_title(f'{x_col} vs {y_col}')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
plt.tight_layout()
plt.savefig('scatter_plots_relationships.png', dpi=300, bbox_inches='tight')
plt.show()

#==============================================================================
# STEP 4: OUTLIERS & ANOMALIES
#==============================================================================
print("\n" + "="*80)
print("STEP 4: OUTLIERS & ANOMALIES")
print("="*80)

for col in numerical_cols:
    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    outliers_count = len(df[(df[col] < lower) | (df[col] > upper)])
    print(f"{col}: IQR={IQR:.2f}, Outliers={outliers_count} ({(outliers_count/len(df)*100):.1f}%)")

fig, ax = plt.subplots(figsize=(12, 6))
df_normalized = df[numerical_cols].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
ax.boxplot([df_normalized[col] for col in numerical_cols], labels=numerical_cols, patch_artist=True, boxprops=dict(facecolor='cyan'))
ax.set_title('Box Plots - All Features (Normalized)', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('boxplots_all_features.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\nTop 5 Highest Priced:\n{df.nlargest(5, 'price')[['name', 'brand', 'price', 'rating']]}")
print(f"\nTop 5 Lowest Priced:\n{df.nsmallest(5, 'price')[['name', 'brand', 'price', 'rating']]}")
print(f"\nTop 5 Highest Rated:\n{df.nlargest(5, 'rating')[['name', 'brand', 'rating', 'price']]}")
print(f"\nTop 5 Lowest Rated:\n{df.nsmallest(5, 'rating')[['name', 'brand', 'rating', 'price']]}")
print(f"\nTop 5 Most Reviewed:\n{df.nlargest(5, 'num_reviews')[['name', 'brand', 'num_reviews', 'rating']]}")
print(f"\nTop 5 Highest Discount:\n{df.nlargest(5, 'discount_percent')[['name', 'brand', 'discount_percent', 'price']]}")

#==============================================================================
# STEP 5: SUMMARY PART 1
#==============================================================================
print("\n" + "="*80)
print("STEP 5: SUMMARY - PART 1")
print("="*80)

print(f"\nTotal Products: {len(df)}")
print(f"Unique Brands: {df['brand'].nunique()}")
print(f"\nPrice: Mean=EGP {df['price'].mean():.2f}, Range=[{df['price'].min():.2f}, {df['price'].max():.2f}]")
print(f"Rating: Mean={df['rating'].mean():.2f}, Products >=4.0: {len(df[df['rating'] >= 4.0])} ({(len(df[df['rating'] >= 4.0])/len(df)*100):.1f}%)")
print(f"Reviews: Mean={df['num_reviews'].mean():.0f}")
print(f"Discount: {df['has_discount'].sum()} products ({(df['has_discount'].sum()/len(df)*100):.1f}%), Mean={df['discount_percent'].mean():.2f}%")
print(f"\nKey Correlations:")
print(f"  Price-Rating: {df['price'].corr(df['rating']):.3f}")
print(f"  Reviews-Rating: {df['num_reviews'].corr(df['rating']):.3f}")

print("\n" + "="*80)
print("COMPLETED - Files saved: histograms_numerical.png, boxplots_numerical.png, density_plots_numerical.png, correlation_heatmap.png, scatter_plots_relationships.png, boxplots_all_features.png")
print("="*80)