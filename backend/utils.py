from flask import jsonify, current_app
from datetime import datetime, timedelta
import jwt
import os
from alpaca.data import StockHistoricalDataClient
from alpaca.data import StockBarsRequest, TimeFrame
from alpaca.data.requests import StockLatestQuoteRequest
from datetime import datetime
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv

def generic_error_response(e):
    return jsonify({'error': f"An error occurred: {str(e)}"}), 500  


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
url = os.getenv('ALPACA_URL')

def get_assets():
    api = tradeapi.REST(api_key, secret_key, base_url=url)
    assets = api.list_assets()
    tradable_assets = [asset for asset in assets if asset.tradable]
    print("Scrape successful")
    return tradable_assets

def get_stock_data(symbol):
    client = StockHistoricalDataClient(api_key, secret_key)
    request_params = StockLatestQuoteRequest(symbol_or_symbols=symbol)
    quote = client.get_stock_latest_quote(request_params)[symbol]
    print(quote.timestamp)
    return {
        "symbol": symbol,
        "price": quote.ask_price,
        "timestamp": quote.timestamp.isoformat()
    }

def create_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.now() + timedelta(hours=1)
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
    return token  