import pandas
import matplotlib.pyplot as plt

myDataFrame = pandas.read_csv("sale.csv")
# entekhabe sotun haye numeric
numeric_cols = myDataFrame.select_dtypes(include=["float64", "int64"])

numeric_cols.boxplot()
plt.show()