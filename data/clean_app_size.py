import pandas as pd


def clean_app_size(size):
    if pd.isna(size):
        return None
    size = size.strip()
    if size.lower() == "varies with device":
        return None

    multiplier = 1
    if "M" in size:
        size = size.replace("M", "")
        multiplier = 1
    elif "k" in size:
        size = size.replace("k", "")
        multiplier = 1/1024
    try:
        return float(size) * multiplier
    except ValueError:
        return None
