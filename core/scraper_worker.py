import urllib.request
import json
import ssl
import time
import html
import re
import os
import threading

STOPWORDS = {
    "the", "in", "and", "a", "of", "to", "for", "on", "with", "at", "by", "from", "an", "is", "was", "were", "be", "has", "have", "had", "this", "that", "these", "those"
}

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^<]+?>', '', text)
    text = html.unescape(text)
    return " ".join(text.split()).strip()

def extract_keywords(title, year, artists=""):
    words = []
    if year:
        words.append(str(year))
    title_words = re.findall(r'\b\w+\b', title.lower())
    for w in title_words:
        if w not in STOPWORDS and len(w) > 2 and not w.isdigit():
            words.append(w)
    if artists:
        artist_words = re.findall(r'\b\w+\b', artists.lower())
        for w in artist_words:
            if w not in STOPWORDS and len(w) > 2:
                words.append(w)
    return list(set(words))

class ScraperWorker:
    def __init__(self, kb_path: str, interval_seconds: int = 86400):
        self.kb_path = kb_path
        self.interval = interval_seconds
        self.running = False
        self.thread = None

    def start(self):
        """Starts the scraper worker in a background thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"[ScraperWorker] Started background scraper for: {self.kb_path} (interval: {self.interval}s)")

    def stop(self):
        """Stops the scraper worker loop."""
        self.running = False
        print("[ScraperWorker] Stopped background scraper.")

    def _run_loop(self):
        # Run once immediately on startup, then sleep
        self.scrape_latest()
        
        while self.running:
            # Sleep in small increments to respond to shutdown quickly
            for _ in range(self.interval):
                if not self.running:
                    break
                time.sleep(1)
            if self.running:
                self.scrape_latest()

    def scrape_latest(self):
        """Scrapes the latest 10 posts from PICA's API and merges them into the KB."""
        if not os.path.exists(self.kb_path):
            print(f"[ScraperWorker] Warning: Knowledge base path not found: {self.kb_path}")
            return
            
        print(f"[ScraperWorker] Running periodic scan on PICA website API...")
        url = "https://pica.org.au/wp-json/wp/v2/whats-on?per_page=10"
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, context=ctx, timeout=5.0) as response:
                data = json.loads(response.read().decode('utf-8'))
                if not data:
                    return
                
                # Load current database
                with open(self.kb_path, 'r', encoding='utf-8') as f:
                    kb_data = json.load(f)
                    
                seen_facts = {entry.get("fact") for entry in kb_data}
                new_entries_count = 0
                
                for item in data:
                    title = clean_text(item.get('title', {}).get('rendered', ''))
                    link = item.get('link', '')
                    
                    # Extract year
                    date_str = item.get('date', '')
                    year = date_str[:4] if date_str and len(date_str) >= 4 else ""
                    
                    # Excerpt
                    content = clean_text(item.get('content', {}).get('rendered', ''))
                    excerpt = content[:150].strip()
                    if len(content) > 150:
                        excerpt += "..."
                        
                    # ACF
                    acf = item.get('acf', {})
                    artists = ""
                    if isinstance(acf, dict):
                        artists_field = acf.get('artists') or acf.get('artist')
                        if isinstance(artists_field, str):
                            artists = clean_text(artists_field)
                        elif isinstance(artists_field, list):
                            artists = ", ".join([clean_text(str(a)) for a in artists_field])
                            
                    # Construct fact
                    fact_parts = []
                    if year:
                        fact_parts.append(f"In {year},")
                    else:
                        fact_parts.append("In my history,")
                    fact_parts.append(f"my spaces hosted '{title}'")
                    if artists:
                        fact_parts.append(f"featuring {artists}")
                    fact_parts.append(f"({link}).")
                    if excerpt:
                        fact_parts.append(f"Context: {excerpt}")
                    fact_str = " ".join(fact_parts)
                    
                    if fact_str not in seen_facts:
                        # Generate keywords
                        keywords = extract_keywords(title, year, artists)
                        kb_data.append({
                            "keywords": keywords,
                            "fact": fact_str
                        })
                        seen_facts.add(fact_str)
                        new_entries_count += 1
                        
                if new_entries_count > 0:
                    with open(self.kb_path, 'w', encoding='utf-8') as f:
                        json.dump(kb_data, f, indent=2, ensure_ascii=False)
                    print(f"[ScraperWorker] Merged {new_entries_count} new show(s) into database. Total: {len(kb_data)}")
                else:
                    print(f"[ScraperWorker] Completed scan. No new updates found.")
        except Exception as e:
            print(f"[ScraperWorker] Error during scan: {e}")
