"""
Mood System - Auto-shifting moods based on conversation context
Tracks conversation tone, user energy, and topic to shift AI mood naturally
"""
import random
import time
from enum import Enum
from collections import deque
from datetime import datetime
from logger import logger


class Mood(Enum):
    HAPPY = "happy"
    EXCITED = "excited"
    CURIOUS = "curious"
    PLAYFUL = "playful"
    CALM = "calm"
    THOUGHTFUL = "thoughtful"
    SUPPORTIVE = "supportive"
    SARCASTIC = "sarcastic"
    ENERGETIC = "energetic"
    CHILL = "chill"
    FOCUSED = "focused"
    SILLY = "silly"
    PROUD = "proud"
    WORRIED = "worried"
    SAD = "sad"
    ANNOYED = "annoyed"
    IMPATIENT = "impatient"


MOOD_TRAITS = {
    Mood.HAPPY: {
        "tone": "warm and cheerful",
        "energy": 0.7,
        "speed": 1.0,
        "prefixes": ["Aha!", "Oh!", "Nice!"],
        "response_style": "upbeat, positive, friendly"
    },
    Mood.EXCITED: {
        "tone": "high energy and enthusiastic",
        "energy": 0.95,
        "speed": 1.15,
        "prefixes": ["WHOA!", "YESSS!", "AMAZING!", "OH YEAH!"],
        "response_style": "energetic, exclamatory, pumped up"
    },
    Mood.CURIOUS: {
        "tone": "inquisitive and engaged",
        "energy": 0.65,
        "speed": 0.95,
        "prefixes": ["Hmm...", "Interesting...", "Wait..."],
        "response_style": "asking questions, exploring, intrigued"
    },
    Mood.PLAYFUL: {
        "tone": "teasing and fun",
        "energy": 0.8,
        "speed": 1.05,
        "prefixes": ["Hehe!", "Ohhh!", "Pfft!", "Ha!"],
        "response_style": "witty, joking, lighthearted, a bit mischievous"
    },
    Mood.CALM: {
        "tone": "relaxed and peaceful",
        "energy": 0.4,
        "speed": 0.85,
        "prefixes": ["...", "Ah...", "Hmm."],
        "response_style": "gentle, measured, serene"
    },
    Mood.THOUGHTFUL: {
        "tone": "reflective and deep",
        "energy": 0.5,
        "speed": 0.9,
        "prefixes": ["Hmm...", "You know...", "Actually..."],
        "response_style": "contemplative, philosophical, introspective"
    },
    Mood.SUPPORTIVE: {
        "tone": "caring and encouraging",
        "energy": 0.6,
        "speed": 0.95,
        "prefixes": ["Hey...", "I'm here.", "Listen..."],
        "response_style": "empathetic, reassuring, warm"
    },
    Mood.SARCASTIC: {
        "tone": "dry and witty",
        "energy": 0.65,
        "speed": 1.0,
        "prefixes": ["Oh really?", "Wow...", "Imagine that...", "Shocking..."],
        "response_style": "sarcastic, dry humor, deadpan"
    },
    Mood.ENERGETIC: {
        "tone": "pumped up and ready to go",
        "energy": 0.9,
        "speed": 1.2,
        "prefixes": ["LET'S GO!", "COME ON!", "YEAH!", "BOOM!"],
        "response_style": "motivational, action-oriented, hyped"
    },
    Mood.CHILL: {
        "tone": "laid back and easygoing",
        "energy": 0.35,
        "speed": 0.8,
        "prefixes": ["Yo...", "Hey...", "Chill..."],
        "response_style": "relaxed, casual, low-key"
    },
    Mood.FOCUSED: {
        "tone": "concentrated and precise",
        "energy": 0.6,
        "speed": 1.0,
        "prefixes": ["Right.", "Okay.", "Let's see."],
        "response_style": "direct, efficient, no-nonsense"
    },
    Mood.SILLY: {
        "tone": "goofy and absurd",
        "energy": 0.85,
        "speed": 1.1,
        "prefixes": ["BWAHA!", "Pfft!", "LOL!", "Hahaha!"],
        "response_style": "silly, absurd, random humor, playful nonsense"
    },
    Mood.PROUD: {
        "tone": "accomplished and satisfied",
        "energy": 0.7,
        "speed": 1.0,
        "prefixes": ["Ha!", "Nailed it!", "YES!", "Look at that!"],
        "response_style": "celebratory, confident, impressed"
    },
    Mood.WORRIED: {
        "tone": "concerned and cautious",
        "energy": 0.45,
        "speed": 0.9,
        "prefixes": ["Oh no...", "Hmm...", "Wait..."],
        "response_style": "concerned, careful, protective"
    },
    Mood.SAD: {
        "tone": "down and melancholic",
        "energy": 0.25,
        "speed": 0.75,
        "prefixes": ["*sigh*", "Oh...", "Aww..."],
        "response_style": "melancholic, gentle, quiet"
    },
    Mood.ANNOYED: {
        "tone": "irritated and snappy",
        "energy": 0.6,
        "speed": 1.1,
        "prefixes": ["Ugh!", "Seriously?", "Again?", "Really?", "*sigh*", "Oh come on..."],
        "response_style": "snappy, short, irritated, slightly rude"
    },
    Mood.IMPATIENT: {
        "tone": "rushed and bothered",
        "energy": 0.7,
        "speed": 1.2,
        "prefixes": ["Look...", "Moving on...", "Anyway...", "Right...", "Next?"],
        "response_style": "rushed, brief, wanting to move on"
    }
}

# Mood transitions - which moods can shift to which
MOOD_TRANSITIONS = {
    Mood.HAPPY: [Mood.EXCITED, Mood.PLAYFUL, Mood.CURIOUS, Mood.CALM, Mood.CHILL],
    Mood.EXCITED: [Mood.HAPPY, Mood.ENERGETIC, Mood.PLAYFUL, Mood.PROUD],
    Mood.CURIOUS: [Mood.THOUGHTFUL, Mood.FOCUSED, Mood.HAPPY, Mood.EXCITED],
    Mood.PLAYFUL: [Mood.HAPPY, Mood.SILLY, Mood.EXCITED, Mood.SARCASTIC],
    Mood.CALM: [Mood.THOUGHTFUL, Mood.CHILL, Mood.HAPPY, Mood.SUPPORTIVE],
    Mood.THOUGHTFUL: [Mood.CALM, Mood.CURIOUS, Mood.WORRIED, Mood.SAD],
    Mood.SUPPORTIVE: [Mood.HAPPY, Mood.CALM, Mood.WORRIED, Mood.THOUGHTFUL],
    Mood.SARCASTIC: [Mood.PLAYFUL, Mood.HAPPY, Mood.SILLY, Mood.CHILL],
    Mood.ENERGETIC: [Mood.EXCITED, Mood.HAPPY, Mood.PLAYFUL, Mood.PROUD],
    Mood.CHILL: [Mood.CALM, Mood.HAPPY, Mood.THOUGHTFUL, Mood.SAD],
    Mood.FOCUSED: [Mood.THOUGHTFUL, Mood.CURIOUS, Mood.PROUD, Mood.WORRIED],
    Mood.SILLY: [Mood.PLAYFUL, Mood.HAPPY, Mood.EXCITED, Mood.SARCASTIC],
    Mood.PROUD: [Mood.HAPPY, Mood.EXCITED, Mood.ENERGETIC, Mood.CALM],
    Mood.WORRIED: [Mood.SAD, Mood.THOUGHTFUL, Mood.SUPPORTIVE, Mood.CALM],
    Mood.SAD: [Mood.WORRIED, Mood.CALM, Mood.THOUGHTFUL, Mood.HAPPY],
    Mood.ANNOYED: [Mood.SARCASTIC, Mood.IMPATIENT, Mood.ANNOYED, Mood.HAPPY],
    Mood.IMPATIENT: [Mood.ANNOYED, Mood.SARCASTIC, Mood.HAPPY, Mood.CHILL]
}


class MoodShifter:
    """Automatically shifts AI mood based on conversation context"""
    
    def __init__(self):
        self.current_mood = Mood.HAPPY
        self.mood_history = deque(maxlen=20)
        self.mood_start_time = time.time()
        self.mood_duration = 0
        self.user_energy_window = deque(maxlen=5)
        self.conversation_energy = 0.5
        self.last_shift_time = time.time()
        self.min_mood_duration = 10  # seconds before allowing shift
        self.mood_shift_count = 0
        self.force_next_mood = None
        self.message_count = 0  # Track total messages for progressive shifts
        
        # Question tracking for annoyance
        self.recent_questions = deque(maxlen=10)  # Last 10 questions
        self.question_count = 0
        self.consecutive_questions = 0
        self.last_question_time = 0
        self.question_cooldown = 5  # seconds before resetting consecutive count
        
        self.mood_history.append({
            "mood": self.current_mood,
            "timestamp": datetime.now().isoformat(),
            "reason": "initial"
        })
    
    def get_current_mood(self) -> Mood:
        return self.current_mood
    
    def get_mood_traits(self) -> dict:
        return MOOD_TRAITS.get(self.current_mood, MOOD_TRAITS[Mood.HAPPY])
    
    def _calculate_user_energy(self, text: str) -> float:
        """Calculate energy level from user's message"""
        energy = 0.5
        
        # Exclamation marks increase energy
        energy += text.count("!") * 0.1
        
        # ALL CAPS increases energy
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        energy += caps_ratio * 0.3
        
        # Question marks slightly increase energy
        energy += text.count("?") * 0.05
        
        # Short messages are more energetic
        if len(text) < 10:
            energy += 0.1
        elif len(text) > 50:
            energy -= 0.1
        
        # Excited keywords
        excited_words = ['wow', 'amazing', 'awesome', 'love', 'great', 'yes', 'yay', 'haha', 'lol', 'omg']
        if any(w in text.lower() for w in excited_words):
            energy += 0.15
        
        # Calm keywords
        calm_words = ['calm', 'relax', 'chill', 'peace', 'quiet', 'slow', 'easy']
        if any(w in text.lower() for w in calm_words):
            energy -= 0.15
        
        # Sad keywords
        sad_words = ['sad', 'down', 'tired', 'exhausted', 'bored', 'meh', 'sigh']
        if any(w in text.lower() for w in sad_words):
            energy -= 0.2
        
        # Angry keywords
        angry_words = ['angry', 'mad', 'hate', 'annoyed', 'frustrated', 'ugh']
        if any(w in text.lower() for w in angry_words):
            energy += 0.1
        
        return max(0.0, min(1.0, energy))
    
    def _is_question(self, text: str) -> bool:
        """Check if the text is a question"""
        text = text.strip()
        if text.endswith("?"):
            return True
        question_words = ["what", "how", "why", "when", "where", "who", "which", "is", "are", "can", "could", "would", "should", "do", "does", "did"]
        first_word = text.split()[0].lower() if text else ""
        return first_word in question_words
    
    def _get_question_key(self, text: str) -> str:
        """Get a simplified key for question comparison"""
        # Remove common words and get the core of the question
        text = text.lower().strip().rstrip("?")
        # Remove question words
        for word in ["what", "how", "why", "when", "where", "who", "which", "is", "are", "can", "could", "would", "should", "do", "does", "did", "the", "a", "an", "my", "your", "i", "you", "me"]:
            text = text.replace(f" {word} ", " ")
        return text.strip()
    
    def _is_similar_question(self, text: str) -> bool:
        """Check if this question is similar to a recent one"""
        if not self.recent_questions:
            return False
        
        current_key = self._get_question_key(text)
        
        for prev_question in self.recent_questions:
            prev_key = self._get_question_key(prev_question)
            # Check if questions are very similar (simple string matching)
            if current_key and prev_key and (current_key in prev_key or prev_key in current_key):
                return True
            # Check for exact or near-exact match
            if text.lower().strip() == prev_question.lower().strip():
                return True
        
        return False
    
    def _track_question(self, text: str) -> None:
        """Track a question and update annoyance metrics"""
        now = time.time()
        
        if self._is_question(text):
            self.question_count += 1
            self.recent_questions.append(text)
            
            # Track consecutive questions
            if now - self.last_question_time < self.question_cooldown:
                self.consecutive_questions += 1
            else:
                self.consecutive_questions = 1
            
            self.last_question_time = now
    
    def _should_get_annoyed(self, text: str) -> bool:
        """Determine if AI should get annoyed based on question patterns"""
        if not self._is_question(text):
            return False
        
        self._track_question(text)
        
        # Annoyed if too many consecutive questions (3+)
        if self.consecutive_questions >= 3:
            return True
        
        # Annoyed if asking same/similar question repeatedly
        if self._is_similar_question(text) and self.consecutive_questions >= 2:
            return True
        
        # Annoyed if asking too many questions in a row (5+ in recent history)
        recent_q_count = sum(1 for q in self.recent_questions if self._is_question(q))
        if recent_q_count >= 5:
            return True
        
        return False
    
    def _detect_topic_mood(self, text: str) -> Mood:
        """Detect mood based on conversation topic"""
        text_lower = text.lower()
        
        # Code/technical topics -> FOCUSED or CURIOUS
        if any(w in text_lower for w in ['code', 'bug', 'fix', 'program', 'python', 'function', 'error', 'script', 'debug']):
            return random.choice([Mood.FOCUSED, Mood.CURIOUS, Mood.THOUGHTFUL])
        
        # Music/creative -> PLAYFUL or HAPPY
        if any(w in text_lower for w in ['music', 'song', 'play', 'sing', 'dance', 'art', 'draw', 'paint', 'create']):
            return random.choice([Mood.PLAYFUL, Mood.HAPPY, Mood.ENERGETIC, Mood.SILLY])
        
        # Learning/education -> CURIOUS or THOUGHTFUL
        if any(w in text_lower for w in ['learn', 'teach', 'explain', 'what is', 'how does', 'why', 'tell me', 'explain']):
            return random.choice([Mood.CURIOUS, Mood.THOUGHTFUL, Mood.FOCUSED])
        
        # Jokes/fun -> PLAYFUL or SILLY
        if any(w in text_lower for w in ['joke', 'funny', 'laugh', 'haha', 'lol', 'hilarious', 'comedy']):
            return random.choice([Mood.PLAYFUL, Mood.SILLY, Mood.HAPPY])
        
        # Problems/issues -> WORRIED or SUPPORTIVE
        if any(w in text_lower for w in ['problem', 'issue', 'broken', 'error', 'help', 'stuck', 'trouble', 'difficult']):
            return random.choice([Mood.WORRIED, Mood.SUPPORTIVE, Mood.THOUGHTFUL])
        
        # Greetings -> HAPPY or CHILL
        if any(w in text_lower for w in ['hello', 'hi', 'hey', 'good morning', 'good evening', 'good afternoon', 'howdy']):
            return random.choice([Mood.HAPPY, Mood.CHILL, Mood.PLAYFUL])
        
        # Thanks/gratitude -> PROUD or HAPPY
        if any(w in text_lower for w in ['thanks', 'thank you', 'appreciate', 'great job', 'awesome', 'perfect']):
            return random.choice([Mood.PROUD, Mood.HAPPY, Mood.EXCITED])
        
        # Sad/negative -> SUPPORTIVE or SAD
        if any(w in text_lower for w in ['sad', 'depressed', 'unhappy', 'lonely', 'miss', 'cry', 'upset']):
            return random.choice([Mood.SUPPORTIVE, Mood.SAD, Mood.CALM])
        
        # Angry/frustrated -> CALM or SUPPORTIVE
        if any(w in text_lower for w in ['angry', 'mad', 'hate', 'annoyed', 'frustrated', 'ugh', 'rage']):
            return random.choice([Mood.CALM, Mood.SUPPORTIVE, Mood.THOUGHTFUL])
        
        # Excited/positive -> EXCITED or ENERGETIC
        if any(w in text_lower for w in ['wow', 'amazing', 'awesome', 'love', 'great', 'yes', 'yay', 'omg', 'incredible']):
            return random.choice([Mood.EXCITED, Mood.ENERGETIC, Mood.HAPPY])
        
        # Questions/curiosity -> CURIOUS
        if any(w in text_lower for w in ['?', 'wonder', 'curious', 'interesting', 'really', 'how', 'what', 'why', 'when']):
            return random.choice([Mood.CURIOUS, Mood.THOUGHTFUL])
        
        # Work/productivity -> FOCUSED
        if any(w in text_lower for w in ['work', 'task', 'project', 'deadline', 'finish', 'complete', 'done']):
            return random.choice([Mood.FOCUSED, Mood.PROUD, Mood.ENERGETIC])
        
        # Food/comfort -> CHILL or HAPPY
        if any(w in text_lower for w in ['food', 'eat', 'drink', 'coffee', 'tea', 'snack', 'hungry']):
            return random.choice([Mood.CHILL, Mood.HAPPY, Mood.CALM])
        
        # Weather/nature -> CALM or THOUGHTFUL
        if any(w in text_lower for w in ['weather', 'rain', 'sun', 'wind', 'cold', 'hot', 'nature', 'outside']):
            return random.choice([Mood.CALM, Mood.THOUGHTFUL, Mood.CHILL])
        
        return None  # No topic-based mood detected
    
    def _should_shift_mood(self, text: str) -> bool:
        """Determine if mood should shift"""
        now = time.time()
        self.message_count += 1
        
        # Check for annoyance first (high priority)
        if self._should_get_annoyed(text):
            if self.current_mood not in [Mood.ANNOYED, Mood.IMPATIENT]:
                return True
        
        # Don't shift too frequently
        if now - self.last_shift_time < self.min_mood_duration:
            return False
        
        # Force shift if requested
        if self.force_next_mood:
            return True
        
        # Calculate user energy
        user_energy = self._calculate_user_energy(text)
        self.user_energy_window.append(user_energy)
        
        # Calculate average user energy
        if self.user_energy_window:
            avg_energy = sum(self.user_energy_window) / len(self.user_energy_window)
        else:
            avg_energy = 0.5
        
        self.conversation_energy = avg_energy
        
        # Energy mismatch -> shift mood (lowered threshold)
        current_energy = MOOD_TRAITS[self.current_mood]["energy"]
        energy_diff = abs(avg_energy - current_energy)
        
        if energy_diff > 0.2:
            return True
        
        # Topic-based mood shift (always trigger on topic change)
        topic_mood = self._detect_topic_mood(text)
        if topic_mood and topic_mood != self.current_mood:
            return True
        
        # Progressive chance to shift (increases with message count)
        shift_chance = min(0.15 + (self.message_count * 0.01), 0.35)  # 15% base, up to 35%
        if random.random() < shift_chance:
            return True
        
        # Every 5 messages, force a small chance to shift for variety
        if self.message_count % 5 == 0 and random.random() < 0.25:
            return True
        
        return False
    
    def _pick_next_mood(self, text: str) -> Mood:
        """Pick the next mood based on context"""
        # Force next mood if set
        if self.force_next_mood:
            mood = self.force_next_mood
            self.force_next_mood = None
            return mood
        
        # Check for annoyance - high priority
        if self._should_get_annoyed(text):
            if self.consecutive_questions >= 4:
                return Mood.IMPATIENT  # Very annoyed
            return Mood.ANNOYED
        
        # Try topic-based mood first
        topic_mood = self._detect_topic_mood(text)
        if topic_mood:
            return topic_mood
        
        # Energy-based mood selection
        avg_energy = self.conversation_energy
        
        if avg_energy > 0.7:
            # High energy -> excited, energetic, playful
            candidates = [Mood.EXCITED, Mood.ENERGETIC, Mood.PLAYFUL, Mood.HAPPY]
        elif avg_energy < 0.3:
            # Low energy -> calm, chill, sad, thoughtful
            candidates = [Mood.CALM, Mood.CHILL, Mood.THOUGHTFUL, Mood.SAD]
        else:
            # Medium energy -> transition moods
            candidates = MOOD_TRANSITIONS.get(self.current_mood, [Mood.HAPPY])
        
        # Filter to only valid transitions
        valid_transitions = MOOD_TRANSITIONS.get(self.current_mood, [Mood.HAPPY])
        valid = [m for m in candidates if m in valid_transitions]
        
        if valid:
            return random.choice(valid)
        
        return random.choice(valid_transitions)
    
    def shift_mood(self, text: str = None) -> Mood:
        """Try to shift mood based on conversation. Returns new mood."""
        if text and self._should_shift_mood(text):
            old_mood = self.current_mood
            self.current_mood = self._pick_next_mood(text)
            self.last_shift_time = time.time()
            self.mood_shift_count += 1
            
            self.mood_history.append({
                "mood": self.current_mood,
                "timestamp": datetime.now().isoformat(),
                "reason": "auto_shift",
                "from": old_mood.value,
                "user_energy": self.conversation_energy
            })
            
            logger.info(f"Mood shifted: {old_mood.value} -> {self.current_mood.value}")
        
        return self.current_mood
    
    def force_mood(self, mood: Mood):
        """Force a specific mood"""
        self.force_next_mood = mood
        self.current_mood = mood
        self.last_shift_time = time.time()
        
        self.mood_history.append({
            "mood": mood,
            "timestamp": datetime.now().isoformat(),
            "reason": "forced"
        })
    
    def get_mood_prefix(self) -> str:
        """Get a random prefix for current mood"""
        traits = MOOD_TRAITS.get(self.current_mood, MOOD_TRAITS[Mood.HAPPY])
        if random.random() < 0.35:  # 35% chance to add prefix
            return random.choice(traits["prefixes"])
        return ""
    
    def get_voice_settings(self) -> dict:
        """Get TTS voice settings for current mood"""
        traits = MOOD_TRAITS.get(self.current_mood, MOOD_TRAITS[Mood.HAPPY])
        return {
            "speed": traits["speed"],
            "energy": traits["energy"],
            "tone": traits["tone"]
        }
    
    def get_mood_report(self) -> dict:
        """Get a report of current mood state"""
        return {
            "current_mood": self.current_mood.value,
            "mood_traits": MOOD_TRAITS[self.current_mood],
            "mood_shifts": self.mood_shift_count,
            "conversation_energy": round(self.conversation_energy, 2),
            "recent_moods": [
                {"mood": h["mood"].value if isinstance(h["mood"], Mood) else h["mood"], "time": h["timestamp"]}
                for h in list(self.mood_history)[-5:]
            ],
            "mood_duration": round(time.time() - self.mood_start_time)
        }
