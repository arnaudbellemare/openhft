#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import datetime
import os
from datetime import datetime, timedelta
import arrow
from scipy.stats import percentileofscore
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import warnings
from itertools import combinations
from statsmodels.tsa.stattools import coint
import xgboost as xgb
from xgboost import XGBClassifier
from xgboost import plot_importance, plot_tree
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix,classification_report
from sklearn import metrics
import sklearn
import pickle


def ml_model_predict():
	with open('ml_model/model.pkl', 'rb') as f:
	    model = pickle.load(f)
	
	feature_set=pd.read_csv("ml_model/feature_predict.csv")
	feature_set=feature_set.rename_axis(columns=None).reset_index()
	feature_set=feature_set[['Datetime','ScripName','V15D_SD','V30D_SD','V45D_SD','R03D_DR','R15D_DR','R30D_DR','R45D_DR','K','D','oversold','overbought','weighted_vol','weighted_daily_return','stochastic_signal']]
	df=feature_set.copy()
	drop_cols = ['ScripName','Datetime']
	test_df  = df.drop(columns=drop_cols, axis=1)
	X_test  = test_df.copy()
	y_pred = model.predict(X_test)
	df['pred']=y_pred
	df=df[['Datetime','ScripName','weighted_vol','weighted_daily_return','stochastic_signal','pred']]
	return(df)

