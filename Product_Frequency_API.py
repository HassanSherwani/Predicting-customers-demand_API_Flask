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



if __name__ == '__main__':
	app.run(debug=True)