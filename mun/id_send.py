import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook

# Step 2: Read the existing Excel file
df = pd.read_excel('existing_file.xlsx')

# Step 3: Extract the particular row
row = df.iloc[[19]]  # Change the index to the row you want

# Step 4: Write the row to a new Excel file
row.to_excel('new_file.xlsx', index=False)

# Step 5: Read the new Excel file
wb = load_workbook(filename='new_file.xlsx')
sheet = wb.active

# Step 6: Convert the Excel file to a DataFrame
data = sheet.values
cols = next(data)[1:]
data_rows = list(data)
df_new = pd.DataFrame(data_rows, columns=cols)

# Step 7: Plot the DataFrame
df_new.plot(kind='bar')

# Step 8: Save the plot as a JPEG image
plt.savefig('output.jpg')