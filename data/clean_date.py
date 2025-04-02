import pandas as pd


def clean_date(date_str):
    if pd.isna(date_str):
        return None
    try:
        parsed_date = pd.to_datetime(date_str)
        return parsed_date.strftime("%Y-%m-%d")
    except Exception:
        return date_str