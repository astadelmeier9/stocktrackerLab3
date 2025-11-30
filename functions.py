import streamlit as st
import requests


REQUEST_TIMEOUT = 3  

API_KEYS = st.secrets["API_KEYS"]
current_key_index = 0

def reset_key_index():
    global current_key_index
    current_key_index = 0

def get_current_key():
    return API_KEYS[current_key_index]

def rotate_key():
    global current_key_index
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    return True


def safe_api_call(func, symbol, period=None):
    key = get_current_key()

    try:
        if period:
            data, meta = func(symbol, key, period, timeout=REQUEST_TIMEOUT)
            return data, meta
        else:
            data = func(symbol, key, timeout=REQUEST_TIMEOUT)

          
            if isinstance(data, dict) and "Note" in data:
                if "frequency" in data["Note"] or "rate limit" in data["Note"].lower():
                    rotate_key()
                    return None

            return data

    except requests.exceptions.Timeout:
        return None

    except Exception as e:
        print("API error:", e)
        return None


def get_stock_quote(symbol, api_key, timeout=3):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    try:
        response = requests.get(url, timeout=timeout)
        data = response.json()
        if "Global Quote" in data and data["Global Quote"]:
            return data["Global Quote"]
        return None
    except:
        return None

def get_company_overview(symbol, api_key, timeout=3):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
    try:
        response = requests.get(url, timeout=timeout)
        data = response.json()
        if data and "Symbol" in data:
            return data
        return None
    except:
        return None

def get_time_series_data(symbol, api_key, period, timeout=3):
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
        response = requests.get(url, timeout=timeout)
        data = response.json()
        if key in data:
            return data[key], key
        return None, None
    except:
        return None, None
