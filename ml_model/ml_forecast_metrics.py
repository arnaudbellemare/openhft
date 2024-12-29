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


def ml_metrics():

	with open('ml_model/model.pkl', 'rb') as f:
	    model = pickle.load(f)


	feature_set=pd.read_csv("ml_model/feature_past.csv")
	feature_set=feature_set.rename_axis(columns=None).reset_index()
	feature_set=feature_set[['Datetime','ScripName','V15D_SD','V30D_SD','V45D_SD','R03D_DR','R15D_DR','R30D_DR','R45D_DR','K','D','oversold','overbought','weighted_vol','weighted_daily_return','stochastic_signal','target']]
	df=feature_set.copy()
	test_size  = 0.1
	valid_size = 0.1
	
	test_split_idx  = int(df.shape[0] * (1-test_size))
	valid_split_idx = int(df.shape[0] * (1-(valid_size+test_size)))
	
	train_df  = df.loc[:valid_split_idx].copy()
	valid_df  = df.loc[valid_split_idx+1:test_split_idx].copy()
	test_df   = df.loc[test_split_idx+1:].copy()
	
	drop_cols = ['ScripName','Datetime']
	
	train_df = train_df.drop(columns=drop_cols, axis=1)
	valid_df = valid_df.drop(columns=drop_cols, axis=1)
	test_df  = test_df.drop(columns=drop_cols, axis=1)
	
	y_train = train_df['target'].copy()
	X_train = train_df.drop(columns=['target'], axis=1)
	
	y_valid = valid_df['target'].copy()
	X_valid = valid_df.drop(['target'], axis=1)
	
	y_test  = test_df['target'].copy()
	X_test  = test_df.drop(['target'], axis=1)

	
	y_pred = model.predict(X_test)

	out = pd.DataFrame(columns=['pred', 'actual'])
	out['pred']=y_pred
	out['actual']=np.array(y_test)[:]
	cm=confusion_matrix(np.array(y_test)[:],y_pred)

	return(cm)

