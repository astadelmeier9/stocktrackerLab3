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




class Stock:
    def __init__(self, symbol, quote_data, company_data):
        self.symbol = symbol
        self.quote_data = quote_data
        self.company_data = company_data
        self.domain = (
            company_data.get("OfficialSite", "")
            .replace("https://", "")
            .replace("http://", "")
            .replace("www.", "")
            .split("/")[0]
        )

    def summary(self):
        price_keys = {
            "05. price": "Price",
            "02. open": "Open",
            "03. high": "High",
            "04. low": "Low",
            "10. change percent": "Change %"
        }

        company_keys = {
            "Name": "Name",
            "Sector": "Sector",
            "Industry": "Industry",
            "MarketCapitalization": "Market Cap",
            "PERatio": "P/E",
            "ForwardPE": "Forward P/E",
            "EPS": "EPS",
            "Beta": "Beta",
            "DividendYield": "Dividend Yield",
            "52WeekHigh": "52W High",
            "52WeekLow": "52W Low",
            "QuarterlyRevenueGrowthYOY": "Revenue Growth YoY",
            "QuarterlyEarningsGrowthYOY": "Earnings Growth YoY"
        }

        summary_text = f"{self.symbol} Summary:\n"

        for key, label in price_keys.items():
            if key in self.quote_data:
                summary_text += f"{label}: {self.quote_data[key]}\n"

        summary_text += "\n"

        for key, label in company_keys.items():
            if key in self.company_data:
                summary_text += f"{label}: {self.company_data[key]}\n"

        return summary_text


st.set_page_config(page_title="AI Stock Analyst", page_icon="💼", layout="wide")

st.title("AI Stock Analyst")
st.write("Enter two stocks for comparison and specify your risk profile to receive tailored investment guidance.")

st.image(
    "https://wrightcl.wordpress.com/wp-content/uploads/2014/01/the-wolf-of-wall-street-movie-wallpaper-14.jpg",
    use_container_width=True
)

symbol_1 = st.text_input("Enter first stock:").upper()
symbol_2 = st.text_input("Enter second stock:").upper()
risk_level = st.selectbox("Select Risk Level", ["low", "medium", "high"], index=0)




if st.button("Generate"):

    if not symbol_1 or not symbol_2:
        st.error("Please enter both stock symbols.")
        st.stop()

    with st.spinner("Generating comparison..."):

        reset_key_index()

        s1 = safe_api_call(get_stock_quote, symbol_1)
        c1 = safe_api_call(get_company_overview, symbol_1)

        s2 = safe_api_call(get_stock_quote, symbol_2)
        c2 = safe_api_call(get_company_overview, symbol_2)

        if not s1 or not s2 or not c1 or not c2:
            st.error("All API keys exhausted or rate limited.")
            st.stop()

        stock1 = Stock(symbol_1, s1, c1)
        stock2 = Stock(symbol_2, s2, c2)

        if not stock1.domain or not stock2.domain:
            st.warning("Could not resolve company domains. Skipping logos.")

        logo1 = f"https://img.logo.dev/{stock1.domain}?token=pk_BsPpN1xgTzaMCbPETQNDRg"
        logo2 = f"https://img.logo.dev/{stock2.domain}?token=pk_BsPpN1xgTzaMCbPETQNDRg"
        vs_image = "https://upload.wikimedia.org/wikipedia/commons/7/70/Street_Fighter_VS_logo.png"

        col1, col2, col3 = st.columns(3)

        with col1:
            if stock1.domain:
                st.image(logo1, width=220)

        with col2:
            st.image(vs_image, width=240)

        with col3:
            if stock2.domain:
                st.image(logo2, width=220)

        summary1 = stock1.summary()
        summary2 = stock2.summary()

        prompt = f"""
You are a helpful stock assistant.

Compare these two stocks for someone with {risk_level} risk tolerance.

Focus on:
- Differences in business type
- Growth vs stability
- Risk vs reward


{summary1}
{summary2}
"""

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.4,
                "max_output_tokens": 2000
            }
        )

        st.subheader("AI Stock Comparison")

        if response and hasattr(response, "text") and response.text:
            st.write(response.text)
        else:
            st.warning("AI returned no valid text.")
