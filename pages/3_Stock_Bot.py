import streamlit as st
import google.generativeai as genai

from functions import (
    safe_api_call,
    reset_key_index,
    get_stock_quote,
    get_company_overview,
)



genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-2.0-flash")

BOT_AVATAR = "https://i.insider.com/601448566dfbe10018e00c5d?width=700"

st.set_page_config(page_title="Stock Chat Bot", page_icon="🤖", layout="wide")
st.title("🤖📈 Stocky the Stock Chat Bot")



if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi, I’m Stocky! Ask me about any specific stocks!"
    })

for m in st.session_state.messages:
    avatar = BOT_AVATAR if m["role"] == "assistant" else None
    with st.chat_message(m["role"], avatar=avatar):
        st.write(m["content"])



class Stock:
    def __init__(self, symbol, quote_data, company_data):
        self.symbol = symbol
        self.quote_data = quote_data
        self.company_data = company_data

    def summary(self):
        text = f"\n=== {self.symbol} ===\n"

        price_keys = {
            "05. price": "Price",
            "02. open": "Open",
            "03. high": "High",
            "04. low": "Low",
            "10. change percent": "Change %"
        }

        for key, label in price_keys.items():
            if key in self.quote_data:
                text += f"{label}: {self.quote_data[key]}\n"

        text += "\n"

        company_keys = {
            "Name": "Name",
            "Sector": "Sector",
            "Industry": "Industry",
            "MarketCapitalization": "Market Cap",
            "PERatio": "P/E",
            "EPS": "EPS",
            "Beta": "Beta",
        }

        for key, label in company_keys.items():
            if key in self.company_data:
                text += f"{label}: {self.company_data[key]}\n"

        return text


user_text = st.chat_input("Ask about a stock ticker (AAPL, MSFT, TSLA)...")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

 


    extract_prompt = f"""
Given this message: "{user_text}"
Extract stock tickers mentioned by symbol or company name.
Return them in FULL CAPS, separated by commas.
If none found, return "NONE".
"""

    try:
        out = model.generate_content(extract_prompt).text.strip().upper()
        tickers = [] if out == "NONE" else [t.strip() for t in out.split(",")]
    except:
        tickers = []

    if not tickers:
        msg = "Please mention a valid stock ticker so I can look it up."
        st.session_state.messages.append({"role": "assistant", "content": msg})
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            st.write(msg)
        st.stop()


    reset_key_index()
    summaries = ""

    for t in tickers:
        quote = safe_api_call(get_stock_quote, t)
        company = safe_api_call(get_company_overview, t)

 
        if not quote or not company:
            st.error("AlphaVantage API limit reached or all API keys exhausted.")
            st.stop()

        stock = Stock(t, quote, company)
        summaries += stock.summary()

    


    last_msgs = st.session_state.messages[-6:]
    convo = "\n".join(f"{m['role']}: {m['content']}" for m in last_msgs)




    ai_prompt = f"""
You are Stocky, a friendly stock analysis helper.

Conversation so far:
{convo}

Here is the stock information you may use:
{summaries}

Rules:
- Only answer using the data provided.
- If something is missing, say you don't have that information.
- Keep the response clear and simple.
"""

    try:
        ai_response = model.generate_content(
            ai_prompt,
            generation_config={
                "temperature": 0.4,
                "max_output_tokens": 350
            }
        )
        reply = ai_response.text.strip() if ai_response and ai_response.text else "I couldn't generate a response."
    except Exception as e:
        reply = f"Gemini Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        st.write(reply)
