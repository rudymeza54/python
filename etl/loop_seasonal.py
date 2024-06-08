import mysql.connector
import pandas as pd
import glob
import numpy as np
import os
import csv
import yaml
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from dateutil.parser import parse








print('Reading mrts data\n reshaping now...')

dir = os.getcwd()


file = ''.join(os.path.join(dir,'output.csv'))


df = pd.read_csv(file)


result_df = pd.DataFrame()


def deseasonalize(series, freq = "M"):
    result = seasonal_decompose(series, model = 'additive', period = 12)
    return series - result.seasonal


df['deseasonal'] = np.nan


for business in df['business'].unique():
    business_data = df[df['business']==business]
    df.loc[business_data.index,'deseasonal'] = deseasonalize(business_data['sales'])


df.to_csv('output.csv')