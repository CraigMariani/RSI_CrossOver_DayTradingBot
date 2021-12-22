from bs4 import BeautifulSoup
import numpy as np
import requests
import pprint
from tiingo import TiingoClient
import pandas as pd 
import datetime
from secret import Secret
import alpaca_trade_api as tradeapi
from urllib.request import Request, urlopen

class Get_Crypto:

    def __innit__():
        pass
    
    # get price data alpaca
    def price_data_alpaca(tickers):
        # coins = ['BTCUSD', 'BCHUSD', 'ETHUSD', 'LTCUSD']
        # tickers = ['AAPL']
        

        api_key = Secret.paper_api_key
        secret_key = Secret.secret_key
        alp_base_url = 'https://paper-api.alpaca.markets'
        api = tradeapi.REST(api_key, secret_key, alp_base_url, api_version='v2')

        # barset = api.get_barset('AAPL', '15Min', limit=10)
        barset = api.get_barset('ETHUSD', '1D', limit=100)
        # barset
        return barset




    # def penny_stocks(self):
    #     # url = 'https://swing-trading.org/penny-stocks/'
    #     url = 'https://penny-stocks.co/gainers/'

    #     req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #     webpage = urlopen(req).read()
    #     soup = BeautifulSoup(webpage, "html.parser")
    #     table = soup.find('table', attrs = {'class','styled'})


    #     # slicing array starting at 0 ending at the end of the array, go by every 7th step
    #     rows = table.find_all('td')
    #     # tickers = rows[:len(rows):7]
    #     tickers = rows[:len(rows):8]
    #     for i, ticker in enumerate(tickers):
    #         tickers[i] = ticker.get_text()

    #     return tickers
    
    # gets trending ticker labels for crypto
    def trending_crypto():
        # url = 'https://coinmarketcap.com/trending-cryptocurrencies/'
        url = 'https://coinmarketcap.com'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')


        # tickers = soup.find_all('p', class_='sc-1eb5slv-0 gGIpIK coin-item-symbol') # tickers
        tickers = soup.find_all('p', class_='sc-1eb5slv-0 gGIpIK coin-item-symbol')
        # names = soup.find_all('p', class_='sc-1eb5slv-0 iworPT')) # names

        ticker_symbols = np.array([])
        for ticker in tickers:
            ticker_text = ticker.text
            # print(type(ticker_text))
            symbol = ticker_text.split(">")
            ticker_symbols = np.append(ticker_symbols, symbol[0])
        
        return ticker_symbols