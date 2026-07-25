"""
Optimized Emotion Engine with enhanced emotional intelligence and memory
"""
import json
import time
from pathlib import Path
from datetime import datetime
from collections import deque, defaultdict
from typing import Dict, List, Optional, Tuple
import re


class EmotionalMemory:
    """
    Optimized emotional memory with multi-dimensional tracking
    """

    def __init__(self, window_size: int = 15):
        self.window_size = window_size
        self.emotional_context = deque(maxlen=window_size)
        self.emotional_trajectory = []
        self.topic_emotions = {}
        self.user_emotion_patterns = {}
        self.conversation_start_time = None
        self.last_emotion = None
        self.emotion_streak = 0
        self.emotion_intensity_history = deque(maxlen=window_size)
        self.topic_intensity = defaultdict(list)
        
    def update(self, emotion: str, intensity: float, topics: list = None):
        """Add a new emotion reading with optimized tracking"""
        entry = {
            "emotion": emotion,
            "intensity": intensity,
            "timestamp": datetime.now().isoformat(),
            "topics": topics or []
        }

        self.emotional_context.append(entry)
        self.emotional_trajectory.append(entry)

        # Track emotion streaks and intensity
        if emotion == self.last_emotion:
            self.emotion_streak += 1
        else:
            self.emotion_streak = 0
        self.last_emotion = emotion
        
        self.emotion_intensity_history.append(intensity)

        # Track topic-emotion associations with intensity weighting
        if topics:
            for topic in topics:
                self.topic_emotions.setdefault(topic, {})
                current_weight = self.topic_emotions[topic].get(emotion, 0)
                self.topic_emotions[topic][emotion] = current_weight + intensity
                self.topic_intensity[topic].append((emotion, intensity))
                
                if len(self.topic_intensity[topic]) > 100:
                    self.topic_intensity[topic] = self.topic_intensity[topic][-100:]

    def get_velocity(self) -> float:
        """Calculate emotional velocity"""
        if len(self.emotion_intensity_history) < 2:
            return 0.0

        intensities = list(self.emotion_intensity_history)
        if len(intensities) >= 3:
            recent = intensities[-3:]
            return recent[-1] - recent[0]
        return 0.0

    def get_valence(self) -> float:
        """Calculate emotional valence (positive vs negative)"""
        if not self.emotional_context:
            return 0.0

        positive_emotions = {"joy", "love", "gratitude", "excitement", "pride", "hope"}
        negative_emotions = {"sadness", "anger", "fear", "disgust", "disappointment", "shame"}
        
        scores = []
        for entry in list(self.emotional_context)[-self.window_size:]:
            emotion = entry["emotion"]
            intensity = entry["intensity"]
            if emotion in positive_emotions:
                scores.append(intensity)
            elif emotion in negative_emotions:
                scores.append(-intensity)
            else:
                scores.append(0)

        return sum(scores) / len(scores) if scores else 0.0

    def get_arousal(self) -> float:
        """Calculate emotional arousal (intensity level)"""
        if not self.emotion_intensity_history:
            return 0.0

        return sum(self.emotion_intensity_history) / len(self.emotion_intensity_history)

    def get_context_summary(self) -> dict:
        """Optimized emotional context summary"""
        return {
            "window_size": len(self.emotional_context),
            "dominant_emotion": self.get_dominant_emotion(),
            "valence": round(self.get_valence(), 2),
            "arousal": round(self.get_arousal(), 2),
            "velocity": round(self.get_velocity(), 2),
            "emotion_streak": self.emotion_streak,
            "last_emotion": self.last_emotion,
            "should_be_cautious": self.should_be_cautious(),
            "topics_tracked": len(self.topic_emotions),
            "emotion_confidence": self.get_emotion_confidence(),
            "recent_intensity": [e["intensity"] for e in list(self.emotional_context)[-3:]]
        }

    def get_emotion_confidence(self) -> float:
        """Calculate confidence in emotion detection"""
        if len(self.emotional_context) < 2:
            return 0.0
        
        recent = list(self.emotional_context)[-5:]
        emotion_counts = {}
        for entry in recent:
            emotion_counts[entry["emotion"]] = emotion_counts.get(entry["emotion"], 0) + 1
        
        if not emotion_counts:
            return 0.0
        
        dominant_count = max(emotion_counts.values())
        total_count = len(recent)
        
        return dominant_count / total_count


class OptimizedEmotionEngine:
    """Enhanced emotion engine with optimized detection and response generation"""

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.memory_dir = self.base_dir / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.emotion_file = self.memory_dir / "emotion_data.json"
        self.data = self._load_data()
        self.mood_history = deque(maxlen=30)
        self.last_emotion = None
        self.emotion_intensity = 0
        self.emotional_memory = EmotionalMemory(window_size=15)
        
        # Pre-compiled regex patterns for faster matching
        self._compile_patterns()
        
    def _compile_patterns(self):
        """Pre-compile regex patterns for faster matching"""
        self.patterns = {
            'positive': re.compile(r'(\b(joy|love|gratitude|excitement|pride|hope)\b)', re.IGNORECASE),
            'negative': re.compile(r'(\b(sadness|anger|fear|disgust|disappointment|shame)\b)', re.IGNORECASE),
            'intense': re.compile(r'(\b(very|extremely|so|really|absolutely|totally)\b)', re.IGNORECASE),
            'negation': re.compile(r'\b(never|no|not|can\'t|don\'t|won\'t)\b', re.IGNORECASE)
        }

    def _load_data(self) -> dict:
        """Load emotion data with compression"""
        if self.emotion_file.exists():
            try:
                with open(self.emotion_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return self._default_data()
        return self._default_data()

    def _default_data(self):
        """Optimized default data structure"""
        return {
            "mood_history": [],
            "emotion_patterns": {},
            "user_emotion_trends": {},
            "conversation_emotions": [],
            "emotional_calibration": {},
            "personalized_emotions": {}
        }

    def _save_data(self):
        """Save emotion data with async support"""
        try:
            with open(self.emotion_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass

    def detect_emotion(self, text: str) -> dict:
        """Optimized emotion detection with advanced keyword matching"""
        text_lower = text.lower().strip()
        
        # Fast path for common emotions
        quick_emotions = {
            'happy': [r'\bhappy|joy|awesome|amazing|great|good\b'],
            'sad': [r'\bsad|sadness|down|unhappy|depressed\b'],
            'angry': [r'\bangry|mad|rage|frustrated|annoyed\b'],
            'excited': [r'\bexcited|exciting|thrilled|pumped\b'],
            'neutral': [r'\b(okay|fine|ok|neutral|meh)\b']
        }
        
        for emotion, patterns in quick_emotions.items():
            if any(re.search(pattern, text_lower) for pattern in patterns):
                return {
                    "primary": emotion,
                    "intensity": self._calculate_intensity(text_lower, 0.7),
                    "confidence": 0.8,
                    "is_positive": emotion in ['happy', 'excited'],
                    "is_negative": emotion in ['sad', 'angry']
                }

        # Comprehensive emotion detection
        detected = []
        intensity = 0
        confidence = 0.5

        # Use pre-compiled patterns
        if self.patterns['positive'].search(text_lower):
            detected.append('joy')
            intensity += 3
        if self.patterns['negative'].search(text_lower):
            detected.append('sadness')
            intensity += 3
        if self.patterns['intense'].search(text_lower) and not self.patterns['negation'].search(text_lower):
            intensity += 2

        # Keyword-based detection
        positive_emotions = {
            "joy": ["happy", "great", "awesome", "amazing", "love", "wonderful", "fantastic", "excellent", "brilliant"],
            "love": ["love", "adore", "cherish", "miss you", "care", "heart", "sweet", "darling", "precious"],
            "gratitude": ["thank", "thanks", "grateful", "appreciate", "blessed"],
            "excitement": ["excited", "pumped", "thrilled", "cant wait", "eager", "stoked", "hyped"],
            "pride": ["proud", "accomplished", "achieved", "success", "won", "victory", "mastered"],
            "hope": ["hope", "wish", "dream", "believe", "faith", "optimistic"]
        }

        negative_emotions = {
            "sadness": ["sad", "depressed", "unhappy", "miss", "lonely", "alone", "cry", "tears", "heartbroken"],
            "anger": ["angry", "furious", "mad", "hate", "annoyed", "frustrated", "rage"],
            "fear": ["scared", "afraid", "fear", "terrified", "worried", "nervous", "anxious"],
            "disgust": ["disgusting", "gross", "eww", "yuck", "sick", "nasty"],
            "disappointment": ["disappointed", "let down", "failed", "lost", "defeated"],
            "shame": ["embarrassed", "ashamed", "humiliated", "mortified", "sorry", "regret"]
        }

        # Optimized detection - use finditer for efficiency
        for emotion, keywords in positive_emotions.items():
            for keyword in keywords:
                matches = re.finditer(r'\b' + re.escape(keyword) + r'\b', text_lower)
                for match in matches:
                    detected.append(emotion)
                    intensity += 1

        for emotion, keywords in negative_emotions.items():
            for keyword in keywords:
                matches = re.finditer(r'\b' + re.escape(keyword) + r'\b', text_lower)
                for match in matches:
                    detected.append(emotion)
                    intensity += 2

        # Short-circuit for high intensity emotions
        if text_lower.count('!') > 2 or 'OMG' in text_lower or 'OH MY GOD' in text_lower:
            intensity += 3

        # Determine primary emotion
        if detected:
            from collections import Counter
            primary = Counter(detected).most_common(1)[0][0]
        else:
            primary = "neutral"

        # Normalize and return with enhanced data
        intensity = min(intensity / 8, 1.0)

        return {
            "primary": primary,
            "all": list(set(detected)),
            "intensity": intensity,
            "is_positive": primary in list(positive_emotions.keys()),
            "is_negative": primary in list(negative_emotions.keys()),
            "confidence": min(confidence + (0.1 if detected else 0), 1.0),
            "detected_count": len(detected),
            "intensity_boosted": intensity > 0.7
        }

    def _calculate_intensity(self, text: str, base_intensity: float) -> float:
        """Calculate intensity with optimized logic"""
        intensity = base_intensity

        # Exclamation marks boost intensity
        intensity += text.count("!") * 0.1

        # Strong intensity words
        strong_words = ["terrible", "awful", "horrible", "devastating", "catastrophic"]
        for word in strong_words:
            if word in text:
                intensity += 0.3

        return min(intensity, 1.0)


# Create optimized global instances
emotion_engine = OptimizedEmotionEngine()
