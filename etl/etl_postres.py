import psycopg2
import pandas as pd
import glob
import numpy as np
import os
import csv
import yaml


# READING IN DATA FROM LOCAL DIRECTORY

print('Reading mrts data\n reshaping now...')

dir = os.getcwd()

file = ''.join(os.path.join(dir,'mrtsales.xlsx'))
df = pd.read_excel(file, sheet_name = None, skiprows = 4,nrows = 66)

# CONVERT DF DICTIONARY TO PANDAS DF
# ONLY EXTRACT COLUMNS WITH DATES

main = pd.concat(df.values(), ignore_index=True)

main.drop(columns = ['CY CUM','PY CUM'], inplace=True)

cols = [ele for ele in main.columns if '20' in ele or '19' in ele]


# RESHAPE DATA INTO A LONGER FORMAT

new = pd.melt(main,id_vars = ['Unnamed: 0','Unnamed: 1'], value_vars=cols, var_name = 'month_year', value_name = 'sales')
new = new[new['sales'].notna()]
new = new[new['sales']!='(S)']
new = new[new['sales']!='(NA)']

new.rename(columns = {'Unnamed: 0':'naics_code','Unnamed: 1':'business'}, inplace=True)
new['month_year'] = new['month_year'].str.replace('.','',regex=False).str.replace('(p)','',regex=False)
new['month_year'] = new['month_year'].apply(lambda x: '01'+' '+ str(x))






new.to_csv('output.csv')


# CREATE DB AND TABLE FOR SALES DATA
# INSERT IN SQL AND RUN CHECKS





db = yaml.safe_load(open('pw_postres.yaml'))



HOST = db['HOST']
DATABASE = db['DATABASE']
USERNAME = db['USERNAME']
PASSWORD = db['PASSWORD']
PORT = db['PORT']



connectionString = f"dbname='{DATABASE}' user='{USERNAME}' host='{HOST}' password='{PASSWORD}' port='{PORT}'"


conn = psycopg2.connect(connectionString)


cursor = conn.cursor()

cursor.execute(f'DROP TABLE IF EXISTS sales')

cursor.execute(

    """

    CREATE TABLE sales ( 

        naics_code varchar(50),
        business varchar(200),
        month_year varchar(20),
        sales varchar(150)
    )

"""
)

conn.commit()







print("Inserting Data into Table Now...")

sql = (f'INSERT INTO sales(naics_code,business,month_year,sales) VALUES(%s,%s,%s,%s);')

with open('output.csv') as csv_file:
      csv = csv.reader(csv_file,delimiter = ',')
      next(csv)
      for row in csv:
            value = (row[1],row[2],row[3],row[4])
            cursor.execute(sql,value)
            conn.commit()




print(f'Checking row count from csv file')

with open('output.csv','r') as file:
      row = sum(1 for line in file)-1


print(f'Total Rows: {row}')


cursor.execute(f'SELECT COUNT(*) FROM sales')

x = [cursor.fetchone()[0]].pop()

# CHECK IF ROW MATCHES COUNT IN SQL QUERY

if row == x:
      print(f'Rows Match on MRTSData and SQL TABLE')
else:
      print(f'Rows do not match')



file = ''.join(os.path.join(dir,'output.csv'))


df = pd.read_csv(file)


df['month_year'] = pd.to_datetime(df['month_year'], format = '%d %b %Y')
df['month_year'] = df['month_year'] .dt.strftime('%m-%d-%Y').str.strip()

df['sales'] = df['sales'].astype(float)

df.to_csv('output.csv', index=False)

print(f'Script complete')