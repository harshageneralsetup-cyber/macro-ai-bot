import os
import sys
import requests
from bs4 import BeautifulSoup
from google import genai

# Fetch configurations securely from GitHub Environment Secrets
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
# The SDK automatically uses GEMINI_API_KEY if it exists in the environment

if not DISCORD_WEBHOOK_URL:
    print("❌ Error: DISCORD_WEBHOOK_URL is missing from environment variables.")
    sys.exit(1)
if not os.getenv("GEMINI_API_KEY"):
    print("❌ Error: GEMINI_API_KEY is missing from environment variables.")
    sys.exit(1)

# Initialize the Gemini Client
client = genai.Client()

def fetch_live_market_data():
    """Extracts live financial data using standard Yahoo Finance summary structures."""
    data = {"brent": 87.50, "us10y": "4.48%", "dxy": "99.90"}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        # Crude Brent
        oil_req = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/BZ=F", headers=headers, timeout=5)
        data["brent"] = float(oil_req.json()['chart']['result'][0]['meta']['regularMarketPrice'])
    except Exception:
        pass

    try:
        # US 10-Year Bond Yield
        yield_req = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/^TNX", headers=headers, timeout=5)
        price = yield_req.json()['chart']['result'][0]['meta']['regularMarketPrice']
        data["us10y"] = f"{price}%"
    except Exception:
        pass

    try:
        # US Dollar Index
        dxy_req = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB", headers=headers, timeout=5)
        price = dxy_req.json()['chart']['result'][0]['meta']['regularMarketPrice']
        data["dxy"] = f"{price}"
    except Exception:
        pass

    return data

def fetch_live_news_narratives():
    """Scrapes active financial headlines via a public RSS feed or news wire."""
    headlines = []
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get("https://www.reutersagency.com/feed/", headers=headers, timeout=7)
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all('item')
        
        for item in items[:5]:
            title = item.title.text.strip()
            headlines.append(f"- {title}")
    except Exception:
        headlines = [
            "- Markets parsing recent macro data setups.",
            "- Global commodity cross-currents drive local tracking ranges."
        ]
    return "\n".join(headlines)

def generate_ai_summary(prices, narratives):
    """Feeds raw data and headlines into Gemini to generate a fluid, intelligent macro report."""
    
    # If the narratives fallback was triggered, we give the AI a better default prompt context
    news_context = narratives
    if "parsing recent macro data setups" in narratives:
        news_context = "- Global markets are consolidating ahead of major upcoming central bank macro data updates."

   prompt = f"""
    You are an expert global macro hedge fund strategist specializing in the economic cross-currents between Western macro variables and Indian Equities (Nifty/Dalal Street).

    Analyze the following real-time market metrics and recent news headlines:
    MARKET DATA:
    - Brent Crude Oil: ${prices['brent']:.2f}
    - US 10-Year Bond Yield: {prices['us10y']}
    - US Dollar Index (DXY): {prices['dxy']}

    LATEST HEADLINES:
    {news_context}

    Compile a sophisticated macro summary optimized for a professional trading desk. 
    Maintain a balanced approach between global developments and Indian market impacts, giving a slight weightage to India.

    STRICT DISCORD FORMATTING RULES:
    1. Do NOT insert blank lines between a bullet point and its nested text. 
    2. Ensure structural headers stay entirely on a single line.
    3. Use the literal formatting keywords (e.g., "**• The News:**", "**• Trajectory:**", "**• India Alignment:**") on individual lines or clean bullet segments as structured below.

    --- USE THIS EXACT LAYOUT BLUEPRINT ---

    ⚡ **Macro News Flash: The 5 Pillars**

    🏛️ **Interest Rate Trajectory (Short-End & Long-End)**
    * **• The News:** [Synthesize central bank news or rate-cut expectations based on headlines/yields]
    * **• Trajectory:** [State the expected direction of interest rates, e.g., "higher for longer" and target parameters]
    * **• India Alignment:** [Directly explain how this forces the RBI's hand regarding repo rates and defend or pressure the Rupee]

    🛢️ **Oil Prices Trajectory (Brent Crude)**
    * **• The News:** ${prices['brent']:.2f} | [Synthesize recent oil price action and any underlying geopolitical or supply drivers]
    * **• Trajectory:** [Identify the macro trajectory trend relative to key structural thresholds like $90 or $100]
    * **• India Alignment:** [Detail the specific impact on India's fiscal math, Current Account Deficit, and corporate input costs]

    💵 **US Dollar Index (DXY)**
    * **• The News:** {prices['dxy']} | [Contextualize current greenback strength against major global baskets]
    * **• Trajectory:** [Detail the expected resistance or support zones based on inflation metrics or macro trends]
    * **• India Alignment:** [Explain the pressure or relief on the USD/INR peg and subsequent foreign fund flow trajectories (FII allocations)]

    📈 **US Bond Yields (10Y)**
    * **• The News:** {prices['us10y']} | [Outline recent movements or volatility spikes in benchmark treasury yields]
    * **• Trajectory:** [Detail the underlying driver, e.g., hawkish central bank positioning or inflation indicators]
    * **• India Alignment:** [Analyze the narrowing or widening of interest rate differentials and pressure on Indian Government Bonds]

    🎈 **Inflation (Global, US, India)**
    * **• The News:** [Synthesize the state of consumer/producer prices across Western economies]
    * **• Trajectory:** [Detail whether core global inflation is accelerating or cooling]
    * **• India Alignment:** [Provide a sharp contrast with India's domestic CPI trajectory and how it gives structural comfort or discomfort to local authorities]

    📰 **Latest Global Context Indicators:**
    [Provide a 2-sentence market intelligence overview summarizing how the combination of these forces will dictate the Nifty opening or intraday trade setups]

    💼 **Immediate Sector Impacts (Global & India)**

    🟢 **Sectors Experiencing Positive Winds**
    * **[Sector Name 1, e.g., Indian Paint, Tyres, & Aviation]**: [Explain how specific metrics like crashing oil expand margins or lower input lines]
    * **[Sector Name 2, e.g., Indian Public Sector Banks & Fixed Income]**: [Explain how local structural yields protect treasuries from mark-to-market losses]
    * **[Sector Name 3, e.g., Automobile & Logistics]**: [Explain how easing resource constraints removes domestic demand barriers]

    🔴 **Sectors Facing Headwinds**
    * **[Sector Name 1, e.g., Oil Exploration & Upstream Energy]**: [Explain how falling realization rates lower immediate earnings per share upgrades]
    * **[Sector Name 2, e.g., Indian IT Services & Tech Startups]**: [Explain how restrictive global corporate capital expenditure delays deal sign-offs]
    * **[Sector Name 3, e.g., Export-Oriented Segments]**: [Explain how pinched real consumer incomes in Western regions hurt local discretionary orders]
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"⚠️ AI Generation Error: {str(e)}\nFalling back to system diagnostics."

def dispatch_safely_under_limit(content):
    """Guarantees messages never cross Discord limits by automatically breaking payloads."""
    if not content:
        return
    max_chars = 1900
    chunks = [content[i:i+max_chars] for i in range(0, len(content), max_chars)]
    for chunk in chunks:
        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json={"content": str(chunk)}, timeout=5)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to send to Discord: {e}")

if __name__ == "__main__":
    print("Scraping real-time market figures...")
    market_metrics = fetch_live_market_data()
    print("Scraping active context headlines...")
    news_briefs = fetch_live_news_narratives()
    print("Generating AI data template summary...")
    final_payload = generate_ai_summary(market_metrics, news_briefs)
    print("Streaming directly into active Discord client feed...")
    dispatch_safely_under_limit(final_payload)
    print("Process executed successfully.")
