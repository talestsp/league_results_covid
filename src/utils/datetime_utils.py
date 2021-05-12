import pandas as pd

def date_str_to_datetime(date_str):
    if pd.isna(date_str):
        return None

    elif len(date_str) == 8:
        dt = pd.to_datetime(date_str, format="%d/%m/%y")
    elif len(date_str) == 10:
        dt = pd.to_datetime(date_str, format="%d/%m/%Y")
    else:
        raise Exception("Date format unknown")

    return dt
