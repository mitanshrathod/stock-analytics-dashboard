import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from sklearn.linear_model import LinearRegression # type: ignore
from Api import GetData  # Custom API to fetch data

# List of available companies
companies = [
    "AAPL",  # Apple
    "TSLA",  # Tesla
    "IBM",   # IBM
    "GOOGL", # Alphabet (Google)
    "MSFT",  # Microsoft
    "AMZN",  # Amazon
    "META",  # Meta (Facebook)
    "NFLX",  # Netflix
    "NVDA",  # NVIDIA
    "ADBE"   # Adobe
]

# Sidebar: Company selection and fetch button
st.sidebar.header("Select Company:")
selected_company = st.sidebar.selectbox("Choose a company", companies)

if st.sidebar.button("Fetch and Store Data"):
    GetData(selected_company)  # Fetch only selected company
    st.success(f"Data for {selected_company} fetched successfully!")

# App Title
st.title(f"📈 Forex Stock Analytics - {selected_company}")

# Read CSV data for selected company
data_folder = "./Data"
df = None

for file_name in os.listdir(data_folder):
    if file_name.startswith(selected_company):
        file_path = os.path.join(data_folder, file_name)
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        st.dataframe(df)
        break

if df is not None:
    # ---------------- Candlestick Chart ----------------
    fig = go.Figure(data=[
        go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close']
        )
    ])
    fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig, use_container_width=True)
    
    #---------------Making future predictions--------------------
    st.header("Stock Market Metrics Future Prediction :")
    model = LinearRegression()
    X = df[['open','high','low','volume']].values
    y = df['close']

    model.fit(X,y)

    # -----------------Taking User Input :------------
    open = st.number_input("Open",min_value=0)
    high = st.number_input("High",min_value=0)
    low = st.number_input("Low",min_value=0)
    volume = st.number_input("Volume",min_value=0)

    p = model.predict([[open,high,low,volume]])
    st.write(f"Predicted Close Price : ${p[0]:.2f}")

    # ---------------- Technical Indicators ----------------
    # Adding 5 Stock Market Calculations
    st.header("Key Stock Market Metrics")

    # Moving Averages
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()

    # RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Bollinger Bands
    df['STD_20'] = df['close'].rolling(window=20).std()
    df['Upper_Band'] = df['SMA_20'] + (2 * df['STD_20'])
    df['Lower_Band'] = df['SMA_20'] - (2 * df['STD_20'])

    # MACD
    df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']

    # ATR
    df['High-Low'] = df['high'] - df['low']
    df['High-PrevClose'] = abs(df['high'] - df['close'].shift(1))
    df['Low-PrevClose'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=14).mean()

    # ---------------- Display Metrics ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Moving Averages")
        st.write(f"20-Day SMA: ${df['SMA_20'].iloc[-1]:.2f}")
        st.write(f"50-Day SMA: ${df['SMA_50'].iloc[-1]:.2f}")
        st.write(f"Current Price: ${df['close'].iloc[-1]:.2f}")
        st.write(f"Price / 50-Day SMA Ratio: {(df['close'].iloc[-1] / df['SMA_50'].iloc[-1]):.2f}")

    with col2:
        st.subheader("RSI (14)")
        rsi_value = df['RSI'].iloc[-1]
        st.write(f"RSI Value: {rsi_value:.2f}")
        if rsi_value < 30:
            st.write("Status: 🔻 Potentially Oversold")
        elif rsi_value > 70:
            st.write("Status: 🔺 Potentially Overbought")
        else:
            st.write("Status: ⚖️ Neutral")

    st.subheader("Bollinger Bands")
    st.write(f"Upper Band: ${df['Upper_Band'].iloc[-1]:.2f}")
    st.write(f"Middle Band (20-SMA): ${df['SMA_20'].iloc[-1]:.2f}")
    st.write(f"Lower Band: ${df['Lower_Band'].iloc[-1]:.2f}")

    st.subheader("MACD")
    st.write(f"MACD Line: {df['MACD'].iloc[-1]:.4f}")
    st.write(f"Signal Line: {df['MACD_Signal'].iloc[-1]:.4f}")
    st.write(f"Histogram: {df['MACD_Histogram'].iloc[-1]:.4f}")

    st.subheader("Volatility (ATR-14)")
    st.write(f"ATR Value: ${df['ATR'].iloc[-1]:.2f}")
    st.write(f"ATR as % of Price: {(df['ATR'].iloc[-1] / df['close'].iloc[-1] * 100):.2f}%")

    # ---------------- Moving Average Chart ----------------
    st.header("Technical Analysis Visualization")

    fig_ma = go.Figure()
    fig_ma.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], name='Price', line=dict(color='green')))
    fig_ma.add_trace(go.Scatter(x=df['timestamp'], y=df['SMA_20'], name='20-Day SMA', line=dict(color='blue')))
    fig_ma.add_trace(go.Scatter(x=df['timestamp'], y=df['SMA_50'], name='50-Day SMA', line=dict(color='red')))
    fig_ma.update_layout(title='Price vs Moving Averages', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig_ma, use_container_width=True)

    # ---------------- Price Change ----------------
    if len(df) >= 2:
        recent_change = ((df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2]) * 100
        if recent_change > 0:
            st.success(f"📈 Recent Change: +{recent_change:.2f}%")
        else:
            st.error(f"📉 Recent Change: {recent_change:.2f}%")
    else:
        st.info("Not enough data to calculate recent change.")

    # ---------------- Trend Analysis ----------------
    st.subheader("Trend Analysis")
    short_term = "Bullish" if df['close'].iloc[-1] > df['SMA_20'].iloc[-1] else "Bearish"
    long_term = "Bullish" if df['close'].iloc[-1] > df['SMA_50'].iloc[-1] else "Bearish"

    st.write(f"Short-term trend (vs 20-Day SMA): **{short_term}**")
    st.write(f"Long-term trend (vs 50-Day SMA): **{long_term}**")

else:
    st.warning(f"No data available for {selected_company}. Please fetch the data using the sidebar.")



