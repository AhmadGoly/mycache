import pandas

df = pandas.read_csv('sale.csv')

print("Old Summary statistics for numeric columns:\n", df.describe(include='number'))
print("Old Summary statistics for string columns:\n", df.describe(include='object'))

categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    df[col] = pandas.factorize(df[col])[0]

print("New Summary statistics for numeric columns:\n", df.describe(include='number'))
#print("New Summary statistics for string columns:\n", df.describe(include='object'))
