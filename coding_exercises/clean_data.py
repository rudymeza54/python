#'#####################################################################
#' Author: Rudy Meza
#' Date: 5/13/2023
#' Purpose: Clean Data
########################################################################




#' Import Lbraries for analysis  -----------------------------------------

import os 
import pandas as pd
import numpy as np



#' Create path for importing data  -----------------------------------------


user = os.getenv("USERNAME")

path = (r"C:\Users\{}\OneDrive\Desktop".format(user))



dir = os.listdir(path)


#' Import dataset ----------------------------------------------------------


for file in dir:
    if file.endswith("titanic_dataset.csv"):
        data_path = os.path.join(path,file)
        data = pd.read_csv(data_path)

#' Clean Column names
data.columns = data.columns.str.lower()


#' Initial Cleaning ----------------------------------------------------------


## See all the null values and fill with media
age_median = data["age"].median()

data["age"] = data["age"].fillna(age_median)

data["embarked"] = data["embarked"].fillna("missiing")



## extract title to fill cabin

data["full_name"] = data["name"].replace("")

data["title"] = data["name"].str.extract(r'\,(.\S*)')[0]



remove = ['cabin','ticket']
data.drop(remove, inplace =True, axis =1)

#' Check for missing values


np.sum(data.isnull())