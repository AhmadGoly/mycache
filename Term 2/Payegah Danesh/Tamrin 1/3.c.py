import pandas
import matplotlib.pyplot as plt
import numpy as np

df = pandas.read_csv("sale.csv")


print("Old Summary statistics for numeric columns:\n", df.describe(include='number'))
print("Old Summary statistics for string columns:\n", df.describe(include='object'))

df["Item_Visibility"].plot(kind="box")
plt.title("Item_Visibility BoxPlot")
plt.show()

#removing outliers for Item_Visibility Column:
z_scores = np.abs((df["Item_Visibility"] - df["Item_Visibility"].mean()) / df["Item_Visibility"].std())
threshold = 2.37
mask = z_scores < threshold
df = df[mask]


print("New Summary statistics for numeric columns:\n", df.describe(include='number'))
print("New Summary statistics for string columns:\n", df.describe(include='object'))


df["Item_Visibility"].plot(kind="box")
plt.title("Item_Visibility BoxPlot")
plt.show()