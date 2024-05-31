
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






db = yaml.safe_load(open('pw.yaml'))




config = {
      'user':   db['user'],
      'password':   db['pwrd'],
      'host':   db['host'],
      'database':   db['db'],
      'auth_plugin':    'mysql_native_password'
}




cnx = mysql.connector.connect(**config)



cursor = cnx.cursor()


sql = (
    """
    SELECT business,DATE_FORMAT(STR_TO_DATE(month_year, '%d %b %Y'),'%Y-%m-%d'), CAST(sum(sales) as UNSIGNED) as sale
    FROM sales
    WHERE business IN ('Women''s clothing stores','men''s clothing stores','Book stores','Sporting goods stores', 'Hobby, toy, and game stores','Retail and food services sales, total')
    GROUP BY 1,2
    ORDER BY 1,2;
    """
)


cursor.execute(sql)


business = []
date = []
sales = []


for i in cursor.fetchall():
    business.append(i[0])
    date.append(i[1])
    sales.append(i[2])


df = pd.DataFrame({
    'business': business,
    'date' : date,
    'sales' : sales
})

retail = df[df['business'] == 'Retail and food services sales, total']

retail.drop(columns = ['business'], inplace = True)
retail['date'] = pd.to_datetime(retail['date'])
retail.set_index(retail['date'],inplace=True)


# TREND DIFFERENCES


retail_mul = seasonal_decompose(retail['sales'], model='multiplicative', extrapolate_trend='freq')
retail_add = seasonal_decompose(retail['sales'], model='additive', extrapolate_trend='freq')



deseasonalized = retail['sales'] / retail_mul.seasonal

# Plot
plt.figure(figsize = (8,6))

plt.plot(deseasonalized, color = 'midnightblue', label = 'Deseasonal')
plt.plot(retail['sales'], color = 'yellow',label = 'Series')
plt.title('Retail and Food Services: Sales Deseasonalized', fontsize=16)
plt.legend()
plt.show()



plt.rcParams.update({'figure.figsize': (8,6)})
retail_mul.plot().suptitle('Multiplicative Decompose', fontsize=10)
plt.show()


# Additional Trends


trend1 = df[df['business'] == 'Book stores']
trend2 = df[df['business'] == 'Sporting goods stores']
trend3 = df[df['business'] == 'Hobby, toy, and game stores']
trend4 = df[df['business'] == "Women's clothing stores"]
trend5 = df[df['business'] == "Men's clothing stores"]

# TREND DIFFERENCES



plt.figure(figsize = (8,6))

plt.plot(trend1['date'],trend1['sales'], label = 'Bookstores',color = 'darkslategray')
plt.plot(trend2['date'],trend2['sales'], label = 'Sporting goods stores',color = 'midnightblue')
plt.plot(trend3['date'],trend3['sales'], label = 'Hobby, toy, and game stores',color = 'firebrick')

plt.legend()
plt.show()



# SERIES DECOMPOSITION

trend1.drop(columns = ['business'], inplace = True)
trend1['date'] = pd.to_datetime(trend1['date'])
trend1.set_index(trend1['date'],inplace=True)

result_mul = seasonal_decompose(trend1['sales'], model='multiplicative', extrapolate_trend='freq')


trend2.drop(columns = ['business'], inplace = True)
trend2['date'] = pd.to_datetime(trend2['date'])
trend2.set_index(trend2['date'],inplace=True)

result2_mul = seasonal_decompose(trend2['sales'], model='multiplicative', extrapolate_trend='freq')


trend3.drop(columns = ['business'], inplace = True)
trend3['date'] = pd.to_datetime(trend3['date'])
trend3.set_index(trend2['date'],inplace=True)

result3_mul = seasonal_decompose(trend3['sales'], model='multiplicative', extrapolate_trend='freq')

ds1 = trend1['sales'] / result_mul.seasonal
ds2 = trend2['sales'] / result2_mul.seasonal
ds3 = trend3['sales'] / result3_mul.seasonal



plt.rcParams.update({'figure.figsize': (8,6)})
plt.title('Series Comparison: Sales Deseasonalized (Monthly)', fontsize=16)
ds1.plot(label = 'Bookstores',color = 'darkslategray')
ds2.plot(label = 'Sporting goods stores',color = 'dodgerblue')
ds3.plot(label = 'Hobby, toy, and game stores',color = 'firebrick')
plt.legend()
plt.show()



dsy1 = ds1.resample('A').last()
dsy2 = ds2.resample('A').last()
dsy3 = ds3.resample('A').last()

plt.rcParams.update({'figure.figsize': (8,6)})
plt.title('Series Comparison: Sales Deseasonalized (Annual)', fontsize=16)
dsy1.plot(label = 'Bookstores',color = 'darkslategray')
dsy2.plot(label = 'Sporting goods stores',color = 'dodgerblue')
dsy3.plot(label = 'Hobby, toy, and game stores',color = 'firebrick')
plt.legend()
plt.show()




# Now consider, for example, the women's clothing and men's clothing businesses and their percentage changes.
# How are these two businesses related? What is the percentage of contribution to the whole, and how does it change over time?

pct_c1 = ds1.pct_change(fill_method ='ffill')*100
pct_c2 = ds2.pct_change(fill_method ='ffill')*100
pct_c3 = ds3.pct_change(fill_method ='ffill')*100

plt.rcParams.update({'figure.figsize': (8,6)})
plt.title('Series Comparison: Sales Deseasonalized (Monthly % Change)', fontsize=16)
pct_c1.plot(label = 'Bookstores',color = 'darkslategray')
pct_c2.plot(label = 'Sporting goods stores',color = 'dodgerblue')
pct_c3.plot(label = 'Hobby, toy, and game stores',color = 'firebrick')
plt.legend()
plt.show()


pct_c1 = dsy1.pct_change(fill_method ='ffill')*100
pct_c2 = dsy2.pct_change(fill_method ='ffill')*100
pct_c3 = dsy3.pct_change(fill_method ='ffill')*100

plt.rcParams.update({'figure.figsize': (8,6)})
plt.title('Series Comparison: Sales Deseasonalized (Annual % Change)', fontsize=16)
pct_c1.plot(label = 'Bookstores',color = 'darkslategray')
pct_c2.plot(label = 'Sporting goods stores',color = 'dodgerblue')
pct_c3.plot(label = 'Hobby, toy, and game stores',color = 'firebrick')
plt.legend()
plt.show()





trend4.drop(columns = ['business'], inplace = True)
trend4['date'] = pd.to_datetime(trend4['date'])
trend4.set_index(trend4['date'],inplace=True)

result4_mul = seasonal_decompose(trend4['sales'], model='multiplicative', extrapolate_trend='freq')

ds4 = trend4['sales'] / result4_mul.seasonal

trend5.drop(columns = ['business'], inplace = True)
trend5['date'] = pd.to_datetime(trend5['date'])
trend5.set_index(trend5['date'],inplace=True)
trend5['date'] = pd.to_datetime(trend5['date'])




pct_c4 = trend4['sales'].pct_change(fill_method ='ffill')*100
pct_c5 = trend5['sales'].pct_change(fill_method ='ffill')*100




plt.rcParams.update({'figure.figsize': (8,6)})
plt.title('Series Comparison: Men and Women Clothing Sales (Monthly % Change)', fontsize=16)
pct_c4.plot(label = "Women's clothing stores",color = 'darkslategray')
pct_c5.plot(label = "Men's clothing stores",color = 'dodgerblue')
plt.legend()
plt.show()



sql2 = (
    """
    SELECT DATE_FORMAT(STR_TO_DATE(month_year, '%d %b %Y'),'%Y-%m-%d') as date,SUM(total) as grand
    FROM (SELECT 
            business,
            month_year,
            SUM(sales) total
    FROM sales
    GROUP BY business, month_year) AS total_sales
    GROUP BY 1
    ORDER BY 1;

"""
)



cursor.execute(sql2)


date = []
total = []


for i in cursor.fetchall():
    date.append(i[0])
    total.append(i[1])


df_grand = pd.DataFrame({
    'date' : date,
    'total' : total
})




# JOIN IN DATA WITH MENS AND WOMENS CLOTHING

trend4 = df[df['business'] == "Women's clothing stores"]
trend5 = df[df['business'] == "Men's clothing stores"]

t4_main = trend4.merge(df_grand, on = 'date', how = 'left')

t5_main = trend5.merge(df_grand, on = 'date', how = 'left')

t4_main['pct'] = (t4_main['sales']/t4_main['total'])*100
t5_main['pct'] = (t5_main['sales']/t5_main['total'])*100

womens = np.sum(t4_main['pct'])
mens = np.sum(t5_main['pct'])

print(f'Percent of Womens clothing to total: {womens}')
print(f'Percent of Mens clothing to total: {mens}')


# CREATE ROLLING AVG WITH WINDOW FUNCTION


sql3 = (
    """
    SELECT
	business,
    STR_TO_DATE(month_year, '%d %b %Y') as time_date,
    sales,
    AVG(sales) OVER( ORDER BY STR_TO_DATE(month_year, '%d %b %Y') ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling
    FROM sales
    WHERE business = 'Women''s clothing stores'
    ORDER BY 2 
"""
)



cursor.execute(sql3)


date_w = []
rolling_w = []


for i in cursor.fetchall():
    date_w.append(i[1])
    rolling_w.append(i[3])


df_rolling_w= pd.DataFrame({
    'date' : date_w,
    'rolling' : rolling_w
})

df_rolling_w = df_rolling_w.iloc[::2]






sql4 = (
    """
    SELECT
	business,
    STR_TO_DATE(month_year, '%d %b %Y') as time_date,
    sales,
    AVG(sales) OVER( ORDER BY STR_TO_DATE(month_year, '%d %b %Y') ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling
    FROM sales
    WHERE business = 'men''s clothing stores'
    ORDER BY 2 
"""
)



cursor.execute(sql4)


date_m = []
rolling_m = []


for i in cursor.fetchall():
    date_m.append(i[1])
    rolling_m.append(i[3])


df_rolling_m= pd.DataFrame({
    'date' : date_m,
    'rolling' : rolling_m
})

df_rolling_m = df_rolling_m.iloc[::2]



# Plots


plt.rcParams.update({'figure.figsize': (8,6)})
plt.title('Series Comparison: Men and Women Clothing Sales \n(Rolling 3 Month AVG)', fontsize=16)
plt.plot(df_rolling_w['rolling'],label = "Women's clothing stores",color = 'darkslategray')
plt.plot(df_rolling_m['rolling'],label = "Men's clothing stores",color = 'dodgerblue')
plt.tight_layout()
plt.legend()
plt.show()