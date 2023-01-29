"""
This module for list the best known cryptocurrencies and prices from binance app and 
to create technical indicators in future versions
"""

#importing libraries
import pandas as pd
from binance import Client




# instance of binance Client module
client=Client()

# defining symbols
symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'SOLUSDT', 'DOTUSDT', 'DOGEUSDT', 'MATICUSDT',
            'SHIBUSDT', 'AVAXUSDT', 'CHZUSDT', 'LTCUSDT', 'FTTUSDT']

# The main function that converts the symbol, interval, lookback values ​​received from the user(frontend) to pandas dataframe using the binance client module
def get_data(symbol, interval="4h", lookback="100"):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+" hours UTC"))
    frame = frame.iloc[:,0:6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame.set_index('Time', inplace=False)
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)

    return frame

# part of technical indicators that will be developed in future versions
def indicators(frame, roll=15):
    frame['RollHigh'] = frame.High.rolling(roll).max()
    frame['RollLow'] = frame.Low.rolling(roll).min()
    frame['Mid'] = (frame.RollHigh + frame.RollLow)/2

    return frame



