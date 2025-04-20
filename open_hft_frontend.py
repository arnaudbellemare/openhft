#----------------------------------------------------------------------------------------------
#Community Cloud | Deployment Guidelines
#1. Make sure to modify the "devcontainer.json" file in the .devcontainer folder in root directory
#2. Change the name of execution file to open_hft_frontend.py
#----------------------------------------------------------------------------------------------


#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import warnings

#--------------------------------------------------------------------
#IMPORT ALL INTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
from api.momentum_strategy_1_api import *
from api.data_snapshot_date_api import *
from api.stochastic_oscillator_1_api import *
from api.valid_date_return_api import *
from api.stochastic_charts_api import *
from api.volatility_skew_strategy_api import *
from api.volatility_charts_api import *
from api.trend_following_strategy_api import *
from api.trend_following_charts_api import *
from api.pairs_trading_strategy_api import *
from api.spread_trading_api import *
from api.spread_trading_consolidated_api import *


#--------------------------------------------------------------------
#SET DISPLAY PARAMETERS FOR STREAMLIT
#--------------------------------------------------------------------
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
warnings.filterwarnings('ignore')

#--------------------------------------------------------------------
#SECTION 0 - INTERNAL VARIABLE DECLARATION
#--------------------------------------------------------------------
strategies=['Momentum Strategy','Stochastic Oscillator Strategy','Volatility Skew Strategy','Trend Following Strategy','Pairs Trading Strategy','Spread Trading Strategy']

scrip_name=['ASIANPAINT','EICHERMOT','HEROMOTOCO','TATAMOTORS','APOLLOHOSP','SBIN','M&M',
          'BEL','JSWSTEEL','ICICIBANK','INDUSINDBK','ONGC','BAJAJ-AUTO','BRITANNIA','NESTLEIND',
          'HINDALCO','RELIANCE','TRENT','TATASTEEL','DRREDDY','SHRIRAMFIN','KOTAKBANK','HDFCBANK',
          'AXISBANK','NTPC','TECHM','SBILIFE','CIPLA','GRASIM','HINDUNILVR','LT','TATACONSUM','WIPRO',
          'TITAN','BPCL','INFY','SUNPHARMA','TCS','MARUTI','HCLTECH','COALINDIA','ULTRACEMCO']


#--------------------------------------------------------------------
#HOME PAGE CODE STARTS HERE
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
st.sidebar.write('🍵 Data Last Refreshed On ' + str(data_snapshot_date()))
st.sidebar.write('--------------')
strategy_selectbox_side = st.sidebar.selectbox('Select your Quant Strategy', (strategies))

#--------------------------------------------------------------------
#SECTION 1 - MAIN PANEL CODE & FUNCTIONAL CALLS
#--------------------------------------------------------------------

#--------------------------------------------------------------------
#QUANT STRATEGY 1 - MOMENTUM STRATEGY
#--------------------------------------------------------------------


if (strategy_selectbox_side==strategies[0]):
  'Below are the stock recommendations for ', strategy_selectbox_side
  df1=momentum_strategy_1(str(data_snapshot_date()))
  st.dataframe(df1,hide_index=True,
    column_config=dict(
      R1Y_return=st.column_config.NumberColumn('R1Y Return', format='%.2f %%'),
      R6M_return=st.column_config.NumberColumn('R6M Return', format='%.2f %%'),
      R3M_return=st.column_config.NumberColumn('R3M Return', format='%.2f %%'),
      R1M_return=st.column_config.NumberColumn('R1M Return', format='%.2f %%'),
      Momentum_Score=st.column_config.NumberColumn('Momentum Score', format='%.2f')
      )

    )
  '-----------------------------------------'
  st.write("""
  **🌁Legend**

  • **R1Y Return** - _Rolling 1 Years Return_  
  • **R6M Return** - _Rolling 6 Months Return_  
  • **R3M Return** - _Rolling 3 Months Return_  
  • **R1M Return** - _Rolling 1 Months Return_  
  • **Momentum Score** - _Arithmetic Average of R1Y, R6M, R3M & R1M Percentiles_
  """)
  '-----------------------------------------'
  

#--------------------------------------------------------------------
#QUANT STRATEGY 2 - STOCHASTIC STRATEGY
#--------------------------------------------------------------------

elif (strategy_selectbox_side==strategies[1]):


  col1, col2 = st.columns(2)
  with col1:
    'Below are the stock recommendations for ', strategy_selectbox_side
    df1=stochastic_strategy_1(data_snapshot_date())
    st.dataframe(df1,hide_index=True,
      column_config=dict(
      K=st.column_config.NumberColumn('Fast Signal (K)'),
      D=st.column_config.NumberColumn('Slow Signal (D)'),
      overbought=st.column_config.NumberColumn('Overbought'),
      oversold=st.column_config.NumberColumn('Oversold'),
      signal_sanitized=st.column_config.NumberColumn('Buy Signal')
      )
    )
  
  with col2:
    scrip_selectbox_main = st.selectbox('Select your Stock', (scrip_name))
    start_date=  st.date_input('Select Start Date for Chart', value=valid_date_return()[0])
    end_date=str(data_snapshot_date())
    df2=stochastic_strategy_1_chart(scrip_selectbox_main,str(start_date),end_date)
    #st.dataframe(df2)
    fig = px.line(
      df2,
      x="Datetime",
      y=["K","D"]
    )
  
    fig.update_layout(
    title={
        'text': "Stochastic Indicator Chart",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig.add_hline(y=100)
    fig.add_hline(y=80,line_dash='dash',line_color="red")
    fig.add_hline(y=20,line_dash='dash',line_color="green")
    fig.add_hline(y=0)
    fig.update_xaxes(title=" ")
    fig.update_yaxes(title=" ")
    #fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

#--------------------------------------------------------------------
#QUANT STRATEGY 2 - VOLATILITY SKEW STRATEGY
#--------------------------------------------------------------------


elif (strategy_selectbox_side==strategies[2]):
  col1, col2 = st.columns(2)
  with col1:
    'Below are the stock recommendations for ', strategy_selectbox_side
    df1=volatility_skew_strategy(data_snapshot_date())
    st.dataframe(df1,hide_index=True
        ,
        column_config=dict(
        V15D_SD=st.column_config.NumberColumn('15D Vol'),
        V30D_SD=st.column_config.NumberColumn('30D Vol'),
        V45D_SD=st.column_config.NumberColumn('45D Vol'),
        weighted_vol=st.column_config.NumberColumn('Weighted Vol')
        )
      )
  with col2:
    scrip_selectbox_main = st.selectbox('Select your Stock', (scrip_name))
    start_date=  st.date_input('Select Start Date for Chart', value=valid_date_return()[0])
    end_date=str(data_snapshot_date())
    df2=volatility_chart(scrip_selectbox_main,str(start_date),end_date)
    #st.dataframe(df2)

    fig = px.line(
      df2,
      x="Datetime",
      y=["V15D_SD"]
    )
    fig.update_layout(
    title={
        'text': "Volatility Chart",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig.update_xaxes(title=" ")
    fig.update_yaxes(title=" ")
    fig.update_layout(showlegend=False)
    fixed_vol=volatility_average(scrip_selectbox_main)
    fig.add_hline(y=fixed_vol,line_dash='dash',line_color="green")
    st.plotly_chart(fig, use_container_width=True)

#--------------------------------------------------------------------
#QUANT STRATEGY 3 - TREND FOLLOWING STRATEGY
#--------------------------------------------------------------------


elif (strategy_selectbox_side==strategies[3]):
  col1, col2 = st.columns(2)
  with col1:
    print("Entered Trend Following Strategy")
    #st.write("Data Refresh Date: "+str(data_snapshot_date()))
    'Below are the stock recommendations for ', strategy_selectbox_side
    df1=trend_following_strategy(data_snapshot_date())
    #st.dataframe(df1)
    st.dataframe(df1,hide_index=True
        ,
        column_config=dict(
        R03D_DR=st.column_config.NumberColumn('A03DD Return',format='%.3f %%'),
        R15D_DR=st.column_config.NumberColumn('A15DD Return',format='%.3f %%'),
        R30D_DR=st.column_config.NumberColumn('A30DD Return',format='%.3f %%'),
        R45D_DR=st.column_config.NumberColumn('A45DD Return',format='%.3f %%'),
        weighted_daily_return=st.column_config.NumberColumn('Weighted Average Return',format='%.2f %%')
        )
      )
    

  with col2:
    scrip_selectbox_main = st.selectbox('Select your Stock', (scrip_name))
    start_date=  st.date_input('Select Start Date for Chart', value=valid_date_return()[0])
    end_date=str(data_snapshot_date())
    df2=daily_return_chart(scrip_selectbox_main,str(start_date),end_date)
    #st.dataframe(df2)

    fig = px.line(
      df2,
      x="Datetime",
      y=["daily_return"]  
    )

    fig.update_layout(
    title={
        'text': "Daily Return Profile (in %)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig.update_xaxes(title=" ")
    fig.update_yaxes(title=" ")
    fig.update_layout(showlegend=False)
    #fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    #fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    #fixed_vol=volatility_average(scrip_selectbox_main)
    #st.write(fixed_vol)
    #fig.add_hline(y=fixed_vol,line_dash='dash',line_color="green")
    st.plotly_chart(fig, use_container_width=True)   
    #-------------------------------------------------------------------------------------------------
    #Use st.metrics to display the final recommendations in a fancy manner at a later stage of the MVP
    #-------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------
#QUANT STRATEGY 4 - PAIRS TRADING STRATEGY
#--------------------------------------------------------------------

elif (strategy_selectbox_side==strategies[4]):
  display = pairs_trading(str(data_snapshot_date()))
  options = list(range(len(display)))
  value = st.selectbox("Select your Stock Pair", options, format_func=lambda x: display[x])
  asset1,asset2=display[value]
  df=pairs_trading_spread(value)
  fig = px.line(
  df,
  x="Datetime",
  y=["return"]  
  )

  fig.update_layout(
  title={
        'text': "Spread Between "+str(asset1)+" & "+str(asset2),
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
  fig.update_xaxes(title=" ")
  fig.update_yaxes(title=" ")
  fig.update_layout(showlegend=False)
  lb=-df.loc[:, 'return'].std()
  ub=df.loc[:, 'return'].std()
  avg=df.loc[:, 'return'].mean()
  fig.add_hline(y=lb,line_dash='dash',line_color="red")
  fig.add_hline(y=2*lb,line_dash='dot',line_color="green")
  fig.add_hline(y=ub,line_dash='dash',line_color="red")
  fig.add_hline(y=2*ub,line_dash='dot',line_color="green")
  fig.add_hline(y=avg,line_dash='dot',line_color="yellow")
  #fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
  #fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
  #fixed_vol=volatility_average(scrip_selectbox_main)
  #st.write(fixed_vol)
  #fig.add_hline(y=fixed_vol,line_dash='dash',line_color="green")
  st.plotly_chart(fig, use_container_width=True)


  col1, col2 = st.columns(2)
  with col1:
    fig1 = px.line(
    df,
    x="Datetime",
    y=["asset1"]  
    )
    fig1.update_layout(
    title={
        'text': "Stock Price Chart for "+str(asset1),
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})   
    fig1.update_xaxes(title=" ")
    fig1.update_yaxes(title=" ")
    fig1.update_layout(showlegend=False)
  
    st.plotly_chart(fig1, use_container_width=True)

  with col2:
    fig2 = px.line(
    df,
    x="Datetime",
    y=["asset2"]  
    )   
    fig2.update_layout(
    title={
        'text': "Stock Price Chart for "+str(asset2),
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}) 

    fig2.update_xaxes(title=" ")
    fig2.update_yaxes(title=" ")
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)



#--------------------------------------------------------------------
#QUANT STRATEGY 5 - SPREAD TRADING STRATEGY
#--------------------------------------------------------------------


elif (strategy_selectbox_side==strategies[5]):
  'Below are the stock recommendations for ', strategy_selectbox_side
  df3=spread_trading_consolidated()
  st.dataframe(df3,hide_index=True)
  st.divider()
  col1, col2 = st.columns(2)
  with col1:
    'Select parameters to determine the spreads observed over the selected period'
    scrip_selectbox_main = st.selectbox('Select your Stock', (scrip_name))
    start_date=  st.date_input('Select Start Date for Chart', value=valid_date_return()[0])
    end_date=str(data_snapshot_date())
    df2=spread_trading(scrip_selectbox_main,str(start_date),end_date)
    df1=df2
    st.dataframe(df1,hide_index=True)
    
  with col2:
    #print("Testing")
    'Below chart represents the spreads observed for the stock over the selected period'
    #scrip_selectbox_main_1 = st.selectbox('Select your Current Stock', (scrip_name))
    #start_date_1=  st.date_input('Select Start Date for Chart', value=valid_date_return()[0])
    #end_date_1=str(data_snapshot_date())
    #print(end_date)
    fig = px.bar(
      df1,
      x="Datetime",
      y=["Spread"]
    )
    st.plotly_chart(fig, use_container_width=True)



else:
  'Strategy not yet configured'
