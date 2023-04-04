import pandas
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Step 1: Load the Dataset
OldDataFrame = pandas.read_csv("sale.csv")

print("Old Summary statistics for numeric columns:\n", OldDataFrame.describe(include='number'))
print("Old Summary statistics for string columns:\n", OldDataFrame.describe(include='object'))

# Step 2: joda sazi dadehaye adadi va gheyre adadi
numeric_cols = OldDataFrame.select_dtypes(include="number").columns
non_numeric_cols = OldDataFrame.select_dtypes(exclude="number").columns

# Step 3: Normal sazi va bartaraf kardane moshkelate missing values.
imputer = SimpleImputer(strategy="mean")
OldDataFrame[numeric_cols] = imputer.fit_transform(OldDataFrame[numeric_cols])
scaler = StandardScaler()
OldDataFrame[numeric_cols] = scaler.fit_transform(OldDataFrame[numeric_cols])

# Step 4: PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(OldDataFrame[numeric_cols])
Pca_Dataframe = pandas.DataFrame(data = pca_result, columns = ['PC1', 'PC2'])
Pca_Dataframe[non_numeric_cols] = OldDataFrame[non_numeric_cols]

print("New Summary statistics for numeric columns:\n", Pca_Dataframe.describe(include='number'))
print("New Summary statistics for string columns:\n", Pca_Dataframe.describe(include='object'))
Pca_Dataframe.to_csv('newSale',index=False)