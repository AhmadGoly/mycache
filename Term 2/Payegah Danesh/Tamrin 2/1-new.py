import csv
from collections import Counter
import matplotlib.pyplot as plt
import statistics
import pandas as pd


df = pd.read_csv('A:/Assignment-1_Data.csv', delimiter=';')
bill_item_dict = {}
for bill, items in df.groupby('BillNo')['Itemname']:
    bill_item_dict[bill] = list(items)
transactions = list(bill_item_dict.values())

purchases=transactions
#print(purchases[:5])
all_items = [item for purchase in purchases for item in purchase]
num_transactions = len(purchases)
num_unique_items = len(set(all_items))
print(f'Total number of transactions: {num_transactions}')
print(f'Total number of unique Products: {num_unique_items}.')
#print(f'Here is the list of unique Products:\n*****************************\n{set(all_items)}\n*****************************')

# top 10 and kamtarin va bishtarin
item_counts = Counter(all_items)
top_items = item_counts.most_common(10)
print('Top 10 Products:\n------------------------------------------')
for item, count in top_items:
    print(f'{item}: {count}')

print('------------------------------------------')
most_sold_item = max(item_counts, key=item_counts.get)
least_sold_item = min(item_counts, key=item_counts.get)
print(f"Bishtarin Foroosh: {most_sold_item} ({item_counts[most_sold_item]} times)")
print(f"Kamtarin Foroosh: {least_sold_item} ({item_counts[least_sold_item]} times)")

#avg and median
avg_num_products = sum(len(purchase) for purchase in purchases) / len(purchases)
median_num_products = statistics.median(len(purchase) for purchase in purchases)
print(f"Average: {avg_num_products:.2f}")
print(f"Median: {median_num_products}")

# Histogram
transaction_lengths = [len(purchase) for purchase in purchases]
n_bins = max(transaction_lengths)
plt.hist(transaction_lengths, bins=range(1, n_bins+2), align='left')
plt.xlabel('Number of items per transaction')
plt.ylabel('Frequency')
plt.title('Number of items per transaction')
column_counts = [0] * n_bins
for length in transaction_lengths:
    column_counts[length-1] += 1
plt.xticks(range(1, n_bins+1), [str(i) + '\n(' + str(count) + ')' for i, count in enumerate(column_counts, start=1)])
plt.show()

# Box plot
plt.boxplot(transaction_lengths)
plt.ylabel('Number of items per transaction')
plt.title('Number of items per transaction')
plt.show()

# Scatter plot
transaction_length_counts = dict(sorted(Counter(transaction_lengths).items()))
plt.scatter(list(transaction_length_counts.keys()), list(transaction_length_counts.values()))
plt.xlabel('Number of items per transaction')
plt.ylabel('Frequency')
plt.title('Transaction length and frequency')
plt.show()