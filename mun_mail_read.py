import pandas as pd
def get_columns(path):
    id_column = pd.read_excel(path, usecols=[0], sheet_name=0)

    email_column = pd.read_excel(path, usecols=[1], sheet_name=0)
    return id_column, email_column
