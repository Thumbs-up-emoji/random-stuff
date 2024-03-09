import pandas as pd

def read():
    # Load the data
    df = pd.read_excel(r'C:\Users\ASUS\OneDrive - BITS Pilani K K Birla Goa Campus\Desktop\Stuff\CS\random-stuff\mun\new.xlsx')

    # Convert DataFrame to list of lists
    data = df.values.tolist()

    return data

if __name__ == "__main__":
    data=read()
    print(data)