import pandas as pd
from datetime import datetime


def clean_date(date_str):
    if pd.isna(date_str):
        return datetime(1900, 1, 1).date()
    try:
        parsed_date = pd.to_datetime(date_str)
        return parsed_date.strftime("%Y-%m-%d")
    except Exception:
        return datetime(1900, 1, 1).date()