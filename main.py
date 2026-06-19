import os
from dotenv import load_dotenv
from modules.news_fetcher import get_latest_news
from modules.price_tracker import get_crypto_prices
from modules.ai_analysis import analyze_text_with_gemini
from modules.web_scraper import fetch_page_text, extract_prices, screenshot_with_playwright

load_dotenv()

def main():
    print("=== AI Competitive Intelligence Tool ===\n")

    # 1) News
    print("[1] Latest AI News")
    news = get_latest_news("Artificial Intelligence", 5)
    for idx, article in enumerate(news, 1):
        print(f"{idx}. {article['title']} - {article['url']}")
    print()

    # 2) Prices
    print("[2] Crypto Prices")
    import requests

    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(url)
    prices = response.json()
    print(prices)


    # 3) Competitor Page
    url = input("Enter competitor pricing page URL: ").strip()
    text = fetch_page_text(url)
    
    print()

    # 4) Screenshot
    result = screenshot_with_playwright(url)
    print(result)
    print()

    # 5) AI Analysis
    print("[4] AI Analysis")
    analysis = analyze_text_with_gemini(text)
    print(analysis)

if __name__ == "__main__":
    main()
