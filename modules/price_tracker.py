import requests

# Free crypto prices via CoinGecko (no API key)
def get_crypto_prices(coins=("bitcoin", "ethereum"), vs_currency="usd"):
    ids = ",".join(coins)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ids, "vs_currencies": vs_currency}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        # Return as a dictionary {coin_name: price}
        return {c: data.get(c, {}).get(vs_currency) for c in coins if data.get(c, {}).get(vs_currency) is not None}

    except Exception:
        return {}
