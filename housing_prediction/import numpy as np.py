import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os
import glob
import matplotlib.pyplot as plt

pd.set_option('display.float_format', str)

dir = "C:/Users/rudym/OneDrive/Desktop/VS Code/python/housing_prediction"

file = "".join(glob.glob(os.path.join(dir, "houseSmallData.csv")))

df = pd.read_csv(file)

df.dropna(axis=1, inplace=True)

X = df.drop(columns = ['SalePrice'])
y = df['SalePrice']


X_train,X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2, random_state=43)



categorical_Features = X.select_dtypes(include = ['object']).columns.tolist()


numerical_features = X.select_dtypes(include = ['int64','float']).columns.tolist()

preprocessor = ColumnTransformer(
    transformers= [('num',StandardScaler(),numerical_features),
                   ('cat',OneHotEncoder(handle_unknown='ignore'),categorical_Features)]
)



pipeline = Pipeline(steps = [('preprocessor',preprocessor),
                             ('model',Lasso(max_iter = 10000))])


param_grid = {'model__alpha':np.logspace(-4,4,50)}



grid_search = GridSearchCV(pipeline,param_grid, cv = 10, scoring='neg_mean_squared_error')

grid_search.fit(X_train,y_train)


results = grid_search.cv_results_

alpha = results['param_model__alpha'].data
mse = -results['mean_test_score']

mse_df = pd.DataFrame({
    'Alpha':alpha,
    'MSE': mse
})


mse_df['MSE'] = mse_df['MSE'].apply(lambda x: '%.9f' % x)

plt.figure(figsize = (10,8))
plt.plot(mse_df['Alpha'],mse_df['MSE'], marker = 'o')
plt.xscale('log')
plt.xlabel('Alpha')
plt.ylabel('Mean Squarred Error')
plt.legend()
plt.show()

best_alpha = grid_search.best_params_['model__alpha']
best_model = grid_search.best_estimator_
print(f"Best alpha: {best_alpha}")

y_pred = best_model.predict(X_test)

best_model.score(X_train,y_train)

best_model.score(X_test,y_test)