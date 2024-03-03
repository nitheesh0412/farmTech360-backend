import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import accuracy_score, precision_score

THRESHOLD = 488

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

y_pred = clf_gini.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: {:.2f}%".format(accuracy * 100))

precision = precision_score(y_test, y_pred)
print("Precision: {:.2f}%".format(precision * 100))

clf_rf = RandomForestClassifier(n_estimators=100, random_state=0) 
clf_rf.fit(X_train, y_train)

y_pred_rf = clf_rf.predict(X_test)

accuracy_rf = accuracy_score(y_test, y_pred_rf)
print("Random Forest Accuracy: {:.2f}%".format(accuracy_rf * 100))

precision_rf = precision_score(y_test, y_pred_rf)
print("Random Forest Precision: {:.2f}%".format(precision_rf * 100))



# Save the model
with open("model.pkl", "wb") as file:
    pickle.dump(clf_gini, file, protocol=4)

new_data = np.array([
    [150, 30, 2500, 4.5, 3.2, 2000, 3.8, 1, 6.8, -0.5, 0.8, 0.2]
])

new_data_encoded = encoder.transform(pd.DataFrame(new_data, columns=X.columns))

prediction_decision_tree = clf_gini.predict(new_data_encoded)
print("Decision Tree Prediction:", prediction_decision_tree)


prediction_random_forest = clf_rf.predict(new_data_encoded)
print("Random Forest Prediction:", prediction_random_forest)