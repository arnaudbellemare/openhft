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

#--------------------------------------------------------------------
#FUNCTION DEFINITION FOR STOCHASTIC CHARTS
#--------------------------------------------------------------------


def stochastic_strategy_1_chart(scrip_name,start_date,date_delim):

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

	#--------------------------------------------------------------------
	#READ SCRIP WISE DAILY MARKET DATA
	#--------------------------------------------------------------------	

	new_path=new_path+'/'+str(ScripCode[0])+'.csv'
	market_data = pd.read_csv(new_path)

	#--------------------------------------------------------------------
	#CREATE STOCHASTIC INDICATOR METRICS
	#K- FAST SIGNAL
	#D- SLOW SIGNAL
	#--------------------------------------------------------------------	
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
	market_data.to_csv('market_data_stochastic.csv')

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
	
	#--------------------------------------------------------------------
	#LEGACY CODE FOR GETTING CURRENT DATE USING MAX DATE IN DATASET
	#--------------------------------------------------------------------			
	timestamp_string=market_data['Datetime'].max()
	format_string = "%Y-%m-%dT%H:%M:%S"
	datetime_object = datetime.strptime(timestamp_string, format_string)
	date_obj = datetime_object.date()
	current_date=date_obj
	current_date=str(current_date)
	
	#-----------------------------------------------------------------------------------------------------
	#RESET CURRENT DATE WITH DATE PASSED ONTO API CALL
	#this would be required when operating as a function for backtesting on specific dates as per API call
	#-----------------------------------------------------------------------------------------------------
	current_date=str(date_delim)
	alternate_format="%Y-%m-%d"
	current_date_dtobj=datetime.strptime(current_date, alternate_format).date()
	
	#-----------------------------------------------------------------------------------------------------
	#PREPARE FILTERED DATA FOR CHART TO BE SENT ACROSS API RESPONSE
	#-----------------------------------------------------------------------------------------------------
	market_data['Datetime']=pd.to_datetime(market_data['Datetime'], format=format_string)
	market_data=market_data[['ScripName','ScripCode','Datetime','Open','K','D']]
	market_data_stochastic=market_data
	market_data_stochastic=market_data_stochastic.dropna() 
	market_data_stochastic=market_data_stochastic[market_data_stochastic['ScripName']==scrip_name]
	mask = (market_data_stochastic['Datetime'] > start_date) & (market_data_stochastic['Datetime'] <= date_delim)
	market_data_stochastic = market_data_stochastic.loc[mask]
	market_data_stochastic=market_data_stochastic.drop_duplicates()

	return market_data_stochastic


