import streamlit as st

st.title("Web Development Lab03 - Stock Research Platform")

st.header("CS 1301")
st.subheader("Team 82, Web Development - Section A")
st.subheader("Adam Stadelmeier, Arik Herzog")

st.write("""
Welcome to our Stock Research Platform! This comprehensive web application leverages the Alpha Vantage API to provide real-time stock market data and analysis. You can navigate between the pages using the sidebar to the left. The following pages are:

1. **Home Page**: Overview of the application and navigation guide
2. **Stock Analysis Dashboard**: Interactive tool for analyzing individual stocks with real-time data, company information, and dynamic candlestick charts

---

### About This Application

Our Stock Research Platform is designed to help investors make informed decisions by providing:
- Real-time stock quotes and historical data
- Company fundamental information
- Interactive candlestick charts and volume analysis
- Statistical summaries and performance metrics

### Data Source

All stock data is powered by the **Alpha Vantage API**, a leading provider of free APIs for realtime and historical financial data.

### Getting Started

1. Navigate to the **Stock Analysis Dashboard** using the sidebar
2. Enter your Alpha Vantage API key (get one free at https://www.alphavantage.co/support/#api-key)
3. Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
4. Select your preferred time period
5. Click "Analyze Stock" to view comprehensive data and charts

---

*Note: This application uses the free Alpha Vantage API which has a rate limit of 25 requests per day for demo API keys.*

""")

st.info("Tip: Start by visiting the Stock Analysis Dashboard to explore real-time stock data!")
