import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import csv

class Arules:
    def __init__(self):
        print('Arules is in use. please pass a list as transactions.')
        return

    def get_frequent_item_sets(self,transactions,min_support,min_confidence):
        #why min_confidence? we dont need it here.
        dataset = pd.DataFrame({'Transaction': ['T{}'.format(i) for i in range(1, len(transactions)+1)],'Items': transactions})
        basket_sets = pd.get_dummies(dataset['Items'].apply(pd.Series).stack()).sum(level=0)
        frequent_itemsets = apriori(basket_sets, min_support=min_support, use_colnames=True)
        return frequent_itemsets.sort_values(by='support', ascending=False)

    def get_arules(self,transactions,min_support=0,min_confidence=0,min_lift=0,sort_by='lift'):
        # sort_by: lift , confidence, support
        if sort_by not in ['lift', 'confidence', 'support']:
            raise ValueError("Invalid parameter for sort_by. Allowed Strings for sort_by are 'lift', 'confidence', and 'support'.")
        #First Calculate Frequent itemsets:
        frequent_itemsets=Arules().get_frequent_item_sets(transactions,min_support,min_confidence)
        #arules:
        association_rules_df = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence, support_only=False)
        association_rules_df = association_rules_df[association_rules_df['lift'] > min_lift]
        association_rules_df = association_rules_df[association_rules_df['consequents'].apply(lambda x: len(x) == 1)]
        association_rules_df = association_rules_df.sort_values(by=sort_by, ascending=False)
        return association_rules_df

Purchases = []
# make it a list and remove nulls.
with open('A:/groceries.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        row = [item.strip() for item in row if item.strip()]
        if row:
            Purchases.append(row)


print(Arules().get_frequent_item_sets(Purchases,0.005,0.2).head(10))

print(Arules().get_arules(Purchases,0.005,0.2,1,"lift"))

