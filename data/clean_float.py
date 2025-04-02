import pandas as pd
import re


def clean_float(rating):
    try:
        value = float(rating) if pd.notna(rating) and str(rating).replace('.', '', 1).isdigit() else None
        if value is None or (value < 0 or value > 5):
            return 0
        return value
    except ValueError:
        return 0
