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
import warnings

#--------------------------------------------------------------------
#IMPORT ALL INTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
from api.trend_following_strategy_api import *
from api.momentum_strategy_1_api import *
from api.stochastic_oscillator_1_api import *
from api.volatility_skew_strategy_api import *


def backtest_vol_skew(start_date,end_date):
	warnings.filterwarnings("ignore")
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
	#READ SCRIP WISE DAILY MARKET DATA
	#--------------------------------------------------------------------	
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

	#-------------------------------
	#Function Inputs Taken here
	#-------------------------------
	backtest_start_date=str(start_date)
	backtest_end_date=str(end_date)



	available_datetime=market_data['Datetime'].values.tolist()
	available_datetime = list(set(available_datetime))
	available_dates=[]
	format_string = "%Y-%m-%dT%H:%M:%S"
	for day in available_datetime:
		converted_date=datetime.strptime(str(day), format_string).date()
		date_chk_1=converted_date>=pd.to_datetime(backtest_start_date,format="%Y-%m-%d").date()
		date_chk_2=converted_date<=pd.to_datetime(backtest_end_date,format="%Y-%m-%d").date()
		if date_chk_1 and date_chk_2:
			available_dates.append((converted_date))
			
		
	i=1
	end=len(available_dates)
	format_string = "%Y-%m-%dT%H:%M:%S"
	market_data['Datetime'] = market_data['Datetime'].apply(lambda x: datetime.strptime(x,format_string).date())
	
	data = [[pd.to_datetime("2000-01-01",format="%Y-%m-%d").date(), 0.0025,0.0025]]
	backtest_df = pd.DataFrame(data, columns=['Datetime', 'OC_return','OH_return'])
	available_dates.sort()
	
	print("Starting Backtesting Module")
	while(i<end):
		performance_backtest_date=available_dates[i]
		api_execution_date=available_dates[i-1]
		df=volatility_skew_strategy(api_execution_date)
		purchase_scrip=df['ScripName'].iloc[0]
		scrip_dataset=market_data[market_data['ScripName']==purchase_scrip]
		scrip_dataset=scrip_dataset[scrip_dataset['Datetime']==performance_backtest_date]
		scrip_dataset['OC_return']=(scrip_dataset['Close']-scrip_dataset['Open'])/scrip_dataset['Open']
		scrip_dataset['OH_return']=(scrip_dataset['High']-scrip_dataset['Open'])/scrip_dataset['Open']
		scrip_dataset=scrip_dataset[["Datetime","OC_return","OH_return"]]
		backtest_df=pd.concat([backtest_df, scrip_dataset])
		i=i+1
		
	print("Backtesting Module ended")
	backtest_df=backtest_df.iloc[1:]
	avg_OC_return=backtest_df.loc[:, 'OC_return'].mean()
	avg_OH_return=backtest_df.loc[:, 'OH_return'].mean()
	
	return backtest_df
