from secret import Secret
from tiingo import TiingoClient
import pandas as pd 
client = TiingoClient(Secret.config)
import datetime

end_test = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

symbols = ['ETHUSD']

for symbol in symbols:
    # prices = client.get_ticker_price(
    #                                 symbol,
    #                                 fmt='json',
    #                                 frequency='1HOUR',
    #                                 startDate=end_test,
    #                                 endDate=end_test
    #                                 )
    prices = client.get_crypto_ticker_price(
                                    symbol,
                                    fmt='json',
                                    frequency='1HOUR',
                                    startDate=end_test,
                                    endDate=end_test
                                    )
    
    price_sheet = pd.DataFrame.from_dict(prices)
    price_sheet['date'] = price_sheet['date'].str.rstrip('T00:00:00.000Z')
    # print(price_sheet.head())
    price_sheet.to_csv('data/{}.csv'.format(symbol))
