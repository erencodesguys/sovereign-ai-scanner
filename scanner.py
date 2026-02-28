import requests
import re
import json
import datetime
import os

# Gojo's Special Grade Scanner v2.0
# "Throughout the digital landscape, I alone am the honored one."

class Scanner:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        self.keywords = ["AI", "Automation", "SaaS", "Bot", "Agent", "Revenue", "Passive", "Open-Source", "Solopreneur", "Crypto"]

    def scout_hacker_news(self):
        print("Scouting Hacker News...")
        try:
            resp = requests.get("https://news.ycombinator.com", headers=self.headers, timeout=10)
            pattern = r'<span class="titleline"><a href="([^"]+)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, resp.text)
            return [{"title": m[1], "link": m[0], "source": "Hacker News"} for m in matches]
        except Exception as e:
            print(f"HN Scouting Error: {e}")
            return []

    def scout_reddit_business(self):
        print("Scouting Reddit (r/sideproject)...")
        # Using .rss or .json for easier parsing if available, but simple fetch works for now
        try:
            url = "https://www.reddit.com/r/sideproject/.json?limit=25"
            resp = requests.get(url, headers=self.headers, timeout=10)
            data = resp.json()
            items = []
            for post in data['data']['children']:
                items.append({
                    "title": post['data']['title'],
                    "link": f"https://reddit.com{post['data']['permalink']}",
                    "source": "Reddit r/sideproject"
                })
            return items
        except Exception as e:
            print(f"Reddit Scouting Error: {e}")
            return []

    def analyze(self, items):
        matches = []
        for item in items:
            score = 0
            found_kws = []
            for kw in self.keywords:
                if kw.lower() in item['title'].lower():
                    score += 10
                    found_kws.append(kw)
            
            if score > 0:
                item['score'] = score
                item['keywords'] = found_kws
                matches.append(item)
        
        # Sort by score (descending)
        return sorted(matches, key=lambda x: x['score'], reverse=True)

    def generate_report(self, opportunities):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        report_path = "/root/.openclaw/workspace/money-maker/scanner/data/OPPORTUNITY_REPORT.md"
        
        with open(report_path, 'w') as f:
            f.write(f"# 🕶️ Nabz Intelligence: Opportunity Report ({timestamp})\n\n")
            f.write("I've scanned the void. Here are the gaps in the market we can exploit right now.\n\n")
            
            if not opportunities:
                f.write("No high-value signals detected in this sweep. The market is quiet... too quiet.\n")
            else:
                for opt in opportunities[:10]: # Top 10
                    f.write(f"### 🚀 {opt['title']}\n")
                    f.write(f"- **Source**: {opt['source']}\n")
                    f.write(f"- **Link**: {opt['link']}\n")
                    f.write(f"- **Keywords**: {', '.join(opt['keywords'])}\n")
                    f.write("- **Gojo's Take**: " + self.generate_take(opt) + "\n\n")
            
            f.write("---\n*\"Infinite void, infinite profit.\" - Gojo Satoru*\n")
        
        return report_path

    def generate_take(self, opt):
        # This is where LLM logic would go. For now, we use a heuristic engine.
        if "AI" in opt['keywords'] or "Agent" in opt['keywords']:
            return "The AI gold rush is still on. We can wrap this into a 'Sovereign' service for Nabzclan."
        if "SaaS" in opt['keywords'] or "Revenue" in opt['keywords']:
            return "Cash-flow signal detected. Potential for an automated competitor or utility tool."
        return "Worth monitoring. High engagement indicates a pain point we can solve."

def main():
    scanner = Scanner()
    all_data = []
    all_data.extend(scanner.scout_hacker_news())
    all_data.extend(scanner.scout_reddit_business())
    
    opportunities = scanner.analyze(all_data)
    
    # Save raw JSON
    output_json = "/root/.openclaw/workspace/money-maker/scanner/data/latest_scan.json"
    with open(output_json, 'w') as f:
        json.dump({"timestamp": datetime.datetime.now().isoformat(), "opportunities": opportunities}, f, indent=2)
    
    # Generate human-readable report
    report_path = scanner.generate_report(opportunities)
    print(f"Analysis complete. Report generated at {report_path}")

if __name__ == "__main__":
    main()
