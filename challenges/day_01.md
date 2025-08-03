# Day 1 Challenge - WhatsApp Group Size Engagement Analysis

You are a Product Analyst on the WhatsApp team investigating group messaging dynamics. Your team wants to understand how large groups are being used and their messaging patterns. You'll leverage data to uncover insights about group participation and communication behaviors.

---

## Question 1 of 3

What is the maximum number of participants among WhatsApp groups that were created in October 2024?  
This metric will help us understand the largest group size available.

### Approach

The goal is to find the maximum value of `participant_count` for groups where `created_date` is in October 2024.

Steps:

1. Filter the DataFrame for rows where `created_date` is in October 2024.
2. Extract the `participant_count` column from those filtered rows.
3. Find the maximum of that column using `.max()`.

```python
# Step 1: Convert created_date to datetime if not already
dim_groups['created_date'] = pd.to_datetime(dim_groups['created_date'])

# Step 2: Filter groups created in October 2024
oct_2024_groups = dim_groups[
    (dim_groups['created_date'].dt.year == 2024) &
    (dim_groups['created_date'].dt.month == 10)
]

# Step 3: Find the max participant count
max_participants = oct_2024_groups['participant_count'].max()

# Step 4: Print the result
print(max_participants)
```

---

## Question 2 of 3

What is the average number of participants in WhatsApp groups that were created in October 2024?  
This number will indicate the typical group size and inform our group messaging feature considerations.

### Approach

1. Ensure `created_date` is in datetime format.
2. Filter the DataFrame for groups created in October 2024.
3. Extract `participant_count` for those filtered rows.
4. Calculate the average using `.mean()`.

```python
# Step 1: Convert created_date to datetime if needed
dim_groups['created_date'] = pd.to_datetime(dim_groups['created_date'])

# Step 2: Filter for October 2024
oct_2024_groups = dim_groups[
    (dim_groups['created_date'].dt.year == 2024) &
    (dim_groups['created_date'].dt.month == 10)
]

# Step 3: Calculate the average number of participants
avg_participants = oct_2024_groups['participant_count'].mean()

# Step 4: Print the result
print("Average number of participants in October 2024 groups:", avg_participants)
```

---

## Question 3 of 3

For WhatsApp groups with more than 50 participants that were created in October 2024, what is the average number of messages sent?
This insight will help assess engagement in larger groups and support recommendations for group messaging features.

### Approach

1. Convert `created_date` to datetime to filter accurately.
2. Filter the DataFrame using two conditions:
   - Groups created in October 2024
   - Groups with more than 50 participants
3. Compute the average of `total_messages`.

```python
# Step 1: Ensure created_date is datetime
dim_groups['created_date'] = pd.to_datetime(dim_groups['created_date'])

# Step 2: Filter for groups created in October 2024 with > 50 participants
large_active_groups = dim_groups[
    (dim_groups['created_date'].dt.year == 2024) &
    (dim_groups['created_date'].dt.month == 10) &
    (dim_groups['participant_count'] > 50)
]

# Step 3: Compute the average number of messages
avg_messages = large_active_groups['total_messages'].mean()

# Step 4: Print result
print("Average number of messages in large groups created in October 2024:", avg_messages)
```
