# For data processing
import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
import sys

# for api

from flask import Flask,render_template,url_for,request
import pickle
from sklearn.externals import joblib

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')
@app.route('/product',methods=['POST'])
def product():
    data_file = '20190207_transactions.json'
    transactions = pd.read_json(data_file, lines= True)
#Unpivots a DataFrame
    pd.melt(transactions.head(2).set_index('id')['products'].apply(pd.Series).reset_index(), 
             id_vars=['id'],
             value_name='products') \
    .dropna().drop(['variable'], axis=1) \
    .groupby(['id', 'products']) \
    .agg({'products': 'count'}) \
    .rename(columns={'products': 'purchase_count'}) \
    .reset_index() \
    .rename(columns={'products': 'productId'})
    
    # Create dataframe with customerid, productid and purchase count
    
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

    
    data['productId'].value_counts(dropna=False)
    prod_freq=data['productId'].value_counts(dropna=False)
    
    # chaning index name
    prod_freq.index.name
    prod_freq.index.name='prod_ID'
    
    #json_object to get request
    json_object = request.get_json()
    prod_ID = json_object["prod_ID"]
    return str(product_frequency(prod_freq, prod_ID))
	
def product_frequency(prod_freq, prod_ID):		
    if prod_ID not in prod_freq.index:
        print('Product ID not found.')
        return prod_ID
    return prod_freq.loc[prod_ID]


if __name__ == '__main__':
	app.run(debug=True)