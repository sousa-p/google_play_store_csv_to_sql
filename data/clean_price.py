import pandas as pd


def clean_price(value):
    if pd.isna(value):
        return 0
    value = str(value).replace("$", "")
    
    try:
        return float(value)
    except ValueError:
        return 0
