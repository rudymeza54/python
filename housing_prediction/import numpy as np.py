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


mse_df['MSE'] = mse_df['MSE'].apply(lambda x: '%.2f' % x)

mse_df = mse_df.sort_values(by = 'MSE', ascending = True)

plt.figure(figsize = (10,8))
plt.plot(mse_df['Alpha'],mse_df['MSE'], marker = 'o')
plt.legend()
plt.show()

best_alpha = grid_search.best_params_['model__alpha']
best_model = grid_search.best_estimator_
print(f"Best alpha: {best_alpha}")

y_pred = best_model.predict(X_test)

best_model.score(X_train,y_train)

best_model.score(X_test,y_test)

min = mse_df['MSE'].min()

mse_df[mse_df['MSE'] == min]

best_model = grid_search.best_estimator_

preprocess = best_model.named_steps['preprocessor']

model = best_model.named_steps['model']

preprocessor.fit(X_train)

num_features = numerical_features
cat_features = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_Features)

features = np.concatenate([num_features, cat_features])

coefs = model.coef_

feature_importance = pd.DataFrame({
    "Features": features,
    "Coefficient": coefs
})

important_features = feature_importance[feature_importance['Coefficient']!=0]
important_features = important_features.sort_values(by = 'Coefficient', ascending = False)


plt.barh(important_features['Features'],important_features['Coefficient'])

plt.show()