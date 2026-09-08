import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    temperature=0
)

search_tool = DuckDuckGoSearchRun()

tools = [search_tool]

agent_executor = create_react_agent(llm, tools)

print("="*60)
print("COMPANY RESEARCH AGENT")
print("="*60)

company = input("\nEnter a company name to research: ")

print(f"\nStarting research on {company}...")
print("(Watch the agent's thought process below)\n")
print("-"*60)

result = agent_executor.invoke({
    "messages": [("human", f"""Research {company} and provide a structured overview with:
    1. What the company does (business model, products/services)
    2. Founding story and key milestones
    3. Recent news and developments (last 6-12 months)
    4. Key considerations for someone analyzing this company""")]
})

print("-"*60)
print("\nFINAL RESEARCH NOTE:")
print("="*60)
print(result["messages"][-1].content)