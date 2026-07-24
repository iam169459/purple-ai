"""
Enhanced Learning Engine
Enables the AI to learn new information from online sources
"""
import json
import os
import re
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from logger import logger
from config import config

class LearningEngine:
    def __init__(self):
        self.knowledge_file = "data/knowledge_base.json"
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.knowledge_file):
                with open(self.knowledge_file, 'r') as f:
                    return json.load(f)
            return {"facts": {}, "definitions": {}, "procedures": {}, "topics": {}, "learned": []}
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            return {"facts": {}, "definitions": {}, "procedures": {}, "topics": {}, "learned": []}
    
    def _save_knowledge_base(self, knowledge: Dict[str, Any]) -> bool:
        try:
            os.makedirs(os.path.dirname(self.knowledge_file), exist_ok=True)
            with open(self.knowledge_file, 'w') as f:
                json.dump(knowledge, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving knowledge base: {e}")
            return False
    
    def learn_new_information(self, query: str, category: str = "facts") -> Optional[str]:
        try:
            logger.info(f"Learning about: {query}")
            
            existing = self._search_knowledge_base(query)
            if existing:
                return f"I already know about {query}: {existing}"
            
            new_info = self._fetch_online_information(query)
            
            if new_info:
                self._store_knowledge(query, new_info, category)
                self._add_to_learned_list(query)
                return f"I learned something new about {query}: {new_info}"
            else:
                return f"Sorry, I couldn't find information about {query} online. But I'll remember to look for it next time!"
        except Exception as e:
            logger.error(f"Error learning: {e}")
            return f"I had trouble learning about {query}. Please try again later."
    
    def _search_knowledge_base(self, query: str) -> Optional[str]:
        query_lower = query.lower()
        for category in ['facts', 'definitions', 'procedures', 'topics']:
            if category in self.knowledge_base:
                for key, value in self.knowledge_base[category].items():
                    if query_lower in key.lower() or query_lower in str(value).lower():
                        return value
        return None
    
    def _fetch_online_information(self, query: str) -> Optional[str]:
        info = self._search_wikipedia(query)
        if info:
            return info
        
        info = self._search_duckduckgo(query)
        if info:
            return info
        
        info = self._search_brave(query)
        if info:
            return info
        
        return None
    
    def _search_wikipedia(self, query: str) -> Optional[str]:
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
            response = requests.get(url, timeout=10, headers={"User-Agent": "PurpleAI/1.0"})
            if response.status_code == 200:
                data = response.json()
                extract = data.get('extract', '')
                if extract:
                    sentences = extract.split('. ')
                    return self._clean_text(sentences[0] + '.' if sentences else extract)
            return None
        except Exception as e:
            logger.error(f"Wikipedia error: {e}")
            return None
    
    def _search_duckduckgo(self, query: str) -> Optional[str]:
        try:
            url = "https://api.duckduckgo.com/"
            params = {'q': query, 'format': 'json', 'no_html': '1', 'skip_disambig': '1'}
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                abstract = data.get('AbstractText', '')
                if abstract:
                    return self._clean_text(abstract)
                related = data.get('RelatedTopics', [])
                if related and isinstance(related, list) and len(related) > 0:
                    first = related[0]
                    if isinstance(first, dict) and 'Text' in first:
                        return self._clean_text(first['Text'])
            return None
        except Exception as e:
            logger.error(f"DuckDuckGo error: {e}")
            return None
    
    def _search_brave(self, query: str) -> Optional[str]:
        try:
            api_key = os.getenv('BRAVE_API_KEY', '')
            if not api_key:
                return None
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {"X-Subscription-Token": api_key}
            params = {"q": query, "count": 1}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get('web', {}).get('results', [])
                if results:
                    return self._clean_text(results[0].get('description', ''))
            return None
        except Exception as e:
            logger.error(f"Brave search error: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'\[\d+\]', '', text)
        return text[:500]
    
    def _store_knowledge(self, topic: str, information: str, category: str = "facts"):
        try:
            if category not in self.knowledge_base:
                self.knowledge_base[category] = {}
            self.knowledge_base[category][topic.lower()] = information
            self.knowledge_base['last_updated'] = datetime.now().isoformat()
            self._save_knowledge_base(self.knowledge_base)
            logger.info(f"Stored knowledge about {topic}")
        except Exception as e:
            logger.error(f"Error storing knowledge: {e}")
    
    def _add_to_learned_list(self, topic: str):
        if 'learned' not in self.knowledge_base:
            self.knowledge_base['learned'] = []
        if topic not in self.knowledge_base['learned']:
            self.knowledge_base['learned'].append(topic)
    
    def get_knowledge_about(self, topic: str) -> Optional[str]:
        return self._search_knowledge_base(topic)
    
    def get_learned_topics(self) -> List[str]:
        return self.knowledge_base.get('learned', [])
    
    def get_knowledge_stats(self) -> Dict[str, int]:
        stats = {}
        for category in ['facts', 'definitions', 'procedures', 'topics']:
            stats[category] = len(self.knowledge_base.get(category, {}))
        stats['total_learned'] = len(self.knowledge_base.get('learned', []))
        return stats
