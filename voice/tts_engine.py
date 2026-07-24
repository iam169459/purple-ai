"""
Emotional Text-to-Speech Engine with Voice Variations
"""
import pyttsx3
import logging
import re
import time
import threading
from typing import Dict, Any
from config import config
from logger import logger

class TTSEngine:
    def __init__(self):
        self._cached_voice_id_en = None
        self._cached_voice_id_bn = None
        self._breathing_enabled = True
        self._speaking = False
        self._emotion_profiles = self._setup_emotion_profiles()
        self._initialize_tts()
    
    def _setup_emotion_profiles(self):
        """Setup voice profiles for different emotions"""
        return {
            'happy': {'rate': 160, 'pitch': 1.1, 'volume': 0.9, 'emphasis': '!'},
            'excited': {'rate': 180, 'pitch': 1.2, 'volume': 1.0, 'emphasis': '!!'},
            'sad': {'rate': 130, 'pitch': 0.85, 'volume': 0.7, 'emphasis': '...'},
            'angry': {'rate': 170, 'pitch': 1.15, 'volume': 0.95, 'emphasis': '!'},
            'worried': {'rate': 145, 'pitch': 1.05, 'volume': 0.75, 'emphasis': '?'},
            'confused': {'rate': 140, 'pitch': 0.95, 'volume': 0.8, 'emphasis': '?'},
            'tired': {'rate': 120, 'pitch': 0.8, 'volume': 0.65, 'emphasis': '...'},
            'proud': {'rate': 155, 'pitch': 1.1, 'volume': 0.9, 'emphasis': '!'},
            'love': {'rate': 135, 'pitch': 1.05, 'volume': 0.85, 'emphasis': ''},
            'sarcastic': {'rate': 150, 'pitch': 0.9, 'volume': 0.85, 'emphasis': '...'},
            'bored': {'rate': 125, 'pitch': 0.85, 'volume': 0.7, 'emphasis': '...'},
            'surprised': {'rate': 175, 'pitch': 1.25, 'volume': 0.95, 'emphasis': '!'},
            'grateful': {'rate': 145, 'pitch': 1.05, 'volume': 0.85, 'emphasis': ''},
            'motivated': {'rate': 170, 'pitch': 1.15, 'volume': 0.95, 'emphasis': '!'},
            'neutral': {'rate': 150, 'pitch': 1.0, 'volume': 0.85, 'emphasis': ''}
        }
    
    def _initialize_tts(self):
        try:
            logger.info("Initializing TTS engine...")
            engine = pyttsx3.init()
            if engine:
                voices = engine.getProperty('voices')
                if voices:
                    # Cache English voice
                    for pref in config.TTS_GIRL_VOICE_PREFERENCES:
                        for voice in voices:
                            if pref in voice.name.lower() or pref in voice.id.lower():
                                self._cached_voice_id_en = voice.id
                                logger.info(f"Cached English voice: {voice.name}")
                                break
                        if self._cached_voice_id_en:
                            break
                    if not self._cached_voice_id_en and voices:
                        self._cached_voice_id_en = voices[0].id
                    
                    # Cache Bangla voice
                    for pref in config.TTS_BANGLA_VOICE_PREFERENCES:
                        for voice in voices:
                            if pref in voice.name.lower() or pref in voice.id.lower():
                                self._cached_voice_id_bn = voice.id
                                logger.info(f"Cached Bangla voice: {voice.name}")
                                break
                        if self._cached_voice_id_bn:
                            break
                    if not self._cached_voice_id_bn:
                        self._cached_voice_id_bn = self._cached_voice_id_en
                del engine
                logger.info("TTS engine initialized successfully")
            else:
                logger.error("pyttsx3.init() returned None")
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
    
    def _create_engine(self, emotion='neutral'):
        try:
            engine = pyttsx3.init()
            if engine:
                # Get voice for current language
                lang = config.CURRENT_LANGUAGE
                if lang == 'bn':
                    voice_id = self._cached_voice_id_bn
                else:
                    voice_id = self._cached_voice_id_en
                
                if voice_id:
                    engine.setProperty('voice', voice_id)
                
                # Apply emotion-based settings
                profile = self._emotion_profiles.get(emotion, self._emotion_profiles['neutral'])
                engine.setProperty('rate', profile['rate'])
                engine.setProperty('volume', profile['volume'])
                
                return engine
        except Exception as e:
            logger.error(f"Failed to create engine: {e}")
        return None
    
    def _add_breathing(self, text, emotion='neutral'):
        if not self._breathing_enabled:
            return text
        
        profile = self._emotion_profiles.get(emotion, self._emotion_profiles['neutral'])
        emphasis = profile.get('emphasis', '')
        
        # Add emotional pauses
        if emotion == 'sad':
            text = re.sub(r',\s+', ', ... ', text)
            text = re.sub(r'\.\s+', '. ... ', text)
        elif emotion == 'excited':
            text = re.sub(r'!', '!!! ', text)
        elif emotion == 'worried':
            text = re.sub(r'\?\s+', '? ... ', text)
        elif emotion == 'confused':
            text = re.sub(r'\?\s+', '? ... ', text)
        elif emotion == 'tired':
            text = re.sub(r'\.\s+', '. ... ... ', text)
        elif emotion == 'sarcastic':
            text = re.sub(r'\.\s+', '. ... ... ', text)
        else:
            text = re.sub(r',\s+', ', ... ', text)
            text = re.sub(r'\.\s+', '. ... ', text)
            text = re.sub(r'[!?]\s+', f'{emphasis} ... ', text)
        
        return text
    
    def _clean_text(self, text):
        text = re.sub(r'[✨💖🌟💫🎉😊😀🙌💪🤖💜😊😢🤩🤔💪😏😂😕😠😴🏆😨😍🙏🤯]', '', text)
        text = re.sub(r'\*[^*]+\*', '', text)
        text = re.sub(r'\.{4,}', '...', text)
        return re.sub(r'\s+', ' ', text).strip()
    
    def _add_emotional_prefix(self, text, emotion):
        """Add emotional expression to speech"""
        prefixes = {
            'happy': ['Aha!', 'Oh!', 'Wow!'],
            'excited': ['WHOA!', 'YESSS!', 'AMAZING!'],
            'sad': ['*sigh*', 'Oh...', 'Aww...'],
            'angry': ['*grumble*', 'Ugh!', 'Hmph!'],
            'worried': ['Oh no...', 'Hmm...', 'Wait...'],
            'confused': ['Hmm?', 'Wait...', 'What?'],
            'tired': ['*yawn*', 'Oh...', 'Ugh...'],
            'proud': ['YES!', 'Ha!', 'Look at you!'],
            'love': ['Aww...', 'Oh my...', 'Sweet...'],
            'sarcastic': ['Oh really?', 'Wow...', 'Imagine that...'],
            'bored': ['*yawn*', 'Ugh...', 'Meh...'],
            'surprised': ['WHOA!', 'No way!', 'OMG!'],
            'grateful': ['Aww...', 'Thank you...', 'That means...'],
            'motivated': ['YES!', 'LET\'S GO!', 'COME ON!'],
            'neutral': []
        }
        
        import random
        prefix_list = prefixes.get(emotion, [])
        if prefix_list and random.random() < 0.3:  # 30% chance to add prefix
            prefix = random.choice(prefix_list)
            text = f"{prefix} {text}"
        
        return text
    
    def _speak_in_thread(self, text, with_breathing=True, emotion='neutral'):
        def worker():
            engine = None
            try:
                engine = self._create_engine(emotion)
                if engine:
                    cleaned = self._clean_text(text)
                    
                    # Add emotional prefix
                    cleaned = self._add_emotional_prefix(cleaned, emotion)
                    
                    if with_breathing:
                        cleaned = self._add_breathing(cleaned, emotion)
                    
                    engine.say(cleaned)
                    engine.runAndWait()
                else:
                    logger.info(f"AI: {text}")
            except Exception as e:
                logger.error(f"Speech error: {e}")
                logger.info(f"AI: {text}")
            finally:
                if engine:
                    try:
                        del engine
                    except Exception:
                        pass
                self._speaking = False
        
        self._speaking = True
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def speak(self, text, async_mode=True):
        while self._speaking:
            time.sleep(0.05)
        self._speak_in_thread(text, with_breathing=True, emotion='neutral')
    
    def speak_fast(self, text):
        while self._speaking:
            time.sleep(0.05)
        self._speak_in_thread(text, with_breathing=False, emotion='neutral')
    
    def speak_with_emotion(self, text, emotion='neutral'):
        while self._speaking:
            time.sleep(0.05)
        self._speak_in_thread(text, with_breathing=True, emotion=emotion)
    
    def stop(self):
        self._speaking = False
    
    def is_available(self):
        return True
    
    def get_voice_info(self):
        lang = config.CURRENT_LANGUAGE
        return {
            'language': lang,
            'voice_en': self._cached_voice_id_en,
            'voice_bn': self._cached_voice_id_bn,
            'emotions': list(self._emotion_profiles.keys())
        }
