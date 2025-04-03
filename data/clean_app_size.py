import pandas as pd


def clean_app_size(size):
    if pd.isna(size):
        return 0
    size = size.strip()
    if size.lower() == "varies with device":
        return -1

    multiplier = 1
    if "M" in size:
        size = size.replace("M", "")
        multiplier = 1024
    elif "k" in size:
        size = size.replace("k", "")
    try:
        return int(float(size) * multiplier)
    except ValueError:
        return 0
