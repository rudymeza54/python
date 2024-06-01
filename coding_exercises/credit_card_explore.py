import os
import pandas as pd


# include directory path for data
path = (r"C:\Users\rudym\OneDrive\Desktop\VS Code\python\credit_card_fraud")

# Check
print(path)

# Find file
dir = os.listdir(path)

# read file in 
for file in dir:
    data_path = os.path.join(path, file)
    df = pd.read_csv(data_path)


# Explore data and see missing data

df.head()