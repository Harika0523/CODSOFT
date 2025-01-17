# -*- coding: utf-8 -*-
"""CUSTOMER CHURN  PREDICTION.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mDc8zBUVFV5_CgnlLIymW3gSPEsUs_eW
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

from google.colab import files
uploaded = files.upload()

# Move the kaggle.json file to the correct location
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/

# Set permissions for the kaggle.json file
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d shantanudhakadd/bank-customer-churn-prediction

# Unzip the downloaded dataset
!unzip /content/bank-customer-churn-prediction.zip -d /content

!ls /content

data = pd.read_csv('/content/Churn_Modelling.csv')

data.head()

data.describe()

data.isnull().sum()

data.dtypes

"""Data Cleaning and Preprocessing"""

data = data.drop(columns=['RowNumber', 'CustomerId', 'Surname'])

label_encoder = LabelEncoder()
data['Geography'] = label_encoder.fit_transform(data['Geography'])
data['Gender'] = label_encoder.fit_transform(data['Gender'])

data.isnull().sum()

scaler = StandardScaler()
numerical_features = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']
data[numerical_features] = scaler.fit_transform(data[numerical_features])

x = data.drop(columns=['Exited'])
y = data['Exited']

"""Feature Engineering"""

poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
x_poly = poly.fit_transform(x)

x_poly_df = pd.DataFrame(x_poly, columns=poly.get_feature_names_out(x.columns))
print(x_poly_df.head())

"""Model Training and Evaluation"""

x_train, x_test, y_train, y_test = train_test_split(x_poly, y, test_size=0.2, random_state=42)

# Logistic Regression
log_reg = LogisticRegression()
log_reg.fit(x_train, y_train)
y_pred_log_reg = log_reg.predict(x_test)
print("Logistic Regression Report")
print(classification_report(y_test, y_pred_log_reg))

# Random Forest
rf = RandomForestClassifier()
rf.fit(x_train, y_train)
y_pred_rf = rf.predict(x_test)
print("Random Forest Report")
print(classification_report(y_test, y_pred_rf))

# Gradient Boosting
gb = GradientBoostingClassifier()
gb.fit(x_train, y_train)
y_pred_gb = gb.predict(x_test)
print("Gradient Boosting Report")
print(classification_report(y_test, y_pred_gb))

# Model comparison using ROC AUC
log_reg_auc = roc_auc_score(y_test, log_reg.predict_proba(x_test)[:, 1])
rf_auc = roc_auc_score(y_test, rf.predict_proba(x_test)[:, 1])
gb_auc = roc_auc_score(y_test, gb.predict_proba(x_test)[:, 1])

print(f"Logistic Regression AUC: {log_reg_auc}")
print(f"Random Forest AUC: {rf_auc}")
print(f"Gradient Boosting AUC: {gb_auc}")

