import pandas as pd

def load_data(file):
    df = pd.read_excel(file)
    df.columns = [col.strip() for col in df.columns]
    if 'Comment' not in df.columns:
        df['Comment'] = ""
    return df
