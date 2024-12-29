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

#--------------------------------------------------------------------
#FUNCTION DEFINITION FOR VOLATILITY STRATEGY
#--------------------------------------------------------------------

def volatility_skew_strategy(date_delim):
	
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


	#--------------------------------------------------------------------
	#READ SCRIP WISE DAILY MARKET DATA
	#--------------------------------------------------------------------	
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
	
	#--------------------------------------------------------------------
	#LEGACY CODE FOR GETTING CURRENT DATE USING MAX DATE IN DATASET
	#--------------------------------------------------------------------
	#timestamp_string=market_data['Datetime'].max()
	format_string = "%Y-%m-%dT%H:%M:%S"
	#datetime_object = datetime.strptime(timestamp_string, format_string)
	#date_obj = datetime_object.date()

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
	market_data['Datetime'] = market_data['Datetime'].apply(lambda x: datetime.strptime(x,format_string).date())
	#market_data_current=market_data[market_data['Datetime']==timestamp_string]
	market_data_current=market_data[market_data['Datetime']==(current_date_dtobj)]

	#-----------------------------------------------------------------------------------------------------
	#Filter Dataset for only required volatility columns
	#-----------------------------------------------------------------------------------------------------
	market_data_filtered=market_data_current[['ScripName','V15D_SD','V30D_SD','V45D_SD']]
	market_data_filtered['weighted_vol']=(0.6*market_data_filtered['V15D_SD'])+(0.2*market_data_filtered['V30D_SD'])+(0.2*market_data_filtered['V45D_SD'])
	market_data_filtered = market_data_filtered.sort_values(by=['weighted_vol'], ascending=True)

	return(market_data_filtered)