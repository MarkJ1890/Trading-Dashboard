import streamlit as st
from data import get_data
from strategies import generate_signals
import plotly.graph_objs as go

st.set_page_config(page_title="TradingBot Dashboard", layout="wide")
st.title("📈 TradingBot Signalen Dashboard")

tickers = {
    "EUR/USD": "EURUSD=X",
    "Goud": "GC=F",  # Vervangen symbool werkt op Yahoo Finance
    "US500": "^GSPC",
    "US100": "^IXIC"
}

ticker_label = st.selectbox("Kies een ticker", list(tickers.keys()))
ticker = tickers[ticker_label]

data = get_data(ticker)
signal_info = generate_signals(data)

st.subheader(f"📊 Analyse voor {ticker_label}")
st.write(f"**Signaal**: `{signal_info['signal']}`")
st.write(f"**Confidence**: {signal_info['confidence']}%")
st.write("**Redenen**:")
for reason in signal_info["reasons"]:
    st.markdown(f"- {reason}")

st.write(f"**Entry**: {signal_info['entry']}")
st.write(f"**Stoploss**: {signal_info['stoploss']}")
st.write(f"**Take Profit**: {signal_info['takeprofit']}")

if not data.empty:
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candles'
    ))
    fig.update_layout(title="Prijsactie", height=500)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("📉 Geen geldige data beschikbaar voor deze ticker.")
