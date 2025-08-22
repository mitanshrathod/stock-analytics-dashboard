# 📊 Forex Stock Analytics Dashboard

A **Streamlit-based Stock Analytics Dashboard** that fetches real-time intraday stock market data using the **Alpha Vantage API**, stores it as CSV, and provides **technical analysis, visualizations, and insights** for major companies like Apple, Tesla, Google, Microsoft, and more.  

---

## 🚀 Features  

- 🔄 Fetches live intraday stock data (5-minute interval) using Alpha Vantage API  
- 💾 Stores data locally as CSV for future use  
- 📉 Interactive **Candlestick Chart** for price visualization  
- 📊 Key **Technical Indicators**:  
  - 20-day & 50-day Simple Moving Averages (SMA)  
  - Relative Strength Index (RSI - 14)  
  - Bollinger Bands  
  - Moving Average Convergence Divergence (MACD)  
  - Average True Range (ATR - 14)  
- 📌 Trend analysis (Bullish / Bearish signals)  
- 📈 Recent price change detection  
- 🎨 Visual comparison of price vs moving averages  

---

## 🛠️ Installation & Setup  

1. Clone the repository  
   ```bash
   git clone https://github.com/mitanshrathod/stock-analytics-dashboard.git
   cd stock-analytics-dashboard
   ```

2. Install required dependencies  
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard  
   ```bash
   streamlit run Dashboard.py
   ```

4. Use the sidebar to **fetch stock data** and start analyzing 📈  

---

## 📂 Project Structure  

```
├── Api.py           # Fetches stock data from Alpha Vantage and saves as CSV
├── Dashboard.py     # Streamlit app for visualization & analytics
├── Data/            # Folder where stock data CSVs are stored
└── requirements.txt # Project dependencies
```

---

## ⚡ Tech Stack  

- **Python** (Pandas, Requests, OS)  
- **Streamlit** (Dashboard UI)  
- **Plotly** (Interactive charts)  
- **Alpha Vantage API** (Stock Market Data)  

---

## 📌 Future Improvements  

- Multi-stock comparison on a single chart  
- Enhanced machine learning prediction models  
- Deployment to **Streamlit Cloud** or **Heroku**  
- More indicators (e.g., EMA, Stochastic Oscillator)  

---

## 👨‍💻 Author  

**Mitansh Rathod**  
📧 mitanshrathod1491@gmail.com  
🔗 www.linkedin.com/in/mitansh-rathod  
