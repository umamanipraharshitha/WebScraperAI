# WebScraperAI

**WebScraperAI** is a Python-based competitive intelligence tool that helps you:

- Fetch the **latest AI news**.
- Track **cryptocurrency prices** (Bitcoin, Ethereum).
- Scrape **competitor websites** for pricing information.
- Capture **screenshots** of competitor pages.
- Perform **AI-based analysis** of competitor page content.

This tool is modular, easy to use, and demonstrates real-world web scraping combined with AI insights.

---

## Features

1. **Latest AI News**  
   Retrieves the top 5 AI-related news articles with titles and URLs.

2. **Crypto Prices**  
   Fetches live Bitcoin and Ethereum prices using the CoinGecko API.

3. **Competitor Page Scraping**  
   Extracts pricing information from a competitor’s website or API URL (supports both HTML pages and JSON APIs).

4. **Screenshots**  
   Takes a screenshot of the competitor page using Playwright.

5. **AI Analysis**  
   Uses your AI module (e.g., Gemini) to analyze page text for competitive insights.

---

## Installation
Install dependencies

pip install -r requirements.txt


Set up environment variables

Create a .env file in the root directory and add any required API keys, e.g.:

GEMINI_API_KEY=your_api_key_here
NEWS_API_KEY=your_api_key_here
Usage

## Run the main script:

python main.py


## Follow the prompts:

View the latest AI news.

Check current crypto prices.

Enter a competitor pricing page URL (HTML page or API URL).

View extracted prices.

Get a screenshot saved locally.

Receive AI-based analysis of the page content.


## git cloning
git clone https://github.com/umamanipraharshitha/WebScraperAI.git
cd WebScraperAI
