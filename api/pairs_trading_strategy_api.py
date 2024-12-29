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

#--------------------------------------------------------------------
#FUNCTION DEFINITION FOR PAIR IDENTIFICATION
#--------------------------------------------------------------------

def pairs_trading(date_delim):

	#--------------------------------------------------------------------
	#SET-UP ALL PATH VARIABLES
	#--------------------------------------------------------------------
	nifty_master_path='marketdata/Nifty_Master.csv'
	temp_path='marketdata/dailydata'
	new_path='marketdata/dailydata'
	warnings.filterwarnings('ignore')

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

	#--------------------------------------------------------------------
	#CREATE DAILY RETURN METRICS
	#--------------------------------------------------------------------	
	market_data['daily_return']=(market_data['Close']-market_data['Open'])/market_data['Open']
	
	for code in ScripCode:
		new_path=temp_path
		new_path=new_path+'/'+str(code)+'.csv'
		additional_market_data=pd.read_csv(new_path)
		additional_market_data['daily_return']=(additional_market_data['Close']-additional_market_data['Open'])/additional_market_data['Open']
		market_data=pd.concat([market_data, additional_market_data])
	
	market_data=market_data.drop_duplicates()
	market_data=market_data[['Datetime','ScripName','daily_return']]
	out = market_data.pivot(index=['Datetime'], columns='ScripName', values='daily_return')
	out=out.dropna()
	out=out.rename_axis(columns=None).reset_index()
	
	#--------------------------------------------------------------------
	#STANDARDIZE DAILY RETURNS
	#--------------------------------------------------------------------	
	assets=['ASIANPAINT','EICHERMOT','HEROMOTOCO','TATAMOTORS','APOLLOHOSP','SBIN','M&M',
	          'BEL','JSWSTEEL','ICICIBANK','INDUSINDBK','ONGC','BAJAJ-AUTO','BRITANNIA','NESTLEIND',
	          'HINDALCO','RELIANCE','TRENT','TATASTEEL','DRREDDY','SHRIRAMFIN','KOTAKBANK','HDFCBANK',
	          'AXISBANK','NTPC','TECHM','SBILIFE','CIPLA','GRASIM','HINDUNILVR','LT','TATACONSUM','WIPRO',
	          'TITAN','BPCL','INFY','SUNPHARMA','TCS','MARUTI','HCLTECH','COALINDIA','ULTRACEMCO']
	
	out['ASIANPAINT']=(out['ASIANPAINT']-(out.loc[:, 'ASIANPAINT'].mean()))/(out.loc[:, 'ASIANPAINT'].std())
	out['EICHERMOT']=(out['EICHERMOT']-(out.loc[:, 'EICHERMOT'].mean()))/(out.loc[:, 'EICHERMOT'].std())
	out['HEROMOTOCO']=(out['HEROMOTOCO']-(out.loc[:, 'HEROMOTOCO'].mean()))/(out.loc[:, 'HEROMOTOCO'].std())
	out['TATAMOTORS']=(out['TATAMOTORS']-(out.loc[:, 'TATAMOTORS'].mean()))/(out.loc[:, 'TATAMOTORS'].std())
	out['APOLLOHOSP']=(out['APOLLOHOSP']-(out.loc[:, 'APOLLOHOSP'].mean()))/(out.loc[:, 'APOLLOHOSP'].std())
	out['SBIN']=(out['SBIN']-(out.loc[:, 'SBIN'].mean()))/(out.loc[:, 'SBIN'].std())
	out['M&M']=(out['M&M']-(out.loc[:, 'M&M'].mean()))/(out.loc[:, 'M&M'].std())
	out['BEL']=(out['BEL']-(out.loc[:, 'BEL'].mean()))/(out.loc[:, 'BEL'].std())
	out['JSWSTEEL']=(out['JSWSTEEL']-(out.loc[:, 'JSWSTEEL'].mean()))/(out.loc[:, 'JSWSTEEL'].std())
	out['ICICIBANK']=(out['ICICIBANK']-(out.loc[:, 'ICICIBANK'].mean()))/(out.loc[:, 'ICICIBANK'].std())
	out['INDUSINDBK']=(out['INDUSINDBK']-(out.loc[:, 'INDUSINDBK'].mean()))/(out.loc[:, 'INDUSINDBK'].std())
	out['ONGC']=(out['ONGC']-(out.loc[:, 'ONGC'].mean()))/(out.loc[:, 'ONGC'].std())
	out['BAJAJ-AUTO']=(out['BAJAJ-AUTO']-(out.loc[:, 'BAJAJ-AUTO'].mean()))/(out.loc[:, 'BAJAJ-AUTO'].std())
	out['BRITANNIA']=(out['BRITANNIA']-(out.loc[:, 'BRITANNIA'].mean()))/(out.loc[:, 'BRITANNIA'].std())
	out['NESTLEIND']=(out['NESTLEIND']-(out.loc[:, 'NESTLEIND'].mean()))/(out.loc[:, 'NESTLEIND'].std())
	out['HINDALCO']=(out['HINDALCO']-(out.loc[:, 'HINDALCO'].mean()))/(out.loc[:, 'HINDALCO'].std())
	out['RELIANCE']=(out['RELIANCE']-(out.loc[:, 'RELIANCE'].mean()))/(out.loc[:, 'RELIANCE'].std())
	out['TRENT']=(out['TRENT']-(out.loc[:, 'TRENT'].mean()))/(out.loc[:, 'TRENT'].std())
	out['TATASTEEL']=(out['TATASTEEL']-(out.loc[:, 'TATASTEEL'].mean()))/(out.loc[:, 'TATASTEEL'].std())
	out['DRREDDY']=(out['DRREDDY']-(out.loc[:, 'DRREDDY'].mean()))/(out.loc[:, 'DRREDDY'].std())
	out['SHRIRAMFIN']=(out['SHRIRAMFIN']-(out.loc[:, 'SHRIRAMFIN'].mean()))/(out.loc[:, 'SHRIRAMFIN'].std())
	out['KOTAKBANK']=(out['KOTAKBANK']-(out.loc[:, 'KOTAKBANK'].mean()))/(out.loc[:, 'KOTAKBANK'].std())
	out['HDFCBANK']=(out['HDFCBANK']-(out.loc[:, 'HDFCBANK'].mean()))/(out.loc[:, 'HDFCBANK'].std())
	out['AXISBANK']=(out['AXISBANK']-(out.loc[:, 'AXISBANK'].mean()))/(out.loc[:, 'AXISBANK'].std())
	out['NTPC']=(out['NTPC']-(out.loc[:, 'NTPC'].mean()))/(out.loc[:, 'NTPC'].std())
	out['TECHM']=(out['TECHM']-(out.loc[:, 'TECHM'].mean()))/(out.loc[:, 'TECHM'].std())
	out['SBILIFE']=(out['SBILIFE']-(out.loc[:, 'SBILIFE'].mean()))/(out.loc[:, 'SBILIFE'].std())
	out['CIPLA']=(out['CIPLA']-(out.loc[:, 'CIPLA'].mean()))/(out.loc[:, 'CIPLA'].std())
	out['GRASIM']=(out['GRASIM']-(out.loc[:, 'GRASIM'].mean()))/(out.loc[:, 'GRASIM'].std())
	out['HINDUNILVR']=(out['HINDUNILVR']-(out.loc[:, 'HINDUNILVR'].mean()))/(out.loc[:, 'HINDUNILVR'].std())
	out['LT']=(out['LT']-(out.loc[:, 'LT'].mean()))/(out.loc[:, 'LT'].std())
	out['TATACONSUM']=(out['TATACONSUM']-(out.loc[:, 'TATACONSUM'].mean()))/(out.loc[:, 'TATACONSUM'].std())
	out['WIPRO']=(out['WIPRO']-(out.loc[:, 'WIPRO'].mean()))/(out.loc[:, 'WIPRO'].std())
	out['TITAN']=(out['TITAN']-(out.loc[:, 'TITAN'].mean()))/(out.loc[:, 'TITAN'].std())
	out['BPCL']=(out['BPCL']-(out.loc[:, 'BPCL'].mean()))/(out.loc[:, 'BPCL'].std())
	out['INFY']=(out['INFY']-(out.loc[:, 'INFY'].mean()))/(out.loc[:, 'INFY'].std())
	out['SUNPHARMA']=(out['SUNPHARMA']-(out.loc[:, 'SUNPHARMA'].mean()))/(out.loc[:, 'SUNPHARMA'].std())
	out['TCS']=(out['TCS']-(out.loc[:, 'TCS'].mean()))/(out.loc[:, 'TCS'].std())
	out['MARUTI']=(out['MARUTI']-(out.loc[:, 'MARUTI'].mean()))/(out.loc[:, 'MARUTI'].std())
	out['HCLTECH']=(out['HCLTECH']-(out.loc[:, 'HCLTECH'].mean()))/(out.loc[:, 'HCLTECH'].std())
	out['COALINDIA']=(out['COALINDIA']-(out.loc[:, 'COALINDIA'].mean()))/(out.loc[:, 'COALINDIA'].std())
	out['ULTRACEMCO']=(out['ULTRACEMCO']-(out.loc[:, 'ULTRACEMCO'].mean()))/(out.loc[:, 'ULTRACEMCO'].std())
	
	prices_df=out.copy()
	prices_df=prices_df.loc[:, prices_df.columns != 'Datetime']
	
	correlation_matrix=prices_df.corr()
	
	#--------------------------------------------------------------------
	# Find pairs with high positive correlation
	#--------------------------------------------------------------------
	highly_correlated_pairs = []
	for pair in combinations(assets, 2):
	    asset1, asset2 = pair
	    correlation = correlation_matrix.loc[asset1, asset2]
	    if correlation > 0.5:
	        highly_correlated_pairs.append(pair)
	
	
	#--------------------------------------------------------------------
	# Implement cointegration analysis for pair selection
	#--------------------------------------------------------------------
	def cointegration_analysis(data):
	    cointegrated_pairs = []
	
	    for pair in highly_correlated_pairs:
	        asset1, asset2 = pair
	        result = coint(data[asset1], data[asset2])
	
	        if result[1] < 0.05:  # Check for p-value significance
	            cointegrated_pairs.append(pair)
	
	    return cointegrated_pairs
	
	#--------------------------------------------------------------------
	# Perform cointegration analysis on the returns data
	#--------------------------------------------------------------------
	cointegrated_pairs = cointegration_analysis(prices_df)
	
	
	return(cointegrated_pairs)


#--------------------------------------------------------------------
#FUNCTION DEFINITION FOR CALCULATING SPREAD
#--------------------------------------------------------------------

def pairs_trading_spread(pair_num_value):

	#--------------------------------------------------------------------
	#SET-UP ALL PATH VARIABLES
	#--------------------------------------------------------------------
	nifty_master_path='marketdata/Nifty_Master.csv'
	temp_path='marketdata/dailydata'
	new_path='marketdata/dailydata'
	warnings.filterwarnings('ignore')

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

	#--------------------------------------------------------------------
	#CREATE DAILY RETURN METRICS
	#--------------------------------------------------------------------
	market_data['daily_return']=(market_data['Close']-market_data['Open'])/market_data['Open']
	
	for code in ScripCode:
		new_path=temp_path
		new_path=new_path+'/'+str(code)+'.csv'
		additional_market_data=pd.read_csv(new_path)
		additional_market_data['daily_return']=(additional_market_data['Close']-additional_market_data['Open'])/additional_market_data['Open']
		market_data=pd.concat([market_data, additional_market_data])
	
	market_data=market_data.drop_duplicates()
	backup_df=market_data.copy()
	market_data=market_data[['Datetime','ScripName','daily_return']]
	out = market_data.pivot(index=['Datetime'], columns='ScripName', values='daily_return')
	out=out.dropna()
	out=out.rename_axis(columns=None).reset_index()
	

	open_price_df=backup_df.pivot(index=['Datetime'], columns='ScripName', values='Close')
	open_price_df=open_price_df.dropna()
	open_price_df=open_price_df.rename_axis(columns=None).reset_index()

	#--------------------------------------------------------------------
	#STANDARDIZE DAILY RETURNS
	#--------------------------------------------------------------------	
	
	assets=['ASIANPAINT','EICHERMOT','HEROMOTOCO','TATAMOTORS','APOLLOHOSP','SBIN','M&M',
	          'BEL','JSWSTEEL','ICICIBANK','INDUSINDBK','ONGC','BAJAJ-AUTO','BRITANNIA','NESTLEIND',
	          'HINDALCO','RELIANCE','TRENT','TATASTEEL','DRREDDY','SHRIRAMFIN','KOTAKBANK','HDFCBANK',
	          'AXISBANK','NTPC','TECHM','SBILIFE','CIPLA','GRASIM','HINDUNILVR','LT','TATACONSUM','WIPRO',
	          'TITAN','BPCL','INFY','SUNPHARMA','TCS','MARUTI','HCLTECH','COALINDIA','ULTRACEMCO']
	
	out['ASIANPAINT']=(out['ASIANPAINT']-(out.loc[:, 'ASIANPAINT'].mean()))/(out.loc[:, 'ASIANPAINT'].std())
	out['EICHERMOT']=(out['EICHERMOT']-(out.loc[:, 'EICHERMOT'].mean()))/(out.loc[:, 'EICHERMOT'].std())
	out['HEROMOTOCO']=(out['HEROMOTOCO']-(out.loc[:, 'HEROMOTOCO'].mean()))/(out.loc[:, 'HEROMOTOCO'].std())
	out['TATAMOTORS']=(out['TATAMOTORS']-(out.loc[:, 'TATAMOTORS'].mean()))/(out.loc[:, 'TATAMOTORS'].std())
	out['APOLLOHOSP']=(out['APOLLOHOSP']-(out.loc[:, 'APOLLOHOSP'].mean()))/(out.loc[:, 'APOLLOHOSP'].std())
	out['SBIN']=(out['SBIN']-(out.loc[:, 'SBIN'].mean()))/(out.loc[:, 'SBIN'].std())
	out['M&M']=(out['M&M']-(out.loc[:, 'M&M'].mean()))/(out.loc[:, 'M&M'].std())
	out['BEL']=(out['BEL']-(out.loc[:, 'BEL'].mean()))/(out.loc[:, 'BEL'].std())
	out['JSWSTEEL']=(out['JSWSTEEL']-(out.loc[:, 'JSWSTEEL'].mean()))/(out.loc[:, 'JSWSTEEL'].std())
	out['ICICIBANK']=(out['ICICIBANK']-(out.loc[:, 'ICICIBANK'].mean()))/(out.loc[:, 'ICICIBANK'].std())
	out['INDUSINDBK']=(out['INDUSINDBK']-(out.loc[:, 'INDUSINDBK'].mean()))/(out.loc[:, 'INDUSINDBK'].std())
	out['ONGC']=(out['ONGC']-(out.loc[:, 'ONGC'].mean()))/(out.loc[:, 'ONGC'].std())
	out['BAJAJ-AUTO']=(out['BAJAJ-AUTO']-(out.loc[:, 'BAJAJ-AUTO'].mean()))/(out.loc[:, 'BAJAJ-AUTO'].std())
	out['BRITANNIA']=(out['BRITANNIA']-(out.loc[:, 'BRITANNIA'].mean()))/(out.loc[:, 'BRITANNIA'].std())
	out['NESTLEIND']=(out['NESTLEIND']-(out.loc[:, 'NESTLEIND'].mean()))/(out.loc[:, 'NESTLEIND'].std())
	out['HINDALCO']=(out['HINDALCO']-(out.loc[:, 'HINDALCO'].mean()))/(out.loc[:, 'HINDALCO'].std())
	out['RELIANCE']=(out['RELIANCE']-(out.loc[:, 'RELIANCE'].mean()))/(out.loc[:, 'RELIANCE'].std())
	out['TRENT']=(out['TRENT']-(out.loc[:, 'TRENT'].mean()))/(out.loc[:, 'TRENT'].std())
	out['TATASTEEL']=(out['TATASTEEL']-(out.loc[:, 'TATASTEEL'].mean()))/(out.loc[:, 'TATASTEEL'].std())
	out['DRREDDY']=(out['DRREDDY']-(out.loc[:, 'DRREDDY'].mean()))/(out.loc[:, 'DRREDDY'].std())
	out['SHRIRAMFIN']=(out['SHRIRAMFIN']-(out.loc[:, 'SHRIRAMFIN'].mean()))/(out.loc[:, 'SHRIRAMFIN'].std())
	out['KOTAKBANK']=(out['KOTAKBANK']-(out.loc[:, 'KOTAKBANK'].mean()))/(out.loc[:, 'KOTAKBANK'].std())
	out['HDFCBANK']=(out['HDFCBANK']-(out.loc[:, 'HDFCBANK'].mean()))/(out.loc[:, 'HDFCBANK'].std())
	out['AXISBANK']=(out['AXISBANK']-(out.loc[:, 'AXISBANK'].mean()))/(out.loc[:, 'AXISBANK'].std())
	out['NTPC']=(out['NTPC']-(out.loc[:, 'NTPC'].mean()))/(out.loc[:, 'NTPC'].std())
	out['TECHM']=(out['TECHM']-(out.loc[:, 'TECHM'].mean()))/(out.loc[:, 'TECHM'].std())
	out['SBILIFE']=(out['SBILIFE']-(out.loc[:, 'SBILIFE'].mean()))/(out.loc[:, 'SBILIFE'].std())
	out['CIPLA']=(out['CIPLA']-(out.loc[:, 'CIPLA'].mean()))/(out.loc[:, 'CIPLA'].std())
	out['GRASIM']=(out['GRASIM']-(out.loc[:, 'GRASIM'].mean()))/(out.loc[:, 'GRASIM'].std())
	out['HINDUNILVR']=(out['HINDUNILVR']-(out.loc[:, 'HINDUNILVR'].mean()))/(out.loc[:, 'HINDUNILVR'].std())
	out['LT']=(out['LT']-(out.loc[:, 'LT'].mean()))/(out.loc[:, 'LT'].std())
	out['TATACONSUM']=(out['TATACONSUM']-(out.loc[:, 'TATACONSUM'].mean()))/(out.loc[:, 'TATACONSUM'].std())
	out['WIPRO']=(out['WIPRO']-(out.loc[:, 'WIPRO'].mean()))/(out.loc[:, 'WIPRO'].std())
	out['TITAN']=(out['TITAN']-(out.loc[:, 'TITAN'].mean()))/(out.loc[:, 'TITAN'].std())
	out['BPCL']=(out['BPCL']-(out.loc[:, 'BPCL'].mean()))/(out.loc[:, 'BPCL'].std())
	out['INFY']=(out['INFY']-(out.loc[:, 'INFY'].mean()))/(out.loc[:, 'INFY'].std())
	out['SUNPHARMA']=(out['SUNPHARMA']-(out.loc[:, 'SUNPHARMA'].mean()))/(out.loc[:, 'SUNPHARMA'].std())
	out['TCS']=(out['TCS']-(out.loc[:, 'TCS'].mean()))/(out.loc[:, 'TCS'].std())
	out['MARUTI']=(out['MARUTI']-(out.loc[:, 'MARUTI'].mean()))/(out.loc[:, 'MARUTI'].std())
	out['HCLTECH']=(out['HCLTECH']-(out.loc[:, 'HCLTECH'].mean()))/(out.loc[:, 'HCLTECH'].std())
	out['COALINDIA']=(out['COALINDIA']-(out.loc[:, 'COALINDIA'].mean()))/(out.loc[:, 'COALINDIA'].std())
	out['ULTRACEMCO']=(out['ULTRACEMCO']-(out.loc[:, 'ULTRACEMCO'].mean()))/(out.loc[:, 'ULTRACEMCO'].std())
	
	
	
	prices_df=out.copy()
	prices_df=prices_df.loc[:, prices_df.columns != 'Datetime']
	correlation_matrix=prices_df.corr()
	
	highly_correlated_pairs = []
	for pair in combinations(assets, 2):
	    asset1, asset2 = pair
	    correlation = correlation_matrix.loc[asset1, asset2]
	    if correlation > 0.5:
	        highly_correlated_pairs.append(pair)
	

	def cointegration_analysis(data):
	    cointegrated_pairs = []
	
	    for pair in highly_correlated_pairs:
	        asset1, asset2 = pair
	        result = coint(data[asset1], data[asset2])
	
	        if result[1] < 0.05:  # Check for p-value significance
	            cointegrated_pairs.append(pair)
	
	    return cointegrated_pairs
	
	#--------------------------------------------------------------------
	# Perform cointegration analysis on the returns data
	#--------------------------------------------------------------------
	cointegrated_pairs = cointegration_analysis(prices_df)
	counter=0

	spread = pd.DataFrame(columns=['Datetime','asset1','asset2', 'return'])
	for pair in cointegrated_pairs:
		if counter==pair_num_value:
			asset1, asset2 = pair
			spread['asset1']=open_price_df[asset1]
			spread['asset2']=open_price_df[asset2]
			spread['return']=prices_df[asset1]-prices_df[asset2]
			spread['Datetime']=out['Datetime']
		counter=counter+1

	return(spread)