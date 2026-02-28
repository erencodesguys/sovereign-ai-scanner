import requests
import re
import json
import datetime

def scan_hacker_news():
    print("Scanning Hacker News...")
    url = "https://news.ycombinator.com"
    response = requests.get(url, timeout=10)
    html = response.text
    pattern = r'<span class="titleline"><a href="([^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)
    items = []
    for link, title in matches:
        items.append({"title": title, "link": link, "source": "Hacker News"})
    return items

def analyze_opportunities(items):
    keywords = ["AI", "Automation", "SaaS", "Bot", "Agent", "Money", "Revenue", "Passive", "Open-Source"]
    matches = []
    for item in items:
        for kw in keywords:
            if kw.lower() in item['title'].lower():
                matches.append(item)
                break
    return matches

def main():
    all_items = []
    try:
        all_items.extend(scan_hacker_news())
    except Exception as e:
        print(f"Error scanning HN: {e}")
    
    opportunities = analyze_opportunities(all_items)
    
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total_scanned": len(all_items),
        "opportunities": opportunities
    }
    
    output_path = "/root/.openclaw/workspace/money-maker/scanner/data/latest_scan.json"
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Scan complete. Found {len(opportunities)} opportunities. Saved to {output_path}")

if __name__ == "__main__":
    main()
