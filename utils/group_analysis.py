import pandas as pd

def load_data(filepath):
    df = pd.read_csv(filepath)
    df['created_date'] = pd.to_datetime(df['created_date'])
    return df

def filter_oct_2024(df):
    return df[
        (df['created_date'].dt.year == 2024) &
        (df['created_date'].dt.month == 10)
    ]

def max_participants(df):
    return df['participant_count'].max()

def avg_participants(df):
    return df['participant_count'].mean()

def avg_messages(df, min_size=50):
    return df[df['participant_count'] > min_size]['total_messages'].mean()