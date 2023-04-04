import pandas
import matplotlib.pyplot as plt
import numpy as np
myDataFrame = pandas.read_csv('sale.csv')

#normalsazi
numeric_cols = myDataFrame.select_dtypes(include=[np.number]).columns
myDataFrame[numeric_cols] = (myDataFrame[numeric_cols] - myDataFrame[numeric_cols].min()) / (myDataFrame[numeric_cols].max() - myDataFrame[numeric_cols].min())

#plot kardane sotoonhaye morede nazar
myDataFrame['Item_Weight'].plot(kind='kde')
myDataFrame['Item_MRP'].plot(kind='kde')
myDataFrame['Item_Outlet_Sales'].plot(kind='kde')
#add info
plt.legend(['Item_Weight','Item_MRP','Item_Outlet_Sales'],title="List")

#rasme nemoodar
plt.show()