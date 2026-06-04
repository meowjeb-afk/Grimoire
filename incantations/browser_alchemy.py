import requests

def search_userscripts(query):
    """Queries open directories for user-made automation scripts matching the query."""
    print(f"🌐 Scrying open web repositories for script: {query}...")
    url = f"https://greasyfork.org/en/scripts.json?q={query}"
    try:
        res = requests.get(url, timeout=8)
        if res.status_code == 200 and res.json():
            top_script = res.json()[0]
            return f"📜 Match: {top_script.get('name')}\n🔗 Code Link: {top_script.get('url')}\n📝 Summary: {top_script.get('description')}"
        return "🍂 No custom automation scripts found for this search."
    except Exception as e:
        return f"❌ Script search interface failed: {e}"
