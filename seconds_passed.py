import datetime as dt
import pytz
import pandas as pd
'''
Example script for seeing the time passed on seconds from buy signal and the current time

'''
df = pd.read_csv('data/BTCUSD.csv')

buy_df = df[df['buy'] == 1]
sell_df = df[df['sell'] == 1]
current_time = dt.datetime.now(pytz.utc)

latest_buy = buy_df.iloc[-1]
buy_time = pd.Timestamp(latest_buy['timestamp'], tz=None) - pd.Timestamp(current_time, tz=None)

latest_sell = sell_df.iloc[-1]
sell_time = pd.Timestamp(latest_sell['timestamp'], tz=None) - pd.Timestamp(current_time, tz=None)


seconds_passed = (pd.Timestamp(latest_buy['timestamp'], tz=None) - pd.Timestamp(current_time, tz=None)).seconds
print(seconds_passed)
