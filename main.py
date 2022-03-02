
# from alpaca_trade_api.rest import TimeFrame
import time
import numpy as np
import pandas as pd

from secret import Secret
# from get_data import Get_Data
import alpaca_trade_api as tradeapi
import datetime as dt

class Bot:

    def __init__(self):
        api_key = Secret.paper_api_key
        secret_key = Secret.paper_secret_key
        alp_base_url = 'https://paper-api.alpaca.markets'
        api = tradeapi.REST(api_key, secret_key, alp_base_url, api_version='v2')
        
        self.data_url = 'https://data.alpaca.markets/v1beta1/crypto'
        self.header = { 
                        'APCA-API-KEY-ID' : Secret.paper_api_key,
                        'APCA-API-SECRET-KEY' : Secret.paper_secret_key}

        self.api_key = api_key
        self.secret_key = secret_key
        self.api = api

    # calculate ema crossovers    
    def calculate_cross_over(self, df):
        df['9_EMA'] = df['close'].ewm(span=9).mean()
        df['21_EMA'] = df['close'].ewm(span=21).mean()
        df['golden_cross'] = np.where(df['9_EMA'] > df['21_EMA'], 1, 0)
        df['death_cross'] = np.where(df['21_EMA'] > df['9_EMA'], 1, 0) 

        return df

    def calculate_rsi(self, df):
        n = 14 # period or number of look back days when calculating

        close = df['close'] # current days closing price
        close_past = df['close'].shift(1) # previous days closing price
        close_delta = close - close_past # change in closing price
        delta_sign = np.sign(close_delta) # positive or negative if above or below 0, this will determine if the price went up or down

        df['up_moves'] = np.where(delta_sign > 0, close_delta, 0) # shows up trend
        df['down_moves'] = np.where(delta_sign < 0, close_delta.abs(), 0) # shows down trend
        avg_d = df['down_moves'].rolling(n).mean() # calculate moving average up moves over 14 days
        avg_u = df['up_moves'].rolling(n).mean() # calculate moving average down moves over 14 days

        rs = avg_u / avg_d # calculate relative strength
        rsi = 100 - 100 / (1 + rs) # calculate relative strength index
        df['rsi'] = rsi 
        df.dropna(inplace=True)

        # upper and lower bounds of the rsi trading signal
        upper_bound = 50
        lower_bound = 25

        # # calculate buy and sell signals depending on the upper and lower bounds
        df['upper_bound'] = np.where(df['rsi'] >=  upper_bound, 1, 0)
        df['lower_bound'] = np.where(df['rsi'] <= lower_bound, 1, 0)

        return df

    # gets bar data for crypto ticker, timezone is UTC (universal time)
    def price_data(self, tickers):
        for ticker in tickers:
            now = dt.datetime.today()
            now = now.strftime("%Y-%m-%d")
            data = self.api.get_crypto_bars(ticker, tradeapi.rest.TimeFrame.Minute, now, now).df
            # print(data.head())
            try:
                data = data[data['exchange'] == 'CBSE']
            except Exception as e:
                print(e)
            data = Bot.calculate_cross_over(self, data)
            data = Bot.calculate_rsi(self, data)
            
            data['buy'] = np.where((data['upper_bound'] == 1) & (data['golden_cross'] == 1), 1, 0)
            # data['sell'] = np.where((data['lower_bound'] == 1) & (data['death_cross'] == 1), 1, 0)

            data.to_csv('data/{}.csv'.format(ticker))
    
    def execute_trade(self, df, ticker):

        api = self.api
        current = df.iloc[len(df.index) - 2]

        
        try:
            if current['buy'] == 1: # using the most recent buy signal
                
                    print('buy: {}'.format(ticker))
                    api.submit_order(symbol=ticker, 
                                    side='buy',
                                    type='market', 
                                    # qty=1, # for buying a part of a BTC

                                    # every order should be 5%-10% of your total portfolio
                                    notional=50, # for buying a fixed USD price amount of BTC 
                                    
                                    # stop_loss={'stop_price' : current['close'] - (current['close'] * .3)} # price drops below 30 percent of current closing price = exit position
                                    
                                    stop_loss={'stop_price' : current['close'] - (current['close'] * .01)}, # stoploss at 1 percent current closing price
                                    take_profit={'limit_price': current['close'] + (current['close'] * .02)} # take profit at 2 percent over the current closing price
                                    ) 

        except Exception as e:
            print('Failed to buy {}'.format(ticker))
            print(e)


    def main(self):
        tickers = ['BTCUSD','ETHUSD','LTCUSD','BCHUSD']
        # Get_Data.price_data(tickers)
        Bot.price_data(self, tickers)
        # Bot.trades_data(self, tickers)

        for ticker in tickers:
        # ticker = 'BTCUSD'
            df = pd.read_csv('data/{}.csv'.format(ticker))
            Bot.execute_trade(self, df, ticker)


    
 
if __name__ == '__main__':
    while True:
        
        bot = Bot()
        bot.main()
        time.sleep(60)

