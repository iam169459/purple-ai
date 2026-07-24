"""
Internet Learning Engine - Auto-learns from the internet continuously
"""
import json
import time
import random
from pathlib import Path
from datetime import datetime
import threading

class InternetLearner:
    """Learns new things from the internet automatically"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.memory_dir = self.base_dir / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.knowledge_file = self.memory_dir / "internet_knowledge.json"
        self.knowledge = self._load_knowledge()
        self.learning_topics = [
            "artificial intelligence", "machine learning", "python programming",
            "web development", "data science", "cybersecurity", "cloud computing",
            "blockchain", "quantum computing", "robotics", "IoT", "AR VR",
            "game development", "mobile apps", "DevOps", "Linux", "networking",
            "database", "API", "automation", "productivity", "health tips",
            "finance", "cryptocurrency", "startups", "technology news"
        ]
        self.learned_count = 0
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        import logging
        logger = logging.getLogger("InternetLearner")
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            logger.propagate = False
        return logger
    
    def _load_knowledge(self) -> dict:
        if self.knowledge_file.exists():
            try:
                with open(self.knowledge_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {"topics": {}, "facts": [], "learned_at": [], "total_learned": 0}
        return {"topics": {}, "facts": [], "learned_at": [], "total_learned": 0}
    
    def _save_knowledge(self):
        try:
            with open(self.knowledge_file, 'w') as f:
                json.dump(self.knowledge, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save knowledge: {e}")
    
    def learn_topic(self, topic: str) -> dict:
        """Learn about a specific topic from the internet"""
        try:
            from utils.web_search import web_search
            
            self.logger.info(f"Learning about: {topic}")
            
            results = web_search.search(topic, num_results=5)
            
            if results:
                knowledge_entry = {
                    "topic": topic,
                    "timestamp": datetime.now().isoformat(),
                    "sources": [r.get("url", "") for r in results],
                    "summaries": [r.get("snippet", "") for r in results],
                    "learned": True
                }
                
                if topic not in self.knowledge["topics"]:
                    self.knowledge["topics"][topic] = []
                
                self.knowledge["topics"][topic].append(knowledge_entry)
                self.knowledge["facts"].extend([r.get("snippet", "") for r in results])
                self.knowledge["learned_at"].append(datetime.now().isoformat())
                self.knowledge["total_learned"] += 1
                self.learned_count += 1
                
                self._save_knowledge()
                
                self.logger.info(f"Learned about {topic}: {len(results)} sources")
                return {"success": True, "topic": topic, "sources": len(results)}
            
            return {"success": False, "topic": topic, "message": "No results found"}
            
        except ImportError:
            self.logger.warning("Web search not available")
            return {"success": False, "message": "Web search module not installed"}
        except Exception as e:
            self.logger.error(f"Learning error: {e}")
            return {"success": False, "message": str(e)}
    
    def auto_learn_continuous(self):
        """Continuously learn random topics from the internet"""
        def learning_loop():
            while True:
                try:
                    topic = random.choice(self.learning_topics)
                    self.learn_topic(topic)
                    
                    delay = random.randint(300, 600)  # 5-10 minutes
                    time.sleep(delay)
                    
                except Exception as e:
                    self.logger.error(f"Auto-learn error: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=learning_loop, daemon=True)
        thread.start()
        self.logger.info("Continuous learning started")
        return {"success": True, "message": "Continuous learning started"}
    
    def search_internet(self, query: str) -> dict:
        """Search the internet for anything"""
        try:
            from utils.web_search import web_search
            
            results = web_search.search(query, num_results=8)
            
            if results:
                formatted = []
                for i, r in enumerate(results[:5], 1):
                    formatted.append({
                        "title": r.get("title", "No title"),
                        "url": r.get("url", ""),
                        "snippet": r.get("snippet", "No description")
                    })
                
                return {
                    "success": True,
                    "query": query,
                    "results": formatted,
                    "count": len(formatted)
                }
            
            return {"success": False, "query": query, "message": "No results found"}
            
        except ImportError:
            return {"success": False, "message": "Web search module not installed"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def get_knowledge_stats(self) -> dict:
        """Get learning statistics"""
        return {
            "topics_learned": len(self.knowledge.get("topics", {})),
            "total_facts": len(self.knowledge.get("facts", [])),
            "total_learned": self.knowledge.get("total_learned", 0),
            "session_learned": self.learned_count
        }


internet_learner = InternetLearner()
