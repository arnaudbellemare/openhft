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
#FUNCTION DEFINITION FOR TREND FOLLOWING CHARTS
#--------------------------------------------------------------------


def daily_return_chart(scrip_name,start_date,date_delim):


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


	#--------------------------------------------------------------------
	#READ SCRIP WISE DAILY MARKET DATA
	#--------------------------------------------------------------------	
	new_path=new_path+'/'+str(ScripCode[0])+'.csv'
	market_data = pd.read_csv(new_path)

	#--------------------------------------------------------------------
	#CREATE TREND INDICATOR METRICS
	#--------------------------------------------------------------------
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
	
	#--------------------------------------------------------------------
	#LEGACY CODE FOR GETTING CURRENT DATE USING MAX DATE IN DATASET
	#--------------------------------------------------------------------			
	format_string = "%Y-%m-%dT%H:%M:%S"
	#market_data['Datetime'] = market_data['Datetime'].apply(lambda x: datetime.strptime(x,format_string).date())
	market_data['Datetime']=pd.to_datetime(market_data['Datetime'], format=format_string)

	#-----------------------------------------------------------------------------------------------------
	#PREPARE FILTERED DATA FOR CHART TO BE SENT ACROSS API RESPONSE
	#-----------------------------------------------------------------------------------------------------
	market_data_trend=market_data.dropna() 
	market_data_trend=market_data_trend[market_data_trend['ScripName']==scrip_name]
	mask = (market_data_trend['Datetime'] > start_date) & (market_data_trend['Datetime'] <= date_delim)
	market_data_trend = market_data_trend.loc[mask]
	market_data_trend=market_data_trend.drop_duplicates()
	market_data_trend['daily_return']=market_data_trend['daily_return']*100
	
	return market_data_trend