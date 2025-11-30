import streamlit as st

st.title("Web Development Lab03 - Stock Research Platform")

st.header("CS 1301")
st.subheader("Team 82, Web Development - Section A")
st.subheader("Adam Stadelmeier, Arik Herzog")

st.write("""
Welcome to our Stock Research Platform! This comprehensive web application leverages the Alpha Vantage API to provide real-time stock market data and analysis. You can navigate between the pages using the sidebar to the left. The following pages are:

1. **Home Page**: Overview of the application and navigation guide
2. **Stock Analysis Dashboard**: Interactive tool for analyzing individual stocks with real-time data, company information, and dynamic candlestick charts
3. **AI Stock Analyst**: AI Guided comparison tool that evaluates two stocks side-by-side and provides personalized investment recommendations based on your risk profile.
4. **Stock Chat Bot**: Interactive chat interface that answers questions about specific stocks using real-time market data and company fundamentals.
---

### About This Application

Our Stock Research Platform is designed to help investors make informed decisions by providing:
- Real-time stock quotes and historical data
- Company fundamental information
- Interactive candlestick charts and volume analysis
- Statistical summaries and performance metrics

### Data Source

All stock data is powered by the **Alpha Vantage API**, a leading provider of free APIs for realtime and historical financial data.
""")
