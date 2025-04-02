import pandas as pd
import re


def clean_float(value):
    if pd.isna(value):
        return None
    try:
        value = re.sub(r"[,+]", "", str(value))
        return float(value)
    except ValueError:
        return None
