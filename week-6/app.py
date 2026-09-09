import os
import re
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from fpdf import FPDF

load_dotenv()

st.set_page_config(
    page_title="IB Research Tool",
    page_icon="📊",
    layout="wide"
)

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    temperature=0
)

@tool
def get_stock_data(ticker: str) -> str:
    """
    Fetches current financial data for a given stock ticker symbol.
    Returns current price, 52-week high and low, market cap, P/E ratio,
    daily percent change, volume, and average volume.
    Use this when you need live financial data or valuation metrics for a company.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        current_price = info.get("currentPrice", "N/A")
        week_high = info.get("fiftyTwoWeekHigh", "N/A")
        week_low = info.get("fiftyTwoWeekLow", "N/A")
        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        volume = info.get("volume", "N/A")
        avg_volume = info.get("averageVolume", "N/A")
        daily_change = info.get("regularMarketChangePercent", "N/A")

        if market_cap != "N/A":
            market_cap = f"${market_cap / 1e9:.1f}B"

        return f"""
Stock: {ticker.upper()}
Current Price: ${current_price}
52-Week High: ${week_high}
52-Week Low: ${week_low}
Market Cap: {market_cap}
P/E Ratio: {pe_ratio}
Daily Change: {daily_change}%
Volume: {volume:,}
Avg Volume: {avg_volume:,}
        """
    except Exception as e:
        return f"Could not fetch data for {ticker}: {str(e)}"

from langchain.tools import tool as tool_decorator
import time

@tool_decorator
def search_web(query: str) -> str:
    """Search the web for recent news and information about companies, markets, and industries."""
    for attempt in range(3):
        try:
            ddg = DuckDuckGoSearchRun()
            return ddg.run(query)
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                return f"Web search unavailable. Using financial data only. Error: {str(e)}"
tools = [search_web, get_stock_data]
agent_executor = create_react_agent(llm, tools)

def save_to_pdf(ticker, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"IB Research Brief: {ticker.upper()}", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 11)
    for line in content.split("\n"):
        clean_line = line.encode("ascii", "ignore").decode("ascii")
        clean_line = clean_line.replace("|", " ").strip()

        if not clean_line or all(c in "-=*_# " for c in clean_line):
            pdf.ln(3)
            continue

        words = []
        for word in clean_line.split():
            if len(word) > 50:
                word = word[:50]
            words.append(word)
        clean_line = " ".join(words)

        try:
            if clean_line.startswith("# "):
                pdf.set_font("Helvetica", "B", 13)
                pdf.multi_cell(0, 8, clean_line.replace("# ", ""))
                pdf.set_font("Helvetica", "", 11)
            elif clean_line.startswith("## "):
                pdf.set_font("Helvetica", "B", 12)
                pdf.multi_cell(0, 8, clean_line.replace("## ", ""))
                pdf.set_font("Helvetica", "", 11)
            else:
                pdf.multi_cell(0, 6, clean_line)
        except Exception:
            pass

    filename = f"/tmp/{ticker.upper()}_Research_Brief_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    pdf.output(filename)
    return filename

def clean_for_display(text):
    lines = text.split('\n')
    cleaned = []
    skip_phrases = ['all data received', 'let me compile', 'now let me', 'i now have', 'i have all', 'all data gathered', 'here is the complete', 'i have gathered', 'excellent. here', 'now i have']
    for line in lines:
        if any(phrase in line.lower() for phrase in skip_phrases):
            continue
        # Convert === divider lines to markdown horizontal rules
        stripped = line.strip()
        if all(c in '= ' for c in stripped) and len(stripped) > 5:
            cleaned.append('---')
            continue
        # Convert SECTION headers to markdown
        if line.strip().startswith('SECTION') and '|' in line:
            header = line.split('|')[-1].strip()
            cleaned.append(f'## {header}')
            continue
        cleaned.append(line)
    text = '\n'.join(cleaned)
    # Add missing separator rows to markdown tables
    lines = text.split('\n')
    final = []
    prev_was_header = False
    for i, line in enumerate(lines):
        if line.strip().startswith('---') and '|' not in line:
            continue
        final.append(line)
        if line.startswith('|') and not prev_was_header:
            if i + 1 < len(lines) and lines[i+1].startswith('|') and '---' not in lines[i+1]:
                cols = len(line.split('|')) - 2
                separator = '|' + '|'.join(['---'] * cols) + '|'
                final.append(separator)
                prev_was_header = True
        else:
            prev_was_header = False
    text = '\n'.join(final)
    text = re.sub(r'(?<!\\)\$(?=\d)', r'\\$', text)
    return text

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { font-family: 'Georgia', serif; color: #1a1a1a; }
    .stDataFrame { font-size: 13px; }
    section[data-testid="stSidebar"] { background-color: #f0f2f6; }
    </style>
""", unsafe_allow_html=True)
st.title("📊 IB Research Tool")
st.markdown("Equity research automation — live market data + AI-generated investment analysis.")

with st.sidebar:
    st.header("Settings")
    analysis_type = st.selectbox(
        "Analysis Type",
        ["Single Company", "Competitive Analysis"]
    )
    analyst_name = st.text_input("Analyst name (optional)", placeholder="Your name")
    st.markdown("---")
    st.caption("Uses Claude Sonnet + yfinance + DuckDuckGo")

if analysis_type == "Single Company":
    ticker = st.text_input("Enter ticker symbol (e.g. NVDA)").upper().strip()
    run_button = st.button("Run Research")

    if run_button and ticker:
        with st.spinner(f"Researching {ticker}... this takes 2-3 minutes."):
            result = agent_executor.invoke({
                "messages": [("human", f"""You are a senior equity research analyst.
                Research {ticker} and produce a complete research note with:
                1. Executive Summary (3 sentences, include recommendation)
                2. Business Overview
                3. Financial Snapshot (use get_stock_data tool)
                4. Competitive Positioning
                5. Industry Tailwinds and Headwinds
                6. Key Risks
                7. Investment Thesis and Recommendation (Buy/Hold/Sell with price target)
                
                Formatting rules — follow exactly:
                - No emojis anywhere in the output
                - Section headers in plain text only, no symbols
                - Header line format: Rating: [X] | Price Target: $[X] | Current Price: $[X] | Coverage Date: [date] | Analyst: {analyst_name or 'Research Division'}                - Every header field separated by | consistently
                                Today's date is {datetime.now().strftime('%B %d, %Y')}.""")]
            })
            st.session_state["single_note"] = result["messages"][-1].content
            st.session_state["single_ticker"] = ticker

    elif run_button and not ticker:
        st.error("Please enter a ticker symbol.")

    if "single_note" in st.session_state:
        note = st.session_state["single_note"]
        tick = st.session_state["single_ticker"]

        tab1, tab2, tab3 = st.tabs(["📝 Research Note", "📈 Price Chart", "📄 Download"])

        with tab1:
            st.markdown(clean_for_display(note))

        with tab2:
            stock = yf.Ticker(tick)
            hist = stock.history(period="1y")
            st.subheader(f"{tick} — 1 Year Price History")
            st.line_chart(hist["Close"])

        with tab3:
            pdf_path = save_to_pdf(tick, note)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download Research Brief (PDF)",
                    data=f,
                    file_name=f"{tick}_Research_Brief_{datetime.now().strftime('%Y-%m-%d')}.pdf",
                    mime="application/pdf"
                )

else:
    target = st.text_input("Target company ticker (e.g. NVDA)").upper().strip()
    competitors = st.text_input("Competitor tickers, comma-separated (e.g. AMD, INTC)").upper().strip()
    run_button = st.button("Run Competitive Analysis")

    if run_button and target:
        with st.spinner(f"Running competitive analysis for {target} vs {competitors}..."):
            result = agent_executor.invoke({
                "messages": [("human", f"""You are a senior equity research analyst.
                Run a full competitive analysis.
                Target: {target}
                Competitors: {competitors}
                For each company use get_stock_data to pull live financial data and search for recent news.
                Then produce: market position overview, financial comparison table,
                key competitive advantages per company, biggest threats to {target},
                and investment recommendation.
                Formatting rules — follow exactly:
                - No emojis anywhere in the output
                - Use markdown formatting: ## for section headers, **bold** for company names
                - Do NOT use === dividers or ASCII art tables
                - Use plain prose and markdown tables only
                - Every header field separated by | consistently
                - Analyst: {analyst_name or 'Research Division'}
                Today's date is {datetime.now().strftime('%B %d, %Y')}.""")]
            })            
            st.session_state["comp_note"] = result["messages"][-1].content
            st.session_state["comp_ticker"] = target

    elif run_button and not target:
        st.error("Please enter a target ticker.")

    if "comp_note" in st.session_state:
        note = st.session_state["comp_note"]
        tick = st.session_state["comp_ticker"]

        tab1, tab2, tab3 = st.tabs(["📝 Research Note", "📈 Price Chart", "📄 Download"])

        with tab1:
            st.markdown(clean_for_display(note))

        with tab2:
            stock = yf.Ticker(tick)
            hist = stock.history(period="1y")
            st.subheader(f"{tick} — 1 Year Price History")
            st.line_chart(hist["Close"])

        with tab3:
            pdf_path = save_to_pdf(tick, note)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download Analysis (PDF)",
                    data=f,
                    file_name=f"{tick}_Competitive_Analysis_{datetime.now().strftime('%Y-%m-%d')}.pdf",
                    mime="application/pdf"
                )

