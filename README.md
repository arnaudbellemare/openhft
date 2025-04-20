![GitHub Logo v6](https://github.com/user-attachments/assets/9d7a22d4-22d9-40b4-8de3-30ef8ac81962)
# OpenHFT
OpenHFT was founded with the mission of democratizing computational finance for all market participants. This repository houses a python application that enables retail traders to deploy quantitative trading strategies for indian markets. Try out our app at https://openhft.streamlit.app/

### Overview
Up till now, sophisticated quantitative strategies have been limited to proprietary trading firms who typically deploy their own army of in-house data engineers and quantitative traders who then deploy this models for US and other markets. At OpenHFT, our aim is to bring these frontier models to retail participants who can then leverage the same for Indian markets. Our python application houses three sections: 
+ Quant Models 
+ Backtests 
+ ML Forecasts

### Model Overview
The package covers the following strategies
1. Momentum Strategy
2. Stochastic Oscillator Strategy
3. Volatility Skew Strategy
4. Trend Following Strategy
5. Pairs Trading Strategy
6. Spread Trading Strategy

Each strategy has been implemented under an API framework to ensure the strategy can be leveraged independently for backtesting. Retail participants can directly visit our application over internet and look at the recommendations basis each strategy for the indian market. For developers all the quant strategies are captured in individual python files inside the api folder for the quanthft package. Backtest frameworks have also been implemented for each of the quantitaive strategies basis an Open Buy - Close Sell algorithm for trading.

### ML Forecasts
Our team at OpenHFT has also trained a machine learning model based on the XGBoost Classifier on historical nifty 50 stocks for indian markets. The classifier has an objective function of maximizing intra-day profits (Buy at Open & Sell at Close) and by passing the features for Nth day, the machine learning model is able to generate a buy/sell signal for retail participants to act upon. The feature dependence plots & confusion matrix can be accessed via the application frontend. The training dataset and the feature generation scripts are housed inside the ml_model folder inside the quanthft package.

### Special Thanks
A lot of passion and love went into the creation of this application, and we would like to say special thank you to [Moulik Adak](https://github.com/ikad95) for his contribution and guidance towards driving the technical architecture for this program and his significant help in building some of these frameworks and strategies in python
