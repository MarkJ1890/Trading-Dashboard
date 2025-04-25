import yfinance as yf
import pandas as pd

def get_data(ticker: str, period='60d', interval='1h'):
    try:
        data = yf.download(ticker, period=period, interval=interval)
        if data.empty or len(data.columns) < 4:
            raise ValueError("Geen geldige data gevonden.")
        return data
    except Exception as e:
        print(f"Fout bij ophalen van data voor {ticker}: {e}")
        return pd.DataFrame()
