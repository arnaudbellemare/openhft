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
#FUNCTION DEFINITION FOR STOCHASTIC STRATEGY
#--------------------------------------------------------------------

stock_name=['ASIANPAINT','EICHERMOT','HEROMOTOCO','TATAMOTORS','APOLLOHOSP','SBIN','M&M',
          'BEL','JSWSTEEL','ICICIBANK','INDUSINDBK','ONGC','BAJAJ-AUTO','BRITANNIA','NESTLEIND',
          'HINDALCO','RELIANCE','TRENT','TATASTEEL','DRREDDY','SHRIRAMFIN','KOTAKBANK','HDFCBANK',
          'AXISBANK','NTPC','TECHM','SBILIFE','CIPLA','GRASIM','HINDUNILVR','LT','TATACONSUM','WIPRO',
          'TITAN','BPCL','INFY','SUNPHARMA','TCS','MARUTI','HCLTECH','COALINDIA','ULTRACEMCO']



def spread_trading(scrip_name,start_date,date_delim):
	
	#--------------------------------------------------------------------
	#SET-UP ALL PATH VARIABLES
	#--------------------------------------------------------------------

	#os.chdir("D:\\Raid Array\\Array 2\\3. OpenHFT\\Production\\v2")
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
	market_data['Spread'] = market_data['High']-market_data['Low']
	

	for code in ScripCode:
		new_path=temp_path
		new_path=new_path+'/'+str(code)+'.csv'
		additional_market_data=pd.read_csv(new_path)
		additional_market_data['Spread'] = additional_market_data['High']-additional_market_data['Low']
		market_data=pd.concat([market_data, additional_market_data])

	market_data=market_data.drop_duplicates()
	#print(market_data)
	#exit()

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
	#Filter Dataset for date passed to API call
	#String conversion is not required since both objects being compared are date type objects
	#-----------------------------------------------------------------------------------------------------
	#market_data_current=market_data[market_data['Datetime']==str(current_date_dtobj)]
	#market_data['Datetime'] = market_data['Datetime'].apply(lambda x: datetime.strptime(x,format_string).date())
	#market_data_current=market_data[market_data['Datetime']==(current_date_dtobj)]

	#stochastic_data_export=market_data_current[['ScripName','K','D','overbought','oversold','signal_sanitized']]
	#stochastic_data_export = stochastic_data_export.sort_values(by=['signal_sanitized'], ascending=False)

	spread_trading_export=market_data.copy()
	spread_trading_export=spread_trading_export[spread_trading_export['ScripName']==scrip_name]
	mask = (spread_trading_export['Datetime'] > start_date) & (spread_trading_export['Datetime'] <= date_delim)
	spread_trading_export = spread_trading_export.loc[mask]
	spread_trading_export=spread_trading_export.drop_duplicates()
	spread_trading_export=spread_trading_export[['Datetime','ScripName','Volume','Open','Close','Low','High','Spread']]


	return spread_trading_export


#df=spread_trading(stock_name[1],'2025-02-17','2025-02-25')
#print(df)