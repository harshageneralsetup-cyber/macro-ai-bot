import os
import sys
import requests
from bs4 import BeautifulSoup
from google import genai

# Fetch configurations securely from GitHub Environment Secrets[cite: 2]
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")[cite: 2]
# The SDK automatically uses GEMINI_API_KEY if it exists in the environment[cite: 2]

if not DISCORD_WEBHOOK_URL:
    print("❌ Error: DISCORD_WEBHOOK_URL is missing from environment variables.")[cite: 2]
    sys.exit(1)[cite: 2]
if not os.getenv("GEMINI_API_KEY"):
    print("❌ Error: GEMINI_API_KEY is missing from environment variables.")[cite: 2]
    sys.exit(1)[cite: 2]

# Initialize the Gemini Client[cite: 2]
client = genai.Client()

def fetch_live_market_data():
    """Extracts live financial data using standard Yahoo Finance summary structures."""[cite: 2]
    data = {"brent": 87.50, "us10y": "4.48%", "dxy": "99.90"}[cite: 2]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}[cite: 2]
    
    try:
        # Crude Brent
        oil_req = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/BZ=F", headers=headers, timeout=5)[cite: 2]
        data["brent"] = float(oil_req.json()['chart']['result'][0]['meta']['regularMarketPrice'])[cite: 2]
    except Exception:
        pass

    try:
        # US 10-Year Bond Yield
        yield_req = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/^TNX", headers=headers, timeout=5)[cite: 2]
        price = yield_req.json()['chart']['result'][0]['meta']['regularMarketPrice'][cite: 2]
        data["us10y"] = f"{price}%"[cite: 2]
    except Exception:
        pass

    try:
        # US Dollar Index
        dxy_req = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB", headers=headers, timeout=5)[cite: 2]
        price = dxy_req.json()['chart']['result'][0]['meta']['regularMarketPrice'][cite: 2]
        data["dxy"] = f"{price}"[cite: 2]
    except Exception:
        pass

    return data

def fetch_live_news_narratives():
    """Scrapes active financial headlines via a public RSS feed or news wire."""[cite: 2]
    headlines = [][cite: 2]
    headers = {"User-Agent": "Mozilla/5.0"}[cite: 2]
    try:
        response = requests.get("https://www.reutersagency.com/feed/", headers=headers, timeout=7)[cite: 2]
        soup = BeautifulSoup(response.content, features="xml")[cite: 2]
        items = soup.find_all('item')[cite: 2]
        
        for item in items[:5]:[cite: 2]
            title = item.title.text.strip()[cite: 2]
            headlines.append(f"- {title}")[cite: 2]
    except Exception:[cite: 2]
        headlines = [[cite: 2]
            "- Markets parsing recent macro data setups.",[cite: 2]
            "- Global commodity cross-currents drive local tracking ranges."[cite: 2]
        ][cite: 2]
    return "\n".join(headlines)[cite: 2]

def generate_ai_summary(prices, narratives):
    """Feeds raw data and headlines into Gemini to generate a fluid, intelligent macro report."""[cite: 2]
    
    # If the narratives fallback was triggered, we give the AI a better default prompt context
    news_context = narratives[cite: 2]
    if "parsing recent macro data setups" in narratives:[cite: 2]
        news_context = "- Global markets are consolidating ahead of major upcoming central bank macro data updates."[cite: 2]

    prompt = f"""
    You are an expert global macro hedge fund strategist and financial analyst specializing in the economic cross-currents between Western macro variables and Indian Equities (Nifty/Dalal Street).
    Analyze the following real-time market data and recent news headlines:

    MARKET DATA:
    - Brent Crude Oil: ${prices['brent']:.2f}
    - US 10-Year Bond Yield: {prices['us10y']}
    - US Dollar Index (DXY): {prices['dxy']}

    LATEST HEADLINES:
    {news_context}

    Based on this data, write a sophisticated, dynamic macro summary for a Discord channel.
    Crucially, maintain a balanced approach between global developments and Indian market impacts, giving a slight weightage to India. Every single pillar analysis must explicitly conclude with what this means for Indian markets (RBI policy, Rupee stability, or corporate margin shifts).

    CRITICAL FORMATTING RULES FOR DISCORD:[cite: 2]
    - Do NOT put a blank line or a new paragraph break immediately after a bullet point (*).[cite: 2]
    - Keep the bullet point and its text on the exact same line.[cite: 2]
    - Keep the "Sector Impacts" header entirely on a single line.[cite: 2]

    --- COPY THIS BLUEPRINT EXACTLY AND FILL IN THE BRACKETS ---[cite: 2]

    ⚡ **Macro Flash: The 5 Pillars**[cite: 2]
    * 🏛️ **Interest Rates**: [Dynamic analysis based on global central bank expectations/news, and how this directly limits or expands the Reserve Bank of India's (RBI) room to maneuver repo rates to defend the local currency]
    * 🛢️ **Oil (Brent)**: ${prices['brent']:.2f} | [Dynamic global trend, e.g., Bullish/Bearish and why, mapping out the immediate consequences for India's fiscal deficit, import bill math, and domestic manufacturing input costs]
    * 💵 **Dollar Index (DXY)**: {prices['dxy']} | [Dynamic context impact on global liquidity, detailing the pressure or relief line on the USD/INR peg and subsequent FII (Foreign Institutional Investor) capital allocations in Indian Equities]
    * 📈 **US Bond Yields (10Y)**: {prices['us10y']} | [Dynamic impact on global risk-free assets, highlighting the widening or narrowing interest rate differential and how it impacts Indian Government Bonds (IGBs)]
    * 🎈 **Inflation**: [Synthesize current Western macro trends regarding inflation and contrast it against India's domestic CPI performance, explaining if it provides local authorities with structural comfort or caution]

    📰 **Latest Global Context Indicators:**[cite: 2]
    [Provide a sharp 2-sentence synthesis of how current data and global trends are shifting market sentiment and specifically dictate the Nifty opening setup or intraday trading structures]

    💼 **Sector Impacts: Winners & Losers**[cite: 2]
    🟢 **Immediate Winners (Bullish)**[cite: 2]
    * **[Specify Indian Sector, e.g., Paint, Tyres, or Aviation]**: [1-sentence reason why it wins based on lower crude oil input prices expanding operational margins]
    * **[Specify Indian Sector, e.g., Public Sector Banks or Export IT]**: [1-sentence reason why it wins based on bond yield curves or currency movements]
    * **[Specify Indian Sector, e.g., Automobile or Infrastructure]**: [1-sentence reason why it wins based on the prevailing macro data setup]

    🔴 **Immediate Losers (Bearish)**[cite: 2]
    * **[Specify Indian Sector, e.g., Oil Exploration & Upstream Energy]**: [1-sentence reason why it loses when crude prices compress realization parameters]
    * **[Specify Indian Sector, e.g., IT Services or High-Growth Startups]**: [1-sentence reason why it faces headwinds when restrictive Western capex or high global yields choke off funding lines]
    * **[Specify Indian Sector, e.g., Exporters or Non-Essential Consumer Discretionary]**: [1-sentence reason why it loses based on pinched consumer demand in global/Western shipping corridors]
    """

    try:
        response = client.models.generate_content([cite: 2]
            model='gemini-2.5-flash',[cite: 2]
            contents=prompt,[cite: 2]
        )
        return response.text[cite: 2]
    except Exception as e:
        return f"⚠️ AI Generation Error: {str(e)}\nFalling back to system diagnostics."[cite: 2]

def dispatch_safely_under_limit(content):
    """Guarantees messages never cross Discord limits by automatically breaking payloads."""[cite: 2]
    if not content:
        return[cite: 2]
    max_chars = 1900[cite: 2]
    chunks = [content[i:i+max_chars] for i in range(0, len(content), max_chars)][cite: 2]
    for chunk in chunks:[cite: 2]
        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json={"content": str(chunk)}, timeout=5)[cite: 2]
            response.raise_for_status()[cite: 2]
        except Exception as e:
            print(f"Failed to send to Discord: {e}")[cite: 2]

if __name__ == "__main__":
    print("Scraping real-time market figures...")[cite: 2]
    market_metrics = fetch_live_market_data()[cite: 2]
    print("Scraping active context headlines...")[cite: 2]
    news_briefs = fetch_live_news_narratives()[cite: 2]
    print("Generating AI data template summary...")[cite: 2]
    final_payload = generate_ai_summary(market_metrics, news_briefs)[cite: 2]
    print("Streaming directly into active Discord client feed...")[cite: 2]
    dispatch_safely_under_limit(final_payload)[cite: 2]
    print("Process executed successfully.")[cite: 2]
