import pandas
import matplotlib.pyplot as plt

df = pandas.read_csv("sale.csv")

df["Item_Visibility"].plot(kind="box")
plt.title("Item_Visibility BoxPlot")
plt.show()

df["Item_Outlet_Sales"].plot(kind="box")
plt.title("Item_Outlet_Sales BoxPlot")
plt.show()