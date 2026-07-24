"""
Reliable Text-to-Speech Engine with Bangla Support
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
        self._initialize_tts()
    
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
    
    def _create_engine(self):
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
                engine.setProperty('rate', config.TTS_RATE)
                engine.setProperty('volume', config.TTS_VOLUME)
                return engine
        except Exception as e:
            logger.error(f"Failed to create engine: {e}")
        return None
    
    def _add_breathing(self, text):
        if not self._breathing_enabled:
            return text
        text = re.sub(r',\s+', ', ... ', text)
        text = re.sub(r'\.\s+', '. ... ', text)
        text = re.sub(r'[!?]\s+', '! ... ', text)
        words = text.split()
        if len(words) > 15:
            mid = len(words) // 2
            for i in range(mid, len(words)):
                if words[i].endswith(('.', '!', '?')):
                    words.insert(i + 1, '...')
                    break
            text = ' '.join(words)
        return text
    
    def _clean_text(self, text):
        text = re.sub(r'[✨💖🌟💫🎉😊😀🙌💪🤖💜]', '', text)
        text = re.sub(r'\*[^*]+\*', '', text)
        text = re.sub(r'\.{4,}', '...', text)
        return re.sub(r'\s+', ' ', text).strip()
    
    def _speak_in_thread(self, text, with_breathing=True):
        def worker():
            engine = None
            try:
                engine = self._create_engine()
                if engine:
                    cleaned = self._clean_text(text)
                    if with_breathing:
                        cleaned = self._add_breathing(cleaned)
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
        self._speak_in_thread(text, with_breathing=True)
    
    def speak_fast(self, text):
        while self._speaking:
            time.sleep(0.05)
        self._speak_in_thread(text, with_breathing=False)
    
    def speak_with_emotion(self, text, emotion='neutral'):
        while self._speaking:
            time.sleep(0.05)
        self._speak_in_thread(text, with_breathing=True)
    
    def stop(self):
        self._speaking = False
    
    def is_available(self):
        return True
    
    def get_voice_info(self):
        lang = config.CURRENT_LANGUAGE
        return {
            'language': lang,
            'voice_en': self._cached_voice_id_en,
            'voice_bn': self._cached_voice_id_bn
        }
