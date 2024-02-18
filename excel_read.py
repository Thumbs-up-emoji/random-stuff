import pandas as pd

def read():
    # Load the data
    df = pd.read_excel('new.xlsx')

    # Convert DataFrame to list of lists
    data = df.values.tolist()

    return data

if __name__ == "__main__":
    read()