import pandas as pd
import time
import numpy as np
from sklearn.model_selection import train_test_split
import sys

# 2)-Loading dataset
data_file = '20190207_transactions.json'
transactions = pd.read_json(data_file, lines= True)

pd.melt(transactions.head(2).set_index('id')['products'].apply(pd.Series).reset_index(), 
             id_vars=['id'],
             value_name='products') \
    .dropna().drop(['variable'], axis=1) \
    .groupby(['id', 'products']) \
    .agg({'products': 'count'}) \
    .rename(columns={'products': 'purchase_count'}) \
    .reset_index() \
    .rename(columns={'products': 'productId'})

s=time.time()

data = pd.melt(transactions.set_index('id')['products'].apply(pd.Series).reset_index(), 
             id_vars=['id'],
             value_name='products') \
    .dropna().drop(['variable'], axis=1) \
    .groupby(['id', 'products']) \
    .agg({'products': 'count'}) \
    .rename(columns={'products': 'purchase_count'}) \
    .reset_index() \
    .rename(columns={'products': 'productId'})
data['productId'] = data['productId'].astype(np.int64)

print("Execution time:", round((time.time()-s)/60,2), "minutes")

prod_freq=data['productId'].value_counts(dropna=False)

prod_freq.index.name
prod_freq.index.name='prod_ID'

def product_frequency(prod_ID):
    if prod_ID not in prod_freq.index:
        print('Product not found.')
        return prod_ID
    return prod_freq.loc[prod_ID]

prod_ID=int(input("enter a product ID to find frequency: "))

print(product_frequency(prod_ID))