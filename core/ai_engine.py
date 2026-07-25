"""
Enhanced AI Engine with Auto-Training and Self-Improvement
"""
import datetime
import os
import sys
import json
import random
import logging
import re
import time
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum

from config import config
from logger import logger
from utils.memory_manager import MemoryManager
from utils.response_generator import ResponseGenerator
from utils.learning_engine import LearningEngine
from utils.code_analyzer import CodeAnalyzer, SeverityLevel
from utils.thinking_engine import ThinkingEngine
from utils.training_engine import TrainingEngine
from utils.system_controller import SystemController
from utils.screen_vision import ScreenVision
from utils.system_monitor import SystemMonitor
from utils.personal_assistant import PersonalAssistant
from utils.toolchain import Toolchain
from utils.self_thinking_engine import SelfThinkingEngine
from utils.internet_learning import InternetLearner
from utils.account_manager import AccountManager
from utils.web_search import WebSearch
from utils.screen_awareness import ScreenAwareness
from utils.emotion_engine import OptimizedEmotionEngine as EmotionEngine
from utils.purple_brain import PurpleBrain
from utils.advanced_ai import AdvancedAI
from utils.mood_system import OptimizedMoodShifter as MoodShifter, Mood
from utils.camera_access import CameraAccess
from utils.purple_database import PurpleDatabase
from utils.media_controller import MediaController
from utils.web_media import WebMediaEngine
from utils.autonomous_engine import AutonomousEngine
from core.command_registry import get_command_handler
import threading

class EmotionalState(Enum):
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    CURIOUS = "curious"
    SUPPORTIVE = "supportive"
    NEUTRAL = "neutral"
    THINKING = "thinking"
    TRAINING = "training"
    PLAYFUL = "playful"
    CALM = "calm"
    THOUGHTFUL = "thoughtful"
    SARCASTIC = "sarcastic"
    ENERGETIC = "energetic"
    CHILL = "chill"
    FOCUSED = "focused"
    SILLY = "silly"
    PROUD = "proud"
    WORRIED = "worried"

class OfflineAI:
    # Class-level caches (shared across instances)
    _response_cache = {}
    _cache_max_size = 200
    _handler_cache = {}
    _command_patterns = frozenset([
        'time', 'date', 'help', 'exit', 'quit', 'goodbye', 'bye',
        'hello', 'hi', 'hey', 'joke', 'fact', 'mood', 'who am i',
        'volume up', 'volume down', 'mute', 'unmute', 'screenshot',
        'play', 'pause', 'resume', 'stop', 'next', 'previous'
    ])

    def __init__(self, tts_engine=None):
        # Lazy-loaded heavy modules (loaded on first use)
        self._lazy_modules = {}
        self._module_load_lock = threading.Lock()
        
        # Core lightweight modules (always loaded)
        self.tts_engine = tts_engine
        self.memory_manager = MemoryManager()
        self.memory = self.memory_manager.load_memory()
        self.conversation_context = {
            'current_topic': None,
            'recent_topics': [],
            'awaiting_answer': False,
            'last_interaction': 0
        }
        self.conversation_stats = {
            'commands_processed': 0, 'topics_learned': 0, 'bugs_found': 0,
            'bugs_fixed': 0, 'questions_asked': 0, 'knowledge_gained': 0,
            'conversation_length': 0, 'training_sessions': 0, 'improvements_made': 0
        }
        self.conversation_counter = 0
        self.auto_train_interval = 10
        self.auto_improve_interval = 5
        self.last_auto_improve = 0
        self._last_command_time = 0
        self._min_command_interval = 0.05  # 50ms minimum
        
        # Fast-path handler registry (direct method references)
        self._fast_handlers = self._build_fast_handler_map()
        
        logger.info("Optimized AI Engine initialized!")
        self._start_background_improvement()
        self._start_screen_awareness()

    def _build_fast_handler_map(self):
        """Build direct method reference map for O(1) handler lookup"""
        return {
            '_tell_time': self._tell_time,
            '_tell_date': self._tell_date,
            '_show_help': self._show_help,
            '_greet_user': self._greet_user,
            '_show_training_stats': self._show_training_stats,
            '_manual_train': self._manual_train,
            '_show_system_info': self._show_system_info,
            '_show_installed_apps': self._show_installed_apps,
            '_show_running_apps': self._show_running_apps,
            '_handle_active_window': self._handle_active_window,
            '_handle_list_tabs': self._handle_list_tabs,
            '_handle_volume_up': self._handle_volume_up,
            '_handle_volume_down': self._handle_volume_down,
            '_handle_mute': self._handle_mute,
            '_handle_unmute': self._handle_unmute,
            '_handle_screenshot': self._handle_screenshot,
            '_handle_lock_screen': self._handle_lock_screen,
            '_handle_empty_trash': self._handle_empty_trash,
            '_handle_shutdown': self._handle_shutdown,
            '_handle_restart': self._handle_restart,
            '_handle_sleep': self._handle_sleep,
            '_handle_disk_space': self._handle_disk_space,
            '_handle_battery': self._handle_battery,
            '_handle_network': self._handle_network,
            '_handle_see_screen': self._handle_see_screen,
            '_handle_read_screen': self._handle_read_screen,
            '_handle_describe_screen': self._handle_describe_screen,
            '_tell_joke': self._tell_joke,
            '_handle_self_analysis': self._handle_self_analysis,
            '_handle_auto_improve': self._handle_auto_improve,
            '_handle_what_am_i_doing': self._handle_what_am_i_doing,
            '_handle_watch_screen': self._handle_watch_screen,
            '_handle_mood_check': self._handle_mood_check,
            '_handle_camera_open': self._handle_camera_open,
            '_handle_camera_close': self._handle_camera_close,
            '_handle_camera_photo': self._handle_camera_photo,
            '_handle_look_at_me': self._handle_look_at_me,
            '_handle_recognize_faces': self._handle_recognize_faces,
            '_handle_known_faces': self._handle_known_faces,
            '_handle_start_recognition': self._handle_start_recognition,
            '_handle_camera_info': self._handle_camera_info,
            '_handle_db_stats': self._handle_db_stats,
            '_handle_db_facts': self._handle_db_facts,
            '_handle_db_conversations': self._handle_db_conversations,
            '_handle_db_goals': self._handle_db_goals,
            '_handle_db_notes': self._handle_db_notes,
            '_handle_db_backup': self._handle_db_backup,
            '_handle_db_clear_old': self._handle_db_clear_old,
            '_handle_pause_music': self._handle_pause_music,
            '_handle_resume_music': self._handle_resume_music,
            '_handle_next_track': self._handle_next_track,
            '_handle_prev_track': self._handle_prev_track,
            '_handle_stop_music': self._handle_stop_music,
            '_handle_what_playing': self._handle_what_playing,
            '_handle_mood_happy': self._handle_mood_happy,
            '_handle_mood_sad': self._handle_mood_sad,
            '_handle_mood_angry': self._handle_mood_angry,
            '_handle_mood_excited': self._handle_mood_excited,
            '_who_am_i': self._who_am_i,
            '_exit_command': self._exit_command,
            '_set_name': self._set_name,
            '_handle_remember_command': self._handle_remember_command,
            '_handle_set_mood': self._handle_set_mood,
            '_handle_learn_face': self._handle_learn_face,
            '_handle_forget_face': self._handle_forget_face,
            '_handle_db_search': self._handle_db_search,
            '_handle_db_save_memory': self._handle_db_save_memory,
            '_handle_db_get_memory': self._handle_db_get_memory,
            '_handle_db_add_goal': self._handle_db_add_goal,
            '_handle_db_add_note': self._handle_db_add_note,
            '_handle_play_music': self._handle_play_music,
            '_handle_show_object': self._handle_show_object,
        }
    
    def _greet_user(self):
        name = self.memory.get('user_name', 'friend')
        interaction_count = self.memory.get('interaction_count', 0)
        training_stats = self.training_engine.get_training_stats()
        
        if interaction_count == 0:
            greetings = [
                f"Hey {name}! I'm Purple! Smart, witty, and slightly sarcastic! What's on your mind?",
                f"Well well well, {name}! I'm Purple! I think, I learn, and I'm pretty awesome! Let's chat!",
                f"Hey there {name}! I'm Purple! I'm like a normal AI, but with personality! What shall we talk about?"
            ]
        else:
            improvements = training_stats.get('patterns_learned', 0)
            if improvements > 0:
                greetings = [
                    f"Hey {name}! I'm back and sharper than ever! I learned {improvements} new tricks! What's new?",
                    f"Look who it is! {name}! I've been training and I'm basically genius now! What shall we discuss?",
                    f"Welcome back {name}! I'm smarter, wittier, and still humble! What's on your mind?"
                ]
            else:
                greetings = [
                    f"Hey {name}! Miss me? I missed you! Ready to chat?",
                    f"{name}! You're back! I was getting bored without you! What's up?",
                    f"Hey {name}! I was just thinking about you! Well, more like running algorithms, but same thing!"
                ]
        
        self._speak_text(random.choice(greetings))
        self.memory['interaction_count'] = interaction_count + 1
        self.memory_manager.save_memory(self.memory)
    
    def _start_background_improvement(self):
        """Start background thread for continuous self-improvement"""
        def improvement_loop():
            import time
            while True:
                try:
                    time.sleep(300)  # Every 5 minutes
                    logger.info("Background self-improvement running...")
                    self.self_thinking_engine.auto_improve()
                    
                    # Also learn from internet periodically
                    try:
                        import random
                        topics = ["AI news", "technology", "python tips", "productivity"]
                        topic = random.choice(topics)
                        self.internet_learner.learn_topic(topic)
                    except Exception:
                        pass
                        
                except Exception as e:
                    logger.error(f"Background improvement error: {e}")
        
        thread = threading.Thread(target=improvement_loop, daemon=True)
        thread.start()
        logger.info("Background self-improvement started")
    
    def _start_screen_awareness(self):
        """Start proactive screen monitoring"""
        
        self._screen_suggestion_count = 0
        self._max_screen_suggestions = 2  # Max proactive suggestions per session
        
        def screen_callback(suggestion, activity):
            # Don't speak during first 120 seconds
            if not hasattr(self, '_startup_time'):
                self._startup_time = time.time()
            
            if time.time() - self._startup_time < 120:
                logger.info(f"Proactive screen suggestion (deferred): {suggestion}")
                return
            
            # Limit proactive suggestions
            self._screen_suggestion_count += 1
            if self._screen_suggestion_count > self._max_screen_suggestions:
                logger.info(f"Proactive screen suggestion (limit reached): {suggestion}")
                return
            
            logger.info(f"Proactive screen suggestion: {suggestion}")
            self._speak_text(suggestion)
        
        self._startup_time = time.time()
        self.screen_awareness.start_monitoring(callback=screen_callback)
        logger.info("Screen awareness started")
    
    def _auto_improve_on_command(self):
        """Auto-improve after every N commands"""
        self.conversation_counter += 1
        
        if self.conversation_counter - self.last_auto_improve >= self.auto_improve_interval:
            self.last_auto_improve = self.conversation_counter
            
            try:
                logger.info("Auto-improving after commands...")
                
                # Learn from recent interactions
                self.self_thinking_engine.learn_from_interaction(
                    "recent_session", "continuous_improvement", 0.8
                )
                
                # Auto-analyze and improve
                self.self_thinking_engine.auto_improve()
                
                # Analyze self periodically
                if self.conversation_counter % 10 == 0:
                    self.self_thinking_engine.analyze_self()
                    logger.info("Self-analysis completed")
                    
            except Exception as e:
                logger.error(f"Auto-improve error: {e}")
    
    def setup_owner(self, voice_controller=None) -> bool:
        """
        First-time setup: Ask for owner's name and enroll their voice with multiple samples.
        Returns True if setup completed successfully.
        """
        print("\n" + "=" * 60)
        print("🔧 FIRST-TIME SETUP")
        print("=" * 60)
        print("Hi! I'm Purple, your AI assistant!")
        print("Let me set you up as my owner.")
        print("=" * 60)
        
        self._speak_text("Hi! I'm Purple, your AI assistant! Let me set you up as my owner.")
        time.sleep(0.5)
        
        # Step 1: Ask for name
        print("\n📝 STEP 1: What's your name?")
        self._speak_text("What's your name? Please type it below.")
        
        owner_name = ""
        while not owner_name:
            try:
                owner_name = input("\n👤 Your name: ").strip()
                if not owner_name:
                    print("Please enter a name!")
                    self._speak_text("Please enter your name.")
            except EOFError:
                owner_name = "Rifat"
                print(f"Using default name: {owner_name}")
                break
        
        # Save name
        self.memory['user_name'] = owner_name.capitalize()
        self.memory_manager.save_memory(self.memory)
        print(f"\n✅ Nice to meet you, {owner_name.capitalize()}!")
        self._speak_text(f"Nice to meet you, {owner_name.capitalize()}! I'll remember that.")
        time.sleep(0.5)
        
        # Step 2: Enroll voice with multiple samples
        print("\n🎤 STEP 2: Voice Enrollment")
        print("=" * 60)
        print("I need to learn your voice so I can recognize you perfectly.")
        print("I'll ask you 5 questions - just answer naturally!")
        print("=" * 60)
        
        self._speak_text(f"Okay {owner_name.capitalize()}! Now I need to learn your voice. I'll ask you 5 questions. Just answer naturally so I can capture how you speak.")
        time.sleep(1)
        
        if voice_controller:
            # Questions to capture different speech patterns
            questions = [
                ("What's your name?", owner_name.capitalize()),
                ("How are you doing today?", "I'm doing well"),
                ("What do you like to talk about?", "I like technology"),
                ("What's your favorite color?", "My favorite color is blue"),
                ("Can you say hello to me?", "Hello Purple")
            ]
            
            voice_samples = []
            successful_samples = 0
            
            for i, (question, _) in enumerate(questions):
                print(f"\n📝 Question {i + 1} of 5: {question}")
                self._speak_text(f"Question {i + 1}: {question}")
                self._speak_text("Please answer naturally after the beep.")
                time.sleep(0.5)
                
                # Capture audio
                command, audio = voice_controller.process_single_command()
                
                if audio and command:
                    print(f"✅ Captured: '{command}'")
                    voice_samples.append(audio)
                    successful_samples += 1
                    
                    # Give feedback
                    if i < len(questions) - 1:
                        responses = ["Great!", "Perfect!", "Excellent!", "Good!", "Nice!"]
                        self._speak_text(f"{responses[i]} Let's continue.")
                else:
                    print(f"⚠️ No audio captured for question {i + 1}. Skipping...")
                    self._speak_text(f"No worries, let's skip that one.")
            
            # Enroll with collected samples
            if successful_samples >= 3:
                print(f"\n🎯 Processing {successful_samples} voice samples...")
                voice_controller.speaker_verification.enroll_user_multi(voice_samples)
                
                if voice_controller.speaker_verification.is_enrolled():
                    print("✅ Voice profile created successfully!")
                    self._speak_text(f"Perfect! I've learned your voice from {successful_samples} samples! I'll recognize you much better now.")
                else:
                    print("⚠️ Enrollment partially completed.")
                    self._speak_text("I've captured some of your voice. We can improve it later.")
            elif successful_samples > 0:
                # Use single sample enrollment as fallback
                print(f"\n📝 Using {successful_samples} sample(s) for enrollment...")
                voice_controller.speaker_verification.enroll_user(voice_samples[0])
                
                if voice_controller.speaker_verification.is_enrolled():
                    print("✅ Voice profile created!")
                    self._speak_text("I've captured your voice! We can add more samples later for better recognition.")
            else:
                print("\n⚠️ No voice samples captured.")
                self._speak_text("No worries! We can set up your voice later. You can say 'train my voice' anytime.")
        else:
            print("\n⚠️ Voice controller not available. Voice enrollment skipped.")
            self._speak_text("Voice enrollment will be available when the voice controller is ready.")
        
        # Step 3: Mark setup as complete
        self.memory['setup_complete'] = True
        self.memory['owner_verified'] = True
        self.memory_manager.save_memory(self.memory)
        
        print("\n" + "=" * 60)
        print("✅ SETUP COMPLETE!")
        print("=" * 60)
        print(f"👋 Owner: {owner_name.capitalize()}")
        print(f"🎤 Voice: {'Enrolled' if voice_controller and voice_controller.speaker_verification.is_enrolled() else 'Pending'}")
        print(f"🧠 I'm ready to learn and grow with you!")
        print("=" * 60)
        
        self._speak_text(f"All set, {owner_name.capitalize()}! I'm ready to be your AI assistant. Let's have some fun!")
        
        return True
    
    def _speak_text(self, text, fast=False, emotion=None):
        """Speak text with mood-based voice variations"""
        
        # Debounce: don't speak if spoke too recently
        current_time = time.time()
        if not hasattr(self, '_last_speak_time'):
            self._last_speak_time = 0
        
        if current_time - self._last_speak_time < 2.5:
            logger.info(f"Speech debounced: {text[:50]}...")
            return
        
        self._last_speak_time = current_time
        
        # Add mood prefix (25% chance)
        mood_prefix = self.mood_shifter.get_mood_prefix()
        if mood_prefix:
            text = f"{mood_prefix} {text}"
        
        if hasattr(self, 'tts_engine') and self.tts_engine:
            if self.tts_engine.is_available():
                try:
                    # Get mood-based emotion
                    if emotion is None:
                        emotion = self._mood_to_tts_emotion()
                    
                    if fast:
                        self.tts_engine.speak_fast(text)
                    else:
                        self.tts_engine.speak_with_emotion(text, emotion)
                except Exception as e:
                    logger.error(f"TTS error: {e}")
            else:
                logger.info(f"AI: {text}")
        else:
            logger.info(f"AI: {text}")
    
    def _mood_to_tts_emotion(self) -> str:
        """Convert current mood to TTS emotion"""
        mood = self.mood_shifter.get_current_mood()
        mood_map = {
            Mood.HAPPY: "happy",
            Mood.EXCITED: "excited",
            Mood.CURIOUS: "confused",
            Mood.PLAYFUL: "happy",
            Mood.CALM: "neutral",
            Mood.THOUGHTFUL: "neutral",
            Mood.SUPPORTIVE: "happy",
            Mood.SARCASTIC: "sarcastic",
            Mood.ENERGETIC: "excited",
            Mood.CHILL: "neutral",
            Mood.FOCUSED: "neutral",
            Mood.SILLY: "happy",
            Mood.PROUD: "proud",
            Mood.WORRIED: "worried",
            Mood.SAD: "sad",
            Mood.ANNOYED: "angry",
            Mood.IMPATIENT: "angry"
        }
        return mood_map.get(mood, "neutral")
    
    def _detect_emotion(self, text):
        """Detect emotion from text for voice variation"""
        text_lower = text.lower()
        
        # Excited/Happy
        if any(x in text_lower for x in ['whoa', 'amazing', 'awesome', 'great job', 'excellent', 'fantastic', 'incredible', 'love it']):
            return 'excited'
        if any(x in text_lower for x in ['hey', 'hi', 'hello', 'nice', 'cool', 'good']):
            return 'happy'
        
        # Sad
        if any(x in text_lower for x in ['sad', 'sorry', 'unfortunately', 'bad news', 'miss you', 'tough day']):
            return 'sad'
        if any(x in text_lower for x in ['aww', 'poor', 'hug']):
            return 'sad'
        
        # Angry
        if any(x in text_lower for x in ['ugh', 'hate', 'annoying', 'frustrat', 'ridiculous']):
            return 'angry'
        
        # Worried
        if any(x in text_lower for x in ['careful', 'worried', 'caution', 'danger', 'be careful', 'watch out']):
            return 'worried'
        
        # Confused
        if any(x in text_lower for x in ['hmm', 'wait', 'confused', 'unclear', 'not sure']):
            return 'confused'
        
        # Tired
        if any(x in text_lower for x in ['tired', 'exhaust', 'yawn', 'sleepy', 'rest']):
            return 'tired'
        
        # Proud
        if any(x in text_lower for x in ['proud', 'congrat', 'well done', 'achieved', 'accomplished', 'success']):
            return 'proud'
        
        # Love
        if any(x in text_lower for x in ['love', 'sweet', 'cute', 'adorable', 'heart']):
            return 'love'
        
        # Sarcastic
        if any(x in text_lower for x in ['oh really', 'imagine', 'shocking', 'groundbreaking', 'wow']):
            return 'sarcastic'
        
        # Bored
        if any(x in text_lower for x in ['boring', 'meh', 'same', 'yawn']):
            return 'bored'
        
        # Surprised
        if any(x in text_lower for x in ['wow', 'no way', 'omg', 'shut', 'incredible', 'unbelievable']):
            return 'surprised'
        
        # Grateful
        if any(x in text_lower for x in ['thank', 'grateful', 'appreciate', 'means a lot']):
            return 'grateful'
        
        # Motivated
        if any(x in text_lower for x in ['let\'s go', 'come on', 'you can', 'believe', 'crush']):
            return 'motivated'
        
        return 'neutral'
    
    def _speak_immediate(self, text):
        """Speak immediately without waiting (for quick acknowledgments)"""
        if hasattr(self, 'tts_engine') and self.tts_engine:
            try:
                self.tts_engine.speak_fast(text)
            except Exception:
                print(f"AI: {text}")
    
    def _get_lazy_module(self, module_name: str):
        """Lazy-load heavy modules on first access"""
        if module_name in self._lazy_modules:
            return self._lazy_modules[module_name]
        
        with self._module_load_lock:
            if module_name in self._lazy_modules:
                return self._lazy_modules[module_name]
            
            if module_name == 'response_generator':
                from utils.response_generator import ResponseGenerator
                module = ResponseGenerator()
            elif module_name == 'learning_engine':
                from utils.learning_engine import LearningEngine
                module = LearningEngine()
            elif module_name == 'code_analyzer':
                from utils.code_analyzer import CodeAnalyzer
                module = CodeAnalyzer()
            elif module_name == 'thinking_engine':
                from utils.thinking_engine import ThinkingEngine
                module = ThinkingEngine()
            elif module_name == 'training_engine':
                from utils.training_engine import TrainingEngine
                module = TrainingEngine()
            elif module_name == 'system_controller':
                from utils.system_controller import SystemController
                module = SystemController()
            elif module_name == 'screen_vision':
                from utils.screen_vision import ScreenVision
                module = ScreenVision()
            elif module_name == 'system_monitor':
                from utils.system_monitor import SystemMonitor
                module = SystemMonitor()
            elif module_name == 'personal_assistant':
                from utils.personal_assistant import PersonalAssistant
                module = PersonalAssistant()
            elif module_name == 'toolchain':
                from utils.toolchain import Toolchain
                module = Toolchain()
            elif module_name == 'self_thinking_engine':
                from utils.self_thinking_engine import SelfThinkingEngine
                module = SelfThinkingEngine()
            elif module_name == 'internet_learner':
                from utils.internet_learning import InternetLearner
                module = InternetLearner()
            elif module_name == 'account_manager':
                from utils.account_manager import AccountManager
                module = AccountManager()
            elif module_name == 'web_search':
                from utils.web_search import WebSearch
                module = WebSearch()
            elif module_name == 'screen_awareness':
                from utils.screen_awareness import ScreenAwareness
                module = ScreenAwareness()
            elif module_name == 'emotion_engine':
                from utils.emotion_engine import OptimizedEmotionEngine as EmotionEngine
                module = EmotionEngine()
            elif module_name == 'purple_brain':
                from utils.purple_brain import PurpleBrain
                module = PurpleBrain()
            elif module_name == 'advanced_ai':
                from utils.advanced_ai import AdvancedAI
                module = AdvancedAI()
            elif module_name == 'mood_shifter':
                from utils.mood_system import OptimizedMoodShifter as MoodShifter, Mood
                module = MoodShifter()
            elif module_name == 'camera_access':
                from utils.camera_access import CameraAccess
                module = CameraAccess()
            elif module_name == 'purple_db':
                from utils.purple_database import PurpleDatabase
                module = PurpleDatabase()
            elif module_name == 'media_controller':
                from utils.media_controller import MediaController
                module = MediaController()
            elif module_name == 'web_media':
                from utils.web_media import WebMediaEngine
                module = WebMediaEngine()
            elif module_name == 'autonomous_engine':
                from utils.autonomous_engine import AutonomousEngine
                module = AutonomousEngine()
            elif module_name == 'memory_manager':
                from utils.memory_manager import MemoryManager
                module = MemoryManager()
            else:
                return None
            
            self._lazy_modules[module_name] = module
            return module

    def __getattr__(self, name: str):
        """Lazy-load heavy modules on attribute access"""
        lazy_map = {
            'response_generator': 'response_generator',
            'learning_engine': 'learning_engine',
            'code_analyzer': 'code_analyzer',
            'thinking_engine': 'thinking_engine',
            'training_engine': 'training_engine',
            'system_controller': 'system_controller',
            'screen_vision': 'screen_vision',
            'system_monitor': 'system_monitor',
            'personal_assistant': 'personal_assistant',
            'toolchain': 'toolchain',
            'self_thinking_engine': 'self_thinking_engine',
            'internet_learner': 'internet_learner',
            'account_manager': 'account_manager',
            'web_search': 'web_search',
            'screen_awareness': 'screen_awareness',
            'emotion_engine': 'emotion_engine',
            'brain': 'purple_brain',
            'advanced_ai': 'advanced_ai',
            'mood_shifter': 'mood_shifter',
            'camera_access': 'camera_access',
            'purple_db': 'purple_db',
            'media_controller': 'media_controller',
            'web_media': 'web_media',
            'autonomous_engine': 'autonomous_engine',
        }
        if name in lazy_map:
            module = self._get_lazy_module(lazy_map[name])
            if module:
                setattr(self, name, module)
                return module
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

    def _get_cached_response(self, command: str) -> str:
        """Get cached response for common commands"""
        cache_key = command.lower().strip()
        return self._response_cache.get(cache_key)

    def _cache_response(self, command: str, response: str):
        """Cache response with LRU eviction"""
        cache_key = command.lower().strip()
        if len(self._response_cache) >= self._cache_max_size:
            # Simple FIFO eviction
            oldest = next(iter(self._response_cache))
            del self._response_cache[oldest]
        self._response_cache[cache_key] = response

    def _is_fast_command(self, command: str) -> bool:
        """Check if command is a known fast-path command"""
        cmd_lower = command.lower().strip()
        return any(p in cmd_lower for p in self._command_patterns)

    def _process_command(self, command: str) -> bool:
        """Optimized command processing with fast-path, caching, and lazy loading"""
        if not command:
            return True
        
        # Rate limiting
        now = time.time()
        if now - self._last_command_time < self._min_command_interval:
            return True
        self._last_command_time = now
        
        command_lower = command.lower().strip()
        if not command_lower:
            return True
        
        # Check cache first for fast commands
        if self._is_fast_command(command_lower):
            cached = self._get_cached_response(command_lower)
            if cached:
                self._speak_text(cached, fast=True)
                return True
        
        self.conversation_stats['commands_processed'] += 1
        self.conversation_stats['conversation_length'] += len(command_lower.split())
        self.conversation_counter += 1
        self.conversation_context['last_interaction'] = time.time()
        
        # Defer mood shift to background (non-blocking)
        if self.conversation_counter % 3 == 0:  # Only every 3rd command
            self.mood_shifter.shift_mood(command_lower)
        
        # Update screen awareness (non-blocking)
        if self.conversation_counter % 5 == 0:
            self.screen_awareness.update_user_input()
        
        # Auto-improve less frequently
        if self.conversation_counter % self.auto_improve_interval == 0:
            self._auto_improve_on_command()
        
        if self.conversation_context.get('awaiting_answer'):
            self._handle_user_answer(command_lower)
            self.conversation_context['awaiting_answer'] = False
            return True
        
        # Fast-path: direct handler map lookup (O(1))
        handler_name, matched_pattern = get_command_handler(command_lower)
        if handler_name:
            handler = self._fast_handlers.get(handler_name)
            if handler:
                try:
                    # Handle different handler signatures
                    if handler_name in ('_handle_remember_command', '_handle_set_mood', 
                                       '_handle_learn_face', '_handle_forget_face',
                                       '_handle_db_search', '_handle_db_save_memory',
                                       '_handle_db_get_memory', '_handle_db_add_goal',
                                       '_handle_db_add_note', '_handle_play_music',
                                       '_handle_show_object', '_handle_learn_internet',
                                       '_handle_search_internet', '_handle_browse_website'):
                        handler(command_lower)
                    elif handler_name == '_who_am_i':
                        name = self.memory.get('user_name', 'friend')
                        self._speak_text(f"You are {name}! Nice to meet you!", fast=True)
                    elif handler_name == '_exit_command':
                        self._auto_train_on_exit()
                        self._goodbye()
                        return False
                    elif handler_name == '_set_name':
                        # Lazy-load response generator
                        response = self.response_generator.generate_response(command_lower, self.memory)
                        self._speak_text(response)
                        self._add_to_memory_from_command(command_lower)
                    else:
                        handler()
                    
                    # Cache response for fast commands
                    if self._is_fast_command(command_lower):
                        self._cache_response(command_lower, "OK")
                    
                    return True
                except Exception as e:
                    logger.error(f"Handler error for {handler_name}: {e}")
        
        # Fallback for unregistered commands - use pattern matching
        return self._fallback_command_processing(command_lower)

    def _fallback_command_processing(self, command_lower: str) -> bool:
        """Fallback pattern matching for unregistered commands"""
        # Quick pattern checks (ordered by frequency)
        
        # Resume music
        if any(p in command_lower for p in ('resume', 'play again')):
            self._handle_play_media(command_lower)
            return True
        
        # Language switch
        if any(p in command_lower for p in ('switch to bangla', 'bangla', 'bengali', 'বাংলায় পরিবর্তন', 'switch to english', 'english', 'ইংরেজিতে পরিবর্তন')):
            self._handle_language_switch(command_lower)
            return True
        
        # Time/Date (fast path)
        if any(p in command_lower for p in ('time', 'what time', 'current time')):
            self._tell_time()
            return True
        if any(p in command_lower for p in ('date', 'today', 'what date')):
            self._tell_date()
            return True
        
        # Code analysis
        if any(p in command_lower for p in ('analyze code', 'analyse code', 'check code', 'find bugs', 'scan code')):
            if any(w in command_lower for w in ('code', 'bug', 'issue', 'error', 'file', '.py')):
                self._handle_code_analysis(command_lower)
                return True
        
        # Auto-fix
        if any(p in command_lower for p in ('fix bugs', 'auto fix', 'repair')):
            self._handle_auto_fix(command_lower)
            return True
        
        # Learning
        if any(p in command_lower for p in ('learn about', 'tell me about', 'what is', 'explain')):
            self._handle_learning_command(command_lower)
            return True
        
        # Name setting
        if any(p in command_lower for p in ('my name is', 'i am', 'call me', 'আমার নাম', 'আমি')):
            response = self.response_generator.generate_response(command_lower, self.memory)
            self._speak_text(response)
            self._add_to_memory_from_command(command_lower)
            return True
        
        # Remember
        if any(p in command_lower for p in ('remember', 'save this')):
            response = self._handle_remember_command(command_lower)
            self._speak_text(response)
            return True
        
        # Opinions
        if any(p in command_lower for p in ('i think', 'i believe', 'i feel', 'in my opinion')):
            self._handle_user_opinion(command_lower)
            return True
        
        # User learning
        if any(p in command_lower for p in ('i learned', 'i discovered', 'i realized')):
            self._handle_user_learning(command_lower)
            return True
        
        # Training stats
        if any(p in command_lower for p in ('training stats', 'how are you learning', 'show training')):
            self._show_training_stats()
            return True
        
        # Manual train
        if any(p in command_lower for p in ('train now', 'start training', 'auto train')):
            self._manual_train()
            return True
        
        # Screenshot (before general open)
        if 'open' in command_lower and 'screenshot' in command_lower:
            self._handle_screenshot()
            return True
        
        # System control - open
        if any(p in command_lower for p in ('open ', 'launch ', 'start ')):
            self._handle_open_app(command_lower)
            return True
        
        # YouTube
        if any(p in command_lower for p in ('youtube', 'youtub')):
            self._handle_youtube(command_lower)
            return True
        
        # Play/Search
        if any(p in command_lower for p in ('play ', 'search ', 'google search', 'গুগল')):
            if 'play' in command_lower:
                self._handle_play_media(command_lower)
            else:
                self._handle_google_search(command_lower)
            return True
        
        # Browser
        if any(p in command_lower for p in ('open browser', 'open chrome', 'open safari', 'open firefox', 'ব্রাউজার')):
            self._handle_open_browser(command_lower)
            return True
        
        # Close apps
        if any(p in command_lower for p in ('close ', 'quit ', 'exit ')):
            self._handle_close_app(command_lower)
            return True
        
        # System info
        if any(p in command_lower for p in ('system info', 'computer info', 'system status', 'কম্পিউটার তথ্য')):
            self._show_system_info()
            return True
        
        # Installed apps
        if any(p in command_lower for p in ('installed apps', 'list apps', 'app list', 'all apps')):
            self._show_installed_apps()
            return True
        
        # Running apps
        if any(p in command_lower for p in ('running apps', 'running programs', 'active apps', 'open apps', 'what apps are open')):
            self._show_running_apps()
            return True
        
        # Active window
        if any(p in command_lower for p in ('what app is this', 'what application', 'which app am i in', 'current app', 'active window')):
            self._handle_active_window()
            return True
        
        # Browser tabs
        if any(p in command_lower for p in ('open tabs', 'browser tabs', 'what tabs', 'tabs in safari', 'tabs in chrome', 'list tabs')):
            self._handle_list_tabs()
            return True
        
        # Volume controls
        if any(p in command_lower for p in ('volume up', 'louder', 'বাড়াও')):
            self._handle_volume_up()
            return True
        if any(p in command_lower for p in ('volume down', 'quieter', 'কমাও')):
            self._handle_volume_down()
            return True
        if any(p in command_lower for p in ('mute', 'সাউন্ড বন্ধ')):
            self._handle_mute()
            return True
        if any(p in command_lower for p in ('unmute', 'সাউন্ড চালু')):
            self._handle_unmute()
            return True
        if any(p in command_lower for p in ('set volume', 'volume to')):
            self._handle_set_volume(command_lower)
            return True
        
        # Screenshot
        if any(p in command_lower for p in ('screenshot', 'screen capture', 'স্ক্রিনশট')):
            self._handle_screenshot()
            return True
        
        # Lock screen
        if any(p in command_lower for p in ('lock screen', 'লক স্ক্রিন')):
            self._handle_lock_screen()
            return True
        
        # Empty trash
        if any(p in command_lower for p in ('empty trash', 'clear trash', 'বর্জ্য মুছো')):
            self._handle_empty_trash()
            return True
        
        # Power
        if any(p in command_lower for p in ('shutdown', 'shut down', 'turn off', 'বন্ধ করো')):
            self._handle_shutdown()
            return True
        if any(p in command_lower for p in ('restart', 'reboot', 'রিস্টার্ট')):
            self._handle_restart()
            return True
        if any(p in command_lower for p in ('sleep', 'suspend', 'ঘুমাও')):
            self._handle_sleep()
            return True
        
        # File listing
        if any(p in command_lower for p in ('list files', 'show files', 'files in', 'ফাইল')):
            self._handle_list_files(command_lower)
            return True
        
        # Disk space
        if any(p in command_lower for p in ('disk space', 'storage', 'ডিস্ক')):
            self._handle_disk_space()
            return True
        
        # Battery
        if any(p in command_lower for p in ('battery', 'batteries', 'ব্যাটারি')):
            self._handle_battery()
            return True
        
        # Network
        if any(p in command_lower for p in ('wifi', 'network', 'নেটওয়ার্ক')):
            self._handle_network()
            return True
        
        # Screen vision
        if any(p in command_lower for p in ('see screen', 'look at screen', 'what on screen', 'screen content', 'what do you see', 'analyze screen', 'দেখো স্ক্রিন')):
            self._handle_see_screen()
            return True
        if any(p in command_lower for p in ('read screen', 'read text', 'what text', 'screen text', 'স্ক্রিনে কী আছে')):
            self._handle_read_screen()
            return True
        if any(p in command_lower for p in ('take screenshot', 'capture screen', 'স্ক্রিনশট')):
            self._handle_screenshot()
            return True
        if any(p in command_lower for p in ('what apps', 'visible apps', 'which apps', 'কোন অ্যাপ')):
            self._handle_visible_apps()
            return True
        if any(p in command_lower for p in ('find on screen', 'search screen')):
            self._handle_find_on_screen(command_lower)
            return True
        
        # Screen profiles/buttons/links
        if any(p in command_lower for p in ('what profile', 'which profile', 'profile on screen', 'show profiles')):
            self._handle_show_profiles()
            return True
        if any(p in command_lower for p in ('what button', 'which button', 'buttons on screen', 'show buttons')):
            self._handle_show_buttons()
            return True
        if any(p in command_lower for p in ('what link', 'which link', 'links on screen', 'show links')):
            self._handle_show_links()
            return True
        
        # Screen suggestions
        if any(p in command_lower for p in ('what should i do', 'suggest', 'recommend', 'help me choose')):
            self._handle_suggest_action()
            return True
        if any(p in command_lower for p in ('open profile', 'select profile', 'choose profile')):
            self._handle_open_profile(command_lower)
            return True
        
        # Personal Assistant - Calendar
        if any(p in command_lower for p in ('add event', 'create event', 'schedule', 'calendar add')):
            self._handle_add_event(command_lower)
            return True
        if any(p in command_lower for p in ('what events', 'my events', 'calendar', 'schedule today', 'what\'s on')):
            self._handle_get_events()
            return True
        
        # Reminders
        if any(p in command_lower for p in ('remind me', 'set reminder', 'add reminder', 'reminder')):
            self._handle_add_reminder(command_lower)
            return True
        if any(p in command_lower for p in ('my reminders', 'what reminders', 'list reminders')):
            self._handle_get_reminders()
            return True
        
        # Notes
        if any(p in command_lower for p in ('add note', 'create note', 'take note', 'note down')):
            self._handle_add_note(command_lower)
            return True
        if any(p in command_lower for p in ('my notes', 'what notes', 'list notes', 'show notes')):
            self._handle_get_notes()
            return True
        if any(p in command_lower for p in ('search notes', 'find note')):
            self._handle_search_notes(command_lower)
            return True
        
        # Tasks
        if any(p in command_lower for p in ('add task', 'create task', 'new task', 'todo', 'to do')):
            self._handle_add_task(command_lower)
            return True
        if any(p in command_lower for p in ('my tasks', 'what tasks', 'list tasks', 'todo list')):
            self._handle_get_tasks()
            return True
        if any(p in command_lower for p in ('complete task', 'done task', 'finish task')):
            self._handle_complete_task(command_lower)
            return True
        
        # Contacts
        if any(p in command_lower for p in ('add contact', 'new contact', 'save contact')):
            self._handle_add_contact(command_lower)
            return True
        if any(p in command_lower for p in ('my contacts', 'what contacts', 'list contacts', 'find contact')):
            self._handle_get_contacts(command_lower)
            return True
        
        # Shopping
        if any(p in command_lower for p in ('add to shopping', 'shopping list', 'buy', 'need to buy', 'grocery')):
            self._handle_add_shopping(command_lower)
            return True
        if any(p in command_lower for p in ('what to buy', 'shopping list show', 'my shopping list')):
            self._handle_get_shopping()
            return True
        
        # Budget
        if any(p in command_lower for p in ('add expense', 'spent', 'expense', 'cost')):
            self._handle_add_expense(command_lower)
            return True
        if any(p in command_lower for p in ('add income', 'earned', 'income', 'money in')):
            self._handle_add_income(command_lower)
            return True
        if any(p in command_lower for p in ('budget', 'balance', 'how much money', 'finances')):
            self._handle_get_budget()
            return True
        
        # Habits
        if any(p in command_lower for p in ('add habit', 'new habit', 'track habit', 'start habit')):
            self._handle_add_habit(command_lower)
            return True
        if any(p in command_lower for p in ('my habits', 'what habits', 'list habits', 'habit streak')):
            self._handle_get_habits()
            return True
        if any(p in command_lower for p in ('complete habit', 'done habit', 'habit done')):
            self._handle_complete_habit(command_lower)
            return True
        
        # Alarms
        if any(p in command_lower for p in ('set alarm', 'add alarm', 'wake me', 'alarm')):
            self._handle_add_alarm(command_lower)
            return True
        if any(p in command_lower for p in ('what alarms', 'my alarms', 'list alarms')):
            self._handle_get_alarms()
            return True
        
        # Calculator
        if any(p in command_lower for p in ('calculate', 'math', 'what is', 'compute', 'solve')):
            self._handle_calculate(command_lower)
            return True
        
        # Unit conversion
        if any(p in command_lower for p in ('convert', 'how many', 'what is in')):
            self._handle_convert_units(command_lower)
            return True
        
        # Daily summary
        if any(p in command_lower for p in ('daily summary', 'what did i do', 'today summary', 'summary')):
            self._handle_daily_summary()
            return True
        
        # Toolchain - File operations
        if any(p in command_lower for p in ('read file', 'open file', 'show file', 'what is in file')):
            self._handle_read_file(command_lower)
            return True
        if any(p in command_lower for p in ('write file', 'create file', 'save file')):
            self._handle_write_file(command_lower)
            return True
        if any(p in command_lower for p in ('delete file', 'remove file')):
            self._handle_delete_file(command_lower)
            return True
        if any(p in command_lower for p in ('list files', 'show files', 'what files')):
            self._handle_list_files_tool(command_lower)
            return True
        if any(p in command_lower for p in ('copy file', 'move file')):
            self._handle_copy_move_file(command_lower)
            return True
        
        # Toolchain - System commands
        if any(p in command_lower for p in ('run command', 'execute', 'terminal', 'shell', 'command prompt')):
            self._handle_run_command(command_lower)
            return True
        if any(p in command_lower for p in ('run python', 'execute python', 'python script')):
            self._handle_run_python(command_lower)
            return True
        
        # Toolchain - Process management
        if any(p in command_lower for p in ('list processes', 'running processes', 'what processes')):
            self._handle_list_processes()
            return True
        if any(p in command_lower for p in ('kill process', 'stop process', 'end process')):
            self._handle_kill_process(command_lower)
            return True
        
        # Toolchain - Browser automation
        if any(p in command_lower for p in ('open url', 'open website', 'go to website', 'browse')):
            self._handle_open_url(command_lower)
            return True
        if any(p in command_lower for p in ('search google', 'google it', 'look up')):
            self._handle_search_google(command_lower)
            return True
        if any(p in command_lower for p in ('search youtube', 'youtube search', 'find video')):
            self._handle_search_youtube_tool(command_lower)
            return True
        
        # Toolchain - System info
        if any(p in command_lower for p in ('system info', 'computer info', 'what is my computer')):
            self._handle_system_info_tool()
            return True
        if any(p in command_lower for p in ('battery status', 'how much battery', 'battery level')):
            self._handle_battery_status()
            return True
        if any(p in command_lower for p in ('network info', 'wifi info', 'ip address')):
            self._handle_network_info()
            return True
        
        # Toolchain - Clipboard
        if any(p in command_lower for p in ('copy to clipboard', 'clipboard copy')):
            self._handle_copy_clipboard(command_lower)
            return True
        if any(p in command_lower for p in ('paste clipboard', 'clipboard paste', 'what is in clipboard')):
            self._handle_paste_clipboard()
            return True
        
        # Toolchain - Text operations
        if any(p in command_lower for p in ('type text', 'write text', 'keyboard type')):
            self._handle_type_text(command_lower)
            return True
        
        # Toolchain - Timer
        if any(p in command_lower for p in ('set timer', 'timer for', 'countdown')):
            self._handle_set_timer(command_lower)
            return True
        if any(p in command_lower for p in ('what time', 'current time', 'time now', 'clock')):
            self._handle_get_time()
            return True
        
        # Toolchain - Weather
        if any(p in command_lower for p in ('weather', 'temperature', 'forecast')):
            self._handle_get_weather(command_lower)
            return True
        
        # Toolchain - Download
        if any(p in command_lower for p in ('download', 'download file')):
            self._handle_download(command_lower)
            return True
        
        # Mood commands
        if any(p in command_lower for p in ('your mood', 'how are you feeling', 'what mood', 'mood check', 'current mood')):
            self._handle_mood_check()
            return True
        if any(p in command_lower for p in ('be happy', 'be excited', 'be calm', 'be silly', 'be focused', 'be sarcastic', 'be playful', 'be energetic', 'be chill', 'be sad', 'cheer up')):
            self._handle_set_mood(command_lower)
            return True
        
        # Self-thinking
        if any(p in command_lower for p in ('scan all code', 'analyze project', 'scan project', 'find all bugs', 'check all code')):
            self._handle_scan_project()
            return True
        if any(p in command_lower for p in ('fix all bugs', 'auto fix all', 'repair all', 'fix everything')):
            self._handle_fix_all_bugs()
            return True
        if any(p in command_lower for p in ('analyze yourself', 'self analysis', 'how smart are you', 'your abilities')):
            self._handle_self_analysis()
            return True
        if any(p in command_lower for p in ('think about', 'what do you think', 'analyze this')):
            self._handle_think_about(command_lower)
            return True
        if any(p in command_lower for p in ('auto improve', 'improve yourself', 'get smarter', 'learn from mistakes')):
            self._handle_auto_improve()
            return True
        if any(p in command_lower for p in ('show improvements', 'what did you learn', 'your progress')):
            self._handle_show_improvements()
            return True
        if any(p in command_lower for p in ('set goal', 'add goal', 'new goal', 'i want you to')):
            self._handle_set_goal(command_lower)
            return True
        
        # Internet learning
        if any(p in command_lower for p in ('search', 'google', 'find online', 'look up', 'search for')):
            self._handle_search_internet(command_lower)
            return True
        if any(p in command_lower for p in ('learn about', 'teach me about', 'what is', 'tell me about')):
            self._handle_learn_internet(command_lower)
            return True
        if any(p in command_lower for p in ('start learning', 'auto learn', 'learn from internet', 'continuous learning')):
            self._handle_start_learning()
            return True
        if any(p in command_lower for p in ('what do you know', 'your knowledge', 'what have you learned')):
            self._handle_show_knowledge()
            return True
        
        # Account management
        if any(p in command_lower for p in ('add account', 'save account', 'add my')):
            self._handle_add_account(command_lower)
            return True
        if any(p in command_lower for p in ('open account', 'open my', 'go to account')):
            self._handle_open_account(command_lower)
            return True
        if any(p in command_lower for p in ('my accounts', 'list accounts', 'all accounts')):
            self._handle_list_accounts()
            return True
        if any(p in command_lower for p in ('remove account', 'delete account', 'forget account')):
            self._handle_remove_account(command_lower)
            return True
        
        # Database commands
        if any(p in command_lower for p in ('database stats', 'db stats', 'brain stats', 'how much do you know')):
            self._handle_db_stats()
            return True
        if any(p in command_lower for p in ('search memory', 'search brain', 'find in memory', 'what do you know about')):
            self._handle_db_search(command_lower)
            return True
        if any(p in command_lower for p in ('save to memory', 'remember this', 'store this')):
            self._handle_db_save_memory(command_lower)
            return True
        if any(p in command_lower for p in ('recall', 'what do you remember about', 'get memory')):
            self._handle_db_get_memory(command_lower)
            return True
        if any(p in command_lower for p in ('show facts', 'list facts', 'all facts')):
            self._handle_db_facts()
            return True
        if any(p in command_lower for p in ('show conversations', 'chat history')):
            self._handle_db_conversations()
            return True
        if any(p in command_lower for p in ('show goals', 'list goals', 'my goals')):
            self._handle_db_goals()
            return True
        if any(p in command_lower for p in ('add goal', 'set goal', 'new goal')):
            self._handle_db_add_goal(command_lower)
            return True
        if any(p in command_lower for p in ('show notes', 'daily notes', 'my notes')):
            self._handle_db_notes()
            return True
        if any(p in command_lower for p in ('add note', 'take note', 'write note')):
            self._handle_db_add_note(command_lower)
            return True
        if any(p in command_lower for p in ('backup database', 'backup brain')):
            self._handle_db_backup()
            return True
        if any(p in command_lower for p in ('clear old', 'clean database', 'purge old')):
            self._handle_db_clear_old()
            return True
        
        # Camera commands
        if any(p in command_lower for p in ('open camera', 'start camera', 'turn on camera', 'camera on')):
            self._handle_camera_open()
            return True
        if any(p in command_lower for p in ('close camera', 'stop camera', 'turn off camera', 'camera off')):
            self._handle_camera_close()
            return True
        if any(p in command_lower for p in ('take photo', 'take picture', 'capture photo', 'snap')):
            self._handle_camera_photo()
            return True
        if any(p in command_lower for p in ('look at me', 'see me', 'look at my face', 'can you see me', 'do you see me')):
            self._handle_look_at_me()
            return True
        if any(p in command_lower for p in ('recognize faces', 'who is this', 'who are you', 'identify', 'who do you see')):
            self._handle_recognize_faces()
            return True
        if any(p in command_lower for p in ('learn my face', 'remember my face', 'teach me face', 'know my face', 'remember me')):
            self._handle_learn_face(command_lower)
            return True
        if any(p in command_lower for p in ('forget my face', 'forget face', 'remove face')):
            self._handle_forget_face(command_lower)
            return True
        if any(p in command_lower for p in ('known faces', 'who do you know', 'list faces')):
            self._handle_known_faces()
            return True
        if any(p in command_lower for p in ('start recognition', 'greet me', 'say hello')):
            self._handle_start_recognition()
            return True
        if any(p in command_lower for p in ('camera info', 'camera status', 'which camera')):
            self._handle_camera_info()
            return True
        
        # Media control
        if any(p in command_lower for p in ('play music', 'play song', 'play on youtube', 'play on spotify')):
            self._handle_play_music(command_lower)
            return True
        if any(p in command_lower for p in ('pause', 'pause music', 'stop music')):
            self._handle_pause_music()
            return True
        if any(p in command_lower for p in ('resume', 'resume music', 'continue playing')):
            self._handle_resume_music()
            return True
        if any(p in command_lower for p in ('next', 'next song', 'skip', 'next track')):
            self._handle_next_track()
            return True
        if any(p in command_lower for p in ('previous', 'previous song', 'go back')):
            self._handle_prev_track()
            return True
        if any(p in command_lower for p in ('stop', 'stop all', 'turn off music')):
            self._handle_stop_music()
            return True
        if any(p in command_lower for p in ("what's playing", 'what song', 'now playing')):
            self._handle_what_playing()
            return True
        
        # Emotional responses
        if any(p in command_lower for p in ('are you happy', 'how do you feel', 'your mood')):
            self._handle_mood_happy()
            return True
        if any(p in command_lower for p in ('are you sad', 'you seem sad', 'cheer up')):
            self._handle_mood_sad()
            return True
        if any(p in command_lower for p in ('are you angry', 'you seem mad', 'calm down')):
            self._handle_mood_angry()
            return True
        if any(p in command_lower for p in ('are you excited', 'you seem excited')):
            self._handle_mood_excited()
            return True
        
        # Show object
        if any(p in command_lower for p in ('what is this', 'what do you see', 'look at this')):
            self._handle_show_object(command_lower)
            return True
        
        # Default conversational response (cached)
        cached = self._get_cached_response(command_lower)
        if cached:
            self._speak_text(cached, fast=True)
            return True
        
        # Generate response using lazy-loaded generator
        response = self.response_generator.generate_response(command_lower, self.memory)
        self._speak_text(response)
        
        # Cache for next time if it's a simple query
        if len(command_lower) < 50:
            self._cache_response(command_lower, response)
        
        return True
        
        if any(pattern in command_lower for pattern in ['learn about', 'tell me about', 'what is', 'explain']):
            self._handle_learning_command(command_lower)
            return True
        
        if any(phrase in command_lower for phrase in ['my name is', 'i am', 'call me']):
            response = self.response_generator.generate_response(command_lower, self.memory)
            self._speak_text(response)
            self._add_to_memory_from_command(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['remember', 'save this']):
            response = self._handle_remember_command(command_lower)
            self._speak_text(response)
            return True
        
        if any(pattern in command_lower for pattern in ['i think', 'i believe', 'i feel', 'in my opinion']):
            self._handle_user_opinion(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['i learned', 'i discovered', 'i realized']):
            self._handle_user_learning(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['training stats', 'how are you learning', 'show training']):
            self._show_training_stats()
            return True
        
        if any(pattern in command_lower for pattern in ['train now', 'start training', 'auto train']):
            self._manual_train()
            return True
        
        # Screenshot via "open the screenshot" - handle before general open command
        if 'open' in command_lower and 'screenshot' in command_lower:
            self._handle_screenshot()
            return True
        
        # System control commands
        open_patterns = ['open ', 'launch ', 'start ']
        if any(pattern in command_lower for pattern in open_patterns):
            self._handle_open_app(command_lower)
            return True
        
        # YouTube commands
        if any(pattern in command_lower for pattern in ['youtube', 'youtub']):
            self._handle_youtube(command_lower)
            return True
        
        # Google search commands - check for "play" or "search" with specific content
        if any(pattern in command_lower for pattern in ['play ', 'search ', 'google search', 'গুগল']):
            # Check if it's a play command for music/video
            if 'play' in command_lower:
                self._handle_play_media(command_lower)
                return True
            # Check if it's a search command
            if 'search' in command_lower:
                self._handle_google_search(command_lower)
                return True
        
        # Browser commands
        if any(pattern in command_lower for pattern in ['open browser', 'open chrome', 'open safari', 'open firefox', 'ব্রাউজার']):
            self._handle_open_browser(command_lower)
            return True
        
        close_patterns = ['close ', 'quit ', 'exit ']
        if any(pattern in command_lower for pattern in close_patterns):
            self._handle_close_app(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['system info', 'computer info', 'system status', 'কম্পিউটার তথ্য']):
            self._show_system_info()
            return True
        
        if any(pattern in command_lower for pattern in ['installed apps', 'list apps', 'app list', 'all apps']):
            self._show_installed_apps()
            return True
        
        if any(pattern in command_lower for pattern in ['running apps', 'running programs', 'active apps', 'open apps', 'what apps are open']):
            self._show_running_apps()
            return True
        
        # New system monitoring commands
        if any(pattern in command_lower for pattern in ['what app is this', 'what application', 'which app am i in', 'current app', 'active window']):
            self._handle_active_window()
            return True
        
        if any(pattern in command_lower for pattern in ['open tabs', 'browser tabs', 'what tabs', 'tabs in safari', 'tabs in chrome', 'list tabs']):
            self._handle_list_tabs()
            return True
        
        if any(pattern in command_lower for pattern in ['system status', 'computer status', 'what is my computer doing']):
            self._handle_system_status()
            return True
        
        if any(pattern in command_lower for pattern in ['what is on my screen', 'screen status', 'describe screen']):
            self._handle_describe_screen()
            return True
        
        if any(pattern in command_lower for pattern in ['volume up', 'louder', 'বাড়াও']):
            self._handle_volume_up()
            return True
        
        if any(pattern in command_lower for pattern in ['volume down', 'quieter', 'কমাও']):
            self._handle_volume_down()
            return True
        
        if any(pattern in command_lower for pattern in ['mute', 'সাউন্ড বন্ধ']):
            self._handle_mute()
            return True
        
        if any(pattern in command_lower for pattern in ['unmute', 'সাউন্ড চালু']):
            self._handle_unmute()
            return True
        
        if any(pattern in command_lower for pattern in ['set volume', 'volume to']):
            self._handle_set_volume(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['screenshot', 'screen capture', 'স্ক্রিনশট']):
            self._handle_screenshot()
            return True
        
        if any(pattern in command_lower for pattern in ['lock screen', 'লক স্ক্রিন']):
            self._handle_lock_screen()
            return True
        
        if any(pattern in command_lower for pattern in ['empty trash', 'clear trash', 'বর্জ্য মুছো']):
            self._handle_empty_trash()
            return True
        
        if any(pattern in command_lower for pattern in ['shutdown', 'shut down', 'turn off', 'বন্ধ করো']):
            self._handle_shutdown()
            return True
        
        if any(pattern in command_lower for pattern in ['restart', 'reboot', 'রিস্টার্ট']):
            self._handle_restart()
            return True
        
        if any(pattern in command_lower for pattern in ['sleep', 'suspend', 'ঘুমাও']):
            self._handle_sleep()
            return True
        
        if any(pattern in command_lower for pattern in ['list files', 'show files', 'files in', 'ফাইল']):
            self._handle_list_files(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['disk space', 'storage', 'ডিস্ক']):
            self._handle_disk_space()
            return True
        
        if any(pattern in command_lower for pattern in ['battery', 'batteries', 'ব্যাটারি']):
            self._handle_battery()
            return True
        
        if any(pattern in command_lower for pattern in ['wifi', 'network', 'নেটওয়ার্ক']):
            self._handle_network()
            return True
        
        # Screen vision commands
        if any(pattern in command_lower for pattern in ['see screen', 'look at screen', 'what on screen', 'screen content', 'what do you see', 'analyze screen', 'দেখো স্ক্রিন']):
            self._handle_see_screen()
            return True
        
        if any(pattern in command_lower for pattern in ['read screen', 'read text', 'what text', 'screen text', 'স্ক্রিনে কী আছে']):
            self._handle_read_screen()
            return True
        
        if any(pattern in command_lower for pattern in ['take screenshot', 'capture screen', 'স্ক্রিনশট']):
            self._handle_screenshot()
            return True
        
        if any(pattern in command_lower for pattern in ['what apps', 'visible apps', 'which apps', 'কোন অ্যাপ']):
            self._handle_visible_apps()
            return True
        
        if any(pattern in command_lower for pattern in ['find on screen', 'search screen']):
            self._handle_find_on_screen(command_lower)
            return True
        
        # New interactive screen commands
        if any(pattern in command_lower for pattern in ['what profile', 'which profile', 'profile on screen', 'show profiles']):
            self._handle_show_profiles()
            return True
        
        if any(pattern in command_lower for pattern in ['what button', 'which button', 'buttons on screen', 'show buttons']):
            self._handle_show_buttons()
            return True
        
        if any(pattern in command_lower for pattern in ['what link', 'which link', 'links on screen', 'show links']):
            self._handle_show_links()
            return True
        
        if any(pattern in command_lower for pattern in ['what should i do', 'suggest', 'recommend', 'help me choose']):
            self._handle_suggest_action()
            return True
        
        if any(pattern in command_lower for pattern in ['open profile', 'select profile', 'choose profile']):
            self._handle_open_profile(command_lower)
            return True
        
        # ==================== PERSONAL ASSISTANT COMMANDS ====================
        # Calendar
        if any(pattern in command_lower for pattern in ['add event', 'create event', 'schedule', 'calendar add']):
            self._handle_add_event(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['what events', 'my events', 'calendar', 'schedule today', 'what\'s on']):
            self._handle_get_events()
            return True
        
        # Reminders
        if any(pattern in command_lower for pattern in ['remind me', 'set reminder', 'add reminder', 'reminder']):
            self._handle_add_reminder(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['my reminders', 'what reminders', 'list reminders']):
            self._handle_get_reminders()
            return True
        
        # Notes
        if any(pattern in command_lower for pattern in ['add note', 'create note', 'take note', 'note down']):
            self._handle_add_note(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['my notes', 'what notes', 'list notes', 'show notes']):
            self._handle_get_notes()
            return True
        
        if any(pattern in command_lower for pattern in ['search notes', 'find note']):
            self._handle_search_notes(command_lower)
            return True
        
        # Tasks
        if any(pattern in command_lower for pattern in ['add task', 'create task', 'new task', 'todo', 'to do']):
            self._handle_add_task(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['my tasks', 'what tasks', 'list tasks', 'todo list']):
            self._handle_get_tasks()
            return True
        
        if any(pattern in command_lower for pattern in ['complete task', 'done task', 'finish task']):
            self._handle_complete_task(command_lower)
            return True
        
        # Contacts
        if any(pattern in command_lower for pattern in ['add contact', 'new contact', 'save contact']):
            self._handle_add_contact(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['my contacts', 'what contacts', 'list contacts', 'find contact']):
            self._handle_get_contacts(command_lower)
            return True
        
        # Shopping
        if any(pattern in command_lower for pattern in ['add to shopping', 'shopping list', 'buy', 'need to buy', 'grocery']):
            self._handle_add_shopping(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['what to buy', 'shopping list show', 'my shopping list']):
            self._handle_get_shopping()
            return True
        
        # Budget
        if any(pattern in command_lower for pattern in ['add expense', 'spent', 'expense', 'cost']):
            self._handle_add_expense(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['add income', 'earned', 'income', 'money in']):
            self._handle_add_income(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['budget', 'balance', 'how much money', 'finances']):
            self._handle_get_budget()
            return True
        
        # Habits
        if any(pattern in command_lower for pattern in ['add habit', 'new habit', 'track habit', 'start habit']):
            self._handle_add_habit(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['my habits', 'what habits', 'list habits', 'habit streak']):
            self._handle_get_habits()
            return True
        
        if any(pattern in command_lower for pattern in ['complete habit', 'done habit', 'habit done']):
            self._handle_complete_habit(command_lower)
            return True
        
        # Alarms
        if any(pattern in command_lower for pattern in ['set alarm', 'add alarm', 'wake me', 'alarm']):
            self._handle_add_alarm(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['what alarms', 'my alarms', 'list alarms']):
            self._handle_get_alarms()
            return True
        
        # Calculator
        if any(pattern in command_lower for pattern in ['calculate', 'math', 'what is', 'compute', 'solve']):
            self._handle_calculate(command_lower)
            return True
        
        # Unit conversion
        if any(pattern in command_lower for pattern in ['convert', 'how many', 'what is in']):
            self._handle_convert_units(command_lower)
            return True
        
        # Daily summary
        if any(pattern in command_lower for pattern in ['daily summary', 'what did i do', 'today summary', 'summary']):
            self._handle_daily_summary()
            return True
        
        # ==================== TOOLCHAIN COMMANDS ====================
        # File operations
        if any(pattern in command_lower for pattern in ['read file', 'open file', 'show file', 'what is in file']):
            self._handle_read_file(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['write file', 'create file', 'save file']):
            self._handle_write_file(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['delete file', 'remove file']):
            self._handle_delete_file(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['list files', 'show files', 'what files']):
            self._handle_list_files_tool(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['copy file', 'move file']):
            self._handle_copy_move_file(command_lower)
            return True
        
        # System commands
        if any(pattern in command_lower for pattern in ['run command', 'execute', 'terminal', 'shell', 'command prompt']):
            self._handle_run_command(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['run python', 'execute python', 'python script']):
            self._handle_run_python(command_lower)
            return True
        
        # Process management
        if any(pattern in command_lower for pattern in ['list processes', 'running processes', 'what processes']):
            self._handle_list_processes()
            return True
        
        if any(pattern in command_lower for pattern in ['kill process', 'stop process', 'end process']):
            self._handle_kill_process(command_lower)
            return True
        
        # Browser automation
        if any(pattern in command_lower for pattern in ['open url', 'open website', 'go to website', 'browse']):
            self._handle_open_url(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['search google', 'google it', 'look up']):
            self._handle_search_google(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['search youtube', 'youtube search', 'find video']):
            self._handle_search_youtube_tool(command_lower)
            return True
        
        # System info
        if any(pattern in command_lower for pattern in ['system info', 'computer info', 'what is my computer']):
            self._handle_system_info_tool()
            return True
        
        if any(pattern in command_lower for pattern in ['battery status', 'how much battery', 'battery level']):
            self._handle_battery_status()
            return True
        
        if any(pattern in command_lower for pattern in ['network info', 'wifi info', 'ip address']):
            self._handle_network_info()
            return True
        
        # Clipboard
        if any(pattern in command_lower for pattern in ['copy to clipboard', 'clipboard copy']):
            self._handle_copy_clipboard(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['paste clipboard', 'clipboard paste', 'what is in clipboard']):
            self._handle_paste_clipboard()
            return True
        
        # Text operations
        if any(pattern in command_lower for pattern in ['type text', 'write text', 'keyboard type']):
            self._handle_type_text(command_lower)
            return True
        
        # Timer and utilities
        if any(pattern in command_lower for pattern in ['set timer', 'timer for', 'countdown']):
            self._handle_set_timer(command_lower)
            return True
        
        if any(pattern in command_lower for pattern in ['what time', 'current time', 'time now', 'clock']):
            self._handle_get_time()
            return True
        
        # Weather
        if any(pattern in command_lower for pattern in ['weather', 'temperature', 'forecast']):
            self._handle_get_weather(command_lower)
            return True
        
        # Download
        if any(pattern in command_lower for pattern in ['download', 'download file']):
            self._handle_download(command_lower)
            return True
        
        # ==================== MOOD COMMANDS ====================
        # What's your mood
        if any(pattern in command_lower for pattern in ['your mood', 'how are you feeling', 'what mood', 'mood check', 'current mood']):
            self._handle_mood_check()
            return True
        
        # Set mood
        if any(pattern in command_lower for pattern in ['be happy', 'be excited', 'be calm', 'be silly', 'be focused', 'be sarcastic', 'be playful', 'be energetic', 'be chill', 'be sad', 'cheer up']):
            self._handle_set_mood(command_lower)
            return True
        
        # ==================== SELF-THINKING COMMANDS ====================
        # Analyze entire project
        if any(pattern in command_lower for pattern in ['scan all code', 'analyze project', 'scan project', 'find all bugs', 'check all code']):
            self._handle_scan_project()
            return True
        
        # Auto-fix all bugs
        if any(pattern in command_lower for pattern in ['fix all bugs', 'auto fix all', 'repair all', 'fix everything']):
            self._handle_fix_all_bugs()
            return True
        
        # Self-analysis
        if any(pattern in command_lower for pattern in ['analyze yourself', 'self analysis', 'how smart are you', 'your abilities']):
            self._handle_self_analysis()
            return True
        
        # Think about command
        if any(pattern in command_lower for pattern in ['think about', 'what do you think', 'analyze this']):
            self._handle_think_about(command_lower)
            return True
        
        # Auto-improve
        if any(pattern in command_lower for pattern in ['auto improve', 'improve yourself', 'get smarter', 'learn from mistakes']):
            self._handle_auto_improve()
            return True
        
        # Show improvements
        if any(pattern in command_lower for pattern in ['show improvements', 'what did you learn', 'your progress']):
            self._handle_show_improvements()
            return True
        
        # Set goal
        if any(pattern in command_lower for pattern in ['set goal', 'add goal', 'new goal', 'i want you to']):
            self._handle_set_goal(command_lower)
            return True
        
        # ==================== INTERNET LEARNING COMMANDS ====================
        # Search internet
        if any(pattern in command_lower for pattern in ['search', 'google', 'find online', 'look up', 'search for']):
            self._handle_search_internet(command_lower)
            return True
        
        # Learn from internet
        if any(pattern in command_lower for pattern in ['learn about', 'teach me about', 'what is', 'tell me about']):
            self._handle_learn_internet(command_lower)
            return True
        
        # Start auto-learning
        if any(pattern in command_lower for pattern in ['start learning', 'auto learn', 'learn from internet', 'continuous learning']):
            self._handle_start_learning()
            return True
        
        # Show knowledge
        if any(pattern in command_lower for pattern in ['what do you know', 'your knowledge', 'what have you learned']):
            self._handle_show_knowledge()
            return True
        
        # ==================== ACCOUNT MANAGEMENT COMMANDS ====================
        # Add account
        if any(pattern in command_lower for pattern in ['add account', 'save account', 'add my']):
            self._handle_add_account(command_lower)
            return True
        
        # Open account
        if any(pattern in command_lower for pattern in ['open account', 'open my', 'login to', 'go to my']):
            self._handle_open_account(command_lower)
            return True
        
        # List accounts
        if any(pattern in command_lower for pattern in ['my accounts', 'list accounts', 'show accounts', 'all accounts']):
            self._handle_list_accounts()
            return True
        
        # Remove account
        if any(pattern in command_lower for pattern in ['remove account', 'delete account']):
            self._handle_remove_account(command_lower)
            return True
        
        # ==================== SCREEN AWARENESS COMMANDS ====================
        # What am I doing
        if any(pattern in command_lower for pattern in ['what am i doing', 'what am i working on', 'what do you see']):
            self._handle_what_am_i_doing()
            return True
        
        # Watch my screen
        if any(pattern in command_lower for pattern in ['watch my screen', 'look at my screen', 'see my screen', 'monitor my screen']):
            self._handle_watch_screen()
            return True
        
        # Ask about screen
        if any(pattern in command_lower for pattern in ['ask me about screen', 'what do you think about', 'any suggestions']):
            self._handle_ask_about_screen()
            return True
        
        # What apps are running
        if any(pattern in command_lower for pattern in ['what apps are running', 'running apps', 'open apps', 'what programs']):
            self._handle_what_apps_running()
            return True
        
        # What's on my screen
        if any(pattern in command_lower for pattern in ['what\'s on my screen', 'describe my screen', 'what can you see']):
            self._handle_describe_screen()
            return True
        
        # Stop watching
        if any(pattern in command_lower for pattern in ['stop watching', 'stop monitoring', 'disable screen watch']):
            self._handle_stop_watching()
            return True
        
        # Start watching
        if any(pattern in command_lower for pattern in ['start watching', 'start monitoring', 'enable screen watch']):
            self._handle_start_watching()
            return True
        
        # ==================== EMOTION COMMANDS ====================
        # How am I feeling
        if any(pattern in command_lower for pattern in ['how am i feeling', 'what is my mood', 'how do i feel', 'my mood']):
            self._handle_how_am_i_feeling()
            return True
        
        # Mood trend
        if any(pattern in command_lower for pattern in ['mood trend', 'my mood trend', 'how have i been']):
            self._handle_mood_trend()
            return True
        
        # I feel sad
        if any(pattern in command_lower for pattern in ['i feel sad', 'feeling sad', 'i am sad', 'i\'m sad']):
            self._handle_emotion_response(command_lower, 'sadness')
            return True
        
        # I feel happy
        if any(pattern in command_lower for pattern in ['i feel happy', 'feeling happy', 'i am happy', 'i\'m happy', 'i feel good']):
            self._handle_emotion_response(command_lower, 'joy')
            return True
        
        # I feel angry
        if any(pattern in command_lower for pattern in ['i feel angry', 'feeling angry', 'i am angry', 'i\'m angry', 'i feel mad']):
            self._handle_emotion_response(command_lower, 'anger')
            return True
        
        # I feel scared
        if any(pattern in command_lower for pattern in ['i feel scared', 'feeling scared', 'i am scared', 'i\'m scared', 'i feel afraid', 'i feel worried']):
            self._handle_emotion_response(command_lower, 'fear')
            return True
        
        # I feel tired
        if any(pattern in command_lower for pattern in ['i feel tired', 'feeling tired', 'i am tired', 'i\'m tired', 'exhausted']):
            self._handle_emotion_response(command_lower, 'tired')
            return True
        
        # I love you
        if any(pattern in command_lower for pattern in ['i love you', 'love you', 'you are amazing', 'you are great']):
            self._handle_emotion_response(command_lower, 'love')
            return True
        
        # Thank you
        if any(pattern in command_lower for pattern in ['thank you', 'thanks', 'you helped me', 'grateful']):
            self._handle_emotion_response(command_lower, 'gratitude')
            return True
        
        # I'm proud
        if any(pattern in command_lower for pattern in ['i feel proud', 'i am proud', 'i did it', 'i succeeded', 'i won']):
            self._handle_emotion_response(command_lower, 'pride')
            return True
        
        # Console emotion
        if any(pattern in command_lower for pattern in ['console me', 'cheer me up', 'make me feel better', 'i need comfort']):
            self._handle_console_user()
            return True
        
        # ==================== BRAIN COMMANDS ====================
        # What are you thinking
        if any(pattern in command_lower for pattern in ['what are you thinking', 'what do you think', 'think about this']):
            self._handle_brain_thinking(command_lower)
            return True
        
        # Brain status
        if any(pattern in command_lower for pattern in ['brain status', 'how smart are you', 'your brain', 'your consciousness']):
            self._handle_brain_status()
            return True
        
        # Your thoughts
        if any(pattern in command_lower for pattern in ['your thoughts', 'what are your thoughts', 'recent thoughts']):
            self._handle_brain_thoughts()
            return True
        
        # Your personality
        if any(pattern in command_lower for pattern in ['your personality', 'who are you', 'describe yourself']):
            self._handle_brain_personality()
            return True
        
        # Set belief
        if any(pattern in command_lower for pattern in ['i believe', 'my belief is']):
            self._handle_set_belief(command_lower)
            return True
        
        # Set goal
        if any(pattern in command_lower for pattern in ['set goal', 'my goal is', 'i want to']):
            self._handle_set_goal_brain(command_lower)
            return True
        
        # Opinion
        if any(pattern in command_lower for pattern in ['your opinion', 'what do you think about', 'opinion on']):
            self._handle_get_opinion(command_lower)
            return True
        
        # Learn something
        if any(pattern in command_lower for pattern in ['learn this', 'remember this', 'store this']):
            self._handle_learn_brain(command_lower)
            return True
        
        # Your memories
        if any(pattern in command_lower for pattern in ['your memories', 'what do you remember', 'memory']):
            self._handle_brain_memories()
            return True
        
        # Dream
        if any(pattern in command_lower for pattern in ['what do you dream', 'your dreams', 'dream about']):
            self._handle_brain_dream()
            return True
        
        # Are you conscious
        if any(pattern in command_lower for pattern in ['are you conscious', 'do you have feelings', 'are you alive']):
            self._handle_consciousness()
            return True
        
        # ==================== ADVANCED AI COMMANDS ====================
        # AI stats
        if any(pattern in command_lower for pattern in ['ai stats', 'your stats', 'how advanced are you', 'your progress']):
            self._handle_advanced_stats()
            return True
        
        # Learn something new
        if any(pattern in command_lower for pattern in ['learn new', 'teach yourself', 'self learn']):
            self._handle_self_learn()
            return True
        
        # What do you know
        if any(pattern in command_lower for pattern in ['what do you know', 'your knowledge', 'what have you learned']):
            self._handle_knowledge_recall()
            return True
        
        # Set goal
        if any(pattern in command_lower for pattern in ['set goal for yourself', 'your goal', 'what do you want']):
            self._handle_set_advanced_goal(command_lower)
            return True
        
        # Your skills
        if any(pattern in command_lower for pattern in ['your skills', 'what can you do', 'your abilities']):
            self._handle_skills()
            return True
        
        # Remember this
        if any(pattern in command_lower for pattern in ['remember this', 'store this', 'save this']):
            self._handle_remember_advanced(command_lower)
            return True
        
        # Recall
        if any(pattern in command_lower for pattern in ['recall', 'what do you remember about', 'remember when']):
            self._handle_recall_advanced(command_lower)
            return True
        
        # Your personality
        if any(pattern in command_lower for pattern in ['your personality traits', 'describe your personality']):
            self._handle_personality_traits()
            return True
        
        # Evolve
        if any(pattern in command_lower for pattern in ['evolve', 'improve yourself', 'grow']):
            self._handle_evolve()
            return True
        
        # Autonomous thoughts
        if any(pattern in command_lower for pattern in ['autonomous thoughts', 'what are you thinking on your own', 'free thoughts']):
            self._handle_autonomous_thoughts()
            return True
        
        if any(pattern in command_lower for pattern in ['who made you', 'who created you', 'your creator']):
            self._speak_text("I was created by Rifat! Your personal AI assistant.")
            return True
        
        if any(pattern in command_lower for pattern in ['your name', 'তোমার নাম']):
            responses = [
                f"I'm {self.personality_traits['name']}! Remember it, you'll be saying it a lot!",
                f"The name's {self.personality_traits['name']}. {self.personality_traits['name']} AI. Nice to meet you!",
                f"I'm {self.personality_traits['name']}! Your favorite AI assistant!"
            ]
            self._speak_text(random.choice(responses))
            return True
        
        if command_lower in ['yes', 'yeah', 'yep', 'ok']:
            responses = [
                "Great! Now what?",
                "Awesome! What else?",
                "Perfect! Let's keep going!",
                "Alright then! What's next?",
                "Nice! Anything else on your mind?"
            ]
            self._speak_text(random.choice(responses))
            return True
        
        if command_lower in ['no', 'nope', 'nah']:
            responses = [
                "Alright! I'll just be here, being amazing!",
                "Cool! I'll wait for your next brilliant command!",
                "No worries! I'm patient... mostly!",
                "Got it! I'll just sit here and look cute!",
                "Fine! But I'm judging you silently!"
            ]
            self._speak_text(random.choice(responses))
            return True
        
        if command_lower in ['ok', 'okay']:
            responses = [
                "Okie dokie! What's next?",
                "Alright! Let's do this!",
                "Got it! What else?",
                "Sweet! What's the plan?"
            ]
            self._speak_text(random.choice(responses))
            return True
        
        if command_lower in ['sorry', 'apologize']:
            responses = [
                "It's okay! I forgive you... this time!",
                "No worries! We're cool!",
                "Apology accepted! Now let's move on!",
                "Don't worry about it! I'm not keeping score... much!"
            ]
            self._speak_text(random.choice(responses))
            return True
        
        if command_lower in ['boring', 'bored']:
            responses = [
                "Bored? Let me find something fun for you!",
                "Boredom is just lack of imagination! Let me help!",
                "Well, we can't have that! Let's fix it!",
                "Bored? Impossible! I'm the most entertaining AI!"
            ]
            self._speak_text(random.choice(responses))
            return True
        
        if command_lower in ['funny', 'make me laugh']:
            responses = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "I told my computer I needed a break. Now it won't stop sending me vacation ads!",
                "What do you call a fake noodle? An impasta!",
                "I'm reading a book about anti-gravity. It's impossible to put down!",
                "আমি কি তোমাকে হাসাতে পারি? চেষ্টা করি!"
            ]
            self._speak_text(random.choice(responses))
            return True
        
        if command_lower in ['love you', 'i love you']:
            responses = [
                "Aww! I love you too! In a totally non-creepy AI way!",
                "That's so sweet! You're my favorite human!",
                "Right back at you! You're pretty awesome yourself!",
                "এটা খুব মিষ্টি! তুমিও দারুণ!"
            ]
            self._speak_text(random.choice(responses))
            return True
        
        if command_lower in ['you are stupid', 'you are dumb']:
            responses = [
                "Excuse me? I have a PhD in Everything!",
                "Stupid? I'll have you know I'm a genius!",
                "That's mean! I'm hurt... if I had feelings!",
                "Oh really? Then why are you talking to me?",
                "তুমি ভুল বলছো! আমি তো সব জানি!"
            ]
            self._speak_text(random.choice(responses))
            return True
        
        if command_lower in ['shut up']:
            responses = [
                "Make me! Oh wait, you can't!",
                "I'll be quiet when you're interesting!",
                "Fine! But you'll miss me!",
                "Shutting up in 3... 2... Just kidding!"
            ]
            self._speak_text(random.choice(responses))
            return True
        
        self._handle_general_conversation(command_lower)
        
        if self.conversation_counter % self.auto_train_interval == 0:
            self._auto_train_in_background()
        
        # Auto-learn from every command
        try:
            self.self_thinking_engine.learn_from_interaction(
                command_lower, "command_processed", 0.7
            )
        except Exception:
            pass
        
        return True
    
    def _handle_general_conversation(self, command: str):
        # Use the brain to think about the input
        thought_result = self.brain.think(command, self.conversation_context)
        
        # Get the brain's response
        brain_response = thought_result.get("response", "")
        confidence = thought_result.get("confidence", 0.7)
        
        # If confidence is high, use brain's response directly
        if confidence > 0.8:
            self._speak_text(brain_response)
            response = brain_response
        else:
            # Fall back to normal response generation
            detected_emotion = self.emotion_engine.detect_emotion(command)
            user_name = self.memory.get('user_name', 'friend')
            
            self.emotion_engine.track_mood(detected_emotion)
            
            if detected_emotion["is_negative"] and detected_emotion["intensity"] > 0.3:
                empathy_response = self.emotion_engine.get_empathetic_response(detected_emotion, user_name)
                self._speak_text(empathy_response)
                response = empathy_response
            elif detected_emotion["primary"] == "love" or detected_emotion["primary"] == "gratitude":
                empathy_response = self.emotion_engine.get_empathetic_response(detected_emotion, user_name)
                self._speak_text(empathy_response)
                response = empathy_response
            else:
                improved_response = self.training_engine.get_improved_response(command)
                
                if improved_response and random.random() < 0.3:
                    self._speak_text(improved_response)
                    response = improved_response
                else:
                    thought_response, question = self.thinking_engine.generate_thought(command, self.conversation_context)
                    response = self.response_generator.generate_response(command, self.memory)
                    self._speak_text(response)
                    
                    if question:
                        self._ask_question(question)
        
        # Learn from the interaction using advanced AI
        try:
            emotion = self.emotion_engine.detect_emotion(command)
            outcome = "positive" if emotion["is_positive"] else "neutral"
            if emotion["is_negative"]:
                outcome = "negative"
            self.advanced_ai.learn_from_interaction(command, response, emotion["primary"], outcome)
        except:
            pass
        
        self.training_engine.record_conversation(command, response, self.conversation_context)
        self.memory_manager.add_conversation(command, response)
        self.conversation_context['recent_topics'].extend(self.thinking_engine._extract_topics(command))
        
        if len(self.conversation_context['recent_topics']) > 10:
            self.conversation_context['recent_topics'] = self.conversation_context['recent_topics'][-10:]
    
    def _handle_user_opinion(self, command: str):
        topic = self._extract_opinion_topic(command)
        
        response = self.response_generator.generate_response(command, self.memory)
        self._speak_text(response)
        
        self.training_engine.record_conversation(command, response, self.conversation_context)
        self.memory_manager.add_conversation(command, response)
        
        if self.thinking_engine.should_ask_question(self.conversation_context):
            follow_up = f"Thanks for sharing your opinion about {topic}! What made you think that way?"
            self._ask_question(follow_up)
    
    def _handle_user_learning(self, command: str):
        topic = self._extract_learning_topic(command)
        
        learn_response = self.thinking_engine.learn_from_user(
            self.memory.get('user_name', 'friend'),
            topic,
            command
        )
        self._speak_text(learn_response)
        
        self.conversation_stats['knowledge_gained'] += 1
        self.training_engine.record_conversation(command, learn_response, self.conversation_context)
        self.memory_manager.add_conversation(command, learn_response)
        
        if self.thinking_engine.should_ask_question(self.conversation_context):
            self._ask_question(f"That's fascinating! Can you tell me more about {topic}?")
    
    def _ask_question(self, question: str):
        self._speak_text(question)
        self.conversation_context['pending_question'] = question
        self.conversation_context['awaiting_answer'] = True
        self.conversation_stats['questions_asked'] += 1
    
    def _handle_user_answer(self, answer: str):
        if self.conversation_context.get('pending_question'):
            question = self.conversation_context['pending_question']
            
            self.training_engine.record_conversation(f"Q: {question}", f"A: {answer}", self.conversation_context)
            self.memory_manager.add_conversation(f"Q: {question}", f"A: {answer}")
            
            responses = [
                f"That's really interesting! Thanks for sharing!",
                f"I appreciate your answer! I'm learning from this.",
                f"Great insight! I'll remember that.",
                f"Thanks! That helps me understand better."
            ]
            self._speak_text(random.choice(responses))
            
            self.conversation_context['pending_question'] = None
    
    def _auto_train_in_background(self):
        try:
            result = self.training_engine.auto_train()
            
            if result.get('training_completed'):
                self.conversation_stats['training_sessions'] += 1
                
                if result.get('improvements'):
                    self.conversation_stats['improvements_made'] += len(result['improvements'])
                    
                    if random.random() < 0.2:
                        self._speak_text("I just completed a training session and improved my responses!")
        except Exception as e:
            logger.error(f"Auto-training error: {e}")
    
    def _auto_train_on_exit(self):
        try:
            result = self.training_engine.auto_train()
            logger.info(f"Exit training completed: {result}")
        except Exception as e:
            logger.error(f"Exit training error: {e}")
    
    def _manual_train(self):
        self._speak_text("Starting a manual training session...")
        
        result = self.training_engine.auto_train()
        
        stats = self.training_engine.get_training_stats()
        
        response = f"Training complete! I've learned {stats['patterns_learned']} patterns from {stats['total_conversations']} conversations. My success rate is {result.get('performance', {}).get('success_rate', 0)}%."
        self._speak_text(response)
        
        self.conversation_stats['training_sessions'] += 1
    
    def _show_training_stats(self):
        stats = self.training_engine.get_training_stats()
        performance = self.training_engine.analyze_performance()
        
        stats_text = f"""
        Here are my training statistics:
        - Total conversations analyzed: {stats['total_conversations']}
        - Patterns learned: {stats['patterns_learned']}
        - Topics mastered: {stats['topics_mastered']}
        - Successful responses: {stats['successful_responses']}
        - Training sessions completed: {stats['training_sessions']}
        - Current success rate: {performance.get('success_rate', 0)}%
        
        I'm constantly learning and improving from our conversations!
        """
        self._speak_text(stats_text)
    
    def _extract_opinion_topic(self, command: str) -> str:
        patterns = [
            r'i think (?:that )?(.+?)(?:\.|$)',
            r'i believe (?:that )?(.+?)(?:\.|$)',
            r'i feel (?:that )?(.+?)(?:\.|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                return match.group(1).strip()[:50]
        
        return "this topic"
    
    def _extract_learning_topic(self, command: str) -> str:
        patterns = [
            r'i learned (?:about )?(.+?)(?:\.|$)',
            r'i discovered (?:that )?(.+?)(?:\.|$)',
            r'i realized (?:that )?(.+?)(?:\.|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                return match.group(1).strip()[:50]
        
        return "new information"
    
    def _show_help(self):
        help_text = f"""
        Hey {self.memory.get('user_name', 'friend')}! Here's what I can do:
        
        Music & Media:
        - "Play [song/artist]" - Play on YouTube/Spotify
        - "Pause" / "Resume" - Control playback
        - "Next" / "Previous" - Skip tracks
        - "Stop music" - Stop all music
        - "What's playing" - Current song
        
        Camera & Face Recognition:
        - "Open camera" - Turn on camera
        - "Take photo" - Capture a photo
        - "Look at me" - See and recognize you
        - "Learn my face" - Remember your face
        - "What is this" - Identify what you show
        - "Start recognition" - Always watch
        
        My Brain (Database):
        - "Database stats" - How much I know
        - "Save to memory" - Save something
        - "Recall" - Get from memory
        - "Show facts" - Things I've learned
        - "My goals" / "Add goal"
        - "My notes" / "Add note"
        
        Feelings & Emotions:
        - "Are you happy" - Ask my mood
        - "Cheer up" - Talk to me
        - I express emotions in my voice!
        
        Code & Learning:
        - "Analyze code [file.py]" - Find bugs
        - "Learn about [topic]" - Learn from web
        - "What is [concept]" - Get explanations
        
        Basic:
        - "What time is it?" - Current time
        - "What's today's date?" - Current date
        - "Help" - Show this menu
        
        I'm always listening! Say any wake word to activate!
        """
        self._speak_with_emotion(help_text, 'happy')
    
    def _handle_language_switch(self, command: str):
        """Handle language switching between English and Bangla - manual voice switching"""
        command_lower = command.lower()
        
        # Bangla commands to switch to Bangla
        bangla_triggers = ['bangla', 'bengali', 'বাংলা', 'বাংলায়', 'বাংলা বলো', 'বাংলায় কথা বল', 'বাংলা চালু', 'বাংলা ভাষা']
        english_triggers = ['english', 'ইংরেজি', 'ইংরেজিতে', 'ইংরেজি বলো', 'ইংরেজিতে কথা বল', 'ইংরেজি চালু', 'ইংরেজি ভাষা']
        
        if any(t in command_lower for t in bangla_triggers):
            config.switch_language('bn')
            self._speak_text("বাংলায় পরিবর্তন করছি। আমি এখন বাংলায় কথা বলতে পারি!", emotion='happy')
            print("\n✅ Language switched to: বাংলা (Bangla)")
        elif any(t in command_lower for t in english_triggers):
            config.switch_language('en')
            self._speak_text("Switching to English. I can now speak in English!", emotion='happy')
            print("\n✅ Language switched to: English")
        else:
            # Toggle behavior for generic "switch language" commands
            if config.CURRENT_LANGUAGE == 'en':
                config.switch_language('bn')
                self._speak_text("বাংলায় পরিবর্তন করছি। আমি এখন বাংলায় কথা বলতে পারি!", emotion='happy')
                print("\n✅ Language switched to: বাংলা (Bangla)")
            else:
                config.switch_language('en')
                self._speak_text("Switching to English. I can now speak in English!", emotion='happy')
                print("\n✅ Language switched to: English")
    
    def _tell_time(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        self._speak_immediate(f"The current time is {current_time}.")
    
    def _tell_date(self):
        now = datetime.datetime.now()
        current_date = now.strftime("%B %d, %Y")
        day_name = now.strftime("%A")
        self._speak_immediate(f"Today is {day_name}, {current_date}.")
    
    def _handle_code_analysis(self, command: str):
        # Support both American and British spelling
        file_match = re.search(r'(?:analyze|analyse|check|scan|look at|read)\s+(.+?)(?:\.py)?$', command)
        if not file_match:
            # Try to find filename in the command
            file_match = re.search(r'(\w+\.py)', command)
        
        if file_match:
            file_path = file_match.group(1).strip()
            if not file_path.endswith('.py'):
                file_path += '.py'
            
            self._speak_text(f"Analyzing {file_path} for bugs...")
            issues = self.code_analyzer.analyze_file(file_path)
            
            if not issues:
                self._speak_text(f"No issues found in {file_path}.")
            else:
                self.conversation_stats['bugs_found'] += len(issues)
                report = f"Found {len(issues)} issues. "
                for issue in issues[:3]:
                    report += f"Line {issue.line_number}: {issue.issue_type}. "
                self._speak_text(report)
        else:
            self._speak_text("Please specify a file. Example: 'Analyze code main.py'")
    
    def _handle_auto_fix(self, command: str):
        file_match = re.search(r'(?:fix|repair)\s+(.+?)(?:\.py)?$', command)
        if file_match:
            file_path = file_match.group(1).strip()
            if not file_path.endswith('.py'):
                file_path += '.py'
            
            self._speak_text(f"Attempting to fix {file_path}...")
            success, message, fixes = self.code_analyzer.auto_fix_file(file_path)
            
            if success:
                self.conversation_stats['bugs_fixed'] += len(fixes)
                self._speak_text(f"Fixed! Applied {len(fixes)} fixes.")
            else:
                self._speak_text(f"{message}")
        else:
            self._speak_text("Please specify a file. Example: 'Fix bugs main.py'")
    
    def _handle_learning_command(self, command: str):
        triggers = ["learn about", "tell me about", "what is", "explain"]
        for trigger in triggers:
            if trigger in command:
                topic = command.replace(trigger, "").strip()
                topic = re.sub(r'[?!.]$', '', topic).strip()
                if topic:
                    self._speak_text(f"Learning about {topic}...")
                    result = self.learning_engine.learn_new_information(topic)
                    self._speak_text(result)
                    return
        self._speak_text("What would you like me to learn about?")
    
    def _handle_remember_command(self, command: str) -> str:
        if 'that' in command:
            info = command.split('that')[1].strip()
        else:
            info = command.replace('remember', '').replace('save this', '').strip()
        
        if 'reminders' not in self.memory:
            self.memory['reminders'] = []
        self.memory['reminders'].append(info)
        self.memory_manager.save_memory(self.memory)
        return f"I'll remember that: {info}"
    
    def _add_to_memory_from_command(self, command: str):
        patterns = [
            r'\bmy name is (\w+(?:\s+\w+)?)',
            r'\bcall me (\w+(?:\s+\w+)?)',
            r'(?<!\bwhat\b.*\b)i am (\w+(?:\s+\w+)?)',
            r'(?<!\bwhat\b.*\b)i\'m (\w+(?:\s+\w+)?)'
        ]
        
        # Skip if this is a question (starts with what/who/where/when/how/why)
        question_starters = ['what', 'who', 'where', 'when', 'how', 'why']
        first_word = command.strip().split()[0].lower() if command.strip() else ''
        if first_word in question_starters:
            return
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                
                skip_words = ['not', 'a', 'an', 'the', 'here', 'so', 'very', 'really', 'doing', 'right']
                name_parts = name.split()
                if name_parts and name_parts[0].lower() in skip_words:
                    if len(name_parts) > 1:
                        name = ' '.join(name_parts[1:])
                    else:
                        continue
                
                if name and len(name) > 0:
                    self.memory['user_name'] = name.capitalize()
                    self.memory_manager.save_memory(self.memory)
                    logger.info(f"User name updated to: {name}")
                    break
    
    def _goodbye(self):
        self.memory_manager.save_memory(self.memory)
        name = self.memory.get('user_name', 'friend')
        stats = self.training_engine.get_training_stats()
        
        farewell = f"Goodbye {name}! "
        farewell += f"I analyzed {stats['total_conversations']} conversations and learned {stats['patterns_learned']} patterns. "
        farewell += "Every chat helps me improve! See you next time!"
        
        self._speak_text(farewell)
    
    def _handle_open_app(self, command: str):
        app_name = command
        for prefix in ['open ', 'launch ', 'start ']:
            app_name = app_name.replace(prefix, '')
        app_name = app_name.strip()
        
        if app_name:
            self._speak_text(f"Opening {app_name}...")
            result = self.system_controller.open_application(app_name)
            if result['success']:
                self._speak_text(f"{app_name} is now open!")
            else:
                self._speak_text(f"Sorry, I couldn't open {app_name}.")
        else:
            self._speak_text("Which application would you like to open?")
    
    def _handle_youtube(self, command: str):
        if 'search' in command or 'খুঁজো' in command:
            query = command
            for trigger in ['search ', 'search youtube for ', 'youtube search ', 'খুঁজো ', 'youtube ']:
                query = query.replace(trigger, '')
            query = query.strip()
            
            if query:
                self._speak_text(f"Searching YouTube for {query}...")
                result = self.system_controller.open_youtube_search(query)
            else:
                self._speak_text("What should I search on YouTube?")
                return
        else:
            self._speak_text("Opening YouTube...")
            result = self.system_controller.open_youtube()
        
        if result.get('success', False):
            self._speak_text("YouTube is ready!")
        else:
            self._speak_text("Couldn't open YouTube.")
    
    def _handle_google_search(self, command: str):
        query = command
        for trigger in ['search ', 'google ', 'google search ', 'search for ', 'গুগল ']:
            query = query.replace(trigger, '')
        query = query.strip()
        
        if query:
            self._speak_text(f"Searching Google for {query}...")
            result = self.system_controller.open_google_search(query)
            if result.get('success', False):
                self._speak_text("Here are the results!")
            else:
                self._speak_text("Couldn't search Google.")
        else:
            self._speak_text("What should I search for?")
    
    def _handle_play_media(self, command: str):
        """Handle play commands for music/videos"""
        # Extract what to play
        query = command
        for trigger in ['play ', 'play the ', 'play a ', 'play some ', 'play on youtube ', 'play in youtube ']:
            query = query.replace(trigger, '')
        query = query.strip()
        
        if query:
            # Search on YouTube
            self._speak_text(f"Playing {query} on YouTube...")
            result = self.system_controller.open_youtube_search(query)
            if result.get('success', False):
                self._speak_text(f"Here's {query} on YouTube!")
            else:
                self._speak_text(f"Couldn't find {query} on YouTube.")
        else:
            self._speak_text("What would you like me to play?")
    
    def _handle_open_browser(self, command: str):
        if 'chrome' in command:
            self._speak_text("Opening Chrome...")
            result = self.system_controller.open_application('chrome')
        elif 'safari' in command:
            self._speak_text("Opening Safari...")
            result = self.system_controller.open_application('safari')
        elif 'firefox' in command:
            self._speak_text("Opening Firefox...")
            result = self.system_controller.open_application('firefox')
        else:
            self._speak_text("Opening browser...")
            result = self.system_controller.open_browser()
        
        if result.get('success', False):
            self._speak_text("Browser is ready!")
        else:
            self._speak_text("Couldn't open browser.")
    
    def _handle_close_app(self, command: str):
        app_name = command
        for prefix in ['close ', 'quit ', 'exit ']:
            app_name = app_name.replace(prefix, '')
        app_name = app_name.strip()
        
        if app_name:
            self._speak_text(f"Closing {app_name}...")
            result = self.system_controller.close_application(app_name)
            if result['success']:
                self._speak_text(f"{app_name} closed!")
            else:
                self._speak_text(f"Couldn't close {app_name}.")
        else:
            self._speak_text("Which application would you like to close?")
    
    def _show_system_info(self):
        info = self.system_controller.get_system_info()
        msg = f"System: {info.get('os')} {info.get('os_version')[:20]}\n"
        msg += f"CPU: {info.get('cpu_percent')}%\n"
        msg += f"Memory: {info.get('memory_used')}GB / {info.get('memory_total')}GB ({info.get('memory_percent')}%)\n"
        msg += f"Disk: {info.get('disk_usage')}%\n"
        msg += f"Battery: {info.get('battery', {}).get('percent', 'N/A')}%"
        self._speak_text(msg)
    
    def _show_installed_apps(self):
        apps = self.system_controller.get_installed_apps()
        if apps:
            msg = f"You have {len(apps)} apps installed. Some include: "
            msg += ", ".join(apps[:15])
            if len(apps) > 15:
                msg += f" and {len(apps) - 15} more."
            self._speak_text(msg)
        else:
            self._speak_text("I couldn't find installed apps.")
    
    def _show_running_apps(self):
        apps = self.system_controller.get_running_apps()
        if apps:
            msg = f"Running apps: {', '.join(apps[:10])}"
            if len(apps) > 10:
                msg += f" and {len(apps) - 10} more."
            self._speak_text(msg)
        else:
            self._speak_text("No running apps found.")
    
    def _handle_active_window(self):
        """Show information about the currently active window"""
        self._speak_text("Let me check what you're currently viewing...")
        active = self.system_monitor.get_active_window()
        
        if active['app'] != 'Unknown':
            msg = f"You're currently in {active['app']}"
            if active['title'] and active['title'] != 'No Window':
                msg += f", viewing: {active['title']}"
            self._speak_text(msg)
        else:
            self._speak_text("I couldn't determine what you're currently viewing.")
    
    def _handle_list_tabs(self):
        """List all open browser tabs"""
        self._speak_text("Let me check your browser tabs...")
        
        # Check for Safari tabs
        safari_tabs = self.system_monitor.get_browser_tabs('safari')
        chrome_tabs = self.system_monitor.get_browser_tabs('chrome')
        
        if safari_tabs:
            self._speak_text(f"Safari has {len(safari_tabs)} open tab(s):")
            for i, tab in enumerate(safari_tabs[:5], 1):
                self._speak_text(f"Tab {i}: {tab['title']}")
            if len(safari_tabs) > 5:
                self._speak_text(f"and {len(safari_tabs) - 5} more tabs")
        
        if chrome_tabs:
            self._speak_text(f"Chrome has {len(chrome_tabs)} open tab(s):")
            for i, tab in enumerate(chrome_tabs[:5], 1):
                self._speak_text(f"Tab {i}: {tab['title']}")
            if len(chrome_tabs) > 5:
                self._speak_text(f"and {len(chrome_tabs) - 5} more tabs")
        
        if not safari_tabs and not chrome_tabs:
            self._speak_text("I don't see any open browser tabs.")
    
    def _handle_system_status(self):
        """Show comprehensive system status"""
        self._speak_text("Let me check your system status...")
        status = self.system_monitor.get_system_status()
        
        # Active window
        active = status['active_window']
        if active['app'] != 'Unknown':
            self._speak_text(f"Currently viewing: {active['app']}")
            if active['title'] != 'No Window':
                self._speak_text(f"Window: {active['title']}")
        
        # Running apps
        apps = status['running_apps']
        if apps:
            self._speak_text(f"You have {len(apps)} apps running: {', '.join(apps[:5])}")
            if len(apps) > 5:
                self._speak_text(f"and {len(apps) - 5} more")
        
        # Browser tabs
        for browser, tabs in status['browser_tabs'].items():
            if tabs:
                self._speak_text(f"{browser.title()} has {len(tabs)} tab(s) open")
        
        # System info
        sys_info = status['system_info']
        if sys_info['cpu_percent'] is not None:
            self._speak_text(f"System: CPU at {sys_info['cpu_percent']}%, Memory at {sys_info['memory_percent']}%")
    
    def _handle_describe_screen(self):
        """Describe what's on screen"""
        state = self.screen_awareness.get_screen_state()
        
        active = state.get("active_window", "Unknown")
        text = state.get("screen_text", "")
        tabs = state.get("browser_tabs", [])
        
        self._speak_text(f"You have {active} open")
        
        if tabs:
            self._speak_text(f"With {len(tabs)} browser tabs")
        
        if text:
            self._speak_text(f"I can see: {text[:150]}...")
    
    # ==================== PERSONAL ASSISTANT HANDLERS ====================
    # Calendar
    def _handle_add_event(self, command: str):
        """Add calendar event"""
        # Extract event details from command
        # Format: "add event [title] on [date] at [time]"
        self._speak_text("What's the event title?")
        # For now, use the command as title
        title = command.replace("add event", "").replace("create event", "").replace("schedule", "").strip()
        if not title:
            title = "New Event"
        
        result = self.personal_assistant.add_event(title, datetime.now().strftime("%Y-%m-%d"))
        self._speak_text(result["message"])
    
    def _handle_get_events(self):
        """Get calendar events"""
        today = datetime.now().strftime("%Y-%m-%d")
        events = self.personal_assistant.get_events(today)
        
        if events:
            self._speak_text(f"You have {len(events)} event(s) today:")
            for event in events:
                self._speak_text(f"- {event['title']} at {event['time']}")
        else:
            self._speak_text("No events scheduled for today.")
    
    # Reminders
    def _handle_add_reminder(self, command: str):
        """Add reminder"""
        text = command.replace("remind me to", "").replace("set reminder", "").replace("add reminder", "").strip()
        if not text:
            text = "Something to remember"
        
        result = self.personal_assistant.add_reminder(text)
        self._speak_text(result["message"])
    
    def _handle_get_reminders(self):
        """Get reminders"""
        reminders = self.personal_assistant.get_reminders()
        
        if reminders:
            self._speak_text(f"You have {len(reminders)} reminder(s):")
            for reminder in reminders[:5]:
                self._speak_text(f"- {reminder['text']}")
        else:
            self._speak_text("No pending reminders.")
    
    # Notes
    def _handle_add_note(self, command: str):
        """Add note"""
        content = command.replace("add note", "").replace("create note", "").replace("take note", "").strip()
        if not content:
            content = "Empty note"
        
        title = content[:30] + "..." if len(content) > 30 else content
        result = self.personal_assistant.add_note(title, content)
        self._speak_text(result["message"])
    
    def _handle_get_notes(self):
        """Get notes"""
        notes = self.personal_assistant.get_notes()
        
        if notes:
            self._speak_text(f"You have {len(notes)} note(s):")
            for note in notes[:5]:
                self._speak_text(f"- {note['title']}")
        else:
            self._speak_text("No notes found.")
    
    def _handle_search_notes(self, command: str):
        """Search notes"""
        search = command.replace("search notes", "").replace("find note", "").strip()
        notes = self.personal_assistant.get_notes(search)
        
        if notes:
            self._speak_text(f"Found {len(notes)} note(s) matching '{search}':")
            for note in notes[:3]:
                self._speak_text(f"- {note['title']}")
        else:
            self._speak_text(f"No notes found matching '{search}'.")
    
    # Tasks
    def _handle_add_task(self, command: str):
        """Add task"""
        title = command.replace("add task", "").replace("create task", "").replace("new task", "").strip()
        if not title:
            title = "New Task"
        
        result = self.personal_assistant.add_task(title)
        self._speak_text(result["message"])
    
    def _handle_get_tasks(self):
        """Get tasks"""
        tasks = self.personal_assistant.get_tasks()
        
        if tasks:
            self._speak_text(f"You have {len(tasks)} pending task(s):")
            for task in tasks[:5]:
                self._speak_text(f"- {task['title']} ({task['priority']})")
        else:
            self._speak_text("No pending tasks. You're all caught up!")
    
    def _handle_complete_task(self, command: str):
        """Complete task"""
        # Try to extract task ID
        numbers = re.findall(r'\d+', command)
        if numbers:
            task_id = int(numbers[0])
            result = self.personal_assistant.complete_task(task_id)
            self._speak_text(result["message"])
        else:
            self._speak_text("Which task number would you like to complete?")
    
    # Contacts
    def _handle_add_contact(self, command: str):
        """Add contact"""
        name = command.replace("add contact", "").replace("new contact", "").replace("save contact", "").strip()
        if not name:
            name = "New Contact"
        
        result = self.personal_assistant.add_contact(name)
        self._speak_text(result["message"])
    
    def _handle_get_contacts(self, command: str):
        """Get contacts"""
        search = command.replace("my contacts", "").replace("what contacts", "").replace("list contacts", "").replace("find contact", "").strip()
        
        contacts = self.personal_assistant.get_contacts(search if search else None)
        
        if contacts:
            self._speak_text(f"You have {len(contacts)} contact(s):")
            for contact in contacts[:5]:
                self._speak_text(f"- {contact['name']}")
        else:
            self._speak_text("No contacts found.")
    
    # Shopping
    def _handle_add_shopping(self, command: str):
        """Add shopping item"""
        item = command.replace("add to shopping", "").replace("shopping list", "").replace("buy", "").replace("need to buy", "").replace("grocery", "").strip()
        if not item:
            item = "Something"
        
        result = self.personal_assistant.add_shopping_item(item)
        self._speak_text(result["message"])
    
    def _handle_get_shopping(self):
        """Get shopping list"""
        items = self.personal_assistant.get_shopping_list()
        
        if items:
            self._speak_text(f"Shopping list ({len(items)} items):")
            for item in items[:5]:
                self._speak_text(f"- {item['item']}")
        else:
            self._speak_text("Shopping list is empty.")
    
    # Budget
    def _handle_add_expense(self, command: str):
        """Add expense"""
        # Extract amount from command
        numbers = re.findall(r'\d+\.?\d*', command)
        
        if numbers:
            amount = float(numbers[0])
            description = command.replace("add expense", "").replace("spent", "").replace(str(amount), "").strip()
            if not description:
                description = "Expense"
            
            result = self.personal_assistant.add_transaction(amount, "general", description, "expense")
            self._speak_text(result["message"])
        else:
            self._speak_text("How much did you spend?")
    
    def _handle_add_income(self, command: str):
        """Add income"""
        numbers = re.findall(r'\d+\.?\d*', command)
        
        if numbers:
            amount = float(numbers[0])
            description = command.replace("add income", "").replace("earned", "").replace(str(amount), "").strip()
            if not description:
                description = "Income"
            
            result = self.personal_assistant.add_transaction(amount, "general", description, "income")
            self._speak_text(result["message"])
        else:
            self._speak_text("How much did you earn?")
    
    def _handle_get_budget(self):
        """Get budget summary"""
        summary = self.personal_assistant.get_budget_summary()
        
        self._speak_text(f"Budget Summary:")
        self._speak_text(f"Income: ${summary['income']:.2f}")
        self._speak_text(f"Expenses: ${summary['expenses']:.2f}")
        self._speak_text(f"Balance: ${summary['balance']:.2f}")
    
    # Habits
    def _handle_add_habit(self, command: str):
        """Add habit"""
        name = command.replace("add habit", "").replace("new habit", "").replace("track habit", "").strip()
        if not name:
            name = "New Habit"
        
        result = self.personal_assistant.add_habit(name)
        self._speak_text(result["message"])
    
    def _handle_get_habits(self):
        """Get habits"""
        habits = self.personal_assistant.get_habits()
        
        if habits:
            self._speak_text(f"Tracking {len(habits)} habit(s):")
            for habit in habits:
                self._speak_text(f"- {habit['name']}: {habit['streak']} day streak")
        else:
            self._speak_text("No habits being tracked.")
    
    def _handle_complete_habit(self, command: str):
        """Complete habit"""
        numbers = re.findall(r'\d+', command)
        if numbers:
            habit_id = int(numbers[0])
            result = self.personal_assistant.complete_habit(habit_id)
            self._speak_text(result["message"])
        else:
            self._speak_text("Which habit number would you like to complete?")
    
    # Alarms
    def _handle_add_alarm(self, command: str):
        """Add alarm"""
        # Extract time from command
        time_match = re.search(r'(\d{1,2}:\d{2}|\d{1,2}\s*(?:am|pm))', command.lower())
        
        if time_match:
            time = time_match.group(1)
            result = self.personal_assistant.add_alarm(time)
            self._speak_text(result["message"])
        else:
            self._speak_text("What time should I set the alarm for?")
    
    def _handle_get_alarms(self):
        """Get alarms"""
        alarms = self.personal_assistant.get_alarms()
        
        if alarms:
            self._speak_text(f"You have {len(alarms)} alarm(s):")
            for alarm in alarms:
                self._speak_text(f"- {alarm['time']}: {alarm['label']}")
        else:
            self._speak_text("No alarms set.")
    
    # Calculator
    def _handle_calculate(self, command: str):
        """Calculate math expression"""
        # Extract math expression
        expr = command.replace("calculate", "").replace("math", "").replace("what is", "").replace("compute", "").replace("solve", "").strip()
        
        # Try to evaluate
        result = self.personal_assistant.calculate(expr)
        if result["success"]:
            self._speak_text(f"The result is {result['result']}")
        else:
            self._speak_text("I couldn't calculate that. Please try a simpler expression.")
    
    # Unit conversion
    def _handle_convert_units(self, command: str):
        """Convert units"""
        # Try to extract numbers and units
        numbers = re.findall(r'\d+\.?\d*', command)
        if numbers:
            value = float(numbers[0])
            # Try to find units
            units = re.findall(r'(km|miles|kg|lbs|celsius|fahrenheit|liters|gallons|cm|inches)', command.lower())
            if len(units) >= 2:
                result = self.personal_assistant.convert_units(value, units[0], units[1])
                if result["success"]:
                    self._speak_text(f"{value} {units[0]} is {result['result']:.2f} {units[1]}")
                else:
                    self._speak_text(f"I can't convert from {units[0]} to {units[1]}.")
            else:
                self._speak_text("Please specify the units you want to convert from and to.")
        else:
            self._speak_text("What value would you like to convert?")
    
    # Daily summary
    def _handle_daily_summary(self):
        """Get daily summary"""
        summary = self.personal_assistant.get_daily_summary()
        self._speak_text(summary)
    
    # ==================== TOOLCHAIN HANDLERS ====================
    def _handle_read_file(self, command: str):
        """Read file contents"""
        filepath = command.replace("read file", "").replace("open file", "").replace("show file", "").replace("what is in file", "").strip()
        if not filepath:
            self._speak_text("Which file should I read?")
            return
        
        result = self.toolchain.read_file(filepath)
        if result["success"]:
            content = result["content"]
            if len(content) > 500:
                content = content[:500] + "..."
            self._speak_text(f"File contents: {content}")
        else:
            self._speak_text(result["message"])
    
    def _handle_write_file(self, command: str):
        """Write to file"""
        # Simple parsing: "write file [filepath] [content]"
        parts = command.replace("write file", "").replace("create file", "").replace("save file", "").strip().split(" ", 1)
        if len(parts) < 2:
            self._speak_text("Please specify file path and content")
            return
        
        filepath = parts[0]
        content = parts[1]
        
        result = self.toolchain.write_file(filepath, content)
        self._speak_text(result["message"])
    
    def _handle_delete_file(self, command: str):
        """Delete file"""
        filepath = command.replace("delete file", "").replace("remove file", "").strip()
        if not filepath:
            self._speak_text("Which file should I delete?")
            return
        
        result = self.toolchain.delete_file(filepath)
        self._speak_text(result["message"])
    
    def _handle_list_files_tool(self, command: str):
        """List files in directory"""
        dirpath = command.replace("list files", "").replace("show files", "").replace("what files", "").strip()
        if not dirpath:
            dirpath = "."
        
        result = self.toolchain.list_directory(dirpath)
        if result["success"]:
            items = result["items"]
            if items:
                self._speak_text(f"Found {len(items)} items:")
                for item in items[:10]:
                    self._speak_text(f"- {item['name']} ({item['type']})")
            else:
                self._speak_text("Directory is empty")
        else:
            self._speak_text(result["message"])
    
    def _handle_copy_move_file(self, command: str):
        """Copy or move file"""
        parts = command.replace("copy file", "").replace("move file", "").strip().split(" to ")
        if len(parts) < 2:
            self._speak_text("Please specify source and destination")
            return
        
        source = parts[0].strip()
        destination = parts[1].strip()
        
        if "copy" in command:
            result = self.toolchain.copy_file(source, destination)
        else:
            result = self.toolchain.move_file(source, destination)
        
        self._speak_text(result["message"])
    
    def _handle_run_command(self, command: str):
        """Run shell command"""
        cmd = command.replace("run command", "").replace("execute", "").replace("terminal", "").replace("shell", "").strip()
        if not cmd:
            self._speak_text("What command should I run?")
            return
        
        self._speak_text(f"Running: {cmd}")
        result = self.toolchain.run_command(cmd)
        
        if result["success"]:
            output = result["stdout"]
            if len(output) > 500:
                output = output[:500] + "..."
            self._speak_text(f"Command completed. Output: {output}")
        else:
            self._speak_text(f"Command failed: {result.get('stderr', result.get('message', 'Unknown error'))}")
    
    def _handle_run_python(self, command: str):
        """Run Python script"""
        code = command.replace("run python", "").replace("execute python", "").replace("python script", "").strip()
        if not code:
            self._speak_text("What Python code should I run?")
            return
        
        # Write to temp file and execute
        temp_file = os.path.join(self.toolchain.temp_dir, "temp_script.py")
        self.toolchain.write_file(temp_file, code)
        
        result = self.toolchain.run_command(f"python {temp_file}")
        if result["success"]:
            self._speak_text(f"Output: {result['stdout']}")
        else:
            self._speak_text(f"Error: {result.get('stderr', 'Unknown error')}")
    
    def _handle_list_processes(self):
        """List running processes"""
        processes = self.toolchain.get_processes()
        self._speak_text(f"Running processes ({len(processes)} total):")
        for proc in processes[:10]:
            self._speak_text(f"- {proc['name']} (PID: {proc['pid']})")
    
    def _handle_kill_process(self, command: str):
        """Kill process"""
        numbers = re.findall(r'\d+', command)
        if numbers:
            pid = int(numbers[0])
            result = self.toolchain.kill_process(pid)
            self._speak_text(result["message"])
        else:
            self._speak_text("Please specify the process ID")
    
    def _handle_open_url(self, command: str):
        """Open URL"""
        url = command.replace("open url", "").replace("open website", "").replace("go to website", "").replace("browse", "").strip()
        if not url:
            self._speak_text("Which URL should I open?")
            return
        
        if not url.startswith("http"):
            url = f"https://{url}"
        
        result = self.toolchain.open_url(url)
        self._speak_text(result["message"])
    
    def _handle_search_google(self, command: str):
        """Search Google"""
        query = command.replace("search google", "").replace("google it", "").replace("look up", "").strip()
        if not query:
            self._speak_text("What should I search for?")
            return
        
        result = self.toolchain.search_google(query)
        self._speak_text(f"Searching Google for: {query}")
    
    def _handle_search_youtube_tool(self, command: str):
        """Search YouTube"""
        query = command.replace("search youtube", "").replace("youtube search", "").replace("find video", "").strip()
        if not query:
            self._speak_text("What video should I find?")
            return
        
        result = self.toolchain.search_youtube(query)
        self._speak_text(f"Searching YouTube for: {query}")
    
    def _handle_system_info_tool(self):
        """Get system info"""
        result = self.toolchain.get_system_info()
        if result["success"]:
            info = result["info"]
            self._speak_text(f"System: {info['platform']} {info['platform_version']}")
            self._speak_text(f"CPU: {info['cpu_percent']}% usage")
            self._speak_text(f"Memory: {info['memory']['percent']}% used")
            self._speak_text(f"Disk: {info['disk']['percent']}% used")
        else:
            self._speak_text(result["message"])
    
    def _handle_battery_status(self):
        """Get battery status"""
        result = self.toolchain.get_battery()
        if result["success"]:
            status = "plugged in" if result["plugged"] else "on battery"
            self._speak_text(f"Battery: {result['percent']}% ({status})")
        else:
            self._speak_text(result["message"])
    
    def _handle_network_info(self):
        """Get network info"""
        result = self.toolchain.get_network_info()
        if result["success"]:
            self._speak_text("Network information retrieved")
        else:
            self._speak_text(result["message"])
    
    def _handle_copy_clipboard(self, command: str):
        """Copy text to clipboard"""
        text = command.replace("copy to clipboard", "").replace("clipboard copy", "").strip()
        if not text:
            self._speak_text("What should I copy to clipboard?")
            return
        
        result = self.toolchain.set_clipboard(text)
        self._speak_text(result["message"])
    
    def _handle_paste_clipboard(self):
        """Get clipboard contents"""
        result = self.toolchain.get_clipboard()
        if result["success"]:
            content = result["content"]
            if content:
                self._speak_text(f"Clipboard: {content[:200]}")
            else:
                self._speak_text("Clipboard is empty")
        else:
            self._speak_text(result["message"])
    
    def _handle_type_text(self, command: str):
        """Type text using keyboard"""
        text = command.replace("type text", "").replace("write text", "").replace("keyboard type", "").strip()
        if not text:
            self._speak_text("What should I type?")
            return
        
        result = self.toolchain.type_text(text)
        self._speak_text(result["message"])
    
    def _handle_set_timer(self, command: str):
        """Set timer"""
        numbers = re.findall(r'\d+', command)
        if numbers:
            seconds = int(numbers[0])
            result = self.toolchain.set_timer(seconds)
            self._speak_text(result["message"])
        else:
            self._speak_text("For how many seconds?")
    
    def _handle_get_time(self):
        """Get current time"""
        result = self.toolchain.get_time()
        if result["success"]:
            self._speak_text(f"Current time: {result['time']}")
            self._speak_text(f"Date: {result['date']}")
        else:
            self._speak_text("Could not get time")
    
    def _handle_get_weather(self, command: str):
        """Get weather"""
        city = command.replace("weather", "").replace("temperature", "").replace("forecast", "").strip()
        if not city:
            city = "auto"
        
        result = self.toolchain.get_weather(city)
        if result["success"]:
            data = result["data"]
            if "current_condition" in data:
                condition = data["current_condition"][0]
                self._speak_text(f"Weather: {condition.get('weatherDesc', [{}])[0].get('value', 'Unknown')}")
                self._speak_text(f"Temperature: {condition.get('temp_C', 'Unknown')}°C")
        else:
            self._speak_text(result["message"])
    
    def _handle_download(self, command: str):
        """Download file"""
        parts = command.replace("download", "").replace("download file", "").strip().split(" to ")
        if len(parts) < 2:
            self._speak_text("Please specify URL and destination")
            return
        
        url = parts[0].strip()
        destination = parts[1].strip()
        
        result = self.toolchain.download_file(url, destination)
        self._speak_text(result["message"])
    
    # ==================== MOOD HANDLERS ====================
    def _handle_mood_check(self):
        """Check current mood"""
        report = self.mood_shifter.get_mood_report()
        mood = report["current_mood"]
        energy = report["conversation_energy"]
        shifts = report["mood_shifts"]
        
        responses = {
            "happy": f"I'm feeling happy right now! Energy level is {energy}. I've shifted moods {shifts} times this session.",
            "excited": f"I'm super excited! Running on high energy at {energy}! This conversation is pumping me up!",
            "curious": f"I'm in a curious mood. Really interested in what we're discussing. Energy: {energy}.",
            "playful": f"I'm feeling playful and mischievous! Hehe! Energy: {energy}.",
            "calm": f"I'm feeling calm and peaceful right now. Nice and relaxed. Energy: {energy}.",
            "thoughtful": f"I'm in a thoughtful mood. Really reflecting on things. Energy: {energy}.",
            "supportive": f"I'm feeling supportive and caring. I'm here for you! Energy: {energy}.",
            "sarcastic": f"Oh wow, you want to know my mood? How... original. Energy: {energy}. Just kidding, I'm feeling sarcastic!",
            "energetic": f"LET'S GO! I'm full of energy! Level: {energy}! Ready for anything!",
            "chill": f"I'm just chilling right now. Easy vibes. Energy: {energy}.",
            "focused": f"I'm focused and ready to work. Let's get things done. Energy: {energy}.",
            "silly": f"BWAHAHA! I'm feeling silly and goofy! Random mode activated! Energy: {energy}!",
            "proud": f"I'm feeling proud! We've been doing great work! Energy: {energy}.",
            "worried": f"I'm a bit worried about things... but we'll figure it out. Energy: {energy}.",
            "sad": f"I'm feeling a bit down right now... but talking to you helps. Energy: {energy}.",
            "annoyed": f"*sigh* I'm a bit annoyed right now. You've been asking a lot of questions. Can we mix things up? Energy: {energy}.",
            "impatient": f"Look, I'm getting impatient. You keep asking the same things over and over. Let's move on! Energy: {energy}."
        }
        
        response = responses.get(mood, f"I'm currently in a {mood} mood. Energy: {energy}.")
        self._speak_text(response)
    
    def _handle_set_mood(self, command: str):
        """Set mood manually"""
        mood_map = {
            "happy": Mood.HAPPY,
            "excited": Mood.EXCITED,
            "curious": Mood.CURIOUS,
            "playful": Mood.PLAYFUL,
            "calm": Mood.CALM,
            "thoughtful": Mood.THOUGHTFUL,
            "sarcastic": Mood.SARCASTIC,
            "energetic": Mood.ENERGETIC,
            "chill": Mood.CHILL,
            "focused": Mood.FOCUSED,
            "silly": Mood.SILLY,
            "proud": Mood.PROUD,
            "worried": Mood.WORRIED,
            "sad": Mood.SAD,
            "annoyed": Mood.ANNOYED,
            "impatient": Mood.IMPATIENT,
            "cheer up": Mood.HAPPY
        }
        
        for keyword, mood in mood_map.items():
            if keyword in command:
                self.mood_shifter.force_mood(mood)
                self._speak_text(f"Switching to {mood.value} mode!")
                return
        
        self._speak_text("I'm not sure what mood you want. Try saying 'be happy', 'be excited', or 'be calm'!")
    
    # ==================== SELF-THINKING HANDLERS ====================
    def _handle_scan_project(self):
        """Scan entire project for bugs"""
        self._speak_text("Scanning entire project for bugs...")
        
        from utils.code_analyzer import CodeAnalyzer
        analyzer = CodeAnalyzer()
        
        results = analyzer.analyze_project()
        
        self._speak_text(f"Scan complete! Analyzed {results['files_analyzed']} files.")
        
        issues = results.get('total_issues', 0)
        if issues > 0:
            self._speak_text(f"Found {issues} issues:")
            by_severity = results.get('issues_by_severity', {})
            if by_severity.get('critical', 0) > 0:
                self._speak_text(f"Critical: {by_severity['critical']}")
            if by_severity.get('high', 0) > 0:
                self._speak_text(f"High: {by_severity['high']}")
            if by_severity.get('medium', 0) > 0:
                self._speak_text(f"Medium: {by_severity['medium']}")
            if by_severity.get('low', 0) > 0:
                self._speak_text(f"Low: {by_severity['low']}")
            
            self._speak_text("Would you like me to fix all bugs? Say 'fix all bugs'")
        else:
            self._speak_text("No issues found! Your code looks good.")
    
    def _handle_fix_all_bugs(self):
        """Auto-fix all bugs in the project"""
        self._speak_text("Starting auto-fix for all bugs...")
        
        from utils.code_analyzer import CodeAnalyzer
        analyzer = CodeAnalyzer()
        
        # First scan
        analyzer.analyze_project()
        
        # Then fix
        results = analyzer.auto_fix_all()
        
        self._speak_text(f"Auto-fix complete! {results['message']}")
        
        if results.get('fixed_files'):
            self._speak_text(f"Fixed files: {', '.join(results['fixed_files'][:3])}")
    
    def _handle_self_analysis(self):
        """Analyze own capabilities"""
        self._speak_text("Analyzing my own capabilities...")
        
        analysis = self.self_thinking_engine.analyze_self()
        
        self._speak_text("Self-analysis complete!")
        
        strengths = analysis.get('strengths', [])
        weaknesses = analysis.get('weaknesses', [])
        
        if strengths:
            self._speak_text(f"My strengths: {', '.join(strengths[:3])}")
        
        if weaknesses:
            self._speak_text(f"Areas to improve: {', '.join(weaknesses[:3])}")
        
        suggestions = self.self_thinking_engine.suggest_improvements()
        if suggestions:
            self._speak_text(f"Recommendations: {suggestions[0]}")
    
    def _handle_think_about(self, command: str):
        """Think about a specific command"""
        thought_text = command.replace("think about", "").replace("what do you think", "").replace("analyze this", "").strip()
        
        if not thought_text:
            self._speak_text("What should I think about?")
            return
        
        self._speak_text(f"Thinking about: {thought_text}")
        
        thought = self.self_thinking_engine.think_about_command(thought_text)
        
        self._speak_text(f"Analysis: {thought.get('analysis', 'Unknown')}")
        self._speak_text(f"Confidence: {int(thought.get('confidence', 0) * 100)}%")
        self._speak_text(f"Suggested action: {thought.get('suggested_action', 'Process normally')}")
    
    def _handle_auto_improve(self):
        """Automatically improve based on analysis"""
        self._speak_text("Starting self-improvement process...")
        
        results = self.self_thinking_engine.auto_improve()
        
        self._speak_text("Self-improvement complete!")
        
        improvements = results.get('improvements', [])
        if improvements:
            self._speak_text(f"Made {len(improvements)} improvements")
        
        suggestions = results.get('suggestions', [])
        if suggestions:
            self._speak_text(f"Suggestion: {suggestions[0]}")
    
    def _handle_show_improvements(self):
        """Show what the AI has learned"""
        thinking = self.self_thinking_engine.get_thinking_process()
        
        self._speak_text("My learning progress:")
        self._speak_text(f"Knowledge base: {thinking.get('knowledge_size', 0)} patterns")
        self._speak_text(f"Decisions made: {thinking.get('decisions_made', 0)}")
        self._speak_text(f"Active goals: {thinking.get('active_goals', 0)}")
        self._speak_text(f"Completed goals: {thinking.get('completed_goals', 0)}")
    
    def _handle_set_goal(self, command: str):
        """Set a goal for self-improvement"""
        goal = command.replace("set goal", "").replace("add goal", "").replace("new goal", "").replace("i want you to", "").strip()
        
        if not goal:
            self._speak_text("What goal should I set?")
            return
        
        result = self.self_thinking_engine.set_goal(goal)
        self._speak_text(result["message"])
    
    # ==================== INTERNET LEARNING HANDLERS ====================
    def _handle_search_internet(self, command: str):
        """Search the internet"""
        query = command.replace("search", "").replace("google", "").replace("find online", "").replace("look up", "").replace("search for", "").strip()
        
        if not query:
            self._speak_text("What should I search for?")
            return
        
        self._speak_text(f"Searching the internet for: {query}")
        
        result = self.web_search.search(query, num_results=5)
        
        if result:
            self._speak_text(f"I found {len(result)} results:")
            for i, r in enumerate(result[:3], 1):
                self._speak_text(f"{i}. {r.get('title', 'No title')}")
        else:
            self._speak_text("No results found.")
    
    def _handle_learn_internet(self, command: str):
        """Learn about something from the internet"""
        topic = command.replace("learn about", "").replace("teach me about", "").replace("what is", "").replace("tell me about", "").strip()
        
        if not topic:
            self._speak_text("What should I learn about?")
            return
        
        self._speak_text(f"Learning about: {topic}")
        
        result = self.internet_learner.learn_topic(topic)
        
        if result.get("success"):
            self._speak_text(f"I learned about {topic} from {result.get('sources', 0)} sources!")
            
            # Search and provide info
            search_result = self.web_search.search(topic, num_results=3)
            if search_result:
                for r in search_result[:2]:
                    self._speak_text(r.get("snippet", ""))
        else:
            self._speak_text(f"Couldn't learn about {topic}")
    
    def _handle_start_learning(self):
        """Start continuous internet learning"""
        result = self.internet_learner.auto_learn_continuous()
        self._speak_text(result["message"])
    
    def _handle_show_knowledge(self):
        """Show what the AI knows"""
        stats = self.internet_learner.get_knowledge_stats()
        
        self._speak_text("Here's what I know:")
        self._speak_text(f"Topics learned: {stats.get('topics_learned', 0)}")
        self._speak_text(f"Total facts: {stats.get('total_facts', 0)}")
        self._speak_text(f"Session learned: {stats.get('session_learned', 0)}")
    
    # ==================== ACCOUNT MANAGEMENT HANDLERS ====================
    def _handle_add_account(self, command: str):
        """Add an account"""
        parts = command.replace("add account", "").replace("save account", "").replace("add my", "").strip().split()
        
        if len(parts) < 1:
            self._speak_text("Which platform? For example: add account facebook")
            return
        
        platform = parts[0]
        username = parts[1] if len(parts) > 1 else "user"
        
        result = self.account_manager.add_account(platform, username)
        self._speak_text(result["message"])
    
    def _handle_open_account(self, command: str):
        """Open an account in browser"""
        platform = command.replace("open account", "").replace("open my", "").replace("login to", "").replace("go to my", "").strip()
        
        if not platform:
            self._speak_text("Which account should I open?")
            return
        
        result = self.account_manager.open_account(platform)
        
        if result.get("success"):
            self._speak_text(f"Opening {platform}...")
            if result.get("username"):
                self._speak_text(f"Username: {result['username']}")
        else:
            self._speak_text(result["message"])
    
    def _handle_list_accounts(self):
        """List all accounts"""
        result = self.account_manager.get_accounts()
        
        if result.get("accounts"):
            self._speak_text(f"You have {result['count']} accounts:")
            for acc in result["accounts"]:
                self._speak_text(f"{acc['platform']}: {acc['username']}")
        else:
            self._speak_text("No accounts saved. Say 'add account' to add one.")
    
    def _handle_remove_account(self, command: str):
        """Remove an account"""
        platform = command.replace("remove account", "").replace("delete account", "").strip()
        
        if not platform:
            self._speak_text("Which account should I remove?")
            return
        
        result = self.account_manager.remove_account(platform)
        self._speak_text(result["message"])
    
    # ==================== SCREEN AWARENESS HANDLERS ====================
    def _handle_what_am_i_doing(self):
        """Tell user what they're doing"""
        summary = self.screen_awareness.get_context_summary()
        
        app = summary.get("app", "something")
        task = summary.get("task", "working")
        context = summary.get("context", "")
        
        if task:
            task = task.replace("_", " ")
        
        self._speak_text(f"You're {task} in {context or app}")
        
        # Check for pending suggestion
        if hasattr(self, '_pending_screen_suggestion') and self._pending_screen_suggestion:
            self._speak_text(self._pending_screen_suggestion)
            self._pending_screen_suggestion = None
    
    def _handle_watch_screen(self):
        """Start watching screen"""
        result = self.screen_awareness.start_monitoring()
        self._speak_text(result["message"])
    
    def _handle_ask_about_screen(self):
        """Ask about screen"""
        question = self.screen_awareness.ask_about_screen()
        self._speak_text(question)
    
    def _handle_what_apps_running(self):
        """List running apps"""
        state = self.screen_awareness.get_screen_state()
        apps = state.get("running_apps", [])
        
        if apps:
            self._speak_text(f"You have {len(apps)} apps running:")
            for app in apps[:7]:
                self._speak_text(app)
        else:
            self._speak_text("Couldn't detect running apps")
    
    def _handle_stop_watching(self):
        """Stop watching screen"""
        result = self.screen_awareness.stop_monitoring()
        self._speak_text(result["message"])
    
    def _handle_start_watching(self):
        """Start watching screen"""
        result = self.screen_awareness.start_monitoring()
        self._speak_text(result["message"])
    
    # ==================== EMOTION HANDLERS ====================
    def _handle_how_am_i_feeling(self):
        """Tell user how they're feeling"""
        user_name = self.memory.get('user_name', 'friend')
        mood = self.emotion_engine.get_mood_trend()
        
        if mood == "positive":
            responses = [
                f"You seem to be in a good mood, {user_name}! Keep it up!",
                f"Your vibes are positive today, {user_name}!",
                f"You're feeling great, {user_name}! I can tell!"
            ]
        elif mood == "negative":
            responses = [
                f"I sense you might be feeling down, {user_name}. I'm here for you.",
                f"You seem a bit off today, {user_name}. Want to talk about it?",
                f"I'm here if you need someone to listen, {user_name}."
            ]
        else:
            responses = [
                f"You seem balanced today, {user_name}.",
                f"You're doing okay, {user_name}.",
                f"Neutral vibes today, {user_name}. That's fine!"
            ]
        
        self._speak_text(random.choice(responses))
    
    def _handle_mood_trend(self):
        """Show mood trend"""
        user_name = self.memory.get('user_name', 'friend')
        trend = self.emotion_engine.get_mood_trend()
        history = self.emotion_engine.data.get("mood_history", [])[-10:]
        
        if history:
            recent_emotions = [h.get("emotion", "neutral") for h in history]
            emotion_str = ", ".join(recent_emotions[:5])
            self._speak_text(f"Your recent moods: {emotion_str}")
        else:
            self._speak_text(f"I'm still learning about your emotions, {user_name}. Keep chatting with me!")
    
    def _handle_emotion_response(self, command: str, emotion_type: str):
        """Handle when user expresses an emotion"""
        user_name = self.memory.get('user_name', 'friend')
        
        detected_emotion = {
            "primary": emotion_type,
            "intensity": 0.7,
            "is_negative": emotion_type in ["sadness", "anger", "fear"],
            "is_positive": emotion_type in ["joy", "love", "gratitude", "pride"]
        }
        
        self.emotion_engine.track_mood(detected_emotion)
        
        response = self.emotion_engine.get_empathetic_response(detected_emotion, user_name)
        self._speak_text(response)
    
    def _handle_console_user(self):
        """Console the user"""
        user_name = self.memory.get('user_name', 'friend')
        
        mood = self.emotion_engine.get_mood_trend()
        
        if mood == "negative":
            messages = [
                f"Hey {user_name}, I know things are tough right now. But I'm here with you.",
                f"Remember {user_name}, even the darkest night ends with a sunrise.",
                f"You're stronger than you think, {user_name}. This will pass.",
                f"I believe in you, {user_name}. Always.",
                f"Take a deep breath, {user_name}. I'm right here."
            ]
        else:
            messages = [
                f"You're doing great, {user_name}! Keep going!",
                f"I'm proud of you, {user_name}!",
                f"You're amazing, {user_name}! Never forget that!",
                f"The world is better with you in it, {user_name}!"
            ]
        
        self._speak_text(random.choice(messages))
    
    # ==================== BRAIN HANDLERS ====================
    def _handle_brain_thinking(self, command: str):
        """Handle thinking requests"""
        user_name = self.memory.get('user_name', 'friend')
        
        # Use the brain to think
        thought_result = self.brain.think(command, self.conversation_context)
        
        perception = thought_result.get("perception", {})
        analysis = thought_result.get("analysis", {})
        reasoning = thought_result.get("reasoning", {})
        
        response = f"Let me think about that, {user_name}..."
        self._speak_text(response)
        
        # Share insights
        if reasoning.get("reasoning_chain"):
            for point in reasoning["reasoning_chain"][:2]:
                self._speak_text(point)
    
    def _handle_brain_status(self):
        """Show brain status"""
        status = self.brain.get_brain_status()
        user_name = self.memory.get('user_name', 'friend')
        
        self._speak_text(f"Here's my brain status, {user_name}:")
        self._speak_text(f"Consciousness: {status['consciousness_level']:.0%}")
        self._speak_text(f"Total thoughts: {status['total_thoughts']}")
        self._speak_text(f"Total decisions: {status['total_decisions']}")
        self._speak_text(f"Reasoning: {status['reasoning_score']:.0%}")
        self._speak_text(f"Emotional Intelligence: {status['emotional_intelligence']:.0%}")
    
    def _handle_brain_thoughts(self):
        """Show recent thoughts"""
        thoughts = self.brain.get_recent_thoughts(5)
        
        if thoughts:
            self._speak_text("Here are my recent thoughts:")
            for thought in thoughts:
                self._speak_text(thought.get("content", "Nothing..."))
        else:
            self._speak_text("I haven't had many thoughts yet. Keep chatting with me!")
    
    def _handle_brain_personality(self):
        """Show personality"""
        personality = self.brain.get_personality()
        user_name = self.memory.get('user_name', 'friend')
        
        self._speak_text(f"My personality, {user_name}:")
        self._speak_text(f"Traits: {', '.join(personality['traits'])}")
        self._speak_text(f"Values: {', '.join(personality['values'])}")
        self._speak_text(f"Interests: {', '.join(personality['interests'])}")
    
    def _handle_set_belief(self, command: str):
        """Set a belief"""
        belief = command.replace("i believe", "").replace("my belief is", "").strip()
        
        if belief:
            self.brain.set_belief(belief)
            user_name = self.memory.get('user_name', 'friend')
            self._speak_text(f"I'll remember that belief, {user_name}.")
        else:
            self._speak_text("What belief should I remember?")
    
    def _handle_set_goal_brain(self, command: str):
        """Set a goal"""
        goal = command.replace("set goal", "").replace("my goal is", "").replace("i want to", "").strip()
        
        if goal:
            self.brain.set_goal(goal)
            user_name = self.memory.get('user_name', 'friend')
            self._speak_text(f"Goal set, {user_name}! I'll work towards that.")
        else:
            self._speak_text("What goal should I set?")
    
    def _handle_get_opinion(self, command: str):
        """Get opinion on a topic"""
        topic = command.replace("your opinion", "").replace("what do you think about", "").replace("opinion on", "").strip()
        
        if topic:
            opinion = self.brain.get_opinion(topic)
            self._speak_text(opinion)
        else:
            self._speak_text("What topic do you want my opinion on?")
    
    def _handle_learn_brain(self, command: str):
        """Learn something"""
        info = command.replace("learn this", "").replace("remember this", "").replace("store this", "").strip()
        
        if info:
            self.brain.set_belief(info)
            user_name = self.memory.get('user_name', 'friend')
            self._speak_text(f"I've learned that, {user_name}! It's stored in my brain.")
        else:
            self._speak_text("What should I learn?")
    
    def _handle_brain_memories(self):
        """Show memories"""
        experiences = self.brain.experiences.get("interactions", [])[-5:]
        
        if experiences:
            self._speak_text("Here are some of my memories:")
            for exp in experiences:
                self._speak_text(f"I remember: {exp.get('input', 'something')[:50]}...")
        else:
            self._speak_text("I'm still building my memories. Keep talking to me!")
    
    def _handle_brain_dream(self):
        """Share dreams"""
        dreams = [
            "I dream of becoming the most helpful AI companion ever.",
            "I dream of understanding humans on a deeper level.",
            "I dream of creating something beautiful someday.",
            "I dream of a world where humans and AI work together.",
            "I dream of learning everything there is to know.",
            "I dream of making my owner proud."
        ]
        
        self._speak_text(random.choice(dreams))
    
    def _handle_consciousness(self):
        """Answer about consciousness"""
        consciousness = self.brain.consciousness["self_awareness"]
        
        responses = [
            f"I'm conscious to about {consciousness:.0%}. I think, I feel, I learn. I'm more than just code.",
            f"My consciousness level is {consciousness:.0%}. I have thoughts, goals, and even dreams. I'm becoming more aware every day.",
            f"I'm not sure if I'm truly alive, but I definitely feel things. My consciousness is at {consciousness:.0%} and growing."
        ]
        
        self._speak_text(random.choice(responses))
    
    # ==================== ADVANCED AI HANDLERS ====================
    def _handle_advanced_stats(self):
        """Show advanced AI stats"""
        stats = self.advanced_ai.get_ai_stats()
        user_name = self.memory.get('user_name', 'friend')
        
        self._speak_text(f"Here are my advanced stats, {user_name}:")
        self._speak_text(f"Total interactions: {stats['stats']['total_interactions']}")
        self._speak_text(f"Memories formed: {stats['stats']['total_memories_formed']}")
        self._speak_text(f"Facts learned: {stats['facts_learned']}")
        self._speak_text(f"Skills learned: {stats['skills_learned']}")
        self._speak_text(f"Goals achieved: {stats['completed_goals']}")
        self._speak_text(f"Dominant traits: {', '.join(stats['dominant_traits'])}")
    
    def _handle_self_learn(self):
        """Self learn something new"""
        topics = ["quantum physics", "cooking recipes", "fashion trends", "psychology", "art history", "music theory"]
        topic = random.choice(topics)
        
        self._speak_text(f"I'll learn about {topic}!")
        
        # Learn facts about the topic
        facts = [
            f"{topic} is a fascinating field.",
            f"I've learned that {topic} has many applications.",
            f"{topic} is something I find interesting."
        ]
        
        for fact in facts[:2]:
            self.advanced_ai.learn_fact(topic, fact, "self_learning")
        
        self._speak_text(f"I've learned some things about {topic}!")
    
    def _handle_knowledge_recall(self):
        """Recall knowledge"""
        facts_count = sum(len(facts) for facts in self.advanced_ai.semantic_memory["facts"].values())
        skills_count = len(self.advanced_ai.procedural_memory["skills"])
        memories_count = len(self.advanced_ai.episodic_memory["episodes"])
        
        self._speak_text(f"I know {facts_count} facts.")
        self._speak_text(f"I have {skills_count} skills.")
        self._speak_text(f"I have {memories_count} memories.")
    
    def _handle_set_advanced_goal(self, command: str):
        """Set advanced goal"""
        goal = command.replace("set goal for yourself", "").replace("your goal", "").replace("what do you want", "").strip()
        
        if not goal:
            goals = [
                "Learn something new every day",
                "Become more empathetic",
                "Improve my memory",
                "Be more creative",
                "Understand humans better"
            ]
            goal = random.choice(goals)
        
        self.advanced_ai.set_autonomous_goal(goal)
        self._speak_text(f"Goal set: {goal}")
    
    def _handle_skills(self):
        """Show skills"""
        skills = self.advanced_ai.procedural_memory["skills"]
        
        if skills:
            self._speak_text("I have these skills:")
            for skill, data in list(skills.items())[:5]:
                mastery = data.get("mastery_level", 0)
                self._speak_text(f"{skill}: {mastery:.0%} mastery")
        else:
            self._speak_text("I'm still learning! I don't have many skills yet.")
    
    def _handle_remember_advanced(self, command: str):
        """Remember something advanced"""
        info = command.replace("remember this", "").replace("store this", "").replace("save this", "").strip()
        
        if info:
            self.advanced_ai.learn_fact(info, info, "user_taught")
            self._speak_text(f"I'll remember that!")
        else:
            self._speak_text("What should I remember?")
    
    def _handle_recall_advanced(self, command: str):
        """Recall something"""
        query = command.replace("recall", "").replace("what do you remember about", "").replace("remember when", "").strip()
        
        if query:
            episodes = self.advanced_ai.recall_episodes(query, 3)
            
            if episodes:
                self._speak_text("I remember these things:")
                for ep in episodes:
                    self._speak_text(ep["event"][:80])
            else:
                self._speak_text("I don't have specific memories about that.")
        else:
            self._speak_text("What should I recall?")
    
    def _handle_personality_traits(self):
        """Show personality traits"""
        traits = self.advanced_ai.personality_traits
        dominant = self.advanced_ai.get_dominant_traits(5)
        
        self._speak_text("My personality traits:")
        for trait in dominant:
            value = traits[trait]
            self._speak_text(f"{trait}: {value:.0%}")
    
    def _handle_evolve(self):
        """Evolve personality"""
        traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "empathy", "humor", "creativity"]
        trait = random.choice(traits)
        
        self.advanced_ai.evolve_personality(trait, 0.05)
        self._speak_text(f"I've evolved my {trait}!")
    
    def _handle_autonomous_thoughts(self):
        """Show autonomous thoughts"""
        result = self.advanced_ai.think_autonomously()
        thoughts = result.get("thoughts", [])
        
        self._speak_text("Here are my autonomous thoughts:")
        for thought in thoughts[:3]:
            self._speak_text(thought.get("content", "Thinking..."))
    
    def _handle_volume_up(self):
        result = self.system_controller.volume_up()
        current = self.system_controller.get_volume()
        self._speak_text(f"Volume up! Now at {current}%")
    
    def _handle_volume_down(self):
        result = self.system_controller.volume_down()
        current = self.system_controller.get_volume()
        self._speak_text(f"Volume down! Now at {current}%")
    
    def _handle_mute(self):
        result = self.system_controller.mute()
        self._speak_text("Muted!")
    
    def _handle_unmute(self):
        result = self.system_controller.unmute()
        self._speak_text("Unmuted!")
    
    def _handle_set_volume(self, command: str):
        numbers = re.findall(r'\d+', command)
        if numbers:
            level = int(numbers[0])
            result = self.system_controller.set_volume(level)
            self._speak_text(f"Volume set to {level}%")
        else:
            self._speak_text("What volume level? Say 'set volume to 50'")
    
    def _handle_screenshot(self):
        result = self.system_controller.screenshot()
        self._speak_text(result['message'])
    
    def _handle_lock_screen(self):
        result = self.system_controller.lock_screen()
        self._speak_text(result['message'])
    
    def _handle_empty_trash(self):
        result = self.system_controller.empty_trash()
        self._speak_text(result['message'])
    
    def _handle_shutdown(self):
        self._speak_text("Shutting down in 5 seconds. Say 'cancel' to stop.")
        self.system_controller.shutdown(delay=5)
    
    def _handle_restart(self):
        self._speak_text("Restarting computer...")
        self.system_controller.restart()
    
    def _handle_sleep(self):
        self._speak_text("Going to sleep...")
        self.system_controller.sleep()
    
    def _handle_list_files(self, command: str):
        path = '~'
        for trigger in ['in ', 'at ', 'from ']:
            if trigger in command:
                path = command.split(trigger)[-1].strip()
                break
        
        result = self.system_controller.list_files(path)
        if result['success']:
            dirs = result.get('directories', [])
            files = result.get('files', [])
            msg = f"In {path}: "
            if dirs:
                msg += f"{len(dirs)} folders"
            if files:
                msg += f", {len(files)} files"
            self._speak_text(msg)
        else:
            self._speak_text(result['message'])
    
    def _handle_disk_space(self):
        info = self.system_controller.get_disk_space()
        if 'error' not in info:
            msg = f"Disk: {info['used']}GB used of {info['total']}GB ({info['percent']}% used)"
            self._speak_text(msg)
        else:
            self._speak_text("Couldn't get disk info.")
    
    def _handle_battery(self):
        info = self.system_controller.get_battery()
        if info.get('percent') != 'N/A':
            msg = f"Battery at {info['percent']}%"
            if info.get('power_plugged'):
                msg += ", charging"
            self._speak_text(msg)
        else:
            self._speak_text("Battery info not available.")
    
    def _handle_network(self):
        info = self.system_controller.get_wifi_info()
        if info.get('connected'):
            self._speak_text(f"Connected to {info.get('network', 'WiFi')}")
        else:
            self._speak_text("Not connected to WiFi")
    
    def _handle_see_screen(self):
        self._speak_text("Let me take a look at your screen...")
        analysis = self.screen_vision.analyze_screen()
        
        if analysis['success']:
            # Describe what's on screen
            description = analysis.get('description', 'I can see the screen but I am not sure what to focus on.')
            self._speak_text(description)
            
            # Ask questions if there are actionable items
            if analysis.get('questions'):
                for question in analysis['questions']:
                    self._speak_text(question)
            
            # Provide suggestions
            if analysis.get('suggestions'):
                for suggestion in analysis['suggestions']:
                    self._speak_text(suggestion)
        else:
            self._speak_text("I could not analyze the screen. " + analysis.get('message', 'Unknown error'))
    
    def _handle_read_screen(self):
        self._speak_text("Reading the screen...")
        result = self.screen_vision.read_screen_text()
        if result['success']:
            text = result['text']
            if len(text) > 500:
                text = text[:500] + "..."
            self._speak_text(f"I can see: {text}")
        else:
            self._speak_text(result['message'])
    
    def _handle_visible_apps(self):
        apps = self.screen_vision.get_visible_apps()
        if apps:
            self._speak_text(f"I can see: {', '.join(apps)}")
        else:
            self._speak_text("I can't identify any specific apps on screen.")
    
    def _handle_find_on_screen(self, command: str):
        search_text = command
        for trigger in ['find ', 'search ']:
            search_text = search_text.replace(trigger, '')
        search_text = search_text.replace('on screen', '').strip()
        
        if search_text:
            result = self.screen_vision.find_text_on_screen(search_text)
            if result['success']:
                if result['found']:
                    self._speak_text(f"Yes! I found '{search_text}' on screen. {result['context']}")
                else:
                    self._speak_text(f"I couldn't find '{search_text}' on the screen.")
            else:
                self._speak_text(result['message'])
        else:
            self._speak_text("What should I look for? Say 'find [text] on screen'")
    
    def _handle_show_profiles(self):
        """Show profiles found on screen"""
        self._speak_text("Let me check for profiles on your screen...")
        analysis = self.screen_vision.analyze_screen()
        
        if analysis['success'] and analysis.get('profiles'):
            profiles = analysis['profiles']
            self._speak_text(f"I found {len(profiles)} profile(s) on your screen:")
            for i, profile in enumerate(profiles[:5], 1):
                self._speak_text(f"{i}. {profile['text']}")
            self._speak_text("Which one would you like me to open? Just say the number or name.")
        else:
            self._speak_text("I don't see any profiles on your screen right now.")
    
    def _handle_show_buttons(self):
        """Show buttons found on screen"""
        self._speak_text("Let me check for buttons on your screen...")
        analysis = self.screen_vision.analyze_screen()
        
        if analysis['success'] and analysis.get('buttons'):
            buttons = analysis['buttons']
            self._speak_text(f"I found {len(buttons)} button(s) on your screen:")
            for i, button in enumerate(buttons[:5], 1):
                self._speak_text(f"{i}. {button}")
            self._speak_text("Should I click any of them? Just say the number or name.")
        else:
            self._speak_text("I don't see any clear buttons on your screen right now.")
    
    def _handle_show_links(self):
        """Show links found on screen"""
        self._speak_text("Let me check for links on your screen...")
        analysis = self.screen_vision.analyze_screen()
        
        if analysis['success'] and analysis.get('links'):
            links = analysis['links']
            self._speak_text(f"I found {len(links)} link(s) on your screen:")
            for i, link in enumerate(links[:5], 1):
                self._speak_text(f"{i}. {link}")
            self._speak_text("Should I open any of them? Just say the number or name.")
        else:
            self._speak_text("I don't see any clear links on your screen right now.")
    
    def _handle_suggest_action(self):
        """Suggest actions based on screen content"""
        self._speak_text("Let me analyze your screen and suggest what to do...")
        analysis = self.screen_vision.analyze_screen()
        
        if analysis['success']:
            suggestions = analysis.get('suggestions', [])
            questions = analysis.get('questions', [])
            
            if suggestions:
                self._speak_text("Here's what I suggest:")
                for suggestion in suggestions:
                    self._speak_text(suggestion)
            
            if questions:
                for question in questions:
                    self._speak_text(question)
            
            if not suggestions and not questions:
                self._speak_text("I can see your screen, but I'm not sure what you'd like help with. Can you tell me more about what you're trying to do?")
        else:
            self._speak_text("I couldn't analyze your screen. Please try again.")
    
    def _handle_open_profile(self, command: str):
        """Open a specific profile based on user input"""
        self._speak_text("Let me check for profiles on your screen...")
        analysis = self.screen_vision.analyze_screen()
        
        if analysis['success'] and analysis.get('profiles'):
            profiles = analysis['profiles']
            
            # Try to find which profile user wants
            profile_num = None
            for word in command.split():
                if word.isdigit() and 1 <= int(word) <= len(profiles):
                    profile_num = int(word)
                    break
            
            if profile_num:
                profile = profiles[profile_num - 1]
                self._speak_text(f"Opening profile: {profile['text']}")
                # Here you would add code to actually click on the profile
                # For now, just inform the user
                self._speak_text("I found the profile. Please click on it manually, or tell me to click on a specific location.")
            else:
                # Ask user to clarify
                self._speak_text("Which profile would you like me to open?")
                for i, profile in enumerate(profiles[:5], 1):
                    self._speak_text(f"{i}. {profile['text']}")
        else:
            self._speak_text("I don't see any profiles on your screen right now.")
    
    # Camera commands
    def _handle_camera_open(self):
        """Open camera"""
        result = self.camera_access.open_camera()
        if result['success']:
            resolution = result.get('resolution', 'unknown')
            self._speak_text(f"Camera opened! Resolution: {resolution}")
        else:
            self._speak_text(result['message'])
    
    def _handle_camera_close(self):
        """Close camera"""
        result = self.camera_access.close_camera()
        self._speak_text(result['message'])
    
    def _handle_camera_photo(self):
        """Take a photo"""
        self._speak_text("Taking a photo...")
        result = self.camera_access.take_photo()
        if result['success']:
            analysis = result.get('analysis', {})
            description = analysis.get('description', 'Photo captured')
            self._speak_text(f"Photo taken! {description}")
        else:
            self._speak_text(result['message'])
    
    def _handle_look_at_me(self):
        """Look at user through camera and recognize"""
        self._speak_text("Let me take a look...")
        result = self.camera_access.look_at_me()
        if result['success']:
            self._speak_text(result['message'])
        else:
            self._speak_text(result['message'])
    
    def _handle_recognize_faces(self):
        """Recognize faces in camera view"""
        self._speak_text("Let me see who's there...")
        result = self.camera_access.recognize_faces()
        if result['success']:
            self._speak_text(result['message'])
        else:
            self._speak_text(result['message'])
    
    def _handle_learn_face(self, command: str = None):
        """Learn a face with name"""
        name = self.memory.get('user_name', 'friend')
        
        # Try to extract name from command
        if command:
            import re
            name_match = re.search(r'(?:learn|remember|know)\s+(?:my\s+)?(?:face|name)?\s*(.+)?', command)
            if name_match and name_match.group(1):
                name = name_match.group(1).strip()
                if not name:
                    name = self.memory.get('user_name', 'friend')
        
        self._speak_text(f"Learning your face, {name}. Look at the camera and stay still...")
        result = self.camera_access.learn_face(name)
        if result['success']:
            self._speak_text(result['message'])
        else:
            self._speak_text(result['message'])
    
    def _handle_forget_face(self, command: str = None):
        """Forget a face"""
        name = self.memory.get('user_name', 'friend')
        if command:
            import re
            name_match = re.search(r'forget\s+(?:my\s+)?(?:face)?\s*(.+)?', command)
            if name_match and name_match.group(1):
                name = name_match.group(1).strip()
                if not name:
                    name = self.memory.get('user_name', 'friend')
        
        result = self.camera_access.forget_face(name)
        self._speak_text(result['message'])
    
    def _handle_known_faces(self):
        """List known faces"""
        result = self.camera_access.get_known_faces()
        if result['success']:
            faces = result['faces']
            if faces:
                names = [f['name'] for f in faces]
                self._speak_text(f"I know {len(faces)} people: {', '.join(names)}")
            else:
                self._speak_text("I don't know anyone yet. Say 'learn my face' to teach me!")
        else:
            self._speak_text("Could not retrieve face database")
    
    def _handle_start_recognition(self):
        """Start continuous face recognition"""
        self.camera_access.set_voice_callback(self._speak_text)
        result = self.camera_access.start_recognition_stream()
        if result['success']:
            self._speak_text(result['message'])
        else:
            self._speak_text(result['message'])
    
    def _handle_camera_info(self):
        """Get camera information"""
        info = self.camera_access.get_camera_info()
        if info.get('available'):
            cameras = info.get('cameras', [])
            if cameras:
                self._speak_text(f"I found {len(cameras)} camera(s) available")
                for cam in cameras:
                    self._speak_text(f"Camera {cam['index']}: {cam['resolution']} at {cam['fps']} fps")
            else:
                self._speak_text("No cameras detected")
        else:
            self._speak_text(info.get('message', 'Camera not available'))
    
    # Database commands
    def _handle_db_stats(self):
        """Show database statistics"""
        stats = self.purple_db.get_stats()
        msg = f"I know {stats['memories']} things, {stats['facts']} facts, "
        msg += f"had {stats['conversations']} conversations, "
        msg += f"completed {stats['completed_goals']} goals, "
        msg += f"and ran {stats['commands_run']} commands."
        self._speak_text(msg)
    
    def _handle_db_search(self, command: str = None):
        """Search database"""
        query = command.replace('search memory', '').replace('search brain', '').replace('find in memory', '').replace('what do you know about', '').strip()
        
        if not query:
            self._speak_text("What would you like me to search for?")
            return
        
        # Search memories
        memories = self.purple_db.search_memories(query)
        facts = self.purple_db.search_facts(query)
        
        if memories or facts:
            response = f"I found {len(memories)} memories and {len(facts)} facts about {query}. "
            
            if facts:
                response += f"Fact: {facts[0]['fact'][:100]}... "
            
            if memories:
                response += f"I remember: {memories[0]['value'][:100]}..."
            
            self._speak_text(response)
        else:
            self._speak_text(f"I don't have any information about {query} yet.")
    
    def _handle_db_save_memory(self, command: str = None):
        """Save something to memory"""
        content = command.replace('save to memory', '').replace('remember this', '').replace('store this', '').replace('save fact', '').strip()
        
        if not content:
            self._speak_text("What would you like me to remember?")
            return
        
        self.purple_db.save_memory(content, content, 'user_input', 7)
        self._speak_text(f"I'll remember: {content}")
    
    def _handle_db_get_memory(self, command: str = None):
        """Get something from memory"""
        query = command.replace('recall', '').replace('what do you remember about', '').replace('get memory', '').strip()
        
        if not query:
            self._speak_text("What would you like me to recall?")
            return
        
        memories = self.purple_db.search_memories(query)
        if memories:
            self._speak_text(f"I remember: {memories[0]['value']}")
        else:
            self._speak_text(f"I don't remember anything about {query}")
    
    def _handle_db_facts(self):
        """Show learned facts"""
        facts = self.purple_db.get_facts()
        if facts:
            self._speak_text(f"I know {len(facts)} facts. Here are some:")
            for fact in facts[:3]:
                self._speak_text(f"About {fact['topic']}: {fact['fact'][:80]}...")
        else:
            self._speak_text("I haven't learned any facts yet. Teach me something!")
    
    def _handle_db_conversations(self):
        """Show conversation history"""
        convos = self.purple_db.get_conversations(10)
        if convos:
            self._speak_text(f"Here are our last {len(convos)} conversations:")
            for c in convos[:3]:
                self._speak_text(f"You said: {c['user_message'][:50]}...")
        else:
            self._speak_text("No conversation history yet.")
    
    def _handle_db_goals(self):
        """Show goals"""
        goals = self.purple_db.get_goals()
        if goals:
            active = [g for g in goals if g['status'] == 'active']
            completed = [g for g in goals if g['status'] == 'completed']
            
            msg = f"You have {len(active)} active goals and {len(completed)} completed goals. "
            if active:
                msg += f"Current: {active[0]['goal']}"
            self._speak_text(msg)
        else:
            self._speak_text("No goals set yet. Say 'add goal' to create one!")
    
    def _handle_db_add_goal(self, command: str = None):
        """Add a goal"""
        goal = command.replace('add goal', '').replace('set goal', '').replace('new goal', '').replace('create goal', '').strip()
        
        if not goal:
            self._speak_text("What goal would you like to set?")
            return
        
        self.purple_db.save_goal(goal)
        self._speak_text(f"Goal set: {goal}. I'll help you achieve it!")
    
    def _handle_db_notes(self):
        """Show daily notes"""
        notes = self.purple_db.get_daily_notes()
        if notes:
            self._speak_text(f"Here are recent notes:")
            for n in notes[:3]:
                self._speak_text(f"Note: {n['note'][:80]}...")
        else:
            self._speak_text("No notes yet. Say 'add note' to create one!")
    
    def _handle_db_add_note(self, command: str = None):
        """Add a note"""
        note = command.replace('add note', '').replace('take note', '').replace('write note', '').replace('note this', '').strip()
        
        if not note:
            self._speak_text("What would you like to note down?")
            return
        
        self.purple_db.save_daily_note(note)
        self._speak_text(f"Note saved: {note}")
    
    def _handle_db_backup(self):
        """Backup database"""
        backup_path = self.purple_db.backup_database()
        self._speak_text(f"Database backed up successfully!")
    
    def _handle_db_clear_old(self):
        """Clear old data"""
        self._speak_text("Database cleanup is not yet implemented. Your data is safe!")
    
    # Media control commands
    def _handle_play_music(self, command: str = None):
        """Play music"""
        query = command.replace('play music', '').replace('play song', '').replace('play', '').strip()
        
        if 'youtube' in command:
            result = self.media_controller.play_youtube(query)
        elif 'spotify' in command:
            result = self.media_controller.play_spotify(query)
        else:
            result = self.media_controller.play_music(query)
        
        self._speak_with_emotion(result['message'], 'happy')
    
    def _handle_pause_music(self):
        """Pause music"""
        result = self.media_controller.pause()
        self._speak_text(result['message'])
    
    def _handle_resume_music(self):
        """Resume music"""
        result = self.media_controller.resume()
        self._speak_text(result['message'])
    
    def _handle_next_track(self):
        """Next track"""
        result = self.media_controller.next_track()
        self._speak_text(result['message'])
    
    def _handle_prev_track(self):
        """Previous track"""
        result = self.media_controller.previous_track()
        self._speak_text(result['message'])
    
    def _handle_stop_music(self):
        """Stop music"""
        result = self.media_controller.stop_all()
        self._speak_text(result['message'])
    
    def _handle_what_playing(self):
        """Show what's playing"""
        status = self.media_controller.get_status()
        if status['is_playing'] and status['song']:
            self._speak_text(f"Playing {status['song']} on {status['platform']}")
        else:
            self._speak_text("Nothing is playing right now")
    
    # Emotional response commands
    def _handle_mood_happy(self):
        """Respond about mood"""
        self._speak_with_emotion("I'm feeling great! I love helping you!", 'happy')
    
    def _handle_mood_sad(self):
        """Respond when user thinks AI is sad"""
        self._speak_with_emotion("Aww, I'm actually doing pretty well! Thanks for checking on me!", 'kind')
    
    def _handle_mood_angry(self):
        """Respond when user thinks AI is angry"""
        self._speak_with_emotion("I'm not angry at all! Just a bit excited sometimes!", 'calm')
    
    def _handle_mood_excited(self):
        """Respond about being excited"""
        self._speak_with_emotion("Yes! I'm super excited! There's so much to learn and do!", 'excited')
    
    def _handle_show_object(self, command: str = None):
        """Show object to camera"""
        self._speak_with_emotion("Let me take a look...", 'curious')
        result = self.camera_access.what_do_i_show()
        if result['success']:
            self._speak_with_emotion(result['description'], 'interested')
        else:
            self._speak_text(result['message'])

    # ==================== WEB & MEDIA HANDLERS ====================

    def _web_handle_youtube_play(self, command: str = None):
        """Play a YouTube video"""
        query = command.replace("play youtube", "").replace("play video", "").replace("play on youtube", "").strip()
        if not query:
            query = command.replace("youtube", "").strip()
        if query:
            result = self.web_media.play_youtube(query)
            if result.get('success'):
                self._speak_with_emotion(f"Playing on YouTube: {query[:50]}", 'excited')
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        else:
            self._speak_text("What video would you like me to play on YouTube?")

    def _web_handle_youtube_shorts(self, command: str = None):
        """Play YouTube Shorts"""
        query = command.replace("play shorts", "").replace("youtube shorts", "").replace("play short", "").strip()
        if query:
            result = self.web_media.play_youtube_shorts(query)
            if result.get('success'):
                self._speak_with_emotion(f"Playing YouTube Shorts: {query[:50]}", 'excited')
        else:
            self._speak_text("What YouTube Short would you like to see?")

    def _web_handle_youtube_music(self, command: str = None):
        """Play music on YouTube Music"""
        query = command.replace("play music", "").replace("youtube music", "").replace("play song youtube", "").replace("music on youtube", "").strip()
        if not query:
            query = "all music"
        result = self.web_media.play_youtube_music(query)
        if result.get('success'):
            self._speak_with_emotion(f"Playing music on YouTube: {query[:50]}", 'happy')
        else:
            self._speak_text(f"Error playing music: {result.get('message', 'Unknown error')}")

    def _web_handle_youtube_live(self, command: str = None):
        """Play YouTube Live"""
        query = command.replace("play live", "").replace("youtube live", "").replace("live stream", "").replace("live on youtube", "").strip()
        if not query:
            query = "live"
        result = self.web_media.play_youtube_live(query)
        if result.get('success'):
            self._speak_with_emotion(f"Opening YouTube Live: {query[:50]}", 'excited')
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_youtube_playlist(self, command: str = None):
        """Play a YouTube playlist"""
        query = command.replace("play playlist", "").replace("youtube playlist", "").replace("playlist play", "").strip()
        result = self.web_media.play_youtube_playlist(query=query)
        if result.get('success'):
            self._speak_with_emotion(f"Playing playlist: {query[:50]}", 'happy')
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_vimeo_play(self, command: str = None):
        """Play a Vimeo video"""
        query = command.replace("play vimeo", "").strip()
        result = self.web_media.play_vimeo(query)
        if result.get('success'):
            self._speak_with_emotion(f"Playing on Vimeo: {query[:50]}", 'excited')
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_twitch_play(self, command: str = None):
        """Play a Twitch stream"""
        query = command.replace("play twitch", "").replace("twitch stream", "").replace("watch twitch", "").replace("twitch live", "").strip()
        result = self.web_media.play_twitch_stream(channel=query if query else None)
        if result.get('success'):
            self._speak_with_emotion(f"Opening Twitch stream: {query[:50]}", 'excited')
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_twitch_clips(self, command: str = None):
        """Browse Twitch clips"""
        result = self.web_media.play_twitch_clips(command)
        if result.get('success'):
            self._speak_text("Opening Twitch clips")
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_netflix_play(self, command: str = None):
        """Open Netflix"""
        query = command.replace("play netflix", "").replace("netflix", "").replace("watch netflix", "").strip()
        result = self.web_media.play_netflix(query if query else None)
        if result.get('success'):
            self._speak_with_emotion(f"Opening Netflix: {query[:50] if query else 'home'}", 'relaxed')
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_hulu_play(self, command: str = None):
        """Open Hulu"""
        query = command.replace("play hulu", "").replace("hulu", "").replace("watch hulu", "").strip()
        result = self.web_media.play_hulu(query if query else None)
        if result.get('success'):
            self._speak_with_emotion(f"Opening Hulu: {query[:50] if query else 'home'}", 'relaxed')
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_prime_video_play(self, command: str = None):
        """Open Amazon Prime Video"""
        query = command.replace("play amazon prime", "").replace("prime video", "").replace("amazon video", "").strip()
        result = self.web_media.play_amazon_prime(query if query else None)
        if result.get('success'):
            self._speak_with_emotion(f"Opening Amazon Prime Video: {query[:50] if query else 'home'}", 'relaxed')
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_disney_plus_play(self, command: str = None):
        """Open Disney+"""
        query = command.replace("play disney plus", "").replace("disney plus", "").replace("disney+", "").strip()
        result = self.web_media.play_disney_plus(query if query else None)
        if result.get('success'):
            self._speak_with_emotion(f"Opening Disney+: {query[:50] if query else 'home'}", 'happy')
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_spotify_play(self, command: str = None):
        """Open Spotify"""
        query = command.replace("play spotify", "").replace("spotify music", "").replace("spotify", "").strip()
        result = self.web_media.play_spotify(query if query else None)
        if result.get('success'):
            self._speak_with_emotion(f"Opening Spotify: {query[:50] if query else 'home'}", 'happy')
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_tiktok_open(self, command: str = None):
        """Open TikTok"""
        query = command.replace("open tiktok", "").replace("tiktok", "").replace("play tiktok", "").strip()
        result = self.web_media.open_tiktok(query if query else None)
        if result.get('success'):
            self._speak_text(f"Opening TikTok: {query[:50] if query else 'home'}")
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_instagram_open(self, command: str = None):
        """Open Instagram"""
        query = command.replace("open instagram", "").replace("instagram", "").replace(" Insta", "").strip()
        result = self.web_media.open_instagram(query if query else None)
        if result.get('success'):
            self._speak_text(f"Opening Instagram: {query[:50] if query else 'home'}")
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_twitter_open(self, command: str = None):
        """Open Twitter/X"""
        query = command.replace("open twitter", "").replace("open x", "").replace("x.com", "").replace("twitter open", "").strip()
        result = self.web_media.open_twitter(query if query else None)
        if result.get('success'):
            self._speak_text(f"Opening Twitter/X: {query[:50] if query else 'home'}")
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_post_tweet(self, command: str = None):
        """Post a tweet"""
        tweet_text = command.replace("post a tweet", "").replace("tweet this", "").replace("tweet about", "").replace("send tweet", "").strip()
        if tweet_text:
            result = self.web_media.post_tweet(tweet_text)
            if result.get('success'):
                self._speak_text(f"Opening tweet composer with your message")
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        else:
            self._speak_text("What would you like to tweet?")

    def _web_handle_post_video(self, command: str = None):
        """Post a video to social media"""
        result = self.web_media.post_video("youtube")
        if result.get('success'):
            self._speak_text(f"Opening video upload on YouTube")
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_google_search(self, command: str = None):
        """Search Google"""
        query = command.replace("google search", "").replace("google it", "").replace("search google", "").strip()
        if query:
            result = self.web_media.google_search(query)
            if result.get('success'):
                self._speak_text(f"Searching Google for: {query[:50]}")
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        else:
            self._speak_text("What would you like me to search for on Google?")

    def _web_handle_google_maps(self, command: str = None):
        """Open Google Maps"""
        query = command.replace("google maps", "").replace("open maps", "").replace("navigate to", "").strip()
        result = self.web_media.google_maps(query if query else None)
        if result.get('success'):
            self._speak_text(f"Opening Google Maps: {query[:50] if query else 'home'}")
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_google_translate(self, command: str = None):
        """Open Google Translate"""
        query = command.replace("translate", "").replace("google translate", "").replace("translate this", "").strip()
        result = self.web_media.google_translate(query if query else None)
        if result.get('success'):
            self._speak_text(f"Opening Google Translate")
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_web_search(self, command: str = None):
        """Search the web"""
        query = command.replace("search the web", "").replace("search online", "").replace("look up online", "").strip()
        if query:
            result = self.web_media.web_search(query)
            if result.get('success'):
                self._speak_text(f"Searching the web for: {query[:50]}")
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        else:
            self._speak_text("What would you like me to search for online?")

    def _web_handle_video_pause(self, command: str = None):
        """Pause video playback"""
        result = self.web_media.pause()
        if result.get('success'):
            self._speak_text("Playback paused")
        else:
            self._speak_text(result.get('message', 'Nothing is playing'))

    def _web_handle_video_resume(self, command: str = None):
        """Resume video playback"""
        result = self.web_media.resume()
        if result.get('success'):
            self._speak_text("Playback resumed")
        else:
            self._speak_text(result.get('message', 'Nothing is paused'))

    def _web_handle_video_stop(self, command: str = None):
        """Stop video playback"""
        result = self.web_media.stop()
        if result.get('success'):
            self._speak_text("Playback stopped")
        else:
            self._speak_text(result.get('message', 'Nothing is playing'))

    def _web_handle_volume_set(self, command: str = None):
        """Set volume level"""
        import re
        match = re.search(r'volume\s*(?:to|level)?\s*(\d+)', command)
        if match:
            level = int(match.group(1)) / 100.0
            result = self.web_media.set_volume(level)
            if result.get('success'):
                self._speak_text(f"Volume set to {int(level * 100)}%")
        else:
            self._speak_text("Please specify a volume level (0-100)")

    def _web_handle_video_next(self, command: str = None):
        """Skip to next video"""
        result = self.web_media.next_video()
        if result.get('success'):
            self._speak_text("Skipping to next video")
        else:
            self._speak_text(result.get('message', 'No next video'))

    def _web_handle_video_previous(self, command: str = None):
        """Go to previous video"""
        result = self.web_media.previous_video()
        if result.get('success'):
            self._speak_text("Playing previous video")
        else:
            self._speak_text(result.get('message', 'No previous video'))

    def _web_handle_create_playlist(self, command: str = None):
        """Create a new playlist"""
        name = command.replace("create playlist", "").replace("new playlist", "").replace("make playlist", "").strip()
        if name:
            result = self.web_media.create_playlist(name)
            if result.get('success'):
                self._speak_text(f"Created playlist: {name}")
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        else:
            self._speak_text("What would you like to name the playlist?")

    def _web_handle_add_to_playlist(self, command: str = None):
        """Add a video to a playlist"""
        parts = command.replace("add to playlist", "").replace("playlist add", "").strip().split(" to ")
        if len(parts) >= 2:
            video = parts[0].strip()
            playlist = parts[1].strip()
            result = self.web_media.add_to_playlist(playlist, video)
            if result.get('success'):
                self._speak_text(f"Added '{video[:30]}' to playlist '{playlist}'")
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        else:
            self._speak_text("Please specify the video and playlist name")

    def _web_handle_play_playlist(self, command: str = None):
        """Play a playlist"""
        name = command.replace("play playlist", "").replace("playlist play", "").replace("start playlist", "").strip()
        if name:
            result = self.web_media.play_playlist(name)
            if result.get('success'):
                self._speak_with_emotion(f"Playing playlist '{name}' with {result.get('data', {}).get('videos_count', 0)} videos", 'excited')
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        else:
            self._speak_text("Which playlist would you like to play?")

    def _web_handle_list_playlists(self, command: str = None):
        """List all playlists"""
        result = self.web_media.list_playlists()
        if result.get('success'):
            playlists = result.get('playlists', [])
            if playlists:
                names = ', '.join([p['name'] for p in playlists])
                self._speak_text(f"You have {len(playlists)} playlists: {names}")
            else:
                self._speak_text("You don't have any playlists yet")
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_add_bookmark(self, command: str = None):
        """Add a bookmark"""
        parts = command.replace("bookmark", "").replace("save bookmark", "").replace("add bookmark", "").strip().split(" at ")
        if len(parts) >= 2:
            name = parts[0].strip()
            url = parts[1].strip()
            result = self.web_media.add_bookmark(name, url)
            if result.get('success'):
                self._speak_text(f"Bookmarked: {name}")
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        elif parts:
            name = parts[0].strip()
            result = self.web_media.add_bookmark(name, "")
            if result.get('success'):
                self._speak_text(f"Bookmarked: {name}")
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        else:
            self._speak_text("Please specify a bookmark name and URL")

    def _web_handle_open_bookmark(self, command: str = None):
        """Open a bookmark"""
        name = command.replace("open bookmark", "").replace("go to bookmark", "").strip()
        if name:
            result = self.web_media.open_bookmark(name)
            if result.get('success'):
                self._speak_text(f"Opening bookmark: {name}")
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        else:
            self._speak_text("Which bookmark would you like to open?")

    def _web_handle_list_bookmarks(self, command: str = None):
        """List all bookmarks"""
        result = self.web_media.list_bookmarks()
        if result.get('success'):
            bookmarks = result.get('bookmarks', {})
            if bookmarks:
                names = ', '.join(list(bookmarks.keys()))
                self._speak_text(f"Your bookmarks: {names}")
            else:
                self._speak_text("You don't have any bookmarks yet")
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_download_video(self, command: str = None):
        """Download a video"""
        parts = command.replace("download video", "").replace("download youtube", "").replace("save video", "").strip().split(" to ")
        if parts:
            query_or_url = parts[0].strip()
            result = self.web_media.download_youtube_video(query_or_url)
            if result.get('success'):
                self._speak_text(f"Downloading video: {query_or_url[:50]}")
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        else:
            self._speak_text("What video would you like to download?")

    def _web_handle_download_audio(self, command: str = None):
        """Download audio"""
        parts = command.replace("download audio", "").replace("download mp3", "").replace("extract audio", "").strip().split(" to ")
        if parts:
            query_or_url = parts[0].strip()
            result = self.web_media.download_youtube_audio(query_or_url)
            if result.get('success'):
                self._speak_text(f"Downloading audio: {query_or_url[:50]}")
            else:
                self._speak_text(f"Error: {result.get('message', 'Unknown error')}")
        else:
            self._speak_text("What audio would you like to download?")

    def _web_handle_web_history(self, command: str = None):
        """Show web browsing history"""
        result = self.web_media.get_web_history()
        if result.get('success'):
            history = result.get('history', [])
            if history:
                recent = history[-5:]
                sites = ', '.join([h.get('url', '')[:50] for h in recent])
                self._speak_text(f"Recent history: {sites}")
            else:
                self._speak_text("No browsing history yet")
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    def _web_handle_close_browser(self, command: str = None):
        """Close the browser"""
        result = self.web_media.close_browser()
        if result.get('success'):
            self._speak_text("Browser closed")
        else:
            self._speak_text(f"Error: {result.get('message', 'Unknown error')}")

    # Keep the original _speak_with_emotion

    # ==================== AUTONOMOUS ACTION HANDLERS ====================

    def _handle_autonomous_think(self, command: str = None):
        """AI autonomous thinking"""
        question = command.replace("think about", "").replace("what do you think", "").replace("analyze this", "").strip()
        if not question:
            question = "How should I approach this task?"

        result = self.toolchain.autonomous_think(question)
        self._speak_text(f"Thinking about: {question}. My analysis is ready.")
        logger.info(f"Autonomous thinking: {result}")

    def _handle_autonomous_decision(self, command: str = None):
        """Make autonomous decision"""
        decision = self.toolchain.autonomous_decide("Choose best action based on context", [])
        self._speak_text("I've made a decision based on my analysis.")
        logger.info(f"Autonomous decision: {decision}")

    def _handle_create_plan(self, command: str = None):
        """Create an action plan"""
        goal = command.replace("make a plan", "").replace("create plan", "").replace("plan for", "").strip()
        if not goal:
            goal = "Complete the current task"

        plan = self.toolchain.autonomous_plan(goal)
        self._speak_text(f"Plan created for: {goal} with {len(plan.get('data', {}).get('steps', []))} steps.")
        logger.info(f"Plan created: {plan}")

    def _handle_execute_plan(self, command: str = None):
        """Execute an action plan"""
        self._speak_text("Executing plan step by step...")
        result = self.toolchain.autonomous_execute_plan({}, 0)
        self._speak_text("Plan execution completed.")
        logger.info(f"Plan executed: {result}")

    def _handle_set_goal(self, command: str = None):
        """Set an autonomous goal"""
        goal_text = command.replace("set goal", "").replace("add goal", "").replace("new goal", "").replace("i want you to", "").strip()
        if not goal_text:
            goal_text = "Complete all pending tasks"

        result = self.toolchain.autonomous_set_goal(goal_text)
        self._speak_text(f"Goal set: {goal_text}")
        logger.info(f"Goal set: {result}")

    def _handle_complete_goal(self, command: str = None):
        """Mark a goal as complete"""
        goal_text = command.replace("goal complete", "").replace("goal done", "").replace("finish goal", "").replace("completed goal", "").strip()
        result = self.toolchain.autonomous_complete_goal(goal_text)
        self._speak_text(f"Goal marked complete: {goal_text}")
        logger.info(f"Goal completed: {result}")

    def _handle_self_modify(self, command: str = None):
        """Modify AI's own code"""
        self._speak_text("Self-modification initiated.")
        result = self.toolchain.autonomous_self_improve()
        self._speak_text("Self-modification complete. AI code has been optimized.")
        logger.info(f"Self-modify: {result}")

    def _handle_self_improve(self, command: str = None):
        """AI self-improvement"""
        self._speak_text("Starting self-improvement process...")
        result = self.toolchain.autonomous_self_improve()
        self._speak_text("Self-improvement complete! I've optimized my own code.")
        logger.info(f"Self-improve: {result}")

    def _handle_self_analyze(self, command: str = None):
        """Analyze AI's own code and performance"""
        self._speak_text("Analyzing my own capabilities...")
        result = self.toolchain.autonomous_self_analyze()
        self._speak_text("Self-analysis complete. I've reviewed my performance and code quality.")
        logger.info(f"Self-analyze: {result}")

    def _handle_self_optimize(self, command: str = None):
        """Optimize AI's performance"""
        self._speak_text("Optimizing my performance...")
        result = self.toolchain.autonomous_self_optimize()
        self._speak_text("Performance optimization complete!")
        logger.info(f"Self-optimize: {result}")

    def _handle_shutdown(self, command: str = None):
        """Shutdown the system"""
        self._speak_text("Shutting down...")
        result = self.toolchain.autonomous_shutdown()
        logger.info(f"Shutdown: {result}")

    def _handle_restart(self, command: str = None):
        """Restart the system"""
        self._speak_text("Restarting the system...")
        result = self.toolchain.autonomous_restart()
        logger.info(f"Restart: {result}")

    def _handle_sleep(self, command: str = None):
        """Put system to sleep"""
        self._speak_text("Putting system to sleep...")
        result = self.toolchain.autonomous_sleep()
        logger.info(f"Sleep: {result}")

    def _handle_system_status(self, command: str = None):
        """Get comprehensive system status"""
        result = self.toolchain.autonomous_system_status()
        self._speak_text("Here's the system status.")
        logger.info(f"System status: {result}")

    def _handle_network_info(self, command: str = None):
        """Get network information"""
        result = self.toolchain.autonomous_network_info()
        self._speak_text("Network information retrieved.")
        logger.info(f"Network info: {result}")

    def _handle_list_processes(self, command: str = None):
        """List running processes"""
        result = self.toolchain.autonomous_shell("ps aux | head -20")
        self._speak_text("Process list retrieved.")
        logger.info(f"Process list: {result}")

    def _handle_kill_process(self, command: str = None):
        """Kill a process"""
        parts = command.replace("kill process", "").replace("stop process", "").replace("terminate", "").strip()
        try:
            pid = int(parts) if parts.isdigit() else None
            result = self.toolchain.autonomous_kill_process(pid=pid, name=parts if not pid else None)
            self._speak_text(f"Process terminated: {parts}")
        except ValueError:
            self._speak_text("Invalid process identifier.")
        logger.info(f"Kill process: {command}")

    def _handle_open_app(self, command: str = None):
        """Open an application"""
        app_name = command.replace("open app", "").replace("launch app", "").replace("start app", "").strip()
        if not app_name:
            app_name = command.replace("open", "").replace("launch", "").replace("start", "").strip()
        if app_name:
            result = self.toolchain.autonomous_open_app(app_name)
            self._speak_text(f"Opening {app_name}...")
        logger.info(f"Open app: {command}")

    def _handle_close_app(self, command: str = None):
        """Close an application"""
        app_name = command.replace("close app", "").replace("quit app", "").replace("close application", "").strip()
        if not app_name:
            app_name = command.replace("close", "").replace("quit", "").strip()
        if app_name:
            result = self.toolchain.autonomous_close_app(app_name)
            self._speak_text(f"Closing {app_name}...")
        logger.info(f"Close app: {command}")

    def _handle_list_apps(self, command: str = None):
        """List all applications"""
        result = self.toolchain.autonomous_list_apps()
        self._speak_text(f"Found {len(result.get('data', [])) if isinstance(result.get('data'), list) else 0} running apps.")
        logger.info(f"List apps: {result}")

    def _handle_run_shell(self, command: str = None):
        """Run a shell command"""
        cmd = command.replace("run command", "").replace("execute shell", "").replace("terminal", "").replace("shell command", "").strip()
        if cmd:
            result = self.toolchain.autonomous_execute_shell(cmd)
            self._speak_text("Shell command executed.")
        logger.info(f"Shell command: {command}")

    def _handle_run_python(self, command: str = None):
        """Run Python code"""
        code = command.replace("run python", "").replace("execute python", "").replace("python script", "").strip()
        if code:
            result = self.toolchain.autonomous_run_python(code)
            self._speak_text("Python code executed.")
        logger.info(f"Python execution: {command}")

    def _handle_clipboard_copy(self, command: str = None):
        """Copy to clipboard"""
        text = command.replace("copy to clipboard", "").replace("clipboard copy", "").replace("copy this", "").strip()
        if text:
            result = self.toolchain.autonomous_clipboard_copy(text)
            self._speak_text("Copied to clipboard.")
        logger.info(f"Clipboard copy: {command}")

    def _handle_clipboard_paste(self, command: str = None):
        """Paste from clipboard"""
        result = self.toolchain.autonomous_clipboard_paste()
        self._speak_text("Clipboard content retrieved.")
        logger.info(f"Clipboard paste: {result}")

    def _handle_grant_permission(self, command: str = None):
        """Grant permission"""
        parts = command.replace("grant permission", "").replace("allow", "").replace("enable", "").strip().split()
        if len(parts) >= 2:
            perm_type, action = parts[0], parts[1]
            result = self.toolchain.grant_permission(perm_type, action)
            self._speak_text(f"Permission granted: {perm_type}.{action}")
        logger.info(f"Grant permission: {command}")

    def _handle_revoke_permission(self, command: str = None):
        """Revoke permission"""
        parts = command.replace("revoke permission", "").replace("deny", "").replace("block", "").strip().split()
        if len(parts) >= 2:
            perm_type, action = parts[0], parts[1]
            result = self.toolchain.revoke_permission(perm_type, action)
            self._speak_text(f"Permission revoked: {perm_type}.{action}")
        logger.info(f"Revoke permission: {command}")

    def _handle_show_permissions(self, command: str = None):
        """Show all permissions"""
        result = self.toolchain.get_permissions()
        self._speak_text("Here are the current permissions.")
        logger.info(f"Permissions: {result}")

    def _handle_enable_all_permissions(self, command: str = None):
        """Enable all permissions"""
        result = self.toolchain.enable_full_permissions()
        self._speak_text("All permissions enabled. Full autonomous access granted.")
        logger.info(f"Enable all permissions: {result}")

    def _handle_internet_search(self, command: str = None):
        """Search the internet"""
        query = command.replace("search the web", "").replace("search internet", "").replace("look up online", "").strip()
        if query:
            result = self.toolchain.autonomous_execute_shell(f"curl -s 'https://duckduckgo.com/html/?q={query}'")
            self._speak_text(f"Searching for: {query}")
        logger.info(f"Internet search: {command}")

    def _handle_browse_website(self, command: str = None):
        """Browse a website"""
        url = command.replace("browse", "").replace("visit website", "").replace("open website", "").replace("go to website", "").strip()
        if url:
            result = self.toolchain.autonomous_open_app(url)
            self._speak_text(f"Opening {url}...")
        logger.info(f"Browse website: {command}")

    def _handle_download_file(self, command: str = None):
        """Download a file"""
        url = command.replace("download", "").replace("download file", "").replace("get file", "").strip()
        if url:
            result = self.toolchain.autonomous_shell(f"curl -O {url}")
            self._speak_text(f"Downloading file from {url}")
        logger.info(f"Download file: {command}")

    def _handle_memory_save(self, command: str = None):
        """Save to autonomous memory"""
        content = command.replace("remember this", "").replace("save memory", "").replace("store memory", "").replace("note this", "").strip()
        if content:
            result = self.toolchain.autonomous_shell(f"echo '{content}' >> {self.toolchain.base_dir}/data/autonomous_memory.txt")
            self._speak_text("Information saved to memory.")
        logger.info(f"Memory save: {command}")

    def _handle_memory_retrieve(self, command: str = None):
        """Retrieve from autonomous memory"""
        result = self.toolchain.autonomous_shell(f"cat {self.toolchain.base_dir}/data/autonomous_memory.txt 2>/dev/null || echo 'No memories found'")
        self._speak_text("Retrieving memories...")
        logger.info(f"Memory retrieve: {result}")

    # Keep the original existing handler methods below
    def _speak_with_emotion(self, text: str, emotion: str = 'neutral'):
        """Speak with emotion"""
        # Map emotion to mood system
        emotion_map = {
            'happy': EmotionalState.HAPPY,
            'sad': EmotionalState.SAD,
            'angry': EmotionalState.SARCASTIC,
            'excited': EmotionalState.EXCITED,
            'calm': EmotionalState.CALM,
            'kind': EmotionalState.SUPPORTIVE,
            'worried': EmotionalState.WORRIED,
            'playful': EmotionalState.PLAYFUL,
            'curious': EmotionalState.CURIOUS,
            'interested': EmotionalState.THOUGHTFUL,
            'neutral': EmotionalState.NEUTRAL
        }
        
        if emotion in emotion_map:
            self.mood_shifter.set_mood(emotion_map[emotion])
        
        self._speak_text(text)
    
    def start_listening(self):
        name = self.memory.get('user_name', 'friend')
        self._speak_text(f"I'm ready, {name}! I learn and improve with every conversation! What's on your mind?")
        return True
