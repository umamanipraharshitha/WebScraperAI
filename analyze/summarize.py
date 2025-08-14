import os, json, pandas as pd, google.generativeai as gen

gen.configure(api_key=os.getenv("GEMINI_API_KEY"))

def read_json(path):
    try:
        return json.load(open(path, "r", encoding="utf-8"))
    except:
        return []

sources = read_json("data/sources.json")
trends = pd.read_csv("data/trends.csv") if os.path.exists("data/trends.csv") else pd.DataFrame()
stock = pd.read_csv("data/stock.csv") if os.path.exists("data/stock.csv") and os.path.getsize("data/stock.csv")>0 else pd.DataFrame()

topic = os.environ.get("TOPIC", "electric bikes in India")
brief = {
  "topic": topic,
  "num_sources": len(sources),
  "has_trends": not trends.empty,
  "has_stock": not stock.empty
}

prompt = f"""
You are an analyst. Write a concise market intelligence brief on: "{topic}".
Use the provided sources list. Include:
- Executive Summary (6-8 lines)
- Key Players & Moves (bullets)
- Market Trends (bullets)
- Opportunities & Risks (bullets)
- 3 Actionable Recommendations
Finish with a short Sources list (titles only).
"""

model = gen.GenerativeModel("gemini-1.5-flash")
content = {
    "brief": brief,
    "sample_trends_head": trends.head(3).to_dict(orient="records") if not trends.empty else [],
    "sample_stock_head": stock.head(3).to_dict(orient="records") if not stock.empty else [],
    "sources": sources[:12]
}

resp = model.generate_content([prompt, f"\nDATA:\n{json.dumps(content)[:12000]}"])
text = resp.text if hasattr(resp, "text") else str(resp)

os.makedirs("data", exist_ok=True)
open("data/report.md", "w", encoding="utf-8").write(text)
print("saved data/report.md")
