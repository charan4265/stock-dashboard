import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from stock_data import get_stock_info, get_historical_data, get_moving_averages
from news_sentiment import get_news_with_sentiment
from signals import generate_signal, get_price_change_summary

st.set_page_config(
    page_title="Stock Intelligence Dashboard",
    page_icon="📈",
    layout="wide"
)

POPULAR_STOCKS = {
    "TCS (India)":       "TCS.NS",
    "Infosys (India)":   "INFY.NS",
    "Reliance (India)":  "RELIANCE.NS",
    "Wipro (India)":     "WIPRO.NS",
    "HDFC Bank (India)": "HDFCBANK.NS",
    "Apple (USA)":       "AAPL",
    "Tesla (USA)":       "TSLA",
    "Microsoft (USA)":   "MSFT",
    "Google (USA)":      "GOOGL",
    "Amazon (USA)":      "AMZN",
}

st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d0d 0%, #1a1a00 50%, #0d2d00 100%);
}
section[data-testid="stSidebar"] * { color: #39d353 !important; }
section[data-testid="stSidebar"] input { color: white !important; }
.metric-card {
    background: linear-gradient(135deg, #0d0d0d, #1a1a00);
    border: 1px solid #39d353;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    color: white;
}
.metric-val  { font-size: 1.6rem; font-weight: bold; color: #39d353; }
.metric-lbl  { font-size: 0.85rem; color: #aaa; margin-top: 4px; }
.signal-box  {
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    color: white;
    font-size: 1.1rem;
    font-weight: bold;
    margin: 10px 0;
}
.news-card {
    background: var(--color-background-secondary);
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 10px;
    border-left: 4px solid;
}
.pos { border-color: #39d353; }
.neg { border-color: #e94560; }
.neu { border-color: #f0b429; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 📈 Stock Intelligence")
    st.markdown("---")
    page = st.radio("Navigate", [
        "📊 Stock Overview",
        "🕯️ Price Charts",
        "📰 News & Sentiment",
        "🤖 Buy / Sell Signal",
        "🔄 Compare Stocks",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### 🔍 Select Stock")
    stock_choice = st.selectbox("Popular Stocks", list(POPULAR_STOCKS.keys()))
    custom = st.text_input("Or type ticker (e.g. ZOMATO.NS)")
    ticker = custom.upper() if custom else POPULAR_STOCKS[stock_choice]
    period = st.selectbox("Time Period", ["1mo","3mo","6mo","1y","2y"], index=2)
    st.markdown("---")
    st.caption("Data: Yahoo Finance + NewsAPI")
    st.caption("Not financial advice.")

@st.cache_data(ttl=300)
def load_data(ticker, period):
    info = get_stock_info(ticker)
    df   = get_historical_data(ticker, period)
    df   = get_moving_averages(df)
    return info, df

info, df = load_data(ticker, period)
changes  = get_price_change_summary(df)

if page == "📊 Stock Overview":
    st.title(f"📊 {info['name']}")
    st.markdown(f"*Ticker: `{ticker}` | Sector: {info['sector']} | Country: {info['country']}*")
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    chg_color = "#39d353" if info['change'] >= 0 else "#e94560"
    chg_arrow = "▲" if info['change'] >= 0 else "▼"
    c1.markdown(f'<div class="metric-card"><div class="metric-val">₹{info["price"]}</div><div class="metric-lbl">Current Price</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><div class="metric-val" style="color:{chg_color}">{chg_arrow} {round(info["change"],2)}%</div><div class="metric-lbl">Day Change</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><div class="metric-val">₹{info["52w_high"]}</div><div class="metric-lbl">52W High</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card"><div class="metric-val">₹{info["52w_low"]}</div><div class="metric-lbl">52W Low</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c5,c6,c7,c8 = st.columns(4)
    mcap = f"₹{round(info['market_cap']/1e9,1)}B" if info['market_cap'] else "N/A"
    c5.markdown(f'<div class="metric-card"><div class="metric-val">{mcap}</div><div class="metric-lbl">Market Cap</div></div>', unsafe_allow_html=True)
    c6.markdown(f'<div class="metric-card"><div class="metric-val">{round(info["pe_ratio"],1) if info["pe_ratio"] else "N/A"}</div><div class="metric-lbl">P/E Ratio</div></div>', unsafe_allow_html=True)
    c7.markdown(f'<div class="metric-card"><div class="metric-val">{changes.get("1D","N/A")}%</div><div class="metric-lbl">1 Day Return</div></div>', unsafe_allow_html=True)
    c8.markdown(f'<div class="metric-card"><div class="metric-val">{changes.get("1M","N/A")}%</div><div class="metric-lbl">1 Month Return</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 About the Company")
    st.info(info["summary"][:600] + "..." if len(info["summary"]) > 600 else info["summary"])

    st.markdown("### 📈 Price Returns Summary")
    ret_df = pd.DataFrame({"Period": list(changes.keys()), "Return (%)": list(changes.values())})
    colors = ["#39d353" if v >= 0 else "#e94560" for v in ret_df["Return (%)"]]
    fig = go.Figure(go.Bar(x=ret_df["Period"], y=ret_df["Return (%)"],
                           marker_color=colors, text=ret_df["Return (%)"],
                           textposition="outside"))
    fig.update_layout(plot_bgcolor="#0d0d0d", paper_bgcolor="#0d0d0d",
                      font_color="white", height=300)
    st.plotly_chart(fig, use_container_width=True)

elif page == "🕯️ Price Charts":
    st.title(f"🕯️ Price Charts — {info['name']}")

    st.markdown("### Candlestick Chart")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df["Date"], open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"], name="Price",
        increasing_line_color="#39d353", decreasing_line_color="#e94560"
    ))
    if "MA20" in df.columns:
        fig.add_trace(go.Scatter(x=df["Date"], y=df["MA20"],
                                  name="MA20", line=dict(color="#f0b429", width=1.5)))
    if "MA50" in df.columns:
        fig.add_trace(go.Scatter(x=df["Date"], y=df["MA50"],
                                  name="MA50", line=dict(color="#60a5fa", width=1.5)))
    fig.update_layout(
        plot_bgcolor="#0d0d0d", paper_bgcolor="#0d0d0d",
        font_color="white", xaxis_rangeslider_visible=False,
        height=500, legend=dict(bgcolor="#0d0d0d")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Volume Chart")
    vol_colors = ["#39d353" if df["Close"].iloc[i] >= df["Open"].iloc[i]
                  else "#e94560" for i in range(len(df))]
    fig2 = go.Figure(go.Bar(x=df["Date"], y=df["Volume"],
                             marker_color=vol_colors, name="Volume"))
    fig2.update_layout(plot_bgcolor="#0d0d0d", paper_bgcolor="#0d0d0d",
                       font_color="white", height=250)
    st.plotly_chart(fig2, use_container_width=True)

elif page == "📰 News & Sentiment":
    st.title(f"📰 News & Sentiment — {info['name']}")
    company_name = info["name"].split()[0]

    with st.spinner("Fetching latest news..."):
        news = get_news_with_sentiment(company_name, num_articles=10)

    if not news:
        st.warning("No news found. Check your NewsAPI key in the .env file.")
    else:
        pos = sum(1 for n in news if n["sentiment"] == "Positive")
        neg = sum(1 for n in news if n["sentiment"] == "Negative")
        neu = sum(1 for n in news if n["sentiment"] == "Neutral")
        avg = round(sum(n["score"] for n in news) / len(news), 3)

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Positive News", f"🟢 {pos}")
        c2.metric("Negative News", f"🔴 {neg}")
        c3.metric("Neutral News",  f"🟡 {neu}")
        c4.metric("Avg Sentiment", avg)

        st.markdown("---")
        sent_df = pd.DataFrame({"Sentiment": ["Positive","Negative","Neutral"],
                                 "Count": [pos, neg, neu]})
        fig = px.pie(sent_df, names="Sentiment", values="Count",
                     color="Sentiment",
                     color_discrete_map={"Positive":"#39d353","Negative":"#e94560","Neutral":"#f0b429"})
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white", height=300)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Latest News Articles")
        for n in news:
            css = "pos" if n["sentiment"]=="Positive" else ("neg" if n["sentiment"]=="Negative" else "neu")
            st.markdown(f"""
            <div class="news-card {css}">
                <div style="font-weight:bold;font-size:14px">{n['emoji']} {n['title']}</div>
                <div style="font-size:12px;color:var(--color-text-secondary);margin-top:5px">
                    {n['source']} · {n['published']} · Sentiment: {n['sentiment']} ({n['score']})
                </div>
                <div style="font-size:12px;margin-top:6px">{n['description'][:150] if n['description'] else ''}...</div>
                <a href="{n['url']}" target="_blank" style="font-size:12px;color:#60a5fa">Read full article →</a>
            </div>
            """, unsafe_allow_html=True)

elif page == "🤖 Buy / Sell Signal":
    st.title(f"🤖 AI Signal — {info['name']}")
    st.markdown("*Signal based on Moving Averages + Price Trend + News Sentiment*")

    company_name = info["name"].split()[0]
    with st.spinner("Analysing news sentiment..."):
        news = get_news_with_sentiment(company_name, 5)
    avg_sentiment = sum(n["score"] for n in news) / len(news) if news else 0

    signal, emoji, color = generate_signal(df, avg_sentiment)
    bg = {"green":"#0d2d00","red":"#2d0000","orange":"#2d1f00"}.get(color,"#111")

    st.markdown(f"""
    <div class="signal-box" style="background:{bg};border:2px solid {'#39d353' if color=='green' else '#e94560' if color=='red' else '#f0b429'}">
        <div style="font-size:3rem">{emoji}</div>
        <div style="font-size:2rem;margin:8px 0">{signal}</div>
        <div style="font-size:1rem;opacity:0.8">Signal for {info['name']}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Signal Breakdown")
    latest = df["Close"].iloc[-1]
    prev   = df["Close"].iloc[-2]
    ma20   = df["MA20"].iloc[-1] if "MA20" in df.columns else None
    ma50   = df["MA50"].iloc[-1] if "MA50" in df.columns else None

    factors = [
        ["Price vs MA20",      "🟢 Bullish" if ma20 and latest > ma20 else "🔴 Bearish",   f"Price ₹{round(latest,1)} vs MA20 ₹{round(ma20,1) if ma20 else 'N/A'}"],
        ["Price vs MA50",      "🟢 Bullish" if ma50 and latest > ma50 else "🔴 Bearish",   f"Price ₹{round(latest,1)} vs MA50 ₹{round(ma50,1) if ma50 else 'N/A'}"],
        ["1-Day Price Move",   "🟢 Up" if latest > prev else "🔴 Down",                    f"₹{round(prev,1)} → ₹{round(latest,1)}"],
        ["News Sentiment",     "🟢 Positive" if avg_sentiment > 0.05 else ("🔴 Negative" if avg_sentiment < -0.05 else "🟡 Neutral"), f"Score: {round(avg_sentiment,3)}"],
    ]
    fdf = pd.DataFrame(factors, columns=["Factor","Signal","Detail"])
    st.dataframe(fdf, use_container_width=True, hide_index=True)
    st.warning("This is for educational purposes only. Not real financial advice.")

elif page == "🔄 Compare Stocks":
    st.title("🔄 Compare Two Stocks")
    col1, col2 = st.columns(2)
    with col1:
        s1 = st.selectbox("Stock 1", list(POPULAR_STOCKS.keys()), index=0)
        t1 = POPULAR_STOCKS[s1]
    with col2:
        s2 = st.selectbox("Stock 2", list(POPULAR_STOCKS.keys()), index=1)
        t2 = POPULAR_STOCKS[s2]

    if st.button("🔄 Compare Now"):
        with st.spinner("Fetching data for both stocks..."):
            info1, df1 = load_data(t1, period)
            info2, df2 = load_data(t2, period)

        c1, c2 = st.columns(2)
        for col, inf, dfx, tkr in [(c1,info1,df1,t1),(c2,info2,df2,t2)]:
            chg_c = "#39d353" if inf['change'] >= 0 else "#e94560"
            with col:
                st.markdown(f"### {inf['name']}")
                st.markdown(f'<div class="metric-card"><div class="metric-val">₹{inf["price"]}</div><div class="metric-lbl">Price</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-card" style="margin-top:8px"><div class="metric-val" style="color:{chg_c}">{round(inf["change"],2)}%</div><div class="metric-lbl">Day Change</div></div>', unsafe_allow_html=True)

        st.markdown("### Price Comparison Chart")
        df1["Normalised"] = (df1["Close"] / df1["Close"].iloc[0]) * 100
        df2["Normalised"] = (df2["Close"] / df2["Close"].iloc[0]) * 100
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df1["Date"], y=df1["Normalised"],
                                  name=info1["name"], line=dict(color="#39d353", width=2)))
        fig.add_trace(go.Scatter(x=df2["Date"], y=df2["Normalised"],
                                  name=info2["name"], line=dict(color="#60a5fa", width=2)))
        fig.update_layout(
            plot_bgcolor="#0d0d0d", paper_bgcolor="#0d0d0d",
            font_color="white", height=400,
            yaxis_title="Normalised Price (Base 100)",
            legend=dict(bgcolor="#0d0d0d")
        )
        st.plotly_chart(fig, use_container_width=True)
