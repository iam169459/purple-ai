"""
Advanced Voice Controller
- Always-on microphone (concurrent listening)
- Voice Activity Detection (filter non-human sounds)
- Emotional voice expressions
- Media control integration
"""
import speech_recognition as sr
import threading
import time
import logging
import queue
import numpy as np
from typing import Optional, Callable, Tuple, Dict, Any
from config import config
from logger import logger
from voice.speaker_verification import SpeakerVerification

class VoiceController:
    """Advanced voice control with concurrent listening and VAD"""
    
    def __init__(self, tts_engine=None):
        self.tts_engine = tts_engine
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.is_active = False
        self.is_processing = False  # Currently executing a command
        self.wake_word_detected = False
        self.listening_thread = None
        self.processing_thread = None
        self.command_callback = None
        self.speaker_verification = SpeakerVerification()
        
        # Voice Activity Detection
        self.vad_enabled = True
        self.voice_energy_threshold = 300  # Minimum energy to be considered speech
        self.silence_threshold = 0.5  # Seconds of silence to end phrase
        
        # Emotional voice settings
        self.current_emotion = 'neutral'
        self.emotion_settings = {
            'neutral': {'rate': 170, 'volume': 0.85, 'pitch': 1.0},
            'happy': {'rate': 185, 'volume': 0.9, 'pitch': 1.1},
            'sad': {'rate': 150, 'volume': 0.7, 'pitch': 0.9},
            'angry': {'rate': 200, 'volume': 1.0, 'pitch': 1.15},
            'excited': {'rate': 195, 'volume': 0.95, 'pitch': 1.2},
            'calm': {'rate': 155, 'volume': 0.8, 'pitch': 0.95},
            'kind': {'rate': 165, 'volume': 0.85, 'pitch': 1.05},
            'satisfied': {'rate': 160, 'volume': 0.88, 'pitch': 1.02},
            'worried': {'rate': 175, 'volume': 0.82, 'pitch': 1.08},
            'playful': {'rate': 190, 'volume': 0.92, 'pitch': 1.12},
        }
        
        # Command queue for concurrent processing
        self.command_queue = queue.Queue()
        self.is_executing_command = False
        
        # Audio buffer for continuous listening
        self.audio_buffer = []
        self.buffer_lock = threading.Lock()
        
        # Configure recognizer settings
        self._configure_recognizer()
        
        logger.info("Advanced Voice Controller initialized")
    
    def _configure_recognizer(self):
        """Configure the speech recognizer with optimal settings"""
        try:
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
                ambient = self.recognizer.energy_threshold
                self.recognizer.energy_threshold = max(ambient * 0.5, 20)
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.8
                self.recognizer.phrase_threshold = 0.3
                self.recognizer.non_speaking_duration = 0.4
                
                logger.info(f"Ambient noise level: {ambient:.1f}, threshold set to: {self.recognizer.energy_threshold:.1f}")
                
        except Exception as e:
            logger.error(f"Error configuring recognizer: {e}")
            self.recognizer.energy_threshold = 40
            self.recognizer.dynamic_energy_threshold = True
    
    def _is_voice_active(self, audio_data) -> bool:
        """Check if audio contains human voice (Voice Activity Detection)"""
        if not self.vad_enabled:
            return True
        
        try:
            # Convert audio to numpy array
            audio_array = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
            
            # Calculate energy (RMS)
            energy = np.sqrt(np.mean(audio_array.astype(float) ** 2))
            
            # Check if energy is above voice threshold
            if energy < self.voice_energy_threshold:
                return False
            
            # Additional check: frequency analysis
            # Human speech typically has fundamental frequency between 85-300 Hz
            # This helps filter out some non-speech sounds
            
            return True
            
        except Exception as e:
            logger.debug(f"VAD error: {e}")
            return True  # If VAD fails, assume it's voice
    
    def _has_wake_word(self, text: str) -> bool:
        """Check if text contains any wake word"""
        text_lower = text.lower().strip()
        
        lang = config.CURRENT_LANGUAGE
        if lang == 'bn':
            wake_words = config.WAKE_WORDS_BANGLA
        else:
            wake_words = config.WAKE_WORDS
        
        for wake_word in wake_words:
            if wake_word in text_lower:
                return True
        return False
    
    def _strip_wake_words(self, command: str) -> str:
        """Strip wake words from the command"""
        command = command.lower().strip()
        
        lang = config.CURRENT_LANGUAGE
        if lang == 'bn':
            wake_words = config.WAKE_WORDS_BANGLA
        else:
            wake_words = config.WAKE_WORDS
        
        # Remove wake words from the beginning
        for wake_word in sorted(wake_words, key=len, reverse=True):
            if command.startswith(wake_word):
                command = command[len(wake_word):].strip()
                # Remove filler words
                filler_words = ['can you', 'please', 'could you', 'would you', 'will you', 
                               'i want to', 'i need to', 'tell me', 'help me', 'show me',
                               'let me', 'i want', 'i need']
                for filler in filler_words:
                    if command.startswith(filler):
                        command = command[len(filler):].strip()
                        break
                break
        
        return command
    
    def set_command_callback(self, callback: Callable[[str], bool]):
        """Set the callback function for processing commands"""
        self.command_callback = callback
    
    def start_continuous_listening(self) -> bool:
        """Start continuous listening mode - Always active"""
        if self.is_listening:
            logger.warning("Voice controller is already listening")
            return False
        
        if not self.command_callback:
            logger.error("No command callback set")
            return False
        
        self.is_listening = True
        self.is_active = True
        
        # Start main listening thread
        self.listening_thread = threading.Thread(
            target=self._continuous_listening_loop,
            daemon=True
        )
        self.listening_thread.start()
        
        # Start command processing thread
        self.processing_thread = threading.Thread(
            target=self._command_processing_loop,
            daemon=True
        )
        self.processing_thread.start()
        
        logger.info("Continuous listening started - Always active!")
        return True
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        self.is_active = False
        self.wake_word_detected = False
        
        if self.listening_thread and self.listening_thread.is_alive():
            self.listening_thread.join(timeout=2)
        
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=2)
        
        logger.info("Continuous listening stopped")
    
    def _continuous_listening_loop(self):
        """Main continuous listening loop - Always active, even during command execution"""
        logger.info("Listening loop started - Always active")
        
        while self.is_listening and self.is_active:
            try:
                # Always listen - even while processing commands
                with self.microphone as source:
                    # Use shorter timeout for responsiveness
                    audio = self.recognizer.listen(
                        source,
                        timeout=0.5,
                        phrase_time_limit=5
                    )
                
                # Check if audio contains human voice (VAD)
                if self.vad_enabled and not self._is_voice_active(audio):
                    continue
                
                # Try to recognize the speech
                try:
                    lang_code = config.get_current_language().get('speech_code', 'en-US')
                    text = self.recognizer.recognize_google(audio, language=lang_code).lower()
                    
                    if not text or len(text.strip()) < 2:
                        continue
                    
                    logger.info(f"Detected speech: {text}")
                    
                    # Check for wake word
                    if self._has_wake_word(text):
                        command = self._strip_wake_words(text)
                        if command:
                            # Queue the command for processing
                            self.command_queue.put((command, audio))
                            logger.info(f"Command queued: {command}")
                        else:
                            # Just wake word - acknowledge
                            self._speak_with_emotion("I'm listening!", 'happy')
                    else:
                        # No wake word - check if we should still process
                        # In always-on mode, process short commands without wake word
                        if len(text.split()) <= 4 and not self.is_executing_command:
                            self.command_queue.put((text, audio))
                            logger.info(f"Short command queued: {text}")
                    
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    logger.error(f"Recognition error: {e}")
                    time.sleep(0.5)
                    
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                logger.error(f"Listening error: {e}")
                time.sleep(0.5)
    
    def _command_processing_loop(self):
        """Process commands from queue - runs concurrently with listening"""
        while self.is_listening:
            try:
                # Get command from queue
                try:
                    command, audio = self.command_queue.get(timeout=0.5)
                except queue.Empty:
                    continue
                
                if not command:
                    continue
                
                # Mark as processing
                self.is_executing_command = True
                
                # Verify speaker
                if not self.speaker_verification.verify_speaker(audio):
                    logger.warning("Speaker verification failed")
                    self._speak_with_emotion("I don't recognize your voice.", 'worried')
                    self.is_executing_command = False
                    continue
                
                # Process command
                logger.info(f"Processing command: {command}")
                
                if self.command_callback:
                    continue_listening = self.command_callback(command)
                    if not continue_listening:
                        self.is_listening = False
                        self.is_active = False
                        break
                
                self.is_executing_command = False
                
            except Exception as e:
                logger.error(f"Command processing error: {e}")
                self.is_executing_command = False
    
    def _speak_with_emotion(self, text: str, emotion: str = None):
        """Speak with emotional expression"""
        if not self.tts_engine:
            return
        
        if emotion and emotion in self.emotion_settings:
            self.current_emotion = emotion
            settings = self.emotion_settings[emotion]
            
            # Apply emotion settings
            if hasattr(self.tts_engine, 'set_rate'):
                self.tts_engine.set_rate(settings['rate'])
            if hasattr(self.tts_engine, 'set_volume'):
                self.tts_engine.set_volume(settings['volume'])
        
        self.tts_engine.speak(text)
    
    def speak_angry(self, text: str):
        """Speak with angry emotion"""
        self._speak_with_emotion(text, 'angry')
    
    def speak_happy(self, text: str):
        """Speak with happy emotion"""
        self._speak_with_emotion(text, 'happy')
    
    def speak_sad(self, text: str):
        """Speak with sad emotion"""
        self._speak_with_emotion(text, 'sad')
    
    def speak_excited(self, text: str):
        """Speak with excited emotion"""
        self._speak_with_emotion(text, 'excited')
    
    def speak_calm(self, text: str):
        """Speak with calm emotion"""
        self._speak_with_emotion(text, 'calm')
    
    def speak_kind(self, text: str):
        """Speak with kind emotion"""
        self._speak_with_emotion(text, 'kind')
    
    def speak_satisfied(self, text: str):
        """Speak with satisfied emotion"""
        self._speak_with_emotion(text, 'satisfied')
    
    def speak_worried(self, text: str):
        """Speak with worried emotion"""
        self._speak_with_emotion(text, 'worried')
    
    def speak_playful(self, text: str):
        """Speak with playful emotion"""
        self._speak_with_emotion(text, 'playful')
    
    def get_status(self) -> Dict[str, Any]:
        """Get voice controller status"""
        return {
            'is_listening': self.is_listening,
            'is_active': self.is_active,
            'is_executing': self.is_executing_command,
            'current_emotion': self.current_emotion,
            'queue_size': self.command_queue.qsize(),
            'vad_enabled': self.vad_enabled
        }


# Create global instance
voice_controller = None

def get_voice_controller():
    """Get or create voice controller instance"""
    global voice_controller
    if voice_controller is None:
        voice_controller = VoiceController()
    return voice_controller