#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import datetime
import os
from datetime import datetime, timedelta
import arrow
from scipy.stats import percentileofscore



def data_snapshot_date():
	
	#--------------------------------------------------------------------
	#SET-UP ALL PATH VARIABLES
	#--------------------------------------------------------------------
	nifty_master_path='marketdata/Nifty_Master.csv'
	temp_path='marketdata/dailydata'
	new_path='marketdata/dailydata'
	

	#--------------------------------------------------------------------
	#FUNCTION DEFINITION FOR GETTING THE LATEST DATE IN DAILY DATA
	#--------------------------------------------------------------------
	nifty_master = pd.read_csv(nifty_master_path)
	ScripCode = nifty_master['ScripCode'].values.tolist()
	ScripName = nifty_master['Name'].values.tolist()
	new_path=new_path+'/'+str(ScripCode[0])+'.csv'
	market_data = pd.read_csv(new_path)
	timestamp_string=market_data['Datetime'].max()
	format_string = "%Y-%m-%dT%H:%M:%S"
	datetime_object = datetime.strptime(timestamp_string, format_string)
	date_obj = datetime_object.date()
	
	return(date_obj)