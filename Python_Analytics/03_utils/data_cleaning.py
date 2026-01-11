# 03_utils/data_cleaning.py
import pandas as pd

def fill_na_with_zero(df, columns):
    """
    Replace NaN values with 0 in specified columns
    """
    for col in columns:
        df[col] = df[col].fillna(0)
    return df

def ensure_numeric(df, columns):
    """
    Convert specified columns to numeric type
    """
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df
