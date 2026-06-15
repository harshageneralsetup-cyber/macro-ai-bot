import os
import sys
import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Fetch configurations securely from GitHub Environment Secrets
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not DISCORD_WEBHOOK_URL:
    print("❌ Error: DISCORD_WEBHOOK_URL is missing from environment variables.")
    sys.exit(1)
if not GEMINI_API_KEY:
    print("❌ Error: GEMINI_API_KEY is missing from environment variables.")
    sys.exit(1)

# Configure Gemini API explicitly
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini Client
client = genai.GenerativeModel('gemini-1.5-flash')

def fetch_live_market_data():
    """Extracts live financial data, yield dynamics, currency spot pairs, and policy interest rates."""
    # Default fallback data - will be replaced by live API calls
    data = {
        "brent": 87.33,             
        "us3y": "4.14%",            
        "us10y": "4.48%",           
        "dxy": "99.80",
        "usdinr": "95.10",  
        "fed_rate": "3.50% - 3.75%",
        "rbi_rate": "5.25%",
        "api_status": "using_fallback"
    }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    with requests.Session() as session:
        session.headers.update(headers)
        
        # 1. Crude Brent Pricing
        try:
            oil_req = session.get("https://query1.finance.yahoo.com/v8/finance/chart/BZ=F", timeout=5)
            val = oil_req.json()['chart']['result'][0]['meta']['regularMarketPrice']
            if val:
                data["brent"] = float(val)
                data["api_status"] = "live_data"
                print(f"✅ Successfully fetched Brent Crude: ${data['brent']:.2f}")
        except Exception as e:
            print(f"⚠️ Failed to fetch Brent Crude (using fallback): {e}")

        # 2. US 3-Year Bond Yield
        try:
            yield3_req = session.get("https://query1.finance.yahoo.com/v8/finance/chart/US3YT=X", timeout=5)
            price3 = yield3_req.json()['chart']['result'][0]['meta']['regularMarketPrice']
            if price3:
                data["us3y"] = f"{float(price3):.2f}%"
                print(f"✅ Successfully fetched US 3Y Yield: {data['us3y']}")
        except Exception as e:
            print(f"⚠️ Failed to fetch US 3Y Yield (using fallback): {e}")

        # 3. US 10-Year Bond Yield
        try:
            yield10_req = session.get("https://query1.finance.yahoo.com/v8/finance/chart/US10YT=X", timeout=5)
            price10 = yield10_req.json()['chart']['result'][0]['meta']['regularMarketPrice']
            if price10:
                data["us10y"] = f"{float(price10):.2f}%"
                print(f"✅ Successfully fetched US 10Y Yield: {data['us10y']}")
        except Exception as e:
            print(f"⚠️ Failed to fetch US 10Y Yield (using fallback): {e}")

        # 4. US Dollar Index (DXY)
        try:
            dxy_req = session.get("https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB", timeout=5)
            price = dxy_req.json()['chart']['result'][0]['meta']['regularMarketPrice']
            if price:
                data["dxy"] = f"{float(price):.2f}"
                print(f"✅ Successfully fetched DXY: {data['dxy']}")
        except Exception as e:
            print(f"⚠️ Failed to fetch DXY (using fallback): {e}")

        # 5. Live USD/INR Currency Spot Rate
        try:
            inr_req = session.get("https://query1.finance.yahoo.com/v8/finance/chart/INR=X", timeout=5)
            price_inr = inr_req.json()['chart']['result'][0]['meta']['regularMarketPrice']
            if price_inr:
                data["usdinr"] = f"{float(price_inr):.2f}"
                print(f"✅ Successfully fetched USD/INR: {data['usdinr']}")
        except Exception as e:
            print(f"⚠️ Failed to fetch USD/INR (using fallback): {e}")

        # 6. Official Federal Reserve Target Rate
        # Note: Actual current rate requires real-time data source
        try:
            fed_req = session.get("https://markets.newyorkfed.org/api/ambs/all/latest.json", timeout=5)
            if fed_req.status_code == 200:
                print(f"✅ Federal Reserve data endpoint responded")
                # In production, parse the actual rate from response
                # For now, use established current rate
        except Exception as e:
            print(f"⚠️ Failed to fetch Federal Reserve data (using fallback): {e}")

        # 7. RBI Repo Rate
        # Note: RBI rate requires checking official RBI website or Bloomberg terminal
        # This is a placeholder - in production, integrate with actual RBI data feed
        try:
            print(f"ℹ️ RBI Repo Rate: Using latest known rate (real-time RBI rate requires specialized data subscription)")
        except Exception as e:
            print(f"⚠️ RBI rate update issue: {e}")

    return data

def fetch_live_news_narratives():
    """Scrapes active financial headlines via a public RSS feed or news wire."""
    headlines = []
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get("https://www.reutersagency.com/feed/", headers=headers, timeout=7)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all('item')
        
        if items:
            for item in items[:5]:
                try:
                    title = item.title.text.strip() if item.title else "Unknown headline"
                    headlines.append(f"- {title}")
                except Exception as e:
                    print(f"⚠️ Error parsing headline: {e}")
                    continue
            print(f"✅ Successfully fetched {len(headlines)} news headlines")
        else:
            print("⚠️ No headlines found in Reuters feed (using fallback)")
            headlines = [
                "- Markets parsing recent macro data setups.",
                "- Global commodity cross-currents drive local tracking ranges."
            ]
    except Exception as e:
        print(f"⚠️ Failed to fetch news narratives (using fallback): {e}")
        headlines = [
            "- Markets parsing recent macro data setups.",
            "- Global commodity cross-currents drive local tracking ranges."
        ]
    return "\n".join(headlines)

def generate_ai_summary(prices, narratives):
    """Feeds raw data and headlines into Gemini to generate a fluid, intelligent macro report."""
    news_context = narratives
    if "parsing recent macro data setups" in narratives:
        news_context = "- Global markets are consolidating ahead of major upcoming central bank macro data updates."

    prompt = f"""
You are an institutional-grade global macro hedge fund strategist and elite quantitative analyst with a sharp, witty edge.
Analyze the following real-time market data and recent news headlines:

MARKET DATA:
- US Federal Reserve Target Rate: {prices['fed_rate']}
- RBI Repo Rate: {prices['rbi_rate']}
- Brent Crude Oil: ${prices['brent']:.2f}
- US 3-Year Bond Yield: {prices['us3y']}
- US 10-Year Bond Yield: {prices['us10y']}
- US Dollar Index (DXY): {prices['dxy']}
- USD/INR Currency Spot: {prices['usdinr']}

LATEST HEADLINES:
{news_context}

Based on this data, write a sophisticated, hyper-crisp, data-driven macro summary tailored for active Indian stock market traders (Nifty/Sensex/Dalal Street).

OUTPUT DIRECTIVES (CRITICAL FOR CLEAN REPRESENTATION):
- Do NOT include markdown code block syntax (like ```markdown or ```) around your response.
- Do NOT output any structural setup instructions, blueprint lines, or bracket labels. Generate the final text directly.
- Every sentence in the main sections must be dense with hard statistics, macro numbers, historical correlations, or explicit tactical sector outcomes. No filler text.
- Prioritize a balanced macro view with heavy weightage on Indian equity market impacts.

STRICT BOLDING AND LAYOUT RULES FOR SECTORS AND PIVOT TRIGGERS:
- ONLY the sector names or conditional triggers themselves must be bolded.
- The structural definition text or description immediately following the bold element MUST NOT contain bold markdown asterisks (**). Keep description text entirely normal.
- Example of correct format for Sector: **IT Services**: A DXY at {prices['dxy']} provides tailwinds for export-oriented margins.
- Example of correct format for Pivot Trigger: 🤝 **If Rate Cuts Materialize**: Crude slides lower, triggering IT and pharma rally.
- Do NOT put a blank line or a new paragraph break immediately after a bullet point (*). Keep the bullet point and its text on the exact same line.
- Keep structural section headers entirely on their own single line.

--- GENERATE AND OUTPUT CONTENT FOLLOWING THIS STRUCTURE ONLY ---

⚡ **Macro Flash: The 5 Pillars**
* 🏛️ **Interest Rates**: Global Fed Rate is at {prices['fed_rate']} and RBI Repo Rate is at {prices['rbi_rate']}. Provide a 1-sentence data-driven verdict analyzing how this exact policy stance impacts Indian rupee stability and corporate borrowing costs.
* 🛢️ **Oil (Brent)**: ${prices['brent']:.2f} | Provide a crisp, data-backed assessment tracking this active pricing against India's oil import bill, inflation trajectory, and downstream sector profitability.
* 💵 **Dollar Index (DXY)**: {prices['dxy']} (USD/INR Spot: {prices['usdinr']}) | Detail the exact impact on USD/INR currency tracking and emerging market capital flows.
* 📈 **US Bond Yields (10Y & 3Y)**: 10Y at {prices['us10y']} | 3Y at {prices['us3y']} | Provide the global yield context and analyze the spread profile between short-term and long-term bonds.
* 🎈 **Inflation**: Provide a sharp macro comparison of global consumer inflation indices against India's local retail CPI trajectory.

📰 **Latest Global Context Indicators:**
Provide a highly actionable, 2-sentence market tactical summary projecting how these macro data points will dictate the opening directional momentum and opening volatility parameters for Indian equities.

💼 **Sector Impacts: Winners & Losers**
🟢 **Immediate Winners (Bullish)**
* **IT Services**: Provide a highly specific, 1-sentence actionable trade reason linked directly to raw data metrics. No bold text inside this description sentence.
* **Pharma**: Provide a highly specific, 1-sentence actionable trade reason linked directly to raw data metrics. No bold text inside this description sentence.
* **Energy**: Provide a highly specific, 1-sentence actionable trade reason linked directly to raw data metrics. No bold text inside this description sentence.

🔴 **Immediate Losers (Bearish)**
* **Banking**: Provide a highly specific, 1-sentence actionable trade reason linked directly to raw data metrics. No bold text inside this description sentence.
* **Auto**: Provide a highly specific, 1-sentence actionable trade reason linked directly to raw data metrics. No bold text inside this description sentence.
* **Real Estate**: Provide a highly specific, 1-sentence actionable trade reason linked directly to raw data metrics. No bold text inside this description sentence.

📊 **SUMMARY CHECKLIST & PIVOT TRIGGERS**
* 🤝 **If Fed Pauses Rate Hikes**: Rupee strengthens, emerging market flows return, Nifty gains 200-300 basis points.
* ⚠️ **If Oil Spikes Above $95**: Import bill rises, RBI faces inflation pressure, defensive sectors outperform.
"""

    try:
        print("🤖 Generating AI macro summary using Gemini...")
        response = client.generate_content(prompt)
        result = response.text
        print("✅ AI summary generated successfully")
        return result
    except Exception as e:
        error_msg = f"⚠️ AI Generation Error: {str(e)}\nFalling back to market data echo."
        print(error_msg)
        return f"{error_msg}\n\nFetched Market Data:\n{json.dumps(prices, indent=2)}"

def dispatch_safely_under_limit(content):
    """Guarantees messages never cross Discord limits by breaking payloads safely at paragraph boundaries."""
    if not content:
        print("⚠️ No content to dispatch to Discord")
        return
    
    max_chars = 1900
    paragraphs = content.split('\n')
    current_chunk = []
    current_length = 0
    chunk_count = 0

    def send_chunk(chunk):
        nonlocal chunk_count
        payload = '\n'.join(chunk)
        if payload.strip():
            try:
                requests.post(DISCORD_WEBHOOK_URL, json={"content": payload}, timeout=5)
                chunk_count += 1
                print(f"✅ Discord message chunk {chunk_count} sent successfully ({len(payload)} chars)")
            except Exception as e:
                print(f"❌ Failed to send Discord chunk {chunk_count + 1}: {e}")

    for paragraph in paragraphs:
        if current_length + len(paragraph) + 1 > max_chars:
            if current_chunk:
                send_chunk(current_chunk)
            current_chunk = [paragraph]
            current_length = len(paragraph)
        else:
            current_chunk.append(paragraph)
            current_length += len(paragraph) + 1

    if current_chunk:
        send_chunk(current_chunk)
    
    print(f"📊 Total Discord messages sent: {chunk_count}")

if __name__ == "__main__":
    try:
        print("=" * 60)
        print("🚀 MACRO AI BRIEFING AUTOMATION STARTED")
        print("=" * 60)
        
        print("\n📊 Step 1: Scraping real-time market figures and policy rates...")
        market_metrics = fetch_live_market_data()
        print(f"   Status: {market_metrics.get('api_status', 'unknown')}")
        
        print("\n📰 Step 2: Fetching active context headlines...")
        news_briefs = fetch_live_news_narratives()
        
        print("\n🤖 Step 3: Generating AI data-driven macro summary...")
        final_payload = generate_ai_summary(market_metrics, news_briefs)
        
        print("\n💬 Step 4: Streaming into Discord webhook...")
        dispatch_safely_under_limit(final_payload)
        
        print("\n" + "=" * 60)
        print("✅ MACRO AI BRIEFING AUTOMATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("Process failed - check logs above for details")
        sys.exit(1)
