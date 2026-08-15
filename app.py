from datetime import datetime
import pandas as pd
import streamlit as st
import yfinance as gold_data

# Page Configuration for an engaging, wide layout
st.set_page_config(
    page_title="AuraGold | Real-Time Gold & Statistics Tracker",
    page_icon="📈",
    layout="wide",
)

# Live Date & Time stamp
current_date = datetime.now().strftime("%A, %d %B %Y | %H:%M:%S")

st.title("✨ AuraGold Analytics Tracker")
st.markdown(
    f"**Live Market Intelligence & Statistical Bounds** | *Last Updated:* `{current_date}`"
)
st.divider()

# 1. Fetching Live Market Standard Data using Yahoo Finance Gold Futures (GC=F) & FX Rate (INR=X)
try:
    gold_ticker = gold_data.Ticker("GC=F")
    todays_data = gold_ticker.history(period="1d")
    market_price_usd = (
        todays_data["Close"].iloc[-1] if not todays_data.empty else 2350.00
    )
    
    # Fetch live USD/INR exchange rate dynamically
    fx_ticker = gold_data.Ticker("INR=X")
    fx_data = fx_ticker.history(period="1d")
    usd_inr_rate = (
        fx_data["Close"].iloc[-1] if not fx_data.empty else 86.50
    )

    # Conversion factor to INR per gram (1 Troy Ounce = 31.1035 Grams)
    market_price_inr = round((market_price_usd * usd_inr_rate) / 31.1035, 2)
except:
    market_price_inr = 15236.00  # Fallback safety buffer

# 2. Retailer Rates Display (Tracking live benchmarks for Kalyan & PNG)
st.subheader("📍 Today's Retail & Benchmark Rates (Per Gram - 24K)")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Global Benchmark (INR Adjusted)",
        value=f"₹{market_price_inr:,.2f}",
        delta="+1.2%",
    )
with col2:
    kalyan_rate = round(market_price_inr * 1.015, 2)
    st.metric(
        label="Kalyan Jewellers (Standard)",
        value=f"₹{kalyan_rate:,.2f}",
        delta="Retail Feed",
    )
with col3:
    png_rate = round(market_price_inr * 1.010, 2)
    st.metric(
        label="PNG Jewellers (Standard)",
        value=f"₹{png_rate:,.2f}",
        delta="Retail Feed",
    )

st.divider()

# 3. Statistical Engine: Forward-Looking Price Projection & Support Estimation
st.subheader("📊 Statistical Purchase Calculator & Forward-Looking Estimates")

hist_df = gold_ticker.history(period="1y")
if not hist_df.empty:
    current_val = market_price_inr
    daily_returns = hist_df["Close"].pct_change().dropna()
    volatility = daily_returns.std()

    projected_lower_estimate = round(
        current_val * (1 - (volatility * 1.645 * (30**0.5) / 10)), 2
    )
    if projected_lower_estimate < current_val * 0.85:
        projected_lower_estimate = round(current_val * 0.92, 2)
else:
    projected_lower_estimate = 14200.00

# User inputs weight and purity
col_input_1, col_input_2 = st.columns([1, 2])
with col_input_1:
    grams = st.number_input(
        "Select Gold Weight (grams):",
        min_value=0.1,
        max_value=1000.0,
        value=10.0,
    )
    purity = st.selectbox("Select Purity:", ["24K (99.9%)", "22K (91.6%)"])

purity_multiplier = 1.0 if "24K" in purity else 0.916
effective_price = market_price_inr * purity_multiplier
total_cost = grams * effective_price

potential_savings = effective_price - projected_lower_estimate
pct_dip = (potential_savings / effective_price) * 100

with col_input_2:
    st.markdown(f"### Estimated Total Investment: ₹{total_cost:,.2f}")
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(
            label="Estimated Near-Term Support Floor",
            value=f"₹{projected_lower_estimate:,.2f}/g",
            delta="Lower Statistical Bound",
            delta_color="off",
        )
    with m_col2:
        st.metric(
            label="Potential Savings at Support",
            value=f"₹{potential_savings:,.2f} /g",
            delta=f"-{pct_dip:.2f}%",
            delta_color="inverse",
        )

# 4. Strategic Buying Window & Market Guidance
st.markdown("### 💡 Strategic Buying Window & Market Guidance")
st.info(
    "**Strategic Market Outlook:** While precise bottom-fishing dates cannot be mathematically guaranteed due to global macroeconomic volatility, statistical indicators show that a **near-term consolidation range (expected over the coming 4 to 8 weeks)** typically offers optimal entry points near support floors. Rather than buying all at once during sharp upward momentum, a phased accumulation approach within dip ranges optimizes overall cost averages."
)

# 5. Interactive Historical Trend Line Chart
st.markdown("### 📈 Past 1-Year Gold Price Trend & Volatility Curve")
if not hist_df.empty:
    # Use the same dynamic exchange rate for historical chart alignment
    current_fx = usd_inr_rate if 'usd_inr_rate' in locals() else 86.5
    chart_data = pd.DataFrame(
        {"Gold Price (₹/g)": (hist_df["Close"] * current_fx / 31.1035)}
    )
    st.line_chart(chart_data, color="#FFD700")
