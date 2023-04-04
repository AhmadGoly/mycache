import pandas
import seaborn as sns
import matplotlib.pyplot as plt
myDataFrame = pandas.read_csv('sale.csv')

# Numbers only
numeric_cols = myDataFrame.select_dtypes(include=['float64', 'int64'])

# mohasebeye hambastegi
corr_matrix = numeric_cols.corr()

# Draw using heatmap or pairplot or pandas plotting tool
#sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
sns.pairplot(corr_matrix)
#pandas.plotting.scatter_matrix(corr_matrix,diagonal='hist')

plt.show()
