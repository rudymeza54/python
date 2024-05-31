
# LIBRARIES



import pandas as pd
import glob
import numpy as np
import os
import csv


# PULL PW AND CONNNECT TO DB

with open('pw.txt','r') as file:
      pw = file.read()


import mysql.connector

cnx = mysql.connector.connect(user='root',
                              password=pw,
                              host='127.0.0.1',
                              database='bad_sakila',
                              auth_plugin='mysql_native_password')


cursor = cnx.cursor()


# BEGIN QUERY CHECKS


# CHECK TOTAL COUNT OF ROWS. THIS SHOULD BE 22641

print(f'CHECK # 1: TOTAL COUNT OF ROWS. THIS SHOULD BE 22641')

sql1 = (
      """
    SELECT COUNT(*)
    FROM sales;

"""
)


cursor.execute(sql1)


for row in cursor.fetchall():
      print(row[0])



# CHECK SELECT ALL COLUMNS FOR YEAR 2020 AND BUSINESS 'ALL OTHER HOME FURNISHINGS STORES' LIMIT TO TOP 30


print(f'CHECK# 2: SELECT ALL COLUMNS FOR YEAR 2020 AND BUSINESS ALL OTHER HOME FURNISHINGS STORES LIMIT TO TOP 30 ')

sql2 = (
      """
      SELECT *
      FROM sales
      WHERE month_year LIKE '%2020' AND business = 'All other home furnishings stores'
      LIMIT 30;

"""
)


cursor.execute(sql2)


for row in cursor.fetchall():
      print(row)






#  CHECK TOTALS PER BUSINESS IN THE YEAR 2020. THIS SHOULD MATCH TOTAL COLUMN IN ORIGINAL DATASET

print(f'CHECK # 3: TOTALS PER BUSINESS IN THE YEAR 2020. THIS SHOULD MATCH TOTAL COLUMN IN ORIGINAL DATASET')

sql3 = (
      """
      SELECT business,
		SUM(total) as grand
      FROM (SELECT 
                  business,
            month_year,
            SUM(sales) total
      FROM sales
      WHERE month_year LIKE '%2020'
      GROUP BY business, month_year) AS total_sales
      GROUP BY business;

"""
)


cursor.execute(sql3)


for row in cursor.fetchall():
      print(row)



#  CHECK GRAND TOTAL FOR ALL BUSINESS IN 2020

print(f'CHECK # 4: GRAND TOTAL FOR ALL BUSINESS IN 2020')

sql4 = (
      """
      SELECT SUM(total) as grand
      FROM (SELECT 
                  business,
            month_year,
            SUM(sales) total
      FROM sales
      WHERE month_year LIKE '%2020'
      GROUP BY business, month_year) AS total_sales

"""
)


cursor.execute(sql4)


for row in cursor.fetchall():
      print(row)