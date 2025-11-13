import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Stock Analysis Dashboard", page_icon="📈", layout="wide")

st.title("Stock Analysis Dashboard")
st.write("Analyze individual stocks with real-time data and interactive visualizations")

st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Alpha Vantage API Key", type="password", 
                                 help="Get your free API key at https://www.alphavantage.co/support/#api-key")

if not api_key:
    st.warning("Please enter your Alpha Vantage API key in the sidebar to get started.")
    st.info("""
    **Don't have an API key?**
    
    1. Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
    2. Claim your free API key (takes 30 seconds)
    3. Paste it in the sidebar
    
    The free tier allows 25 API requests per day.
    """)
    st.stop()

st.sidebar.header("Stock Selection")
symbol = st.sidebar.text_input("Enter Stock Symbol", "AAPL", help="e.g., AAPL, MSFT, GOOGL, TSLA").upper()

time_period = st.sidebar.selectbox(
    "Select Time Period",
    ["Daily", "Weekly", "Monthly"],
    index=0
)

def get_stock_quote(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if "Global Quote" in data and data["Global Quote"]:
            return data["Global Quote"]
        return None
    except Exception as e:
        st.error(f"Error fetching quote: {e}")
        return None

def get_company_overview(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data and "Symbol" in data:
            return data
        return None
    except Exception as e:
        st.error(f"Error fetching company overview: {e}")
        return None

def get_time_series_data(symbol, api_key, period):
    if period == "Daily":
        function = "TIME_SERIES_DAILY"
        key = "Time Series (Daily)"
    elif period == "Weekly":
        function = "TIME_SERIES_WEEKLY"
        key = "Weekly Time Series"
    else:
        function = "TIME_SERIES_MONTHLY"
        key = "Monthly Time Series"
    
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if key in data:
            return data[key], key
        return None, None
    except Exception as e:
        st.error(f"Error fetching time series: {e}")
        return None, None

if st.sidebar.button("Analyze Stock", type="primary"):
    with st.spinner(f"Fetching data for {symbol}..."):
        quote = get_stock_quote(symbol, api_key)
        
        if quote:
            st.header(f"{symbol} - Current Quote")
            
            col1, col2, col3, col4 = st.columns(4)
            
            price = float(quote.get("05. price", 0))
            change = float(quote.get("09. change", 0))
            change_percent = quote.get("10. change percent", "0%").rstrip('%')
            
            with col1:
                st.metric("Current Price", f"${price:.2f}", f"{change:.2f} ({change_percent}%)")
            
            with col2:
                st.metric("Open", f"${float(quote.get('02. open', 0)):.2f}")
            
            with col3:
                st.metric("High", f"${float(quote.get('03. high', 0)):.2f}")
            
            with col4:
                st.metric("Low", f"${float(quote.get('04. low', 0)):.2f}")
            
            col5, col6, col7 = st.columns(3)
            
            with col5:
                st.metric("Volume", f"{int(quote.get('06. volume', 0)):,}")
            
            with col6:
                st.metric("Previous Close", f"${float(quote.get('08. previous close', 0)):.2f}")
            
            with col7:
                latest_day = quote.get("07. latest trading day", "N/A")
                st.metric("Latest Trading Day", latest_day)
            
            st.divider()
            
            st.header(f"{symbol} - Company Information")
            company = get_company_overview(symbol, api_key)
            
            if company and "Symbol" in company:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Company Overview")
                    st.write(f"**Name:** {company.get('Name', 'N/A')}")
                    st.write(f"**Sector:** {company.get('Sector', 'N/A')}")
                    st.write(f"**Industry:** {company.get('Industry', 'N/A')}")
                    st.write(f"**Exchange:** {company.get('Exchange', 'N/A')}")
                    st.write(f"**Country:** {company.get('Country', 'N/A')}")
                    
                with col2:
                    st.subheader("Key Financials")
                    market_cap = company.get('MarketCapitalization', 'N/A')
                    if market_cap != 'N/A':
                        market_cap = f"${int(market_cap):,}"
                    st.write(f"**Market Cap:** {market_cap}")
                    st.write(f"**P/E Ratio:** {company.get('PERatio', 'N/A')}")
                    st.write(f"**EPS:** {company.get('EPS', 'N/A')}")
                    st.write(f"**52 Week High:** ${company.get('52WeekHigh', 'N/A')}")
                    st.write(f"**52 Week Low:** ${company.get('52WeekLow', 'N/A')}")
                
                if company.get('Description'):
                    st.subheader("About the Company")
                    st.write(company.get('Description'))
            else:
                st.info("Company overview data not available for this symbol.")
            
            st.divider()
            
            st.header(f"{symbol} - {time_period} Price Chart")
            time_series, key = get_time_series_data(symbol, api_key, time_period)
            
            if time_series:
                df = pd.DataFrame.from_dict(time_series, orient='index')
                df.index = pd.to_datetime(df.index)
                df = df.sort_index()
                
                df.columns = [col.split('. ')[1] for col in df.columns]
                df = df.astype(float)
                
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index,
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    name=symbol
                )])
                
                fig.update_layout(
                    title=f"{symbol} {time_period} Stock Price",
                    yaxis_title="Price (USD)",
                    xaxis_title="Date",
                    template="plotly_white",
                    height=500,
                    hovermode='x unified',
                    xaxis_rangeslider_visible=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Trading Volume")
                fig_volume = go.Figure(data=[go.Bar(
                    x=df.index,
                    y=df['volume'],
                    name="Volume",
                    marker_color='lightblue'
                )])
                
                fig_volume.update_layout(
                    title=f"{symbol} Trading Volume",
                    yaxis_title="Volume",
                    xaxis_title="Date",
                    template="plotly_white",
                    height=300
                )
                
                st.plotly_chart(fig_volume, use_container_width=True)
                
                st.subheader("Statistical Summary")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Average Price", f"${df['close'].mean():.2f}")
                    st.metric("Max Price", f"${df['high'].max():.2f}")
                
                with col2:
                    st.metric("Min Price", f"${df['low'].min():.2f}")
                    st.metric("Price Range", f"${df['high'].max() - df['low'].min():.2f}")
                
                with col3:
                    st.metric("Average Volume", f"{int(df['volume'].mean()):,}")
                    price_change = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
                    st.metric("Period Change", f"{price_change:.2f}%")
                
            else:
                st.error(f"Could not fetch time series data for {symbol}. Please check the symbol and try again.")
        
        else:
            st.error(f"Could not find stock data for symbol: {symbol}. Please check the symbol and try again.")
            st.info("Common symbols: AAPL (Apple), MSFT (Microsoft), GOOGL (Google), TSLA (Tesla), AMZN (Amazon)")

with st.expander("How to Use This Dashboard"):
    st.write("""
    1. **Enter API Key**: Paste your Alpha Vantage API key in the sidebar
    2. **Select Stock**: Enter a valid stock ticker symbol (e.g., AAPL for Apple)
    3. **Choose Time Period**: Select the time frame for historical data (Daily, Weekly, or Monthly)
    4. **Click Analyze**: Press the "Analyze Stock" button to fetch and display data
    
    **What You'll See:**
    - Current stock price with daily change
    - Company overview and financial metrics
    - Interactive candlestick chart showing price movements
    - Trading volume chart
    - Statistical summary of the selected period
    """)
