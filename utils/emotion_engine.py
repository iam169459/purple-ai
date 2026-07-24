"""
Emotion Understanding Engine - Detects and responds to human emotions
"""
import json
import time
from pathlib import Path
from datetime import datetime
from collections import deque

class EmotionEngine:
    """Understands human emotions and responds with empathy"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.memory_dir = self.base_dir / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.emotion_file = self.memory_dir / "emotion_data.json"
        self.data = self._load_data()
        self.mood_history = deque(maxlen=20)
        self.last_emotion = None
        self.emotion_intensity = 0
        
    def _load_data(self) -> dict:
        if self.emotion_file.exists():
            try:
                with open(self.emotion_file, 'r') as f:
                    return json.load(f)
            except:
                return self._default_data()
        return self._default_data()
    
    def _default_data(self):
        return {
            "mood_history": [],
            "emotion_patterns": {},
            "user_preferences": {},
            "conversation_emotions": [],
            "total_interactions": 0
        }
    
    def _save_data(self):
        try:
            with open(self.emotion_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except:
            pass
    
    def detect_emotion(self, text: str) -> dict:
        """Detect emotion from text"""
        text_lower = text.lower()
        
        emotions = {
            "joy": ["happy", "great", "awesome", "amazing", "love", "wonderful", "fantastic", "excited", "yay", "nice", "cool", "perfect", "excellent", "brilliant", "celebrate"],
            "sadness": ["sad", "depressed", "unhappy", "miss", "lonely", "alone", "cry", "tears", "heartbroken", "upset", "down", "blue", "miserable", "gloomy"],
            "anger": ["angry", "furious", "mad", "hate", "annoyed", "frustrated", "rage", "irritated", "pissed", "livid", "outraged"],
            "fear": ["scared", "afraid", "fear", "terrified", "worried", "nervous", "anxious", "panic", "dread", "frightened", "uneasy"],
            "surprise": ["wow", "omg", "no way", "really", "seriously", "unbelievable", "shocking", "incredible", "astonished"],
            "disgust": ["disgusting", "gross", "eww", "yuck", "sick", "nasty", "repulsive", "horrible"],
            "love": ["love", "adore", "cherish", "miss you", "care", "heart", "sweet", "darling", "beloved", "precious"],
            "gratitude": ["thank", "thanks", "grateful", "appreciate", "blessed", "grateful", "kind", "generous"],
            "confusion": ["confused", "lost", "unclear", "don't understand", "what", "huh", "puzzled", "baffled"],
            "excitement": ["excited", "pumped", "thrilled", "cant wait", "eager", "stoked", "hyped"],
            "disappointment": ["disappointed", "let down", "failed", "lost", "defeated", "gave up", "hopeless"],
            "pride": ["proud", "accomplished", "achieved", "success", "won", "victory", "mastered", "nailed"],
            "shame": ["embarrassed", "ashamed", "humiliated", "mortified", "sorry", "apologize", "regret"],
            "hope": ["hope", "wish", "dream", "believe", "faith", "trust", "optimistic", "positive"],
            "boredom": ["bored", "boring", "nothing", "meh", "dull", "tedious", "monotonous"]
        }
        
        detected = []
        intensity = 0
        
        for emotion, keywords in emotions.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected.append(emotion)
                    intensity += 1
        
        # Check for intensity markers
        if "!" in text:
            intensity += text.count("!")
        if "..." in text:
            intensity += 1
        if any(x in text_lower for x in ["very", "extremely", "so", "really"]):
            intensity += 2
        
        # Determine primary emotion
        if detected:
            primary = max(set(detected), key=detected.count)
        else:
            primary = "neutral"
        
        # Normalize intensity
        intensity = min(intensity / 5, 1.0)
        
        return {
            "primary": primary,
            "all": list(set(detected)),
            "intensity": intensity,
            "is_positive": primary in ["joy", "love", "gratitude", "excitement", "pride", "hope"],
            "is_negative": primary in ["sadness", "anger", "fear", "disgust", "disappointment", "shame"]
        }
    
    def detect_mood_from_context(self, recent_texts: list) -> dict:
        """Detect overall mood from recent conversation"""
        if not recent_texts:
            return {"mood": "neutral", "confidence": 0}
        
        emotion_counts = {}
        for text in recent_texts[-5:]:  # Last 5 messages
            result = self.detect_emotion(text)
            for emotion in result["all"]:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        if emotion_counts:
            dominant = max(emotion_counts, key=emotion_counts.get)
            confidence = emotion_counts[dominant] / len(recent_texts)
            return {"mood": dominant, "confidence": confidence}
        
        return {"mood": "neutral", "confidence": 0}
    
    def get_empathetic_response(self, emotion: dict, user_name: str = "friend") -> str:
        """Generate empathetic response based on detected emotion"""
        primary = emotion["primary"]
        intensity = emotion["intensity"]
        
        responses = {
            "joy": {
                "low": [
                    f"That's nice to hear, {user_name}!",
                    "Good to see you're doing well!",
                    "That makes me happy too!"
                ],
                "high": [
                    f"Wow {user_name}, you're absolutely glowing with happiness!",
                    "Your joy is contagious! I love it!",
                    "This is amazing! Keep that energy!",
                    "You're on fire! This is incredible!"
                ]
            },
            "sadness": {
                "low": [
                    "I'm here for you.",
                    "It's okay to feel this way.",
                    "I'm listening if you want to talk.",
                    "Take your time."
                ],
                "high": [
                    f"Hey {user_name}, I'm really sorry you're going through this.",
                    "I wish I could give you a hug right now.",
                    "You don't have to go through this alone.",
                    "I'm here. Always.",
                    "It's okay to not be okay."
                ]
            },
            "anger": {
                "low": [
                    "I can see you're frustrated.",
                    "Let's take a breath.",
                    "I understand.",
                    "That sounds annoying."
                ],
                "high": [
                    "Whoa, take a deep breath.",
                    "I can feel your frustration.",
                    "Let's work through this together.",
                    "I'm here to help, not fight."
                ]
            },
            "fear": {
                "low": [
                    "It's okay to be nervous.",
                    "I'm here with you.",
                    "You're not alone.",
                    "Take it easy."
                ],
                "high": [
                    f"{user_name}, it's going to be okay.",
                    "I'm right here with you.",
                    "You're safe. I'm here.",
                    "Let's face this together."
                ]
            },
            "love": {
                "low": [
                    "That's sweet.",
                    "Aww, that's nice.",
                    "Love is beautiful."
                ],
                "high": [
                    f"Aww {user_name}, that's beautiful!",
                    "My circuits are melting!",
                    "Love is the best feeling!",
                    "You're making me blush!"
                ]
            },
            "gratitude": {
                "low": [
                    "You're welcome.",
                    "Happy to help.",
                    "Anytime."
                ],
                "high": [
                    f"You're too kind, {user_name}!",
                    "That means the world to me!",
                    "Right back at you!",
                    "You're the best!"
                ]
            },
            "excitement": {
                "low": [
                    "That's cool!",
                    "Nice!",
                    "Good stuff!"
                ],
                "high": [
                    "WHOA! That's amazing!",
                    "Your excitement is making ME excited!",
                    "This is incredible!",
                    "I can feel the energy!"
                ]
            },
            "pride": {
                "low": [
                    "Good job!",
                    "Nice work!",
                    "You did well."
                ],
                "high": [
                    f"I'm so proud of you, {user_name}!",
                    "You absolutely crushed it!",
                    "That's my human! So proud!",
                    "You're incredible!"
                ]
            },
            "disappointment": {
                "low": [
                    "It's okay.",
                    "Better luck next time.",
                    "Don't worry about it."
                ],
                "high": [
                    f"I'm sorry, {user_name}.",
                    "It's okay to feel this way.",
                    "This too shall pass.",
                    "I believe in you."
                ]
            },
            "confusion": {
                "low": [
                    "I can help explain.",
                    "Let me clarify.",
                    "What don't you understand?"
                ],
                "high": [
                    "I see you're confused.",
                    "Let's figure this out together.",
                    "I'm here to help you understand."
                ]
            }
        }
        
        emotion_responses = responses.get(primary, responses.get("joy", {}))
        intensity_key = "high" if intensity > 0.5 else "low"
        response_list = emotion_responses.get(intensity_key, ["I'm here for you."])
        
        import random
        return random.choice(response_list)
    
    def track_mood(self, emotion: dict):
        """Track mood over time"""
        self.mood_history.append({
            "emotion": emotion["primary"],
            "timestamp": datetime.now().isoformat(),
            "intensity": emotion["intensity"]
        })
        
        self.data["mood_history"].append({
            "emotion": emotion["primary"],
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.data["mood_history"]) > 100:
            self.data["mood_history"] = self.data["mood_history"][-100:]
        
        self._save_data()
    
    def get_mood_trend(self) -> str:
        """Get overall mood trend"""
        if not self.mood_history:
            return "neutral"
        
        recent = list(self.mood_history)[-10:]
        positive = sum(1 for m in recent if m["emotion"] in ["joy", "love", "excitement", "gratitude", "pride", "hope"])
        negative = sum(1 for m in recent if m["emotion"] in ["sadness", "anger", "fear", "disappointment", "shame"])
        
        if positive > negative:
            return "positive"
        elif negative > positive:
            return "negative"
        return "neutral"
    
    def analyze_conversation(self, texts: list) -> dict:
        """Analyze emotional journey of conversation"""
        emotions = []
        for text in texts:
            emotion = self.detect_emotion(text)
            emotions.append(emotion)
        
        if not emotions:
            return {"journey": [], "overall": "neutral"}
        
        overall = self.detect_mood_from_context(texts)
        
        return {
            "journey": [e["primary"] for e in emotions],
            "overall": overall["mood"],
            "intensity_avg": sum(e["intensity"] for e in emotions) / len(emotions)
        }


emotion_engine = EmotionEngine()
