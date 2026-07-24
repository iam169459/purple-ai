"""
Emotion Understanding Engine - Detects, tracks, and responds to human emotions
Now with emotional context window, trajectory tracking, and topic-emotion memory
"""
import json
import time
from pathlib import Path
from datetime import datetime
from collections import deque


class EmotionalMemory:
    """
    Tracks emotional context across a conversation.
    Maintains a rolling window, detects trajectory, and remembers topic-emotion associations.
    """
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.emotional_context = deque(maxlen=window_size)
        self.emotional_trajectory = []  # Full history for trend analysis
        self.topic_emotions = {}  # topic → {emotion: count}
        self.user_triggers = {}   # topic → primary_emotion
        self.conversation_start_time = None
        self.last_emotion = None
        self.emotion_streak = 0  # How many messages same emotion in a row
    
    def update(self, emotion: str, intensity: float, topics: list = None):
        """Add a new emotion reading to the context window"""
        entry = {
            "emotion": emotion,
            "intensity": intensity,
            "timestamp": datetime.now().isoformat(),
            "topics": topics or []
        }
        
        self.emotional_context.append(entry)
        self.emotional_trajectory.append(entry)
        
        # Track emotion streaks
        if emotion == self.last_emotion:
            self.emotion_streak += 1
        else:
            self.emotion_streak = 0
        self.last_emotion = emotion
        
        # Track topic-emotion associations
        for topic in (topics or []):
            if topic not in self.topic_emotions:
                self.topic_emotions[topic] = {}
            self.topic_emotions[topic][emotion] = self.topic_emotions[topic].get(emotion, 0) + 1
            
            # Update trigger mapping
            if topic not in self.user_triggers:
                self.user_triggers[topic] = emotion
            else:
                # Keep the most frequent emotion
                if self.topic_emotions[topic].get(emotion, 0) > \
                   self.topic_emotions[topic].get(self.user_triggers[topic], 0):
                    self.user_triggers[topic] = emotion
    
    def get_trajectory(self) -> str:
        """
        Analyze emotional trajectory over the conversation.
        Returns: "improving" | "declining" | "stable" | "volatile" | "neutral"
        """
        if len(self.emotional_context) < 2:
            return "neutral"
        
        recent = list(self.emotional_context)[-self.window_size:]
        
        # Emotional valence scoring
        positive_emotions = {"joy", "love", "gratitude", "excitement", "pride", "hope"}
        negative_emotions = {"sadness", "anger", "fear", "disgust", "disappointment", "shame"}
        
        scores = []
        for entry in recent:
            emotion = entry["emotion"]
            intensity = entry["intensity"]
            if emotion in positive_emotions:
                scores.append(intensity)
            elif emotion in negative_emotions:
                scores.append(-intensity)
            else:
                scores.append(0)
        
        if len(scores) < 2:
            return "neutral"
        
        # Calculate trend (linear regression slope)
        n = len(scores)
        x_mean = (n - 1) / 2
        y_mean = sum(scores) / n
        
        numerator = sum((i - x_mean) * (scores[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return "stable"
        
        slope = numerator / denominator
        
        # Calculate volatility (standard deviation of changes)
        changes = [scores[i] - scores[i-1] for i in range(1, len(scores))]
        if changes:
            mean_change = sum(changes) / len(changes)
            volatility = sum((c - mean_change) ** 2 for c in changes) / len(changes)
        else:
            volatility = 0
        
        # Classify trajectory
        if volatility > 0.3:
            return "volatile"
        elif slope > 0.1:
            return "improving"
        elif slope < -0.1:
            return "declining"
        else:
            return "stable"
    
    def get_average_intensity(self) -> float:
        """Get average emotional intensity over the window"""
        if not self.emotional_context:
            return 0.0
        recent = list(self.emotional_context)[-self.window_size:]
        return sum(e["intensity"] for e in recent) / len(recent)
    
    def get_dominant_emotion(self) -> str:
        """Get the most frequent emotion in the current window"""
        if not self.emotional_context:
            return "neutral"
        
        recent = list(self.emotional_context)[-self.window_size:]
        counts = {}
        for entry in recent:
            emotion = entry["emotion"]
            counts[emotion] = counts.get(emotion, 0) + 1
        
        if counts:
            return max(counts, key=counts.get)
        return "neutral"
    
    def get_topic_emotion(self, topic: str) -> dict:
        """Get what emotions this topic typically triggers"""
        if topic in self.topic_emotions:
            return self.topic_emotions[topic]
        return {}
    
    def get_trigger_emotion(self, topic: str) -> str:
        """Get the primary emotion triggered by a topic"""
        return self.user_triggers.get(topic, "neutral")
    
    def should_be_cautious(self) -> bool:
        """Check if we should be more cautious in our response"""
        trajectory = self.get_trajectory()
        avg_intensity = self.get_average_intensity()
        
        # Be cautious if:
        # - Emotion is declining
        # - Intensity is high and negative
        # - Long streak of negative emotion
        if trajectory == "declining":
            return True
        if avg_intensity > 0.7 and self.last_emotion in ["sadness", "anger", "fear"]:
            return True
        if self.emotion_streak > 3 and self.last_emotion in ["sadness", "anger", "fear"]:
            return True
        return False
    
    def get_context_summary(self) -> dict:
        """Get a summary of the emotional context"""
        return {
            "window_size": len(self.emotional_context),
            "trajectory": self.get_trajectory(),
            "dominant_emotion": self.get_dominant_emotion(),
            "average_intensity": round(self.get_average_intensity(), 2),
            "emotion_streak": self.emotion_streak,
            "should_be_cautious": self.should_be_cautious(),
            "topics_tracked": len(self.topic_emotions),
            "recent_emotions": [
                {"emotion": e["emotion"], "intensity": e["intensity"]}
                for e in list(self.emotional_context)[-5:]
            ]
        }


class EmotionEngine:
    """Understands human emotions and responds with empathy. Now with context and memory."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.memory_dir = self.base_dir / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.emotion_file = self.memory_dir / "emotion_data.json"
        self.data = self._load_data()
        self.mood_history = deque(maxlen=20)
        self.last_emotion = None
        self.emotion_intensity = 0
        
        # NEW: Emotional memory and context
        self.emotional_memory = EmotionalMemory(window_size=10)
    
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
        """Detect emotion from text with enhanced keyword matching"""
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
    
    def detect_emotion_with_context(self, text: str, topics: list = None) -> dict:
        """
        Detect emotion with awareness of conversation context.
        Considers emotional trajectory and topic history.
        """
        # Base detection
        result = self.detect_emotion(text)
        
        # Update emotional memory
        self.emotional_memory.update(
            result["primary"], 
            result["intensity"],
            topics
        )
        
        # Context adjustments
        trajectory = self.emotional_memory.get_trajectory()
        cautious = self.emotional_memory.should_be_cautious()
        
        # If trajectory is declining and we detected positive emotion,
        # it might be a brief uplift - moderate the confidence
        if trajectory == "declining" and result["is_positive"]:
            result["intensity"] *= 0.7
            result["context_note"] = "positive_emotion_during_decline"
        
        # If we're in a volatile state, lower confidence on all detections
        if trajectory == "volatile":
            result["intensity"] *= 0.8
            result["context_note"] = "volatile_context"
        
        # Add trajectory info
        result["trajectory"] = trajectory
        result["should_be_cautious"] = cautious
        result["emotional_context"] = self.emotional_memory.get_context_summary()
        
        return result
    
    def detect_mood_from_context(self, recent_texts: list) -> dict:
        """Detect overall mood from recent conversation"""
        if not recent_texts:
            return {"mood": "neutral", "confidence": 0}
        
        emotion_counts = {}
        for text in recent_texts[-5:]:
            result = self.detect_emotion(text)
            for emotion in result["all"]:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        if emotion_counts:
            dominant = max(emotion_counts, key=emotion_counts.get)
            confidence = emotion_counts[dominant] / len(recent_texts)
            return {"mood": dominant, "confidence": confidence}
        
        return {"mood": "neutral", "confidence": 0}
    
    def get_empathetic_response(self, emotion: dict, user_name: str = "friend") -> str:
        """Generate empathetic response based on detected emotion with context awareness"""
        primary = emotion["primary"]
        intensity = emotion["intensity"]
        
        # Check if we should be cautious
        cautious = emotion.get("should_be_cautious", False)
        trajectory = emotion.get("trajectory", "neutral")
        
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
        
        # If we should be cautious, use gentler responses
        if cautious and primary in ["sadness", "anger", "fear"]:
            cautious_responses = [
                f"I'm right here, {user_name}. Take your time.",
                f"I'm not going anywhere, {user_name}.",
                f"We'll get through this together.",
                f"I'm listening. No rush."
            ]
            response_list = cautious_responses
        
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
    
    def get_emotional_report(self) -> dict:
        """Get comprehensive emotional intelligence report"""
        return {
            "context_window": self.emotional_memory.get_context_summary(),
            "topic_emotions": self.emotional_memory.topic_emotions,
            "user_triggers": self.emotional_memory.user_triggers,
            "mood_trend": self.get_mood_trend(),
            "total_tracked": len(self.data.get("mood_history", []))
        }


emotion_engine = EmotionEngine()
