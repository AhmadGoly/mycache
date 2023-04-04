import pandas

oldDataFrame = pandas.read_csv("sale.csv")

newDataFrame = oldDataFrame.dropna(subset=["Item_Weight"])

print("Old Summary statistics for numeric columns:\n", oldDataFrame.describe(include='number'))
print("\n\nNew Summary statistics for numeric columns:\n", newDataFrame.describe(include='number'))