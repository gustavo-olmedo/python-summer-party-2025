from utils.group_analysis import load_data, filter_oct_2024, max_participants, avg_participants, avg_messages

if __name__ == "__main__":
    df = load_data("data/dim_groups.csv")

    # Filter groups created in October 2024
    oct_groups = filter_oct_2024(df)

    # Question 1
    print("Q1: Max participants:", max_participants(oct_groups))

    # Question 2
    print("Q2: Average participants:", avg_participants(oct_groups))

    # Question 3
    print("Q3: Average messages in large groups:", avg_messages(oct_groups, min_size=50))