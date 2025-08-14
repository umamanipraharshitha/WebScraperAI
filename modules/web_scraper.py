import re
from playwright.sync_api import sync_playwright

def fetch_page_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=r"C:\Users\mprah\AppData\Local\ms-playwright\chromium_headless_shell-1181\chrome-win\chrome-win\chrome.exe",
            headless=True
        )
        page = browser.new_page()
        page.goto(url)
        text = page.content()
        browser.close()
        return text

def extract_prices(text):
    """
    Finds all prices like $123.45 in the text and returns them as a list.
    """
    return re.findall(r"\$\d+(?:\.\d{2})?", text)

def screenshot_with_playwright(url, save_path="screenshot.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=r"C:\Users\mprah\AppData\Local\ms-playwright\chromium_headless_shell-1181\chrome-win\chrome-win\chrome.exe",
            headless=True
        )
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=save_path, full_page=True)
        browser.close()
        return save_path