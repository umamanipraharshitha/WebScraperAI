import os
import sys
from dotenv import load_dotenv

# Ensure modules directory is discoverable by the Python path context
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# Import custom application layers
from modules.news_fetcher import get_latest_news
from modules.price_tracker import get_crypto_prices
from modules.ai_analysis import analyze_text_with_gemini
from modules.web_scraper import fetch_page_text, extract_prices, screenshot_with_playwright

# Load environment configuration variables
load_dotenv()

def print_header(title: str):
    """Utility helper to print a consistent, elegant visual section break."""
    print("\n" + "─" * 65)
    print(f" 🌟 SYSTEM WORKSPACE: {title.upper()} ")
    print("─" * 65)

def main():
    # Global state preserved across workspace switching executions
    scraped_text = ""
    target_url = ""

    while True:
        # -------------------------------------------------------------------------
        # CENTRAL CONTROL PANEL & ORCHESTRATION DASHBOARD
        # -------------------------------------------------------------------------
        print("\n" + "═" * 65)
        print(" 🤖       COMPETITIVE INTELLIGENCE & RESEARCH SYSTEM        🤖 ")
        print("═" * 65)
        print(" [1] LINK DISCOVERY   ──  Dynamic Query & Discovery Engine")
        print(" [2] WEB SCRAPER      ──  Raw Document & Asset Extraction Layer")
        print(" [3] AI SUMMARIZER    ──  Token-Optimized Map-Reduce Analytics")
        print(" [4] EXPLORER HUB     ──  Live Market Trading & Vertical Pulse")
        print(" [0] TERMINATE RUN    ──  Flush Subprocesses & Exit")
        print("═" * 65)
        
        choice = input("Select Workspace Module to Deploy (0-4): ").strip()

        match choice:
            case "1":
                print_header("Link Discovery & Web Search")
                search_query = input("On what keywords do you want to search the web?: ").strip()
                
                if search_query:
                    print(f"\n📡 Dispatching queries for '{search_query}'...")
                    news_items = get_latest_news(query=search_query, hits=20)
                    
                    if news_items:
                        print(f"✅ Discovered {len(news_items)} top high-authority references:")
                        for idx, item in enumerate(news_items, 1):
                            print(f"   🔹 [{idx}] {item['title']}")
                            print(f"        URL: {item['url']}")
                    else:
                        print("⚠️ No references found matching that search criterion.")
                else:
                    print("❌ Operation aborted: Empty query keyword payload.")

            case "2":
                print_header("Web Scraper Extraction Engine")
                target_url = input("Enter a valid link target to scrape: ").strip()
                
                if target_url:
                    print(f"\n🌐 Initializing headless automated browser pipeline for:\n   {target_url}")
                    try:
                        # 1. Fetch raw inner body text
                        scraped_text = fetch_page_text(target_url)
                        print(f"💾 Extraction successful: Compiled {len(scraped_text):,} characters.")
                        
                        # Cache raw context data to local storage architecture
                        os.makedirs("data", exist_ok=True)
                        with open("data/scraped_content.txt", "w", encoding="utf-8") as text_file:
                            text_file.write(scraped_text)
                        print("🗃️ Raw structural context cached at: data/scraped_content.txt")

                        # Extract inline regex prices immediately
                        prices_found = extract_prices(scraped_text)
                        if prices_found:
                            print(f"🏷️ Detected inline currencies: {prices_found[:5]}")
                            
                        # 2. Capture layout snapshot via Playwright
                        print("📸 Capturing full visual viewport checkpoint...")
                        screenshot_path = screenshot_with_playwright(target_url, save_path="data/screenshot.png")
                        print(f"🖼️ Layout asset saved securely to: {screenshot_path}")
                        
                    except Exception as e:
                        print(f"❌ Critical error in scraping pipeline subsystem: {e}")
                else:
                    print("❌ Operation aborted: Invalid target URI input.")

            case "3":
                print_header("Token-Optimized AI Summarizer")
                
                data_dir = "data"
                local_scraped_text = ""
                selected_file_name = ""

                # Step 1: Check for files dynamically in the data folder
                if os.path.exists(data_dir):
                    # List only text or markdown files to keep the menu clean
                    available_files = [f for f in os.listdir(data_dir) if f.endswith(('.txt', '.md', '.json'))]
                else:
                    available_files = []

                print("📂 Available cached documents in storage:")
                
                # Show volatile memory as Option 1 if it exists
                option_idx = 1
                file_mapping = {}
                
                if scraped_text:
                    print(f" [{option_idx}] *Volatile Memory Stack* (Active Live Session Text)")
                    file_mapping[str(option_idx)] = "VOLATILE_MEMORY"
                    option_idx += 1
                
                if available_files:
                    for filename in available_files:
                        print(f" [{option_idx}] {filename}")
                        file_mapping[str(option_idx)] = filename
                        option_idx += 1
                else:
                    if not scraped_text:
                        print(" ⚠️  No cached files found in the 'data/' directory.")

                # Step 2: Prompt user for file selection choice
                if file_mapping:
                    file_choice = input(f"\nSelect which resource file to load (1-{len(file_mapping)}): ").strip()
                    
                    if file_choice in file_mapping:
                        target_source = file_mapping[file_choice]
                        
                        if target_source == "VOLATILE_MEMORY":
                            local_scraped_text = scraped_text
                            selected_file_name = "Active Live Session Stream"
                        else:
                            selected_file_name = target_source
                            with open(os.path.join(data_dir, target_source), "r", encoding="utf-8") as target_file:
                                local_scraped_text = target_file.read()
                    else:
                        print("❌ Invalid selection. Defaulting out of summarizer matrix.")
                else:
                    print("❌ No text payload available anywhere. Run Web Scraper [Option 2] first.")

                # Step 3: Send the selected text directly to the Gemini Processing Layer
                if local_scraped_text.strip():
                    print(f"\n🧠 Loading content from [{selected_file_name}] into Gemini Optimization Engine...")
                    analysis_result = analyze_text_with_gemini(
                        local_scraped_text, 
                        system_hint="Analyze this page comprehensively. Map out value propositions, pricing tiers, and major features."
                    )
                    print("\n" + "📊" * 15 + " AI SUMMARY BRIEF " + "📊" * 15)
                    print(analysis_result)
                    print("═" * 65)
                    
                    # Save the new output intelligence report to disk
                    os.makedirs(data_dir, exist_ok=True)
                    with open(os.path.join(data_dir, "report.md"), "w", encoding="utf-8") as report_file:
                        report_file.write(analysis_result)
                    print("📝 Executable executive markdown summary updated at 'data/report.md'.")
                elif file_mapping:
                    print("⚠️ Pipeline Warning: Loaded source text file appears to be completely empty.")
            case "4":
                while True:
                    print_header("Dynamic Intelligence Explorer Hub")
                    print(" [1] Custom News & Trending Search")
                    print(" [2] Live Digital Currency Valuations")
                    print(" [3] Health, Pharma & Biotech Trends")
                    print(" [4] Live Stock & Equity Trading Lookup")
                    print(" [0] Return to Main System Dashboard")
                    print("─" * 65)
                    
                    sub_choice = input("Select Sub-Channel Matrix to Monitor (0-4): ").strip()
                    
                    if sub_choice == "1":
                        topic = input("\nEnter any topic keyword to query current web context: ").strip()
                        if topic:
                            print(f"\n📡 Polling live indices for '{topic}'...")
                            trending = get_latest_news(query=topic, hits=5)
                            for idx, item in enumerate(trending, 1):
                                print(f"   📰 [{idx}] {item['title']}\n        Source: {item['url']}")
                        
                    elif sub_choice == "2":
                        crypto_input = input("\nEnter crypto tokens comma-separated (default: bitcoin,ethereum,solana): ").strip().lower()
                        tokens = [t.strip() for t in crypto_input.split(",") if t.strip()] if crypto_input else ["bitcoin", "ethereum", "solana"]
                        
                        print(f"\n📡 Fetching asset feeds for {tokens}...")
                        market_prices = get_crypto_prices(coins=tokens)
                        if market_prices:
                            print("\n   💰 ── LIVE EXCHANGE MATRIX ──")
                            for asset, valuation in market_prices.items():
                                print(f"      {asset.upper().ljust(12)} : ${valuation:,.2f} USD")
                        else:
                            print("❌ External network error: Could not resolve real-time crypto pairs.")
                            
                    elif sub_choice == "3":
                        medical_kw = input("\nEnter medical/biotech terms to scan (default: general health tech): ").strip()
                        query_str = f"{medical_kw} medical science breakthrough journal" if medical_kw else "health medical technology breakthrough"
                        print(f"\n📡 Querying clinical feeds for: '{medical_kw if medical_kw else 'Global Biotech'}'...")
                        health_links = get_latest_news(query=query_str, hits=5)
                        for idx, item in enumerate(health_links, 1):
                            print(f"   ⚕️ [{idx}] {item['title']}\n        Source: {item['url']}")
                            
                    elif sub_choice == "4":
                        stock_ticker = input("\nEnter target financial ticker asset (e.g. NVDA, AAPL, ^NSEI): ").strip()
                        if stock_ticker:
                            print(f"\n📡 Establishing low-latency feed connection to Yahoo Finance for [{stock_ticker.upper()}]...")
                            from modules.price_tracker import get_live_stock_data
                            stock_metrics = get_live_stock_data(stock_ticker)
                            
                            if stock_metrics:
                                print("\n   📈 ── REAL-TIME MARKET QUOTE ──")
                                print(f"      Ticker Symbol : {stock_metrics['symbol']}")
                                print(f"      Last Traded   : {stock_metrics['price']} USD")
                                print(f"      Session Delta : {stock_metrics['change']}")
                            else:
                                print(f"❌ Failed to parse ticker metrics for '{stock_ticker}'. Check structural notation on Yahoo Finance.")
                    elif sub_choice == "0":
                        print("Closing Explorer workspace module...")
                        break
                    else:
                        print("❌ Invalid entry: Please select a valid tracking index option (0-4).")

            case "0":
                print("\n" + "═" * 65)
                print(" Shutting down microservices. Core engine execution terminated. ")
                print("═" * 65 + "\n")
                break

            case _:
                print("❌ Invalid System Command: Input must match an engine register (0-4).")

if __name__ == "__main__":
    main()