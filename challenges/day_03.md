# Day 3 Challenge - Disney Parks Guest Spending Behavior

You are a data analyst working with the Disney Parks revenue team to understand nuanced guest spending patterns across different park experiences. The team wants to develop a comprehensive view of visitor purchasing behaviors. Your goal is to uncover meaningful insights that can drive personalized marketing strategies.

---

## Question 1 of 3

What is the average spending per guest per visit for each park experience type during July 2024? Ensure that park experience types with no recorded transactions are shown with an average spending of 0.0. This analysis helps establish baseline spending differences essential for later segmentation.

Would you like to talk through your approach first, or are you ready to start coding?

### Data Tables

fct_guest_spending:
Columns: guest_id, visit_date, park_experience_type, amount_spent

### Goal

Group by guest_id, visit_date, and park_experience_type
→ So each "guest-visit" is a unit
Calculate total spent per guest per visit
Then calculate average per guest visit spending per park experience type
Include all experience types, even if spending = 0

### Approach

1. Convert visit_date to datetime
2. Filter for July 2024
3. Group by guest_id, visit_date, and park_experience_type to get total spent per visit
4. Then group by park_experience_type and compute the mean
5. Get all unique experience types and ensure missing ones show up with 0.0

```py
# Step 1: Ensure visit_date is datetime
fct_guest_spending['visit_date'] = pd.to_datetime(fct_guest_spending['visit_date'])

# Step 2: Filter for July 2024
july_data = fct_guest_spending[
    (fct_guest_spending['visit_date'].dt.year == 2024) &
    (fct_guest_spending['visit_date'].dt.month == 7)
]

# Step 3: Calculate total spent per guest per visit per experience type
guest_visit_spending = july_data.groupby(
    ['guest_id', 'visit_date', 'park_experience_type']
)['amount_spent'].sum().reset_index()

# Step 4: Compute average per-visit spending by experience type
avg_spending = guest_visit_spending.groupby('park_experience_type')['amount_spent'].mean().reset_index()

# Step 5: Ensure all experience types are represented
all_experiences = fct_guest_spending['park_experience_type'].unique()
all_experiences_df = pd.DataFrame({'park_experience_type': all_experiences})

avg_spending_full = pd.merge(all_experiences_df, avg_spending, on='park_experience_type', how='left')
avg_spending_full['amount_spent'] = avg_spending_full['amount_spent'].fillna(0.0)

# Step 6: Output result
print(avg_spending_full)
```

## Question 2 of 3

For guests who visited our parks more than once in August 2024, what is the difference in spending between their first and their last visit?
This investigation, using sequential analysis, will reveal any shifts in guest spending behavior over multiple visits.

### Goal

1. Focus on guests with 2+ visits in August 2024
2. For each such guest:
   - Calculate total spent per visit
   - Sort visits chronologically
   - Get spending on first and last visit
   - Compute: difference = last visit − first visit

### Approach

1. Convert visit_date to datetime
2. Filter data to August 2024
3. Group by guest_id and visit_date → sum amount_spent
4. Count visits per guest, filter for guests with >1 visit
5. For each guest:
   - Sort by visit_date
   - Take first and last
   - Compute spending difference
6. Return guest_id, first_visit, last_visit, and difference

```py
import pandas as pd

# Load data
fct_guest_spending = pd.read_csv("data/fct_guest_spending.csv")
fct_guest_spending['visit_date'] = pd.to_datetime(fct_guest_spending['visit_date'])

# Step 1: Filter for August 2024
august_data = fct_guest_spending[
    (fct_guest_spending['visit_date'].dt.year == 2024) &
    (fct_guest_spending['visit_date'].dt.month == 8)
]

# Step 2: Total spending per guest per visit
guest_visits = august_data.groupby(['guest_id', 'visit_date'])['amount_spent'].sum().reset_index()

# Step 3: Filter guests with more than one visit
visit_counts = guest_visits['guest_id'].value_counts()
multi_visitors = visit_counts[visit_counts > 1].index
multi_visit_data = guest_visits[guest_visits['guest_id'].isin(multi_visitors)]

# Step 4: Calculate difference between first and last visit
def calc_diff(df):
    df_sorted = df.sort_values('visit_date')
    first = df_sorted.iloc[0]['amount_spent']
    last = df_sorted.iloc[-1]['amount_spent']
    return pd.Series({
        'first_visit_spending': first,
        'last_visit_spending': last,
        'difference': last - first
    })

spending_diff = multi_visit_data.groupby('guest_id').apply(calc_diff).reset_index()

# Step 5: Output
print(spending_diff)
```

## Question 3 of 3

In September 2024, how can guests be categorized into distinct spending segments such as Low, Medium, and High based on their total spending?
Use the following thresholds for categorization:

- Low: Includes values from $0 up to, but not including, $50.
- Medium: Includes values from $50 up to, but not including, $100.
- High: Includes values from $100 and above. Exclude guests who did not make any purchases in the period.

### Approach

1. Convert visit_date to datetime
2. Filter rows for September 2024
3. Group by guest_id, summing amount_spent
4. Filter out guests with amount_spent == 0
5. Categorize each guest into Low, Medium, or High

```py
import pandas as pd

# Load data
fct_guest_spending = pd.read_csv("data/fct_guest_spending.csv")
fct_guest_spending['visit_date'] = pd.to_datetime(fct_guest_spending['visit_date'])

# Step 1: Filter for September 2024
sept_data = fct_guest_spending[
    (fct_guest_spending['visit_date'].dt.year == 2024) &
    (fct_guest_spending['visit_date'].dt.month == 9)
]

# Step 2: Sum total spending per guest
guest_totals = sept_data.groupby('guest_id')['amount_spent'].sum().reset_index()

# Step 3: Exclude guests with 0 spending
guest_totals = guest_totals[guest_totals['amount_spent'] > 0].copy()

# Step 4: Categorize spending
def categorize(amount):
    if amount < 50:
        return "Low"
    elif amount < 100:
        return "Medium"
    else:
        return "High"

guest_totals['spending_segment'] = guest_totals['amount_spent'].apply(categorize)

# Step 5: Output
print(guest_totals)
```
