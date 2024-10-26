from alpaca.data import StockHistoricalDataClient
from alpaca.data import StockBarsRequest, TimeFrame
from datetime import datetime
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
import os
''' NOT WORRIED ABOUT HISTORICAL DATA FOR NOW

client = StockHistoricalDataClient(api_key, secret_key)

request_params = StockBarsRequest(
                        symbol_or_symbols=["NVDA", "AAPL"],
                        timeframe=TimeFrame.Day,
                        start=datetime(2022, 7, 1),
                        end=datetime(2024, 9, 1)
                 )

bars = client.get_stock_bars(request_params)

print(bars.df)
import matplotlib.pyplot as plt

# Copy the DataFrame from bars.df to a new variable so we can modify it
df = bars.df.copy()

# Reset the index if 'symbol' is part of the index
if 'symbol' not in df.columns:
    df = df.reset_index()

# Now plot the data
for symbol in df['symbol'].unique():
    symbol_data = df[df['symbol'] == symbol]
    plt.plot(symbol_data['timestamp'], symbol_data['close'], label=symbol)

plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Stock Prices')
plt.legend()
plt.show()
'''

load_dotenv()
api_key = os.getenv('ALPACA_KEY')
secret_key = os.getenv('ALPACA_SECRET_KEY')

def get_assets():
    api = tradeapi.REST(api_key, secret_key, base_url='https://paper-api.alpaca.markets')
    assets = api.list_assets()
    tradable_assets = [asset for asset in assets if asset.tradable]
    print("Scrape successful")
    return tradable_assets