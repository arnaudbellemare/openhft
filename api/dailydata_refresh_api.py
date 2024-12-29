#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import datetime
import os

#--------------------------------------------------------------------
#LOGIN CREDENTIALS
#SECURE ENCRYPTION NEEDS TO BE ESTABLISHED FOR THIS
#--------------------------------------------------------------------

from py5paisa import FivePaisaClient
cred={
    "APP_NAME":"5P59704099",
    "APP_SOURCE":"24754",
    "USER_ID":"gTdR58TPfbj",
    "PASSWORD":"QkzqzMNFvet",
    "USER_KEY":"SyKsXvXfGbrllnbrfsRWz3a6nVTcVysq",
    "ENCRYPTION_KEY":"aKqK8EYVrzGvmQuTBxuiwwWbzRuh63CM"
    }

nifty_master_path='marketdata/Nifty_Master.csv'
nifty_master = pd.read_csv(nifty_master_path)


ScripCode = nifty_master['ScripCode'].values.tolist()
ScripName = nifty_master['Name'].values.tolist()


client = FivePaisaClient(cred=cred)
client.get_totp_session('59704099',input("enter totp >>> "),'150395')

new_path='marketdata/dailydata'
os.chdir(new_path)

i=0
for code in ScripCode:
    df=client.historical_data('N','C',code,'1d','2022-01-01',str(datetime.datetime.today()).split()[0])
    df['ScripName']=ScripName[i]
    df['ScripCode']=code
    file_name=str(code)+'.csv'
    print("Saving Data Frame for Scrip "+file_name)
    df.to_csv(file_name)
    i=i+1

