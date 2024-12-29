#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import datetime
import os
from datetime import datetime, timedelta
import arrow
from scipy.stats import percentileofscore

def valid_date_return():


	#--------------------------------------------------------------------
	#SET-UP ALL PATH VARIABLES
	#--------------------------------------------------------------------
	nifty_master_path='marketdata/Nifty_Master.csv'
	temp_path='marketdata/dailydata'
	new_path='marketdata/dailydata'

	nifty_master = pd.read_csv(nifty_master_path)
	ScripCode = nifty_master['ScripCode'].values.tolist()
	ScripName = nifty_master['Name'].values.tolist()

	new_path=new_path+'/'+str(ScripCode[0])+'.csv'
	market_data = pd.read_csv(new_path)
	
	for code in ScripCode:
		new_path=temp_path
		new_path=new_path+'/'+str(code)+'.csv'
		additional_market_data=pd.read_csv(new_path)
		market_data=pd.concat([market_data, additional_market_data])
	
	#--------------------------------------------------------------------
	#FUNCTION DEFINITION FOR CHECKING DATE VALIDITY FOR TRADING DAY
	#--------------------------------------------------------------------
	

	available_datetime=market_data['Datetime'].values.tolist()
	available_dates=[]
	format_string = "%Y-%m-%dT%H:%M:%S"
	for day in available_datetime:
		converted_date=datetime.strptime(str(day), format_string).date()
		available_dates.append((converted_date))

	return available_dates
