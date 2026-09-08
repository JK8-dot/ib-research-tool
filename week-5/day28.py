from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    max_tokens=1000
)

transcript = input("Paste earnings call transcript: ")

# Chain 1 — Earnings Analysis
earnings_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""You are a senior equity research analyst.
Analyze this earnings call transcript and extract:
1. Revenue vs guidance (beat/miss/inline)
2. Management sentiment (confident/cautious/defensive)
3. Top 3 risks mentioned
4. Top 3 opportunities mentioned
5. One-line thesis

Transcript:
{transcript}"""
)

print("\nRunning Chain 1 — Earnings Analysis...")
earnings_analysis = llm.invoke(earnings_prompt.format(transcript=transcript)).content

# Chain 2 — Trade Thesis
trade_prompt = PromptTemplate(
    input_variables=["earnings_analysis"],
    template="""You are a senior equity trader at a hedge fund.
Based on this earnings analysis, provide:
1. Trade direction (Long/Short/Neutral)
2. Entry rationale (2 sentences)
3. Price target rationale (1 sentence)
4. Stop loss level and why

Earnings Analysis:
{earnings_analysis}"""
)

print("Running Chain 2 — Trade Thesis...")
trade_thesis = llm.invoke(trade_prompt.format(earnings_analysis=earnings_analysis)).content

# Chain 3 — Risk Memo
risk_prompt = PromptTemplate(
    input_variables=["earnings_analysis", "trade_thesis"],
    template="""You are a risk manager at a hedge fund.
Given this earnings analysis and trade thesis, write a one-page risk/reward memo for a portfolio manager.
Include: position sizing recommendation, key risks to monitor, suggested hedges, and go/no-go recommendation.

Earnings Analysis:
{earnings_analysis}

Trade Thesis:
{trade_thesis}"""
)

print("Running Chain 3 — Risk Memo...")
risk_memo = llm.invoke(risk_prompt.format(
    earnings_analysis=earnings_analysis,
    trade_thesis=trade_thesis
)).content

print("\n=== EARNINGS ANALYSIS ===")
print(earnings_analysis)

print("\n=== TRADE THESIS ===")
print(trade_thesis)

print("\n=== RISK MEMO ===")
print(risk_memo)