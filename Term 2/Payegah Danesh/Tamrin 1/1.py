import pandas

myDataFrame = pandas.read_csv("sale.csv")
print("Summary statistics for numeric columns:\n", myDataFrame.describe(include='number'))
print("\n\nSummary statistics for string columns:\n", myDataFrame.describe(include='object'))
