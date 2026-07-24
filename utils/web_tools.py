"""
Advanced Web Tools
Multi-source web search, content extraction, and synthesis engine
"""
import re
import json
import time
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional
from html.parser import HTMLParser
from logger import logger

class TextExtractor(HTMLParser):
    """Extract text from HTML"""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header', 'aside'}
        self._skip = 0
    
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self._skip += 1
    
    def handle_endtag(self, tag):
        if tag in self.skip_tags and self._skip > 0:
            self._skip -= 1
    
    def handle_data(self, data):
        if self._skip == 0:
            stripped = data.strip()
            if stripped and len(stripped) > 10:
                self.text.append(stripped)
    
    def get_text(self) -> str:
        return ' '.join(self.text)

class WebTools:
    """Advanced web search and content extraction tools"""
    
    def __init__(self):
        self.session_history = []
        self.rate_limit_delay = 1.0
        self.last_request_time = 0
        logger.info("🌐 Web Tools initialized")
    
    def _rate_limit(self):
        """Respect rate limits between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()
    
    def search_multi_source(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search multiple sources simultaneously and aggregate results.
        Returns a list of result dicts with 'source', 'title', 'snippet', 'url'
        """
        logger.info(f"🔍 Multi-source search: '{query}'")
        all_results = []
        
        # Try Wikipedia
        try:
            wiki = self.search_wikipedia(query)
            if wiki:
                all_results.append({
                    "source": "Wikipedia",
                    "title": wiki.get("title", query),
                    "snippet": wiki.get("extract", "")[:800],
                    "url": wiki.get("url", ""),
                    "reliability": 0.95
                })
        except Exception as e:
            logger.warning(f"Wikipedia search failed: {e}")
        
        # Try DuckDuckGo Instant Answer
        try:
            ddg = self.search_duckduckgo(query)
            if ddg:
                all_results.append({
                    "source": "DuckDuckGo",
                    "title": ddg.get("Heading", query),
                    "snippet": ddg.get("AbstractText", "")[:800],
                    "url": ddg.get("AbstractURL", ""),
                    "reliability": 0.85
                })
        except Exception as e:
            logger.warning(f"DuckDuckGo search failed: {e}")
        
        # Try to fetch related topics from Wikipedia
        try:
            related = self.get_wikipedia_related(query)
            for item in related[:2]:
                all_results.append({
                    "source": "Wikipedia_Related",
                    "title": item.get("title", ""),
                    "snippet": item.get("extract", "")[:500],
                    "url": item.get("url", ""),
                    "reliability": 0.90
                })
        except Exception as e:
            logger.warning(f"Related topics fetch failed: {e}")
        
        self.session_history.append({"query": query, "results_count": len(all_results)})
        logger.info(f"📊 Found {len(all_results)} sources for '{query}'")
        return all_results[:max_results]
    
    def deep_research(self, query: str, depth: int = 2) -> Dict[str, Any]:
        """
        Perform deep research on a topic.
        Depth 1 = basic search, Depth 2 = follow-up on key concepts
        """
        logger.info(f"🔬 Deep research initiated: '{query}' (depth={depth})")
        
        # Phase 1: Primary search
        primary_results = self.search_multi_source(query, max_results=5)
        
        research_package = {
            "query": query,
            "depth": depth,
            "primary_sources": primary_results,
            "follow_up_research": [],
            "synthesis": None,
            "key_concepts": [],
            "confidence": 0.0
        }
        
        if depth >= 2 and primary_results:
            # Extract key concepts from primary results
            combined_text = " ".join([r.get("snippet", "") for r in primary_results])
            key_concepts = self._extract_key_concepts(combined_text, top_n=3)
            research_package["key_concepts"] = key_concepts
            
            # Phase 2: Follow-up research on key concepts
            for concept in key_concepts:
                follow_up = self.search_multi_source(concept, max_results=2)
                research_package["follow_up_research"].append({
                    "concept": concept,
                    "sources": follow_up
                })
        
        # Synthesize all findings
        research_package["synthesis"] = self._synthesize_findings(research_package)
        research_package["confidence"] = self._calculate_confidence(research_package)
        
        logger.info(f"🔬 Deep research complete. Confidence: {research_package['confidence']:.2f}")
        return research_package
    
    def search_wikipedia(self, query: str) -> Optional[Dict[str, Any]]:
        """Search Wikipedia for a topic summary"""
        self._rate_limit()
        try:
            encoded = urllib.parse.quote(query.replace(' ', '_'))
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'PurpleAI/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                return {
                    "title": data.get("title", query),
                    "extract": data.get("extract", ""),
                    "description": data.get("description", ""),
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                    "type": data.get("type", "")
                }
        except Exception as e:
            logger.warning(f"Wikipedia API error: {e}")
            return None
    
    def get_wikipedia_related(self, query: str) -> List[Dict[str, Any]]:
        """Get related Wikipedia pages"""
        self._rate_limit()
        try:
            encoded = urllib.parse.quote(query)
            url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded}&format=json&srlimit=3"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'PurpleAI/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                results = []
                for item in data.get("query", {}).get("search", []):
                    results.append({
                        "title": item.get("title", ""),
                        "extract": item.get("snippet", "").replace('<span class="searchmatch">', '').replace('</span>', ''),
                        "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(item.get('title', '').replace(' ', '_'))}"
                    })
                return results
        except Exception as e:
            logger.warning(f"Wikipedia related fetch error: {e}")
            return []
    
    def search_duckduckgo(self, query: str) -> Optional[Dict[str, Any]]:
        """Search DuckDuckGo Instant Answer API"""
        self._rate_limit()
        try:
            encoded = urllib.parse.quote(query)
            url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1&skip_disambig=1"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'PurpleAI/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                if data.get("AbstractText"):
                    return data
                return None
        except Exception as e:
            logger.warning(f"DuckDuckGo API error: {e}")
            return None
    
    def fetch_webpage_text(self, url: str, max_chars: int = 5000) -> str:
        """Fetch and extract text from a webpage"""
        self._rate_limit()
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'PurpleAI/1.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                html = response.read().decode('utf-8', errors='ignore')
                extractor = TextExtractor()
                extractor.feed(html)
                text = extractor.get_text()
                return text[:max_chars]
        except Exception as e:
            logger.warning(f"Webpage fetch error for {url}: {e}")
            return ""
    
    def _extract_key_concepts(self, text: str, top_n: int = 3) -> List[str]:
        """Extract key concepts from text for follow-up research"""
        # Simple extraction: find capitalized phrases and multi-word terms
        # In a real system, this would use NLP
        concepts = []
        
        # Find capitalized terms (proper nouns)
        proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        noun_counts = {}
        for noun in proper_nouns:
            if len(noun) > 4 and noun.lower() not in ['this', 'that', 'with', 'from', 'they', 'their', 'there']:
                noun_counts[noun] = noun_counts.get(noun, 0) + 1
        
        # Get top frequent proper nouns
        sorted_nouns = sorted(noun_counts.items(), key=lambda x: x[1], reverse=True)
        for noun, _ in sorted_nouns[:top_n]:
            if noun not in concepts:
                concepts.append(noun)
        
        return concepts
    
    def _synthesize_findings(self, research_package: Dict[str, Any]) -> str:
        """Create a coherent synthesis from multiple sources"""
        sources = research_package.get("primary_sources", [])
        follow_ups = research_package.get("follow_up_research", [])
        
        if not sources:
            return "No information found."
        
        parts = []
        
        # Add primary source summaries
        for src in sources[:3]:
            snippet = src.get("snippet", "").strip()
            if snippet:
                parts.append(snippet)
        
        # Add follow-up context
        for fu in follow_ups[:2]:
            for s in fu.get("sources", [])[:1]:
                snippet = s.get("snippet", "").strip()
                if snippet:
                    parts.append(f"Additionally, regarding {fu.get('concept', 'this topic')}: {snippet}")
        
        # Deduplicate and join
        unique_parts = []
        seen = set()
        for part in parts:
            key = part[:50].lower()
            if key not in seen and len(part) > 20:
                seen.add(key)
                unique_parts.append(part)
        
        synthesis = " ".join(unique_parts)
        # Limit length
        if len(synthesis) > 2000:
            synthesis = synthesis[:2000] + "..."
        
        return synthesis
    
    def _calculate_confidence(self, research_package: Dict[str, Any]) -> float:
        """Calculate confidence score based on source quality and quantity"""
        score = 0.0
        sources = research_package.get("primary_sources", [])
        
        # Base score from number of sources
        score += min(len(sources) * 0.2, 0.6)
        
        # Bonus for high-reliability sources
        for src in sources:
            score += src.get("reliability", 0.5) * 0.1
        
        # Bonus for follow-up depth
        if research_package.get("follow_up_research"):
            score += 0.15
        
        return min(score, 1.0)
    
    def get_search_history(self) -> List[Dict[str, Any]]:
        """Get history of searches performed"""
        return self.session_history
