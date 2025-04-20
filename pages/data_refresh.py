#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import os

#--------------------------------------------------------------------
#IMPORT ALL INTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
#from api.data_snapshot_date_api import *


#--------------------------------------------------------------------
#SECTION 0 - INTERNAL VARIABLE DECLARATION
#--------------------------------------------------------------------
strategies=['Momentum Strategy','Stochastic Oscillator Strategy','Volatility Skew Strategy','Trend Following Strategy']

scrip_name=['ASIANPAINT','EICHERMOT','HEROMOTOCO','TATAMOTORS','APOLLOHOSP','SBIN','M&M',
          'BEL','JSWSTEEL','ICICIBANK','INDUSINDBK','ONGC','BAJAJ-AUTO','BRITANNIA','NESTLEIND',
          'HINDALCO','RELIANCE','TRENT','TATASTEEL','DRREDDY','SHRIRAMFIN','KOTAKBANK','HDFCBANK',
          'AXISBANK','NTPC','TECHM','SBILIFE','CIPLA','GRASIM','HINDUNILVR','LT','TATACONSUM','WIPRO',
          'TITAN','BPCL','INFY','SUNPHARMA','TCS','MARUTI','HCLTECH','COALINDIA','ULTRACEMCO']


#--------------------------------------------------------------------
#BACKTEST PAGE CODE STARTS HERE
#--------------------------------------------------------------------
#SECTION 1 - SIDE PANEL CODE
#--------------------------------------------------------------------

st.sidebar.image("logo.jpg")
st.sidebar.write('--------------')
st.sidebar.subheader('Navigation Bar')
st.sidebar.page_link("open_hft_frontend.py", label="Quant Strategies", icon="🏠")
#st.sidebar.page_link("streamlit_app.py", label="Quant Strategies", icon="🏠")
st.sidebar.page_link("pages/intraday_forecasts.py", label="Intraday ML Forecasts", icon="⛅")
st.sidebar.page_link("pages/backtests.py", label="Backtesting Module", icon="📠")
st.sidebar.page_link("pages/data_refresh.py", label="Refresh Dataset", icon="🛢️")
#st.sidebar.write('🍵 Data Last Refreshed On ' + str(data_snapshot_date()))
st.sidebar.write('--------------')


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

title = st.text_input("Enter Two Factor Authentication Password", "")

if st.button("Execute Data Refresh", type="primary"):
    st.write("Executing Market Data Refresh")
    client = FivePaisaClient(cred=cred)
    response=client.get_totp_session('59704099',title,'150395')
    st.write(response)
    new_path='marketdata/dailydata'
    #os.chdir(new_path)

    i=0
    st.write("Entering Data write loop")
    for code in ScripCode:
        df=client.historical_data('N','C',code,'1d','2022-01-01',str(datetime.datetime.today()).split()[0])
        df['ScripName']=ScripName[i]
        df['ScripCode']=code
        file_name=str(code)+'.csv'
        print("Saving Data Frame for Scrip "+file_name)
        compact_path=new_path+'/'+file_name
        #df.to_csv(file_name)
        df.to_csv(compact_path)
        i=i+1
        #b=st.empty()
        #if i%2==0:
        #    b.text("(+ - - - - -)")
        #else:
        #    b.text("(- - - - - +)")
    st.write("Market Data Refresh Finished")
