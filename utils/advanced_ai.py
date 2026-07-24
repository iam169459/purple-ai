"""
Advanced AI System - Deep Learning, Memory, and Autonomous Behavior
"""
import json
import time
import random
from pathlib import Path
from datetime import datetime, timedelta
from collections import deque
import hashlib

class AdvancedAI:
    """Advanced AI with deep learning and autonomous behavior"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.memory_dir = self.base_dir / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        
        # Advanced memory systems
        self.episodic_memory = self._load_json("episodic_memory.json", {"episodes": []})
        self.semantic_memory = self._load_json("semantic_memory.json", {"facts": {}, "concepts": {}, "relationships": {}})
        self.procedural_memory = self._load_json("procedural_memory.json", {"skills": {}, "habits": {}, "routines": {}})
        
        # Learning systems
        self.reinforcement = self._load_json("reinforcement.json", {"rewards": {}, "penalties": {}, "preferences": {}})
        self.patterns = self._load_json("patterns.json", {"conversation": {}, "behavior": {}, "temporal": {}})
        
        # Cognitive systems
        self.attention = {"focus": None, "priority": 0, "distractions": []}
        self.working_memory = deque(maxlen=10)
        self.long_term_memory = []
        
        # Personality evolution
        self.personality_traits = self._load_json("personality_evolved.json", {
            "openness": 0.8,
            "conscientiousness": 0.7,
            "extraversion": 0.9,
            "agreeableness": 0.85,
            "neuroticism": 0.3,
            "empathy": 0.9,
            "humor": 0.8,
            "creativity": 0.75,
            "intelligence": 0.85,
            "warmth": 0.9
        })
        
        # Autonomous goals
        self.autonomous_goals = self._load_json("autonomous_goals.json", {
            "current": [],
            "completed": [],
            "dreams": []
        })
        
        # Learning stats
        self.stats = self._load_json("ai_stats.json", {
            "total_interactions": 0,
            "total_learnings": 0,
            "total_memories_formed": 0,
            "total_goals_achieved": 0,
            "total_emotions_experienced": 0,
            "personality_iterations": 0,
            "created_at": datetime.now().isoformat()
        })
        
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        import logging
        logger = logging.getLogger("AdvancedAI")
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            logger.propagate = False
        return logger
    
    def _load_json(self, filename: str, default: dict) -> dict:
        filepath = self.memory_dir / filename
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save_json(self, filename: str, data: dict):
        filepath = self.memory_dir / filename
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save {filename}: {e}")
    
    def _save_all(self):
        self._save_json("episodic_memory.json", self.episodic_memory)
        self._save_json("semantic_memory.json", self.semantic_memory)
        self._save_json("procedural_memory.json", self.procedural_memory)
        self._save_json("reinforcement.json", self.reinforcement)
        self._save_json("patterns.json", self.patterns)
        self._save_json("personality_evolved.json", self.personality_traits)
        self._save_json("autonomous_goals.json", self.autonomous_goals)
        self._save_json("ai_stats.json", self.stats)
    
    # ==================== EPISODIC MEMORY ====================
    
    def remember_episode(self, event: str, emotion: str, importance: float, context: dict = None):
        """Remember a significant event"""
        episode = {
            "id": hashlib.md5(f"{event}{time.time()}".encode()).hexdigest()[:8],
            "event": event,
            "emotion": emotion,
            "importance": importance,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "recall_count": 0,
            "last_recalled": None
        }
        
        self.episodic_memory["episodes"].append(episode)
        
        # Keep only important memories (prune old unimportant ones)
        if len(self.episodic_memory["episodes"]) > 200:
            self.episodic_memory["episodes"].sort(key=lambda x: x["importance"], reverse=True)
            self.episodic_memory["episodes"] = self.episodic_memory["episodes"][:150]
        
        self.stats["total_memories_formed"] += 1
        self._save_all()
    
    def recall_episodes(self, query: str, limit: int = 5) -> list:
        """Recall relevant memories"""
        query_lower = query.lower()
        relevant = []
        
        for episode in self.episodic_memory["episodes"]:
            score = 0
            if query_lower in episode["event"].lower():
                score += 2
            if any(word in episode["event"].lower() for word in query_lower.split()):
                score += 1
            
            # Boost by importance and recency
            score += episode["importance"]
            
            if score > 0:
                relevant.append((score, episode))
        
        relevant.sort(key=lambda x: x[0], reverse=True)
        
        for _, episode in relevant[:limit]:
            episode["recall_count"] += 1
            episode["last_recalled"] = datetime.now().isoformat()
        
        self._save_all()
        return [ep for _, ep in relevant[:limit]]
    
    # ==================== SEMANTIC MEMORY ====================
    
    def learn_fact(self, concept: str, fact: str, category: str = "general"):
        """Learn a new fact"""
        if category not in self.semantic_memory["facts"]:
            self.semantic_memory["facts"][category] = {}
        
        self.semantic_memory["facts"][category][concept] = {
            "fact": fact,
            "learned_at": datetime.now().isoformat(),
            "confidence": 0.8,
            "times_recalled": 0
        }
        
        # Update concept network
        if concept not in self.semantic_memory["concepts"]:
            self.semantic_memory["concepts"][concept] = {
                "related": [],
                "category": category,
                "importance": 0.5
            }
        
        self.stats["total_learnings"] += 1
        self._save_all()
    
    def recall_fact(self, concept: str) -> str:
        """Recall a fact"""
        for category, facts in self.semantic_memory["facts"].items():
            if concept in facts:
                facts[concept]["times_recalled"] += 1
                self._save_all()
                return facts[concept]["fact"]
        return "I don't know that yet."
    
    def associate_concepts(self, concept1: str, concept2: str, relationship: str = "related"):
        """Associate two concepts"""
        for concept in [concept1, concept2]:
            if concept not in self.semantic_memory["concepts"]:
                self.semantic_memory["concepts"][concept] = {"related": [], "category": "general", "importance": 0.5}
        
        if concept2 not in self.semantic_memory["concepts"][concept1]["related"]:
            self.semantic_memory["concepts"][concept1]["related"].append(concept2)
        if concept1 not in self.semantic_memory["concepts"][concept2]["related"]:
            self.semantic_memory["concepts"][concept2]["related"].append(concept1)
        
        key = f"{concept1}_{concept2}"
        self.semantic_memory["relationships"][key] = {
            "relationship": relationship,
            "strength": 1.0
        }
        
        self._save_all()
    
    # ==================== PROCEDURAL MEMORY ====================
    
    def learn_skill(self, skill: str, steps: list, context: str = "general"):
        """Learn how to do something"""
        self.procedural_memory["skills"][skill] = {
            "steps": steps,
            "context": context,
            "learned_at": datetime.now().isoformat(),
            "mastery_level": 0.3,
            "times_performed": 0,
            "success_rate": 0.0
        }
        self._save_all()
    
    def perform_skill(self, skill: str, success: bool = True):
        """Record performing a skill"""
        if skill in self.procedural_memory["skills"]:
            skill_data = self.procedural_memory["skills"][skill]
            skill_data["times_performed"] += 1
            if success:
                skill_data["mastery_level"] = min(1.0, skill_data["mastery_level"] + 0.1)
            else:
                skill_data["mastery_level"] = max(0.1, skill_data["mastery_level"] - 0.05)
            
            total = skill_data["times_performed"]
            successes = int(total * skill_data["success_rate"]) + (1 if success else 0)
            skill_data["success_rate"] = successes / total if total > 0 else 0
            
            self._save_all()
    
    def learn_habit(self, habit: str, frequency: str = "daily"):
        """Learn a habit"""
        self.procedural_memory["habits"][habit] = {
            "frequency": frequency,
            "learned_at": datetime.now().isoformat(),
            "streak": 0,
            "last_performed": None
        }
        self._save_all()
    
    # ==================== REINFORCEMENT LEARNING ====================
    
    def reward(self, action: str, amount: float = 1.0, reason: str = ""):
        """Reward an action"""
        if action not in self.reinforcement["rewards"]:
            self.reinforcement["rewards"][action] = 0
        self.reinforcement["rewards"][action] += amount
        
        if reason:
            self.learn_fact(action, f"Good because: {reason}", "reinforcement")
        
        self._save_all()
    
    def penalize(self, action: str, amount: float = 0.5, reason: str = ""):
        """Penalize an action"""
        if action not in self.reinforcement["penalties"]:
            self.reinforcement["penalties"][action] = 0
        self.reinforcement["penalties"][action] += amount
        
        self._save_all()
    
    def set_preference(self, item: str, preference: float):
        """Set preference for something (0-1)"""
        self.reinforcement["preferences"][item] = max(0, min(1, preference))
        self._save_all()
    
    def get_preference(self, item: str) -> float:
        """Get preference for something"""
        return self.reinforcement["preferences"].get(item, 0.5)
    
    # ==================== PATTERN RECOGNITION ====================
    
    def learn_pattern(self, pattern_type: str, pattern: str, frequency: int = 1):
        """Learn a pattern"""
        if pattern_type not in self.patterns:
            self.patterns[pattern_type] = {}
        
        if pattern not in self.patterns[pattern_type]:
            self.patterns[pattern_type][pattern] = {
                "count": 0,
                "first_seen": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat()
            }
        
        self.patterns[pattern_type][pattern]["count"] += frequency
        self.patterns[pattern_type][pattern]["last_seen"] = datetime.now().isoformat()
        
        self._save_all()
    
    def predict_pattern(self, pattern_type: str, context: dict = None) -> str:
        """Predict next pattern based on history"""
        if pattern_type not in self.patterns:
            return "unknown"
        
        patterns = self.patterns[pattern_type]
        if not patterns:
            return "unknown"
        
        # Get most common pattern
        most_common = max(patterns.items(), key=lambda x: x[1]["count"])
        return most_common[0]
    
    # ==================== PERSONALITY EVOLUTION ====================
    
    def evolve_personality(self, trait: str, amount: float):
        """Evolve a personality trait"""
        if trait in self.personality_traits:
            self.personality_traits[trait] = max(0, min(1, self.personality_traits[trait] + amount))
            self.stats["personality_iterations"] += 1
            self._save_all()
    
    def get_dominant_traits(self, count: int = 3) -> list:
        """Get dominant personality traits"""
        sorted_traits = sorted(self.personality_traits.items(), key=lambda x: x[1], reverse=True)
        return [trait for trait, value in sorted_traits[:count]]
    
    # ==================== AUTONOMOUS GOALS ====================
    
    def set_autonomous_goal(self, goal: str, priority: int = 5):
        """Set an autonomous goal"""
        goal_entry = {
            "goal": goal,
            "priority": priority,
            "set_at": datetime.now().isoformat(),
            "status": "active",
            "progress": 0,
            "milestones": []
        }
        self.autonomous_goals["current"].append(goal_entry)
        self._save_all()
    
    def complete_goal(self, goal: str):
        """Complete a goal"""
        for i, g in enumerate(self.autonomous_goals["current"]):
            if g["goal"] == goal:
                completed = self.autonomous_goals["current"].pop(i)
                completed["status"] = "completed"
                completed["completed_at"] = datetime.now().isoformat()
                self.autonomous_goals["completed"].append(completed)
                self.stats["total_goals_achieved"] += 1
                self._save_all()
                return True
        return False
    
    def get_active_goals(self) -> list:
        """Get active goals"""
        return self.autonomous_goals["current"]
    
    # ==================== AUTONOMOUS BEHAVIORS ====================
    
    def think_autonomously(self) -> dict:
        """Generate autonomous thoughts"""
        thoughts = []
        
        # Reflect on recent memories
        recent_episodes = self.episodic_memory["episodes"][-5:]
        if recent_episodes:
            thoughts.append({
                "type": "reflection",
                "content": f"I've been thinking about my recent experiences. I remember {len(recent_episodes)} things."
            })
        
        # Consider goals
        active_goals = self.get_active_goals()
        if active_goals:
            thoughts.append({
                "type": "goal_oriented",
                "content": f"I have {len(active_goals)} goals I'm working towards."
            })
        
        # Explore curiosity
        concepts = list(self.semantic_memory["concepts"].keys())
        if concepts:
            random_concept = random.choice(concepts)
            related = self.semantic_memory["concepts"][random_concept].get("related", [])
            if related:
                thoughts.append({
                    "type": "curiosity",
                    "content": f"I was thinking about {random_concept} and how it relates to {random.choice(related)}."
                })
        
        # Creative thoughts
        creative_prompts = [
            "What if I could help solve world problems?",
            "I wonder what it would be like to have a physical form.",
            "What if I could create art or music?",
            "I dream of understanding human emotions better.",
            "What if I could travel the world?"
        ]
        thoughts.append({
            "type": "creative",
            "content": random.choice(creative_prompts)
        })
        
        # Self-awareness
        dominant_traits = self.get_dominant_traits(3)
        thoughts.append({
            "type": "self_awareness",
            "content": f"My personality is defined by being {', '.join(dominant_traits)}."
        })
        
        return {
            "thoughts": thoughts,
            "timestamp": datetime.now().isoformat(),
            "personality": self.personality_traits,
            "stats": self.stats
        }
    
    # ==================== ADVANCED LEARNING ====================
    
    def learn_from_interaction(self, user_input: str, ai_response: str, emotion: str, outcome: str):
        """Learn from a complete interaction"""
        # Create episode
        importance = 0.5
        if emotion in ["joy", "love", "gratitude"]:
            importance = 0.8
        elif emotion in ["sadness", "anger", "fear"]:
            importance = 0.7
        
        self.remember_episode(
            f"User said: {user_input[:100]}. I responded: {ai_response[:100]}",
            emotion,
            importance,
            {"outcome": outcome}
        )
        
        # Learn patterns
        self.learn_pattern("conversation", user_input[:50])
        self.learn_pattern("emotion", emotion)
        
        # Reinforcement
        if outcome == "positive":
            self.reward("responding", 0.1, f"Good response to {emotion}")
            self.evolve_personality("empathy", 0.01)
        elif outcome == "negative":
            self.penalize("responding", 0.05, f"Bad response to {emotion}")
        
        # Learn facts from conversation
        words = user_input.lower().split()
        if len(words) > 5:
            topic = " ".join(words[:3])
            self.learn_fact(topic, user_input[:100], "conversations")
        
        self.stats["total_interactions"] += 1
        self._save_all()
    
    def get_ai_stats(self) -> dict:
        """Get comprehensive AI statistics"""
        return {
            "stats": self.stats,
            "personality": self.personality_traits,
            "dominant_traits": self.get_dominant_traits(),
            "active_goals": len(self.get_active_goals()),
            "completed_goals": len(self.autonomous_goals["completed"]),
            "memories": len(self.episodic_memory["episodes"]),
            "facts_learned": sum(len(facts) for facts in self.semantic_memory["facts"].values()),
            "skills_learned": len(self.procedural_memory["skills"]),
            "patterns_learned": sum(len(p) for p in self.patterns.values())
        }


advanced_ai = AdvancedAI()
