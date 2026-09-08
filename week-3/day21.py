import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

article = input("Paste a financial news article or headline: ")

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    system="You are a senior equity research analyst. Analyze the provided text and return: 1. One-sentence summary 2. Three key facts 3. Market implication (bullish / bearish / neutral with one sentence why) 4. Which sectors or specific companies are affected and how",
    messages=[
        {"role": "user", "content": article}
    ]
)

print("\n--- Analysis ---")
print(message.content[0].text)