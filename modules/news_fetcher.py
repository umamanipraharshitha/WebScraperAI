# modules/news_fetcher.py
import requests
import re
import urllib.parse

def get_latest_news(query="AI", hits=20):
    """
    Performs a universal web search via DuckDuckGo's raw HTML fallback interface.
    Works for any keywords (e.g., 'jee mains') without requiring an API key.
    """
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    # Form payload
    data = {"q": query}
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=15)
        response.raise_for_status()
        html = response.text
        
        links_found = []
        
        # This matches the concrete a-href results container layout inside the raw HTML page
        matches = re.findall(
            r'<a class="result__url" href="([^"]+)".*?>', 
            html, 
            re.DOTALL | re.IGNORECASE
        )
        
        # Extract title anchors matching the general loop index
        titles = re.findall(
            r'<a class="result__snippet"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
            html,
            re.DOTALL | re.IGNORECASE
        )
        
        # Simple reliable fallback pattern for tracking clean links directly:
        if not matches:
            matches = re.findall(r'href="([^"]+uddg=[^"]+)"', html)

        for href in matches:
            if len(links_found) >= hits:
                break
                
            # Clean up tracking wrapper params injected by DDG
            if "uddg=" in href:
                parsed_url = urllib.parse.urlparse(href)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                if 'uddg' in query_params:
                    href = query_params['uddg'][0]
            
            # Clean URL parsing validation
            href = urllib.parse.unquote(href)
            
            if href.startswith("http") and "duckduckgo.com" not in href:
                # Deduplicate links
                if href not in [item['url'] for item in links_found]:
                    # Create a clean display title based on domain metadata
                    domain = urllib.parse.urlparse(href).netloc.replace("www.", "")
                    links_found.append({
                        "title": f"Result from {domain}",
                        "url": href
                    })
                    
        return links_found

    except Exception as e:
        print(f"⚠️ Search engine module warning: {e}")
        return []