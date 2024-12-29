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

warnings.filterwarnings('ignore')

#--------------------------------------------------------------------
#SECTION 1 - DATASET CREATION FOR VOLATILITY METRICS
#--------------------------------------------------------------------

#--------------------------------------------------------------------
#SET-UP ALL PATH VARIABLES
#--------------------------------------------------------------------
nifty_master_path='marketdata/Nifty_Master.csv'
temp_path='marketdata/dailydata'
new_path='marketdata/dailydata'

#--------------------------------------------------------------------
#READ MASTER FILE TO GET ALL SCRIP NAMES
#--------------------------------------------------------------------
nifty_master = pd.read_csv(nifty_master_path)
ScripCode = nifty_master['ScripCode'].values.tolist()
ScripName = nifty_master['Name'].values.tolist()


#--------------------------------------------------------------------
#DEFINE PERIODS FOR LOOKBACK AND AVERAGE CALCULATION
#--------------------------------------------------------------------

period1=15
period2=30
period3=45

new_path=new_path+'/'+str(ScripCode[0])+'.csv'
market_data = pd.read_csv(new_path)
market_data['daily_return']=(market_data['Close']-market_data['Open'])/market_data['Open']
market_data['V15D_SD'] = market_data['daily_return'].rolling(period1).std()
market_data['V30D_SD'] = market_data['daily_return'].rolling(period2).std()
market_data['V45D_SD'] = market_data['daily_return'].rolling(period3).std()

for code in ScripCode:
	new_path=temp_path
	new_path=new_path+'/'+str(code)+'.csv'
	additional_market_data=pd.read_csv(new_path)
	additional_market_data['daily_return']=(additional_market_data['Close']-additional_market_data['Open'])/additional_market_data['Open']
	additional_market_data['V15D_SD'] = additional_market_data['daily_return'].rolling(period1).std()
	additional_market_data['V30D_SD'] = additional_market_data['daily_return'].rolling(period2).std()
	additional_market_data['V45D_SD'] = additional_market_data['daily_return'].rolling(period3).std()
	market_data=pd.concat([market_data, additional_market_data])
	
market_data=market_data.drop_duplicates()
market_data=market_data[['Datetime','ScripName','ScripCode','V15D_SD','V30D_SD','V45D_SD']]
market_data = market_data.dropna()

timestamp_string=market_data['Datetime'].max()
format_string = "%Y-%m-%dT%H:%M:%S"
datetime_object = datetime.strptime(timestamp_string, format_string)
date_obj = datetime_object.date()
current_date=str(date_obj)

alternate_format="%Y-%m-%d"
current_date_dtobj=datetime.strptime(current_date, alternate_format).date()


market_data['Datetime'] = market_data['Datetime'].apply(lambda x: datetime.strptime(x,format_string).date())
market_data=market_data[market_data['Datetime']==(current_date_dtobj)]
feature_vol=market_data.copy()


#--------------------------------------------------------------------
#SECTION 2 - DATASET CREATION FOR TREND FOLLOWING METRICS
#--------------------------------------------------------------------

#--------------------------------------------------------------------
#SET-UP ALL PATH VARIABLES
#--------------------------------------------------------------------
nifty_master_path='marketdata/Nifty_Master.csv'
temp_path='marketdata/dailydata'
new_path='marketdata/dailydata'

#--------------------------------------------------------------------
#READ MASTER FILE TO GET ALL SCRIP NAMES
#--------------------------------------------------------------------
nifty_master = pd.read_csv(nifty_master_path)
ScripCode = nifty_master['ScripCode'].values.tolist()
ScripName = nifty_master['Name'].values.tolist()

#--------------------------------------------------------------------
#DEFINE PERIODS FOR LOOKBACK AND AVERAGE CALCULATION
#--------------------------------------------------------------------

period0=3
period1=15
period2=30
period3=45

new_path=temp_path
new_path=new_path+'/'+str(ScripCode[0])+'.csv'
market_data = pd.read_csv(new_path)
market_data['daily_return']=(market_data['Close']-market_data['Open'])/market_data['Open']
market_data['R03D_DR'] = market_data['daily_return'].rolling(period0).mean()
market_data['R15D_DR'] = market_data['daily_return'].rolling(period1).mean()
market_data['R30D_DR'] = market_data['daily_return'].rolling(period2).mean()
market_data['R45D_DR'] = market_data['daily_return'].rolling(period3).mean()

for code in ScripCode:
	new_path=temp_path
	new_path=new_path+'/'+str(code)+'.csv'
	additional_market_data=pd.read_csv(new_path)
	additional_market_data['daily_return']=(additional_market_data['Close']-additional_market_data['Open'])/additional_market_data['Open']
	additional_market_data['R03D_DR'] = additional_market_data['daily_return'].rolling(period0).mean()
	additional_market_data['R15D_DR'] = additional_market_data['daily_return'].rolling(period1).mean()
	additional_market_data['R30D_DR'] = additional_market_data['daily_return'].rolling(period2).mean()
	additional_market_data['R45D_DR'] = additional_market_data['daily_return'].rolling(period3).mean()
	market_data=pd.concat([market_data, additional_market_data])
	
market_data=market_data.drop_duplicates()
market_data=market_data[['Datetime','ScripName','ScripCode','R03D_DR','R15D_DR','R30D_DR','R45D_DR']]
market_data = market_data.dropna()

timestamp_string=market_data['Datetime'].max()
format_string = "%Y-%m-%dT%H:%M:%S"
datetime_object = datetime.strptime(timestamp_string, format_string)
date_obj = datetime_object.date()
current_date=str(date_obj)

alternate_format="%Y-%m-%d"
current_date_dtobj=datetime.strptime(current_date, alternate_format).date()
market_data['Datetime'] = market_data['Datetime'].apply(lambda x: datetime.strptime(x,format_string).date())
market_data=market_data[market_data['Datetime']==(current_date_dtobj)]

feature_trend=market_data.copy()

#--------------------------------------------------------------------
#SECTION 3 - DATASET CREATION FOR STOCHASTIC METRICS
#--------------------------------------------------------------------

#--------------------------------------------------------------------
#SET-UP ALL PATH VARIABLES
#--------------------------------------------------------------------
nifty_master_path='marketdata/Nifty_Master.csv'
temp_path='marketdata/dailydata'
new_path='marketdata/dailydata'

#--------------------------------------------------------------------
#READ MASTER FILE TO GET ALL SCRIP NAMES
#--------------------------------------------------------------------
nifty_master = pd.read_csv(nifty_master_path)
ScripCode = nifty_master['ScripCode'].values.tolist()
ScripName = nifty_master['Name'].values.tolist()


#--------------------------------------------------------------------
#DEFINE PERIODS FOR LOOKBACK AND AVERAGE CALCULATION
#--------------------------------------------------------------------
k_period = 14
d_period = 3

new_path=temp_path
new_path=new_path+'/'+str(ScripCode[0])+'.csv'
market_data = pd.read_csv(new_path)
market_data['n_high'] = market_data['High'].rolling(k_period).max()
market_data['n_low'] = market_data['Low'].rolling(k_period).min()
market_data['K'] = (market_data['Close'] - market_data['n_low']) * 100 / (market_data['n_high'] - market_data['n_low'])
market_data['D'] = market_data['K'].rolling(d_period).mean()
market_data['overbought_K'] = market_data.K.between(80, 100).astype(np.uint8)
market_data['overbought_D'] = market_data.D.between(80, 100).astype(np.uint8)
market_data['oversold_K'] = market_data.K.between(0, 20).astype(np.uint8)
market_data['oversold_D'] = market_data.D.between(0, 20).astype(np.uint8)
market_data['overbought']=(market_data['overbought_K']+market_data['overbought_D'])/2
market_data['overbought']=market_data.overbought.between(0.6, 1.1).astype(np.uint8)
market_data['oversold']=(market_data['oversold_K']+market_data['oversold_D'])/2
market_data['oversold']=market_data.oversold.between(0.6, 1.1).astype(np.uint8)
market_data['signal']=(market_data['K']-market_data['D'])*market_data['oversold']
market_data['signal_sanitized']=market_data.signal.between(0, 100).astype(np.uint8)


for code in ScripCode:
	new_path=temp_path
	new_path=new_path+'/'+str(code)+'.csv'
	additional_market_data=pd.read_csv(new_path)
	additional_market_data['n_high'] = additional_market_data['High'].rolling(k_period).max()
	additional_market_data['n_low'] = additional_market_data['Low'].rolling(k_period).min()
	additional_market_data['K'] = (additional_market_data['Close'] - additional_market_data['n_low']) * 100 / (additional_market_data['n_high'] - additional_market_data['n_low'])
	additional_market_data['D'] = additional_market_data['K'].rolling(d_period).mean()
	additional_market_data['overbought_K'] = additional_market_data.K.between(80, 100).astype(np.uint8)
	additional_market_data['overbought_D'] = additional_market_data.D.between(80, 100).astype(np.uint8)
	additional_market_data['oversold_K'] = additional_market_data.K.between(0, 20).astype(np.uint8)
	additional_market_data['oversold_D'] = additional_market_data.D.between(0, 20).astype(np.uint8)
	additional_market_data['overbought']=(additional_market_data['overbought_K']+additional_market_data['overbought_D'])/2
	additional_market_data['overbought']=additional_market_data.overbought.between(0.6, 1.1).astype(np.uint8)
	additional_market_data['oversold']=(additional_market_data['oversold_K']+additional_market_data['oversold_D'])/2
	additional_market_data['oversold']=additional_market_data.oversold.between(0.6, 1.1).astype(np.uint8)
	additional_market_data['signal']=(additional_market_data['K']-additional_market_data['D'])*additional_market_data['oversold']
	additional_market_data['signal_sanitized']=additional_market_data.signal.between(0.1, 100).astype(np.uint8)
	market_data=pd.concat([market_data, additional_market_data])
	
market_data=market_data.drop_duplicates()
market_data['Datetime'] = market_data['Datetime'].shift(-1)
market_data = market_data.dropna()

market_data=market_data[['Datetime','ScripName','ScripCode','K','D','oversold','overbought','signal_sanitized']]

timestamp_string=market_data['Datetime'].max()
format_string = "%Y-%m-%dT%H:%M:%S"
datetime_object = datetime.strptime(timestamp_string, format_string)
date_obj = datetime_object.date()
current_date=str(date_obj)

alternate_format="%Y-%m-%d"
current_date_dtobj=datetime.strptime(current_date, alternate_format).date()


market_data['Datetime'] = market_data['Datetime'].apply(lambda x: datetime.strptime(x,format_string).date())
market_data=market_data[market_data['Datetime']==(current_date_dtobj)]

feature_stochastic=market_data.copy()

#--------------------------------------------------------------------
#SECTION 4 - DATASET CREATION FOR BASE TABLE
#--------------------------------------------------------------------

new_path=temp_path
new_path=new_path+'/'+str(ScripCode[0])+'.csv'
market_data = pd.read_csv(new_path)
market_data['daily_return']=(market_data['Close']-market_data['Open'])/market_data['Open']

for code in ScripCode:
	new_path=temp_path
	new_path=new_path+'/'+str(code)+'.csv'
	additional_market_data=pd.read_csv(new_path)
	additional_market_data['daily_return']=(additional_market_data['Close']-additional_market_data['Open'])/additional_market_data['Open']
	market_data=pd.concat([market_data, additional_market_data])
	
market_data=market_data.drop_duplicates()

timestamp_string=market_data['Datetime'].max()
format_string = "%Y-%m-%dT%H:%M:%S"
datetime_object = datetime.strptime(timestamp_string, format_string)
date_obj = datetime_object.date()
current_date=str(date_obj)

alternate_format="%Y-%m-%d"
current_date_dtobj=datetime.strptime(current_date, alternate_format).date()

market_data['Datetime'] = market_data['Datetime'].apply(lambda x: datetime.strptime(x,format_string).date())
market_data=market_data[market_data['Datetime']==(current_date_dtobj)]


#--------------------------------------------------------------------
#SECTION 5 - MERGE ALL TABLES
#--------------------------------------------------------------------

feature_past=pd.merge(market_data, feature_vol, how ='inner', on =['Datetime','ScripName','ScripCode']) 
feature_past=pd.merge(feature_past, feature_trend, how ='inner', on =['Datetime','ScripName','ScripCode']) 
feature_past=pd.merge(feature_past, feature_stochastic, how ='inner', on =['Datetime','ScripName','ScripCode']) 
feature_past['weighted_vol']=(0.6*feature_past['V15D_SD'])+(0.2*feature_past['V30D_SD'])+(0.2*feature_past['V45D_SD'])
feature_past['weighted_daily_return']=(0.5*feature_past['R03D_DR'])+(0.2*feature_past['R15D_DR'])+(0.2*feature_past['R30D_DR'])+(0.1*feature_past['R45D_DR'])
feature_past['stochastic_signal']=feature_past['signal_sanitized']
feature_past['daily_return']=(feature_past['Close']-feature_past['Open'])/feature_past['Open']
feature_past=feature_past.rename_axis(columns=None).reset_index()
feature_past=feature_past[['Datetime','ScripName','V15D_SD','V30D_SD','V45D_SD','R03D_DR','R15D_DR','R30D_DR','R45D_DR','K','D','oversold','overbought','weighted_vol','weighted_daily_return','stochastic_signal']]

#--------------------------------------------------------------------
#EXPORT FINAL DATASET FOR MODEL INFERENCE
#--------------------------------------------------------------------
feature_past.to_csv('ml_model/feature_predict.csv')

