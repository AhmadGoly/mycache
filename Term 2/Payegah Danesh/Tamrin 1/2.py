import pandas

oldDataFrame = pandas.read_csv("sale.csv")

newDataFrame = oldDataFrame.dropna(subset=["Item_Weight"])
newDataFrame["Outlet_Size"] = newDataFrame["Outlet_Size"].fillna("Unknown")

print("Old Summary statistics for numeric columns:\n", oldDataFrame.describe(include='number'))
print("Old Summary statistics for string columns:\n", oldDataFrame.describe(include='object'))

print("\n\nNew Summary statistics for numeric columns:\n", newDataFrame.describe(include='number'))
print("New Summary statistics for string columns:\n", newDataFrame.describe(include='object'))
