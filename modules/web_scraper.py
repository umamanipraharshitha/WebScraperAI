# modules/web_scraper.py
import os
import re
from playwright.sync_api import sync_playwright

def fetch_page_text(url: str) -> str:
    """Uses Playwright with custom desktop headers to fast-load webpage content."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Emulate a real desktop browser to bypass bot-detection delays
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Wait ONLY until the DOM layout loads, rather than waiting for heavy trackers/images
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        
        raw_inner_text = page.locator("body").inner_text()
        browser.close()
        return raw_inner_text.strip()

def extract_prices(text: str) -> list:
    return re.findall(r"\$\d+(?:\.\d{2})?", text)

def screenshot_with_playwright(url: str, save_path="data/screenshot.png") -> str:
    dir_name = os.path.dirname(save_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        page.screenshot(path=save_path, full_page=True)
        browser.close()
        return save_path