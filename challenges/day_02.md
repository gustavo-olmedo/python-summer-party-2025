# Day 2 Challenge - Sponsored Posts Click Performance

You are a Product Analyst on the Amazon Sponsored Advertising team investigating sponsored product ad engagement across electronics categories. Your team wants to understand CTR variations to optimize targeted advertising strategies.

---

## Question 1 of 3

What is the average click-through rate (CTR) for sponsored product ads for each product category that contains the substring 'Electronics' in its name during October 2024?

### Data Tables

fct_ad_performance:
Columns: ad_id, product_id, clicks, impressions, recorded_date

dim_product:
Columns: product_id, product_category, product_name

🎯 Goal
Calculate average CTR (clicks / impressions) per product category, where:

The category contains 'Electronics'

The record is from October 2024

### Approach

1. Convert recorded_date to datetime in fct_ad_performance
2. Filter ad records to only October 2024
3. Join fct_ad_performance with dim_product on product_id
4. Filter product categories that contain 'Electronics'
5. Calculate CTR = clicks / impressions for each row
6. Group by product_category and calculate average CTR

```py
# Step 1: Convert date to datetime
fct_ad_performance['recorded_date'] = pd.to_datetime(fct_ad_performance['recorded_date'])

# Step 2: Filter for October 2024
oct_ads = fct_ad_performance[
(fct_ad_performance['recorded_date'].dt.year == 2024) &
(fct_ad_performance['recorded_date'].dt.month == 10)
]

# Step 3: Merge with product info
merged = pd.merge(oct_ads, dim_product, on='product_id', how='inner')

# Step 4: Filter for categories containing 'Electronics'
electronics_ads = merged[merged['product_category'].str.contains('Electronics', case=False, na=False)]

# Step 5: Calculate CTR
electronics_ads['ctr'] = electronics_ads['clicks'] / electronics_ads['impressions']

# Step 6: Group by category and calculate average CTR
avg_ctr_per_category = electronics_ads.groupby('product_category')['ctr'].mean().reset_index()

# Step 7: Print result
print(avg_ctr_per_category)
```

## Question 2 of 3

Which product categories have a CTR greater than the aggregated overall average CTR for sponsored product ads during October 2024?
This analysis will identify high-performing categories for further optimization. For this question, we want to calculate CTR for each ad, then get the average across ads by product category & overall.

### Approach

1. Convert recorded_date to datetime (if not already)
2. Filter fct_ad_performance for October 2024
3. Calculate CTR per ad: clicks / impressions
4. Join with dim_product on product_id
5. Group by product_category, compute average CTR
6. Compute overall average CTR (from all ad CTRs)
7. Filter product categories where category CTR > overall CTR

```py
# Step 1: Convert recorded_date to datetime
fct_ad_performance['recorded_date'] = pd.to_datetime(fct_ad_performance['recorded_date'])

# Step 2: Filter for October 2024
oct_ads = fct_ad_performance[
    (fct_ad_performance['recorded_date'].dt.year == 2024) &
    (fct_ad_performance['recorded_date'].dt.month == 10)
]

# Step 3: Calculate CTR per ad
oct_ads = oct_ads.copy()
oct_ads['ctr'] = oct_ads['clicks'] / oct_ads['impressions']

# Step 4: Join with product data
merged = pd.merge(oct_ads, dim_product, on='product_id', how='inner')

# Step 5: Calculate average CTR per category
category_ctr = merged.groupby('product_category')['ctr'].mean().reset_index()

# Step 6: Calculate overall average CTR
overall_avg_ctr = merged['ctr'].mean()

# Step 7: Filter categories above the overall average CTR
high_performing = category_ctr[category_ctr['ctr'] > overall_avg_ctr]

# Step 8: Print results
print("Overall Average CTR:", overall_avg_ctr)
print("\nHigh-performing categories:")
print(high_performing)
```

## Question 3 of 3

For the product categories identified in the previous question, what is the percentage difference between their CTR and the overall average CTR for October 2024? This analysis will quantify the performance gap to recommend specific categories for targeted advertising optimization.

### Approach

Assuming you already:

1. Calculated CTR per ad
2. Grouped by category to get average CTR
3. Calculated overall average CTR
4. Identified high-performing categories

Now I will:

1. Use the category_ctr DataFrame from Question 2
2. Filter again for categories where CTR > overall average
3. Calculate % difference for each:

percent_diff=((category CTR − overall CTR) / overall CTR)×100

Return a DataFrame with:

- product_category
- category_ctr
- overall_ctr
- percent_diff

```py
# Convert recorded_date to datetime
fct_ad_performance['recorded_date'] = pd.to_datetime(fct_ad_performance['recorded_date'])

# Filter for October 2024
oct_ads = fct_ad_performance[
    (fct_ad_performance['recorded_date'].dt.year == 2024) &
    (fct_ad_performance['recorded_date'].dt.month == 10)
].copy()

# Calculate CTR per ad
oct_ads['ctr'] = oct_ads['clicks'] / oct_ads['impressions']

# Join with product info
merged = pd.merge(oct_ads, dim_product, on='product_id', how='inner')

# Compute average CTR by category
category_ctr = merged.groupby('product_category')['ctr'].mean().reset_index()

# Compute overall average CTR
overall_avg_ctr = merged['ctr'].mean()

# Filter categories with above-average CTR
high_performing = category_ctr[category_ctr['ctr'] > overall_avg_ctr].copy()

# Calculate % difference
high_performing['overall_ctr'] = overall_avg_ctr
high_performing['percent_diff'] = (
    (high_performing['ctr'] - overall_avg_ctr) / overall_avg_ctr
) * 100

# Show results
print(high_performing[['product_category', 'ctr', 'overall_ctr', 'percent_diff']])
```
