import ta
import pandas as pd
import numpy as np

def ensure_series(data, index):
    try:
        if isinstance(data, pd.DataFrame):
            return data.iloc[:, 0]
        elif isinstance(data, np.ndarray) and data.ndim == 2 and data.shape[1] == 1:
            return pd.Series(data[:, 0], index=index)
        elif isinstance(data, pd.Series):
            return data
        return pd.Series(data, index=index)
    except Exception:
        return pd.Series(dtype=float)

def generate_signals(df):
    if df.empty or len(df) < 60:
        return {
            'signal': 'NO DATA',
            'confidence': 0,
            'reasons': ['Onvoldoende data beschikbaar'],
            'entry': None,
            'stoploss': None,
            'takeprofit': None
        }

    df = df.copy()

    df['rsi'] = ensure_series(ta.momentum.RSIIndicator(close=df['Close']).rsi(), df.index)
    df['macd'] = ensure_series(ta.trend.MACD(close=df['Close']).macd_diff(), df.index)
    df['sma_fast'] = ensure_series(ta.trend.sma_indicator(close=df['Close'], window=20), df.index)
    df['sma_slow'] = ensure_series(ta.trend.sma_indicator(close=df['Close'], window=50), df.index)

    last = df.iloc[-1]
    confidence = 0
    reasons = []

    if last['rsi'] < 30:
        signal = 'LONG'
        confidence += 30
        reasons.append("RSI < 30 (oversold)")
    elif last['rsi'] > 70:
        signal = 'SHORT'
        confidence += 30
        reasons.append("RSI > 70 (overbought)")
    else:
        signal = 'HOLD'

    if last['macd'] > 0 and signal == 'LONG':
        confidence += 20
        reasons.append("MACD bullish")
    elif last['macd'] < 0 and signal == 'SHORT':
        confidence += 20
        reasons.append("MACD bearish")

    if last['sma_fast'] > last['sma_slow'] and signal == 'LONG':
        confidence += 20
        reasons.append("SMA 20 > SMA 50")
    elif last['sma_fast'] < last['sma_slow'] and signal == 'SHORT':
        confidence += 20
        reasons.append("SMA 20 < SMA 50")

    price = last['Close']
    if signal == 'LONG':
        sl = price * 0.98
        tp = price * 1.03
    elif signal == 'SHORT':
        sl = price * 1.02
        tp = price * 0.97
    else:
        sl = tp = None

    return {
        'signal': signal,
        'confidence': confidence,
        'reasons': reasons,
        'entry': round(price, 2),
        'stoploss': round(sl, 2) if sl else None,
        'takeprofit': round(tp, 2) if tp else None,
    }
