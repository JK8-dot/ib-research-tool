import anthropic
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

transcript = """Presentation

Operator

Hello, everyone. Thank you for joining us, and welcome to Oklo's Second Quarter 2026 Financial Results and Webcast. [Operator Instructions] I will now hand the conference over to Sam Doane, Senior Director of Investor Relations. Sam, please go ahead.

Sam Doane
Senior Director of Investor Relations

Thank you, operator, and welcome, everyone, to Oklo's Second Quarter 2026 Earnings and Company Update Call. I'm Sam Doane, Oklo's Senior Director of Investor Relations. Joining me today are Jake Dewitte, Oklo's Co-Founder and Chief Executive Officer; and Craig Bealmear, our Chief Financial Officer. Earlier today, we released our second quarter 2026 financial results. Today's accompanying slide presentation is available on the Investor Relations section of our website.

Before we begin, I'd like to remind everyone that today's discussion, including our prepared remarks and the question-and-answer session that follows, will include forward-looking statements. These statements reflect our current views regarding trends, assumptions, risks, uncertainties and other factors that could cause actual results to differ materially from those discussed today. We encourage you to review our forward-looking statements disclaimer included in our supplemental presentation.

Additional information regarding relevant risks can also be found in our filings with the Securities and Exchange Commission. Oklo undertakes no obligation to update any forward-looking statements as a result of new information, future events or otherwise, except as required by law. With that, I'll turn the call over to Jake. Jake?

Jacob Dewitte
Co-Founder, CEO & Chairman

Thanks, Sam. I want to start with 2 developments that are expanding the capabilities available to execute advanced nuclear projects in the United States. The first is the U.S. Department of Energy Genesis mission. We see Genesis as a sizable opportunity for Oklo and for the broader nuclear industry. DOE is bringing together its 17 national laboratories, industry, academia, advanced computing infrastructure, experimental facilities, scientific data and artificial intelligence capabilities.

In July, DOE announced the first project selections and more than $800 million in mission-wide partner commitments. Prometheus, an INL-led project in which Oklo is participating, was selected for a $60 million Phase I award over 3 years, subject to appropriations. Oklo is participating in multiple projects connected to the Genesis mission. One example is our announced collaboration with NVIDIA and Los Alamos National Laboratory. That work brings together Oklo's reactor and fuel capabilities, NVIDIA's AI infrastructure and Los Alamos' expertise in nuclear fuels and materials.

Together, we are working to develop and deploy physics and chemistry-based AI models, digital twins, modeling and simulation tools that can accelerate fuel validation and improve the workflows used to design, deploy and operate nuclear facilities. These are not generic AI applications. They are focused on some of the most time-intensive and technically demanding parts of nuclear deployment. The second development is on DOE's Nuclear Life Cycle Innovation Campus initiative.

"""

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1500,
    system="""You are a senior equity research analyst. Analyze this earnings call transcript and return ONLY valid JSON with exactly these keys:
{
    "revenue_vs_guidance": "beat / miss / inline / unknown",
    "eps_vs_guidance": "beat / miss / inline / unknown",
    "management_sentiment": "confident / cautious / defensive",
    "top_risks": ["risk 1", "risk 2", "risk 3"],
    "top_opportunities": ["opportunity 1", "opportunity 2", "opportunity 3"],
    "key_metrics": [{"metric": "name", "value": "value", "change": "change"}],
    "guidance_direction": "raised / lowered / maintained / withdrawn / unknown",
    "one_line_thesis": "one sentence investment thesis"
}
Return ONLY the JSON. No markdown, no extra text.""",
    messages=[
        {"role": "user", "content": transcript}
    ]
)

raw = message.content[0].text
cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
data = json.loads(cleaned)

print("\n--- EARNINGS CALL ANALYSIS ---")
print(f"Revenue vs Guidance: {data['revenue_vs_guidance'].upper()}")
print(f"EPS vs Guidance: {data['eps_vs_guidance'].upper()}")
print(f"Management Sentiment: {data['management_sentiment'].upper()}")
print(f"Guidance Direction: {data['guidance_direction'].upper()}")
print(f"\nThesis: {data['one_line_thesis']}")

print("\nTop Risks:")
for risk in data["top_risks"]:
    print(f"  ⚠️  {risk}")

print("\nTop Opportunities:")
for opp in data["top_opportunities"]:
    print(f"  ✅  {opp}")

print("\nKey Metrics:")
for metric in data["key_metrics"]:
    print(f"  {metric['metric']}: {metric['value']} ({metric['change']})")

if data["management_sentiment"] == "defensive":
    print("\n🚨 FLAG: Management sentiment is defensive — investigate further")

if data["guidance_direction"] == "raised":
    print("\n🚀 FLAG: Guidance raised — potential bullish signal")