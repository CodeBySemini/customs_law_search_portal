#24ada059 Vishmi
import pandas as pd

def load_table(file_path):
    return pd.read_csv(file_path)

def format_table(df):
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    return df
