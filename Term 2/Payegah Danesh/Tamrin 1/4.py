import pandas
import numpy as np

df = pandas.read_csv('sale.csv')

print("Old Summary statistics for numeric columns:\n", df.describe(include='number'))
print("Old Summary statistics for string columns:\n", df.describe(include='object'))

# identify the numeric columns and then normal sazi dadeha 
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())

# show the normalized dataset
print("New Summary statistics for numeric columns:\n", df.describe(include='number'))
print("New Summary statistics for string columns:\n", df.describe(include='object'))