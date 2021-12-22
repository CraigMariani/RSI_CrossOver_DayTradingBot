import numpy as np
import pandas as pd

from secret import Secret
from get_data import Get_Crypto
import alpaca_trade_api as tradeapi
import time

class Bot:

    def __init__(self):
        api_key = Secret.paper_api_key
        secret_key = Secret.secret_key
        alp_base_url = 'https://paper-api.alpaca.markets'
        api = tradeapi.REST(api_key, secret_key, alp_base_url, api_version='v2')

        self.api = api

    def main(self):
        tickers = Get_Crypto.trending_crypto()
        # print(tickers)
        # price_data = Get_Crypto.price_data()
        price_data = Get_Crypto.price_data_alpaca(tickers)
        print(price_data)
        
        
    

if __name__ == '__main__':
    bot = Bot()
    bot.main()