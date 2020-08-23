import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import ensemble
import pickle


data = pd.read_csv("kc_house_data.csv")
reg = LinearRegression()
labels = data['price']
train1 = data.drop(['id', 'price', 'date'],axis=1)
x_train , x_test , y_train , y_test = train_test_split(train1 , labels , test_size = 0.10,random_state =2)
reg.fit(x_train,y_train)
print(reg.score(x_test,y_test))
clf = ensemble.GradientBoostingRegressor(n_estimators = 400, max_depth = 5, min_samples_split = 2,
          learning_rate = 0.1, loss = 'ls')

clf.fit(x_train, y_train)
print(clf.score(x_test,y_test))
y_pred = clf.predict(x_test)

pickle.dump(clf, open(r"lr_model_flask.pkl",'wb'))
model=pickle.load(open(r"lr_model_flask.pkl",'rb'))