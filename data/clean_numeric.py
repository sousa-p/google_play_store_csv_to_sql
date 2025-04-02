import pandas as pd
import re


def clean_numeric(value):
    if pd.isna(value):
        return None
    
    try:
        value = re.sub(r"[,+]", "", str(value))
        return int(value)
    except ValueError:
        return None
