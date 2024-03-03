from typing import List
from fastapi import APIRouter, Request
import pickle
import pandas as pd
from config.db import conn
from models.scmModel import SCMModel
from schemas.cow import userEntity,usersEntity
from fastapi.encoders import jsonable_encoder
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import accuracy_score, precision_score

THRESHOLD = 400

data = pd.read_excel('C:/major project IV year/farmTech360-backend/SCMDetection/Data sheet.xlsx', sheet_name='Sheet1')

X = data[['DIM( Days In Milk)','Avg(7 days). Daily MY( L )', 'Kg. milk 305 ( Kg )', 'Fat (%)' , 'SNF (%)', 'Density ( Kg/ m3','Protein (%)','Conductivity (mS/cm)','pH','Freezing point (⁰C)','Salt (%)','Lactose (%)']]
y = data['SCC (103cells/ml)'].apply(lambda x: 0 if x > THRESHOLD else 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import category_encoders as ce 
encoder = ce.OrdinalEncoder(cols=['DIM( Days In Milk)','Avg(7 days). Daily MY( L )', 'Kg. milk 305 ( Kg )', 'Fat (%)' , 'SNF (%)', 'Density ( Kg/ m3','Protein (%)','Conductivity (mS/cm)','pH','Freezing point (⁰C)','Salt (%)','Lactose (%)'])
X_train = encoder.fit_transform(X_train)
X_test = encoder.transform(X_test)

clf_gini = DecisionTreeClassifier(criterion='gini',max_depth=2,random_state=0)
clf_gini.fit(X_train, y_train) 

# Make predictions on the test set
y_pred = clf_gini.predict(X_test)

# Calculate and print accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: {:.2f}%".format(accuracy * 100))

precision = precision_score(y_test, y_pred)
print("Precision: {:.2f}%".format(precision * 100))

clf_rf = RandomForestClassifier(n_estimators=100, random_state=0)  # You can adjust the number of trees (n_estimators) as needed
clf_rf.fit(X_train, y_train)
scm = APIRouter()

@scm.post('/predictscm')
async def predictSCM(scmData : Request):
  scmData = await scmData.json()
  data = pd.Series(scmData).to_frame().T    

  query_df = data[['DIM( Days In Milk)', 
                    'Avg(7 days). Daily MY( L )', 
                    'Kg. milk 305 ( Kg )', 
                    'Fat (%)', 
                    'SNF (%)', 
                    'Density ( Kg/ m3', 
                    'Protein (%)',
                    'Conductivity (mS/cm)',
                    'pH',
                    'Freezing point (⁰C)',
                    'Salt (%)',
                    'Lactose (%)']]
  query_df = encoder.transform(query_df)

    # Make predictions using the clf_gini model
  prediction = clf_gini.predict(query_df)

  # Return the prediction as JSON
  return {"prediction": prediction.tolist()}