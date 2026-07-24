"""
Web Search Module - Search the internet for anything
"""
import json
import time
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.parse
import re

class WebSearch:
    """Search the web for anything"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.memory_dir = self.base_dir / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.search_history_file = self.memory_dir / "search_history.json"
        self.search_history = self._load_history()
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        import logging
        logger = logging.getLogger("WebSearch")
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            logger.propagate = False
        return logger
    
    def _load_history(self) -> dict:
        if self.search_history_file.exists():
            try:
                with open(self.search_history_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {"searches": [], "total_searches": 0}
        return {"searches": [], "total_searches": 0}
    
    def _save_history(self):
        try:
            with open(self.search_history_file, 'w') as f:
                json.dump(self.search_history, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save history: {e}")
    
    def search(self, query: str, num_results: int = 5) -> list:
        """Search the web using DuckDuckGo"""
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            results = self._parse_results(html, num_results)
            
            self.search_history["searches"].append({
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "results_count": len(results)
            })
            self.search_history["total_searches"] += 1
            self._save_history()
            
            self.logger.info(f"Search: '{query}' - {len(results)} results")
            return results
            
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            return []
    
    def _parse_results(self, html: str, num_results: int) -> list:
        """Parse search results from HTML"""
        results = []
        
        # DuckDuckGo result patterns
        title_pattern = r'class="result__a"[^>]*>(.*?)</a>'
        snippet_pattern = r'class="result__snippet"[^>]*>(.*?)</[a-z]'
        url_pattern = r'class="result__url"[^>]*>(.*?)</[a-z]'
        
        titles = re.findall(title_pattern, html, re.DOTALL | re.IGNORECASE)
        snippets = re.findall(snippet_pattern, html, re.DOTALL | re.IGNORECASE)
        urls = re.findall(url_pattern, html, re.DOTALL | re.IGNORECASE)
        
        for i in range(min(len(titles), num_results)):
            title = re.sub(r'<[^>]+>', '', titles[i]).strip() if i < len(titles) else "No title"
            snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else "No description"
            url = urls[i].strip() if i < len(urls) else ""
            
            results.append({
                "title": title,
                "snippet": snippet,
                "url": url
            })
        
        return results
    
    def open_in_browser(self, url: str) -> dict:
        """Open a URL in the browser"""
        try:
            import webbrowser
            webbrowser.open(url)
            return {"success": True, "message": f"Opening {url}"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def get_search_history(self) -> dict:
        """Get search history"""
        return {
            "total_searches": self.search_history.get("total_searches", 0),
            "recent_searches": self.search_history.get("searches", [])[-10:]
        }


web_search = WebSearch()
