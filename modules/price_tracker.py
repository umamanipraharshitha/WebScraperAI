# modules/price_tracker.py
import requests
import yfinance as yf

def get_crypto_prices(coins=None, vs_currency="usd") -> dict:
    """Fetches real-time crypto valuations via CoinGecko's open API tier."""
    if coins is None:
        coins = ["bitcoin", "ethereum", "solana"]
    ids = ",".join(coins)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ids, "vs_currencies": vs_currency}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {c: data.get(c, {}).get(vs_currency) for c in coins if data.get(c, {}).get(vs_currency) is not None}
    except Exception:
        return {}

def get_live_stock_data(ticker_symbol: str) -> dict:
    """Fetches direct, live market quotes dynamically using yfinance."""
    try:
        ticker = yf.Ticker(ticker_symbol.upper().strip())
        # Request fast summary history to extract the absolute latest closure index
        hist = ticker.history(period="1d")
        if not hist.empty:
            latest_close = hist['Close'].iloc[-1]
            latest_open = hist['Open'].iloc[-1]
            change = latest_close - latest_open
            pct_change = (change / latest_open) * 100
            
            return {
                "symbol": ticker_symbol.upper(),
                "price": f"${latest_close:,.2f}",
                "change": f"{'+' if change >= 0 else ''}{change:,.2f} ({pct_change:+.2f}%)"
            }
    except Exception as e:
        print(f"   ⚠️ Yahoo Finance fetch failed: {e}")
    return {}