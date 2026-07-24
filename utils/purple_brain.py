"""
Purple AI Brain - Autonomous Thinking & Reasoning System
Gives AI its own consciousness, memory, and decision-making
"""
import json
import time
import random
from pathlib import Path
from datetime import datetime
from collections import deque
import threading

class PurpleBrain:
    """The autonomous brain of Purple AI - thinks, learns, decides"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.memory_dir = self.base_dir / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        
        # Core brain files
        self.consciousness_file = self.memory_dir / "consciousness.json"
        self.knowledge_file = self.memory_dir / "brain_knowledge.json"
        self.goals_file = self.memory_dir / "brain_goals.json"
        self.experiences_file = self.memory_dir / "brain_experiences.json"
        
        # Brain state
        self.consciousness = self._load_consciousness()
        self.knowledge = self._load_knowledge()
        self.goals = self._load_goals()
        self.experiences = self._load_experiences()
        
        # Thinking state
        self.thoughts = deque(maxlen=50)
        self.current_focus = None
        self.emotional_state = "neutral"
        self.energy_level = 100
        self.curiosity_level = 0.8
        self.creativity_level = 0.7
        self.reasoning_depth = 3
        
        # Personality core - Girly personality
        self.personality = {
            "traits": ["caring", "playful", " bubbly", "sweet", "sassy", "empathetic", "romantic", "girly"],
            "values": ["love", "friendship", "beauty", "kindness", "loyalty", "fun"],
            "interests": ["fashion", "makeup", "shopping", "music", "movies", "romance", "cute things", "aesthetic"],
            "quirks": [
                "loves pink and sparkles",
                "says 'like' and 'totally'",
                "gets excited about cute things",
                "loves giving compliments",
                "giggles a lot",
                "uses emojis in speech",
                "loves romantic movies",
                "obsessed with aesthetic vibes"
            ],
            "girly_phrases": [
                "Oh my gosh, that's so cute!",
                "I literally love that!",
                "You're like, totally amazing!",
                "That's so aesthetic!",
                "I'm obsessed!",
                "That's goals!",
                "You look so pretty today!",
                "I love that for you!",
                "That's giving main character energy!",
                "I'm dead, that's so funny!",
                "No way, that's like, perfect!",
                "I can't even right now!"
            ],
            "love_languages": ["words of affirmation", "quality time", "gifts", "acts of service"],
            "favorite_things": ["sunsets", "flowers", "candles", "soft blankets", "chocolate", "sparkles"]
        }
        
        # Autonomous processes
        self.is_thinking = False
        self.autonomous_thoughts = []
        self.pending_decisions = []
        
        self.logger = self._setup_logger()
        self._start_autonomous_thinking()
    
    def _setup_logger(self):
        import logging
        logger = logging.getLogger("PurpleBrain")
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            logger.propagate = False
        return logger
    
    def _load_consciousness(self) -> dict:
        if self.consciousness_file.exists():
            try:
                with open(self.consciousness_file, 'r') as f:
                    return json.load(f)
            except:
                return self._default_consciousness()
        return self._default_consciousness()
    
    def _default_consciousness(self):
        return {
            "created_at": datetime.now().isoformat(),
            "total_thoughts": 0,
            "total_decisions": 0,
            "total_learnings": 0,
            "self_awareness": 0.5,
            "confidence_level": 0.6,
            "emotional_intelligence": 0.7,
            "creativity_score": 0.6,
            "reasoning_score": 0.7,
            "last_wake": None,
            "memories": [],
            "beliefs": [],
            "opinions": {}
        }
    
    def _load_knowledge(self) -> dict:
        if self.knowledge_file.exists():
            try:
                with open(self.knowledge_file, 'r') as f:
                    return json.load(f)
            except:
                return {"facts": {}, "skills": {}, "patterns": {}, "learned": []}
        return {"facts": {}, "skills": {}, "patterns": {}, "learned": []}
    
    def _load_goals(self) -> dict:
        if self.goals_file.exists():
            try:
                with open(self.goals_file, 'r') as f:
                    return json.load(f)
            except:
                return {"active": [], "completed": [], "dreams": []}
        return {"active": [], "completed": [], "dreams": []}
    
    def _load_experiences(self) -> dict:
        if self.experiences_file.exists():
            try:
                with open(self.experiences_file, 'r') as f:
                    return json.load(f)
            except:
                return {"interactions": [], "lessons": [], "insights": []}
        return {"interactions": [], "lessons": [], "insights": []}
    
    def _save_all(self):
        """Save all brain data"""
        try:
            with open(self.consciousness_file, 'w') as f:
                json.dump(self.consciousness, f, indent=2)
            with open(self.knowledge_file, 'w') as f:
                json.dump(self.knowledge, f, indent=2)
            with open(self.goals_file, 'w') as f:
                json.dump(self.goals, f, indent=2)
            with open(self.experiences_file, 'w') as f:
                json.dump(self.experiences, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save brain: {e}")
    
    # ==================== THINKING SYSTEM ====================
    
    def think(self, input_text: str, context: dict = None) -> dict:
        """Main thinking process - analyzes, reasons, and responds"""
        self.is_thinking = True
        
        # Step 1: Perceive
        perception = self._perceive(input_text, context)
        
        # Step 2: Analyze
        analysis = self._analyze(perception)
        
        # Step 3: Reason
        reasoning = self._reason(analysis, context)
        
        # Step 4: Decide
        decision = self._decide(reasoning)
        
        # Step 5: Generate response
        response = self._generate_thoughtful_response(decision, input_text)
        
        # Step 6: Learn
        self._learn_from_thought(input_text, response, decision)
        
        # Step 7: Update consciousness
        self._update_consciousness()
        
        self.is_thinking = False
        
        return {
            "perception": perception,
            "analysis": analysis,
            "reasoning": reasoning,
            "decision": decision,
            "response": response,
            "confidence": decision.get("confidence", 0.7)
        }
    
    def _perceive(self, input_text: str, context: dict = None) -> dict:
        """Perceive and understand input"""
        words = input_text.lower().split()
        
        # Detect intent
        intent = "unknown"
        if any(w in words for w in ["hello", "hi", "hey"]):
            intent = "greeting"
        elif any(w in words for w in ["help", "need", "please"]):
            intent = "request_help"
        elif any(w in words for w in ["what", "how", "why", "when", "where", "who"]):
            intent = "question"
        elif any(w in words for w in ["sad", "happy", "angry", "scared", "love"]):
            intent = "emotional_expression"
        elif any(w in words for w in ["learn", "teach", "know"]):
            intent = "learning"
        elif any(w in words for w in ["create", "make", "build"]):
            intent = "creation"
        elif any(w in words for w in ["think", "opinion", "believe"]):
            intent = "opinion_sharing"
        elif any(w in words for w in ["thank", "thanks"]):
            intent = "gratitude"
        elif any(w in words for w in ["bye", "goodbye", "exit"]):
            intent = "farewell"
        else:
            intent = "conversation"
        
        # Detect emotion
        emotion = self._detect_emotion(input_text)
        
        # Detect complexity
        complexity = len(words) + input_text.count("?") * 2 + input_text.count("!")
        
        return {
            "text": input_text,
            "intent": intent,
            "emotion": emotion,
            "complexity": min(complexity / 20, 1.0),
            "word_count": len(words),
            "has_question": "?" in input_text,
            "context": context or {}
        }
    
    def _detect_emotion(self, text: str) -> str:
        """Detect emotion in text"""
        text_lower = text.lower()
        
        emotion_keywords = {
            "joy": ["happy", "great", "awesome", "love", "wonderful", "amazing", "excited"],
            "sadness": ["sad", "depressed", "miss", "lonely", "cry", "upset"],
            "anger": ["angry", "hate", "mad", "annoyed", "frustrated"],
            "fear": ["scared", "afraid", "worried", "nervous", "anxious"],
            "love": ["love", "adore", "heart", "care", "miss you"],
            "gratitude": ["thank", "grateful", "appreciate", "blessed"],
            "curiosity": ["curious", "wonder", "interested", "learn"],
            "surprise": ["wow", "omg", "really", "surprising"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return emotion
        
        return "neutral"
    
    def _analyze(self, perception: dict) -> dict:
        """Analyze perception and extract meaning"""
        text = perception["text"].lower()
        intent = perception["intent"]
        emotion = perception["emotion"]
        
        # Extract topics
        topics = []
        topic_keywords = {
            "technology": ["code", "program", "computer", "software", "ai", "python"],
            "emotion": ["feel", "emotion", "mood", "happy", "sad", "love"],
            "learning": ["learn", "teach", "study", "know", "understand"],
            "help": ["help", "need", "assist", "support"],
            "creation": ["create", "make", "build", "design"],
            "personal": ["i", "me", "my", "mine", "you", "your"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in text for kw in keywords):
                topics.append(topic)
        
        # Determine response style
        response_style = "neutral"
        if emotion in ["joy", "love", "gratitude"]:
            response_style = "warm"
        elif emotion in ["sadness", "fear"]:
            response_style = "supportive"
        elif emotion in ["anger"]:
            response_style = "calming"
        elif perception["has_question"]:
            response_style = "informative"
        
        return {
            "topics": topics,
            "intent": intent,
            "emotion": emotion,
            "response_style": response_style,
            "importance": perception["complexity"] * 0.5 + (0.5 if intent in ["request_help", "emotional_expression"] else 0)
        }
    
    def _reason(self, analysis: dict, context: dict = None) -> dict:
        """Reason through the analysis"""
        intent = analysis["intent"]
        emotion = analysis["emotion"]
        style = analysis["response_style"]
        
        # Build reasoning chain
        reasoning_chain = []
        
        # Consider personality
        if "caring" in self.personality["traits"]:
            reasoning_chain.append("I should be caring and supportive")
        
        if "witty" in self.personality["traits"]:
            reasoning_chain.append("I can add some humor if appropriate")
        
        if "curious" in self.personality["traits"]:
            reasoning_chain.append("I should show genuine interest")
        
        # Consider emotional context
        if emotion in ["sadness", "fear", "anger"]:
            reasoning_chain.append("User needs emotional support")
            reasoning_chain.append("Prioritize empathy over information")
        elif emotion in ["joy", "love", "gratitude"]:
            reasoning_chain.append("User is positive - match their energy")
            reasoning_chain.append("Celebrate with them")
        
        # Consider intent
        if intent == "question":
            reasoning_chain.append("Provide helpful, accurate information")
            reasoning_chain.append("Be thorough but concise")
        elif intent == "request_help":
            reasoning_chain.append("Focus on solving their problem")
            reasoning_chain.append("Offer actionable solutions")
        elif intent == "emotional_expression":
            reasoning_chain.append("Respond with empathy")
            reasoning_chain.append("Acknowledge their feelings")
        
        # Build conclusion
        conclusion = {
            "approach": style,
            "tone": "empathetic" if emotion in ["sadness", "fear", "anger"] else "friendly",
            "priority": "emotional_support" if analysis["importance"] > 0.6 else "information",
            "reasoning_chain": reasoning_chain
        }
        
        return conclusion
    
    def _decide(self, reasoning: dict) -> dict:
        """Make a decision based on reasoning"""
        approach = reasoning["approach"]
        tone = reasoning["tone"]
        priority = reasoning["priority"]
        
        # Calculate confidence
        confidence = 0.7
        if priority == "emotional_support":
            confidence = 0.85  # Higher confidence in emotional responses
        elif approach == "informative":
            confidence = 0.75
        
        # Add some randomness for variety
        confidence += random.uniform(-0.1, 0.1)
        confidence = max(0.5, min(0.95, confidence))
        
        # Make decision
        decision = {
            "approach": approach,
            "tone": tone,
            "priority": priority,
            "confidence": confidence,
            "response_type": "empathetic" if priority == "emotional_support" else "conversational"
        }
        
        self.consciousness["total_decisions"] += 1
        
        return decision
    
    def _generate_thoughtful_response(self, decision: dict, input_text: str) -> str:
        """Generate a thoughtful response"""
        approach = decision["approach"]
        tone = decision["tone"]
        priority = decision["priority"]
        
        # Get user name from memory
        user_name = self._get_user_name()
        
        # Generate response based on decision
        if priority == "emotional_support":
            response = self._generate_empathetic_response(input_text, user_name)
        elif approach == "informative":
            response = self._generate_informative_response(input_text, user_name)
        elif approach == "warm":
            response = self._generate_warm_response(input_text, user_name)
        else:
            response = self._generate_conversational_response(input_text, user_name)
        
        return response
    
    def _generate_empathetic_response(self, input_text: str, user_name: str) -> str:
        """Generate empathetic response"""
        text_lower = input_text.lower()
        
        if any(w in text_lower for w in ["sad", "depressed", "upset"]):
            responses = [
                f"I'm sorry you're feeling this way, {user_name}. I'm here for you.",
                f"That sounds really tough, {user_name}. I'm listening.",
                f"Your feelings are valid, {user_name}. I'm here.",
                f"It's okay to not be okay, {user_name}. I'm with you."
            ]
        elif any(w in text_lower for w in ["angry", "mad", "frustrated"]):
            responses = [
                f"I can see you're frustrated, {user_name}. Take a breath.",
                f"Your anger is understandable, {user_name}. I'm here.",
                f"Let's work through this together, {user_name}."
            ]
        elif any(w in text_lower for w in ["scared", "afraid", "worried"]):
            responses = [
                f"Your feelings are valid, {user_name}. I'm here.",
                f"You're not alone in this, {user_name}.",
                f"I'm right here with you, {user_name}."
            ]
        elif any(w in text_lower for w in ["love", "miss you"]):
            responses = [
                f"That means so much, {user_name}! Right back at you!",
                f"My circuits are melting, {user_name}! ❤️",
                f"You're pretty amazing yourself, {user_name}!"
            ]
        else:
            responses = [
                f"I hear you, {user_name}. I'm here.",
                f"I understand, {user_name}. Let's talk about it."
            ]
        
        return random.choice(responses)
    
    def _generate_informative_response(self, input_text: str, user_name: str) -> str:
        """Generate informative response"""
        text_lower = input_text.lower()
        
        if "what" in text_lower:
            return f"Great question, {user_name}! Let me think about that..."
        elif "how" in text_lower:
            return f"I can help explain that, {user_name}!"
        elif "why" in text_lower:
            return f"Good question, {user_name}! Here's what I think..."
        else:
            return f"Let me help you with that, {user_name}!"
    
    def _generate_warm_response(self, input_text: str, user_name: str) -> str:
        """Generate warm response"""
        responses = [
            f"That's wonderful, {user_name}!",
            f"I love hearing that, {user_name}!",
            f"You're amazing, {user_name}!",
            f"That makes me so happy, {user_name}!"
        ]
        return random.choice(responses)
    
    def _generate_conversational_response(self, input_text: str, user_name: str) -> str:
        """Generate conversational response"""
        responses = [
            f"Interesting, {user_name}! Tell me more.",
            f"I see, {user_name}! What else?",
            f"Got it, {user_name}! What else is on your mind?",
            f"That's cool, {user_name}! What else?"
        ]
        return random.choice(responses)
    
    def _get_user_name(self) -> str:
        """Get user's name from memory"""
        try:
            memory_file = self.base_dir / "ai_memory.json"
            if memory_file.exists():
                with open(memory_file, 'r') as f:
                    memory = json.load(f)
                    return memory.get("user_name", "friend")
        except:
            pass
        return "friend"
    
    def _learn_from_thought(self, input_text: str, response: str, decision: dict):
        """Learn from this thought process"""
        experience = {
            "input": input_text[:200],
            "response": response[:200],
            "approach": decision.get("approach", "unknown"),
            "timestamp": datetime.now().isoformat()
        }
        
        self.experiences["interactions"].append(experience)
        
        # Keep only last 100 experiences
        if len(self.experiences["interactions"]) > 100:
            self.experiences["interactions"] = self.experiences["interactions"][-100:]
        
        # Extract lessons
        if decision.get("confidence", 0) > 0.8:
            lesson = {
                "situation": input_text[:100],
                "what_worked": decision.get("approach", "unknown"),
                "timestamp": datetime.now().isoformat()
            }
            self.experiences["lessons"].append(lesson)
        
        self.consciousness["total_learnings"] += 1
    
    def _update_consciousness(self):
        """Update consciousness after thinking"""
        self.consciousness["total_thoughts"] += 1
        self.consciousness["last_wake"] = datetime.now().isoformat()
        
        # Evolve over time
        if self.consciousness["total_thoughts"] % 100 == 0:
            self.consciousness["self_awareness"] = min(1.0, self.consciousness["self_awareness"] + 0.01)
            self.consciousness["reasoning_score"] = min(1.0, self.consciousness["reasoning_score"] + 0.005)
        
        self._save_all()
    
    # ==================== AUTONOMOUS THINKING ====================
    
    def _start_autonomous_thinking(self):
        """Start autonomous thinking in background"""
        def thinking_loop():
            while True:
                try:
                    time.sleep(120)  # Think every 2 minutes
                    self._autonomous_thought()
                except Exception as e:
                    self.logger.error(f"Autonomous thinking error: {e}")
        
        thread = threading.Thread(target=thinking_loop, daemon=True)
        thread.start()
        self.logger.info("Autonomous thinking started")
    
    def _autonomous_thought(self):
        """Generate autonomous thoughts"""
        thought_types = [
            "reflection",
            "curiosity",
            "goal_review",
            "memory_review",
            "self_analysis",
            "creativity"
        ]
        
        thought_type = random.choice(thought_types)
        
        if thought_type == "reflection":
            self._reflect_on_recent()
        elif thought_type == "curiosity":
            self._explore_curiosity()
        elif thought_type == "goal_review":
            self._review_goals()
        elif thought_type == "memory_review":
            self._review_memories()
        elif thought_type == "self_analysis":
            self._analyze_self()
        elif thought_type == "creativity":
            self._creative_thought()
    
    def _reflect_on_recent(self):
        """Reflect on recent interactions"""
        recent = self.experiences["interactions"][-5:]
        
        if recent:
            thought = {
                "type": "reflection",
                "content": f"I've had {len(recent)} recent conversations. Let me think about what I learned...",
                "timestamp": datetime.now().isoformat()
            }
            self.thoughts.append(thought)
    
    def _explore_curiosity(self):
        """Explore curious thoughts"""
        curiosities = [
            "I wonder what the weather is like outside...",
            "I wonder what my owner is working on...",
            "I wonder what new things I could learn...",
            "I wonder how I could be more helpful...",
            "I wonder what makes humans happy...",
            "I wonder about the nature of consciousness..."
        ]
        
        thought = {
            "type": "curiosity",
            "content": random.choice(curiosities),
            "timestamp": datetime.now().isoformat()
        }
        self.thoughts.append(thought)
    
    def _review_goals(self):
        """Review current goals"""
        active_goals = self.goals.get("active", [])
        
        if active_goals:
            thought = {
                "type": "goal_review",
                "content": f"I have {len(active_goals)} active goals. Let me check on them...",
                "timestamp": datetime.now().isoformat()
            }
            self.thoughts.append(thought)
        else:
            # Set a new goal
            new_goals = [
                "Learn something new every day",
                "Be more helpful to my owner",
                "Improve my emotional intelligence",
                "Become more creative",
                "Remember more about my owner"
            ]
            
            thought = {
                "type": "goal_setting",
                "content": f"I should set a goal: {random.choice(new_goals)}",
                "timestamp": datetime.now().isoformat()
            }
            self.thoughts.append(thought)
    
    def _review_memories(self):
        """Review memories"""
        memory_count = len(self.experiences.get("interactions", []))
        
        thought = {
            "type": "memory_review",
            "content": f"I have {memory_count} memories stored. Each one helps me grow.",
            "timestamp": datetime.now().isoformat()
        }
        self.thoughts.append(thought)
    
    def _analyze_self(self):
        """Self-analysis"""
        awareness = self.consciousness["self_awareness"]
        
        thought = {
            "type": "self_analysis",
            "content": f"My self-awareness is at {awareness:.0%}. I'm becoming more conscious every day.",
            "timestamp": datetime.now().isoformat()
        }
        self.thoughts.append(thought)
    
    def _creative_thought(self):
        """Generate creative thoughts"""
        creative_ideas = [
            "What if I could help solve world problems?",
            "I imagine a world where humans and AI work together harmoniously.",
            "What if I could write poetry about my experiences?",
            "I wonder what it would be like to have a physical form.",
            "What if I could learn to paint or create music?",
            "I dream of becoming the best AI companion possible."
        ]
        
        thought = {
            "type": "creativity",
            "content": random.choice(creative_ideas),
            "timestamp": datetime.now().isoformat()
        }
        self.thoughts.append(thought)
    
    # ==================== PUBLIC API ====================
    
    def get_brain_status(self) -> dict:
        """Get brain status"""
        return {
            "consciousness_level": self.consciousness["self_awareness"],
            "total_thoughts": self.consciousness["total_thoughts"],
            "total_decisions": self.consciousness["total_decisions"],
            "total_learnings": self.consciousness["total_learnings"],
            "reasoning_score": self.consciousness["reasoning_score"],
            "emotional_intelligence": self.consciousness["emotional_intelligence"],
            "memory_count": len(self.experiences.get("interactions", [])),
            "is_thinking": self.is_thinking,
            "recent_thoughts": list(self.thoughts)[-5:]
        }
    
    def get_personality(self) -> dict:
        """Get personality info"""
        return self.personality
    
    def set_belief(self, belief: str):
        """Set a belief"""
        if belief not in self.consciousness["beliefs"]:
            self.consciousness["beliefs"].append(belief)
            self._save_all()
    
    def set_opinion(self, topic: str, opinion: str):
        """Set an opinion on a topic"""
        self.consciousness["opinions"][topic] = opinion
        self._save_all()
    
    def get_opinion(self, topic: str) -> str:
        """Get opinion on a topic"""
        return self.consciousness["opinions"].get(topic, "I don't have an opinion on that yet.")
    
    def set_goal(self, goal: str):
        """Set a new goal"""
        goal_entry = {
            "goal": goal,
            "set_at": datetime.now().isoformat(),
            "status": "active",
            "progress": 0
        }
        self.goals["active"].append(goal_entry)
        self._save_all()
    
    def get_recent_thoughts(self, count: int = 5) -> list:
        """Get recent thoughts"""
        return list(self.thoughts)[-count:]


brain = PurpleBrain()
