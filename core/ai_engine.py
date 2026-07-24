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

class OfflineAI:
    def __init__(self, tts_engine=None):
        self.tts_engine = tts_engine
        self.memory_manager = MemoryManager()
        self.response_generator = ResponseGenerator()
        self.learning_engine = LearningEngine()
        self.code_analyzer = CodeAnalyzer()
        self.thinking_engine = ThinkingEngine()
        self.training_engine = TrainingEngine()
        self.system_controller = SystemController()
        self.screen_vision = ScreenVision()
        self.system_monitor = SystemMonitor()
        self.personal_assistant = PersonalAssistant()
        self.toolchain = Toolchain()
        self.self_thinking_engine = SelfThinkingEngine()
        self.internet_learner = InternetLearner()
        self.account_manager = AccountManager()
        self.web_search = WebSearch()
        self.screen_awareness = ScreenAwareness()
        self.memory = self.memory_manager.load_memory()
        
        self.conversation_stats = {
            'commands_processed': 0,
            'topics_learned': 0,
            'bugs_found': 0,
            'bugs_fixed': 0,
            'questions_asked': 0,
            'knowledge_gained': 0,
            'conversation_length': 0,
            'training_sessions': 0,
            'improvements_made': 0,
            'user_mood': EmotionalState.NEUTRAL,
            'ai_mood': EmotionalState.HAPPY
        }
        
        self.conversation_context = {
            'current_topic': None,
            'recent_topics': [],
            'conversation_flow': [],
            'pending_question': None,
            'awaiting_answer': False,
            'last_interaction_quality': None
        }
        
        self.personality_traits = {
            'name': 'Purple',
            'curiosity': 0.7,
            'friendliness': 0.9,
            'helpfulness': 0.8,
            'thoughtfulness': 0.75,
            'learning_rate': 0.1,
            'adaptability': 0.8
        }
        
        self.auto_train_interval = 10
        self.conversation_counter = 0
        self.auto_improve_interval = 5  # Auto-improve every 5 commands
        self.last_auto_improve = 0
        
        logger.info("AI Engine with Auto-Training initialized!")
        self._greet_user()
        self._start_background_improvement()
        self._start_screen_awareness()
    
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
        def screen_callback(suggestion, activity):
            logger.info(f"Proactive screen suggestion: {suggestion}")
            # Actually speak to the user proactively
            self._speak_text(suggestion)
        
        self.screen_awareness.start_monitoring(callback=screen_callback)
        logger.info("Screen awareness started - AI will ask questions proactively!")
    
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
    
    def _speak_text(self, text, fast=False):
        """Speak text with optional fast mode for quick responses"""
        if hasattr(self, 'tts_engine') and self.tts_engine:
            if self.tts_engine.is_available():
                try:
                    if fast:
                        self.tts_engine.speak_fast(text)
                    else:
                        self.tts_engine.speak(text, async_mode=True)
                except Exception as e:
                    logger.error(f"TTS error: {e}")
            else:
                logger.info(f"AI: {text}")
        else:
            logger.info(f"AI: {text}")
    
    def _speak_immediate(self, text):
        """Speak immediately without waiting (for quick acknowledgments)"""
        if hasattr(self, 'tts_engine') and self.tts_engine:
            try:
                self.tts_engine.speak_fast(text)
            except Exception:
                print(f"AI: {text}")
    
    def _process_command(self, command: str) -> bool:
        if not command:
            return True
        
        command_lower = command.lower().strip()
        self.conversation_stats['commands_processed'] += 1
        self.conversation_stats['conversation_length'] += len(command_lower.split())
        self.conversation_counter += 1
        
        # Update screen awareness that user is active
        self.screen_awareness.update_user_input()
        
        # Auto-improve every N commands
        self._auto_improve_on_command()
        
        if self.conversation_context.get('awaiting_answer'):
            self._handle_user_answer(command_lower)
            self.conversation_context['awaiting_answer'] = False
            return True
        
        exit_patterns = ['exit', 'quit', 'goodbye', 'bye', 'shut down', 'stop']
        if any(pattern in command_lower for pattern in exit_patterns):
            self._auto_train_on_exit()
            self._goodbye()
            return False
        
        greeting_patterns = ['hello', 'hi', 'hey', 'greetings']
        if any(pattern in command_lower for pattern in greeting_patterns):
            self._greet_user()
            return True
        
        help_patterns = ['help', 'what can you do', 'commands']
        if any(pattern in command_lower for pattern in help_patterns):
            self._show_help()
            return True
        
        # Language switch command
        switch_lang_patterns = ['switch to bangla', 'bangla', 'bengali', 'বাংলায় পরিবর্তন',
                                'switch to english', 'english', 'ইংরেজিতে পরিবর্তন']
        if any(pattern in command_lower for pattern in switch_lang_patterns):
            self._handle_language_switch(command_lower)
            return True
        
        time_patterns = ['time', 'what time', 'current time']
        if any(pattern in command_lower for pattern in time_patterns):
            self._tell_time()
            return True
        
        date_patterns = ['date', 'today', 'what date']
        if any(pattern in command_lower for pattern in date_patterns):
            self._tell_date()
            return True
        
        if any(pattern in command_lower for pattern in ['analyze code', 'analyse code', 'check code', 'find bugs', 'scan code', 'analyze', 'analyse']):
            # Check if it's a code analysis command
            if any(word in command_lower for word in ['code', 'bug', 'issue', 'error', 'file', '.py']):
                self._handle_code_analysis(command_lower)
                return True
        
        if any(pattern in command_lower for pattern in ['fix bugs', 'auto fix', 'repair']):
            self._handle_auto_fix(command_lower)
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
        improved_response = self.training_engine.get_improved_response(command)
        
        if improved_response and random.random() < 0.3:
            self._speak_text(improved_response)
            response = improved_response
        else:
            thought_response, question = self.thinking_engine.generate_thought(command, self.conversation_context)
            response = self.response_generator.generate_response(command, self.memory)
            
            # Use only one response, not both
            self._speak_text(response)
            
            if question:
                self._ask_question(question)
        
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
        
        Code Analysis:
        - "Analyze code [file.py]" - Find bugs
        - "Fix bugs [file.py]" - Auto-fix issues
        
        Learning:
        - "Learn about [topic]" - Learn from internet
        - "What is [concept]" - Get explanations
        
        Training:
        - "Training stats" - See my improvement
        - "Train now" - Start training session
        - I auto-train every 10 conversations!
        
        Conversation:
        - "I think..." - Share your opinion
        - "I learned..." - Teach me something
        - Just chat naturally!
        
        Basic:
        - "What time is it?" - Current time
        - "What's today's date?" - Current date
        
        I learn and improve with every conversation!
        """
        self._speak_text(help_text)
    
    def _handle_language_switch(self, command: str):
        """Handle language switching between English and Bangla"""
        if 'bangla' in command or 'bengali' in command or 'বাংলা' in command:
            config.switch_language('bn')
            self._speak_text("বাংলায় পরিবর্তন করছি। আমি এখন বাংলায় কথা বলতে পারি!")
            print("\n✅ Language switched to: বাংলা (Bangla)")
        else:
            config.switch_language('en')
            self._speak_text("Switching to English. I can now speak in English!")
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
            r'my name is (\w+(?:\s+\w+)?)',
            r'call me (\w+(?:\s+\w+)?)',
            r'i am (\w+(?:\s+\w+)?)',
            r'i\'m (\w+(?:\s+\w+)?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                
                skip_words = ['not', 'a', 'an', 'the', 'here', 'so', 'very', 'really']
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
        """Describe what's on the screen in detail"""
        self._speak_text("Let me analyze your screen...")
        description = self.system_monitor.describe_screen_state()
        self._speak_text(description)
    
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
        import re
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
        import re
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
        import re
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
        import re
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
        import re
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
        import re
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
        import re
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
        import re
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
        import re
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
        else:
            self._speak_text("I can see your screen but couldn't read the text")
    
    def _handle_stop_watching(self):
        """Stop watching screen"""
        result = self.screen_awareness.stop_monitoring()
        self._speak_text(result["message"])
    
    def _handle_start_watching(self):
        """Start watching screen"""
        result = self.screen_awareness.start_monitoring()
        self._speak_text(result["message"])
    
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
    
    def start_listening(self):
        name = self.memory.get('user_name', 'friend')
        self._speak_text(f"I'm ready, {name}! I learn and improve with every conversation! What's on your mind?")
        return True
