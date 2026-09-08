import anthropic
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

article = input("Paste a financial news article or headline: ")

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    system="""You are a senior equity research analyst. Analyze the provided text and return ONLY valid JSON with exactly these keys:
{
    "summary": "one sentence summary",
    "key_facts": ["fact 1", "fact 2", "fact 3"],
    "market_implication": "bullish / bearish / neutral",
    "implication_reason": "one sentence why",
    "sentiment": "positive / negative / neutral",
    "affected_entities": ["company or sector 1", "company or sector 2"]
}
Return ONLY the JSON. No extra text, no markdown, no explanation.""",
    messages=[
        {"role": "user", "content": article}
    ]
)

raw = message.content[0].text
cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
data = json.loads(cleaned)

print("\n--- SUMMARY ---")
print(data["summary"])

print("\n--- KEY FACTS ---")
for fact in data["key_facts"]:
    print(f"  • {fact}")

print("\n--- MARKET IMPLICATION ---")
print(f"{data['market_implication'].upper()} — {data['implication_reason']}")

print("\n--- SENTIMENT ---")
print(data["sentiment"].upper())

print("\n--- AFFECTED ENTITIES ---")
for entity in data["affected_entities"]:
    print(f"  • {entity}")

print("\n\n--- PROMPT COMPARISON ---")
print("Running same article with vague prompt...")

vague = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    system="Analyze this financial news.",
    messages=[
        {"role": "user", "content": article}
    ]
)

print("\nVAGUE PROMPT OUTPUT:")
print(vague.content[0].text)