import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

df = pd.read_csv("D:\\Educational\\Projects\\Python\\DSM\\jumia_1500_cleanedd.csv")
print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns\n")

#==============================================================================
# STEP 6-7: BRAND & RATING ANALYSIS
#==============================================================================
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

df['brand'].value_counts().head(10).plot(kind='barh', ax=axes[0,0], color='coral', edgecolor='black')
axes[0,0].set_title('Top 10 Brands', fontweight='bold')

axes[0,1].pie(df['brand'].value_counts().head(5), labels=df['brand'].value_counts().head(5).index, autopct='%1.1f%%')
axes[0,1].set_title('Top 5 Brands', fontweight='bold')

top_brands = df['brand'].value_counts().head(10).index
df[df['brand'].isin(top_brands)].groupby('brand')['rating'].mean().sort_values(ascending=False).plot(
    kind='bar', ax=axes[0,2], color='mediumpurple', edgecolor='black')
axes[0,2].axhline(df['rating'].mean(), color='red', linestyle='--', label='Avg')
axes[0,2].set_title('Avg Rating by Brand', fontweight='bold')
axes[0,2].legend()
plt.setp(axes[0,2].xaxis.get_majorticklabels(), rotation=45, ha='right')

df['price_range'].value_counts().plot(kind='bar', ax=axes[1,0], color='lightgreen', edgecolor='black')
axes[1,0].set_title('Price Range Distribution', fontweight='bold')
plt.setp(axes[1,0].xaxis.get_majorticklabels(), rotation=45, ha='right')

df.groupby('brand')['discount_value'].mean().sort_values(ascending=False).head(10).plot(
    kind='barh', ax=axes[1,1], color='gold', edgecolor='black')
axes[1,1].set_title('Avg Discount by Brand', fontweight='bold')

df.groupby('brand')['num_reviews'].mean().sort_values(ascending=False).head(10).plot(
    kind='bar', ax=axes[1,2], color='teal', edgecolor='black')
axes[1,2].set_title('Avg Reviews by Brand', fontweight='bold')
plt.setp(axes[1,2].xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('step6_7_brand_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

#==============================================================================
# STEP 8-9: PRICE & DISCOUNT ANALYSIS
#==============================================================================
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

scatter1 = axes[0,0].scatter(df['price'], df['rating'], c=df['rating'], cmap='RdYlGn', alpha=0.6, vmin=0, vmax=5)
axes[0,0].set_xlabel('Price (EGP)')
axes[0,0].set_ylabel('Rating')
axes[0,0].set_title('Price vs Rating', fontweight='bold')
axes[0,0].grid(True, alpha=0.3)
plt.colorbar(scatter1, ax=axes[0,0], label='Rating')

axes[0,1].hist(df['price'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
axes[0,1].axvline(df['price'].mean(), color='red', linestyle='--', label=f'Mean: {df["price"].mean():.0f}')
axes[0,1].axvline(df['price'].median(), color='green', linestyle='--', label=f'Median: {df["price"].median():.0f}')
axes[0,1].set_title('Price Distribution', fontweight='bold')
axes[0,1].legend()

discount_data = df[df['has_discount'] == 1]['discount_percent']
axes[0,2].hist(discount_data, bins=30, color='orange', edgecolor='black', alpha=0.7)
axes[0,2].axvline(discount_data.mean(), color='red', linestyle='--', label=f'Mean: {discount_data.mean():.1f}%')
axes[0,2].set_title('Discount % Distribution', fontweight='bold')
axes[0,2].legend()

price_range_order = ['Low', 'Small', 'Medium', 'Large', 'High']
existing = [pr for pr in price_range_order if pr in df['price_range'].unique()]
sns.violinplot(data=df, x='price_range', y='price', order=existing, ax=axes[1,0], palette='muted')
axes[1,0].set_title('Price by Range', fontweight='bold')
plt.setp(axes[1,0].xaxis.get_majorticklabels(), rotation=45, ha='right')

df.groupby('price_range')['rating'].mean().reindex(existing).plot(
    kind='line', ax=axes[1,1], marker='s', color='green', linewidth=2)
axes[1,1].set_title('Avg Rating by Price Range', fontweight='bold')
axes[1,1].set_ylim(0, 5)
axes[1,1].grid(True, alpha=0.3)

df['price_range'].value_counts().reindex(existing).plot(
    kind='line', ax=axes[1,2], marker='o', color='crimson', linewidth=2)
axes[1,2].set_title('Products by Price Range', fontweight='bold')
axes[1,2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('step8_9_price_discount.png', dpi=300, bbox_inches='tight')
plt.show()

#==============================================================================
# TIME-BASED TRENDS
#==============================================================================
if 'date' in df.columns or 'year' in df.columns:
    print("\nTIME-BASED TRENDS ANALYSIS")
    if 'date' in df.columns:
        df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year
    
    if 'year' in df.columns and df['year'].notna().sum() > 0:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        df.groupby('year')['price'].mean().plot(kind='line', ax=axes[0,0], marker='o', color='steelblue', linewidth=2)
        axes[0,0].set_title('Avg Price Over Years', fontweight='bold')
        axes[0,0].grid(True, alpha=0.3)
        
        df['year'].value_counts().sort_index().plot(kind='bar', ax=axes[0,1], color='coral', edgecolor='black')
        axes[0,1].set_title('Products Per Year', fontweight='bold')
        plt.setp(axes[0,1].xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        df.groupby('year')['rating'].mean().plot(kind='line', ax=axes[1,0], marker='s', color='green', linewidth=2)
        axes[1,0].set_title('Avg Rating Over Years', fontweight='bold')
        axes[1,0].set_ylim(0, 5)
        axes[1,0].grid(True, alpha=0.3)
        
        df.groupby('year')['discount_value'].mean().plot(kind='line', ax=axes[1,1], marker='^', color='orange', linewidth=2)
        axes[1,1].set_title('Avg Discount Over Years', fontweight='bold')
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('time_based_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("Time-based trends completed\n")
    else:
        print("No valid year data\n")
else:
    print("\nNo date/year column - skipping time trends\n")

#==============================================================================
# STEP 10: SEGMENTATION
#==============================================================================
df['rating_category'] = pd.cut(df['rating'], bins=[0, 3, 4, 4.5, 5], labels=['Low', 'Medium', 'Good', 'Excellent'])
df['price_segment'] = pd.qcut(df['price'], q=4, labels=['Budget', 'Economy', 'Mid-Range', 'Premium'])

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

rating_counts = df['rating_category'].value_counts()
rating_counts.plot(kind='bar', ax=axes[0,0], color=['red', 'orange', 'lightgreen', 'darkgreen'], edgecolor='black')
axes[0,0].set_title('Rating Categories', fontweight='bold')
plt.setp(axes[0,0].xaxis.get_majorticklabels(), rotation=45, ha='right')

axes[0,1].pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%',
              colors=['red', 'orange', 'lightgreen', 'darkgreen'])
axes[0,1].set_title('Rating Distribution', fontweight='bold')

df[df['rating'] >= 4.5]['brand'].value_counts().head(10).plot(kind='barh', ax=axes[1,0], color='gold', edgecolor='black')
axes[1,0].set_title('Top Brands (Rating ≥4.5)', fontweight='bold')

df['price_segment'].value_counts().plot(kind='bar', ax=axes[1,1], color='purple', edgecolor='black')
axes[1,1].set_title('Price Segments', fontweight='bold')
plt.setp(axes[1,1].xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('step10_segmentation.png', dpi=300, bbox_inches='tight')
plt.show()

#==============================================================================
# STEP 11: MULTIVARIATE ANALYSIS
#==============================================================================
num_cols = ['price', 'old_price', 'rating', 'discount_value', 'discount_percent']

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.heatmap(df[num_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm', 
            ax=axes[0], center=0, square=True, cbar_kws={'label': 'Correlation'})
axes[0].set_title('Correlation Matrix', fontweight='bold')

top_brands_list = df['brand'].value_counts().head(10).index
pivot = df[df['brand'].isin(top_brands_list)].groupby(['brand', 'price_segment']).size().unstack(fill_value=0)
sns.heatmap(pivot, annot=True, fmt='d', cmap='YlOrRd', ax=axes[1], cbar_kws={'label': 'Count'})
axes[1].set_title('Brand × Price Segment', fontweight='bold')

plt.tight_layout()
plt.savefig('step11_multivariate.png', dpi=300, bbox_inches='tight')
plt.show()

# Brand × Discount Range
crosstab_bd = pd.crosstab(df['brand'], df['discount_range'])
crosstab_filtered = crosstab_bd.loc[df['brand'].value_counts().head(10).index]

plt.figure(figsize=(10, 6))
sns.heatmap(crosstab_filtered, annot=True, fmt='d', cmap='Oranges', cbar_kws={'label': 'Count'})
plt.title('Brand × Discount Range', fontweight='bold')
plt.tight_layout()
plt.savefig('brand_discount_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

# Pair Plot
sns.pairplot(df[num_cols].sample(min(500, len(df))), diag_kind='kde', plot_kws={'alpha': 0.6})
plt.suptitle('Pair Plot - Numerical Features', y=1.02, fontweight='bold')
plt.tight_layout()
plt.savefig('step11_pairplot.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nAnalysis Complete!")