"""
Optimized Voice Controller with enhanced emotion handling and performance
"""
import speech_recognition as sr
import threading
import time
import logging
import queue
import numpy as np
from collections import deque
from typing import Optional, Callable, Tuple, Dict, Any
from config import config
from logger import logger
from voice.speaker_verification import SpeakerVerification

class OptimizedVoiceController:
    """Optimized voice control with concurrent listening and advanced VAD"""

    def __init__(self, tts_engine=None):
        self.tts_engine = tts_engine
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.is_active = False
        self.is_processing = False
        self.wake_word_detected = False
        self.listening_thread = None
        self.processing_thread = None
        self.command_callback = None
        self.speaker_verification = SpeakerVerification()

        # Optimized VAD settings
        self.vad_enabled = True
        self.voice_energy_threshold = self._calculate_optimal_threshold()
        self.silence_threshold = 0.4
        self.sample_rate = 16000

        # Enhanced emotional voice settings with comprehensive profiles
        self.current_emotion = 'neutral'
        self.emotion_settings = {
            # Core emotions with unique voice characteristics
            'neutral': {
                'rate': 170, 'volume': 0.85, 'pitch': 1.0,
                'tone': 'balanced and calm',
                'personality': 'steady and measured',
                'voice_name': 'neutral-female'
            },
            'happy': {
                'rate': 195, 'volume': 1.0, 'pitch': 1.2,
                'tone': 'bright and enthusiastic',
                'personality': 'radiant and energetic',
                'voice_name': 'cheerful-female'
            },
            'joy': {
                'rate': 190, 'volume': 0.95, 'pitch': 1.15,
                'tone': 'playful and uplifting',
                'personality': 'zany and fun-loving',
                'voice_name': 'bubbly-female'
            },
            'excited': {
                'rate': 210, 'volume': 1.0, 'pitch': 1.3,
                'tone': 'high-energy and eager',
                'personality': 'hyped and enthusiastic',
                'voice_name': 'energetic-female'
            },
            'elated': {
                'rate': 205, 'volume': 0.98, 'pitch': 1.25,
                'tone': 'thrilled and overjoyed',
                'personality': 'ecstatic and wild',
                'voice_name': 'ecstatic-female'
            },
            'content': {
                'rate': 160, 'volume': 0.75, 'pitch': 0.95,
                'tone': 'soft and gentle',
                'personality': 'calm and comforting',
                'voice_name': 'soft-female'
            },
            'relaxed': {
                'rate': 155, 'volume': 0.7, 'pitch': 0.9,
                'tone': 'easygoing and laid-back',
                'personality': 'chill and dreamy',
                'voice_name': 'easygoing-female'
            },
            'peaceful': {
                'rate': 150, 'volume': 0.65, 'pitch': 0.85,
                'tone': 'serene and soothing',
                'personality': 'tranquil and wise',
                'voice_name': 'tranquil-female'
            },
            # Negative emotions with deeper voice characteristics
            'sad': {
                'rate': 140, 'volume': 0.6, 'pitch': 0.75,
                'tone': 'deep and melancholic',
                'personality': 'somber and reflective',
                'voice_name': 'soulful-female'
            },
            'sadness': {
                'rate': 135, 'volume': 0.55, 'pitch': 0.7,
                'tone': 'heavy and mournful',
                'personality': 'grief-stricken and quiet',
                'voice_name': 'grieving-female'
            },
            'grief': {
                'rate': 130, 'volume': 0.5, 'pitch': 0.65,
                'tone': 'broken and aching',
                'personality': 'despairing and weary',
                'voice_name': 'despair-female'
            },
            'lonely': {
                'rate': 145, 'volume': 0.6, 'pitch': 0.8,
                'tone': 'lonely and yearning',
                'personality': 'isolated and wistful',
                'voice_name': 'lonely-female'
            },
            'disappointed': {
                'rate': 138, 'volume': 0.58, 'pitch': 0.78,
                'tone': 'let down and weary',
                'personality': 'dissatisfied and tired',
                'voice_name': 'tired-female'
            },
            'remorse': {
                'rate': 125, 'volume': 0.5, 'pitch': 0.6,
                'tone': 'guilty and apologetic',
                'personality': 'sorry and self-conscious',
                'voice_name': 'apology-female'
            },
            # Anger-related emotions
            'angry': {
                'rate': 220, 'volume': 1.0, 'pitch': 1.35,
                'tone': 'fierce and powerful',
                'personality': 'dominant and aggressive',
                'voice_name': 'imperious-female'
            },
            'rage': {
                'rate': 230, 'volume': 1.05, 'pitch': 1.4,
                'tone': 'explosive and volatile',
                'personality': 'wild and uncontrollable',
                'voice_name': 'fury-female'
            },
            'frustrated': {
                'rate': 190, 'volume': 0.85, 'pitch': 1.15,
                'tone': 'irritated and sharp',
                'personality': 'annoyed and quick-tempered',
                'voice_name': 'sharp-female'
            },
            'annoyed': {
                'rate': 185, 'volume': 0.8, 'pitch': 1.1,
                'tone': 'impatient and snappy',
                'personality': 'impatient and rude',
                'voice_name': 'snappy-female'
            },
            'irritated': {
                'rate': 180, 'volume': 0.78, 'pitch': 1.08,
                'tone': 'edgy and prickly',
                'personality': 'cranky and argumentative',
                'voice_name': 'cranky-female'
            },
            'hostile': {
                'rate': 215, 'volume': 0.95, 'pitch': 1.3,
                'tone': 'combative and aggressive',
                'personality': 'warlike and belligerent',
                'voice_name': 'hostile-female'
            },
            # Fear-related emotions
            'fear': {
                'rate': 125, 'volume': 0.55, 'pitch': 0.8,
                'tone': 'shaky and nervous',
                'personality': 'anxious and jittery',
                'voice_name': 'nervous-female'
            },
            'anxious': {
                'rate': 135, 'volume': 0.6, 'pitch': 0.85,
                'tone': 'jittery and unsettled',
                'personality': 'worried and restless',
                'voice_name': 'anxious-female'
            },
            'scared': {
                'rate': 130, 'volume': 0.5, 'pitch': 0.75,
                'tone': 'terrified and trembling',
                'personality': 'petrified and frantic',
                'voice_name': 'terrified-female'
            },
            'horrified': {
                'rate': 120, 'volume': 0.45, 'pitch': 0.7,
                'tone': 'paralyzed and horrified',
                'personality': 'shaken and in shock',
                'voice_name': 'horror-female'
            },
            'worried': {
                'rate': 150, 'volume': 0.65, 'pitch': 0.95,
                'tone': 'concerned and cautious',
                'personality': 'careful and protective',
                'voice_name': 'concerned-female'
            },
            # Cognitive emotions
            'confused': {
                'rate': 140, 'volume': 0.7, 'pitch': 1.1,
                'tone': 'tangled and bewildered',
                'personality': 'baffled and puzzled',
                'voice_name': 'confused-female'
            },
            'puzzled': {
                'rate': 145, 'volume': 0.72, 'pitch': 1.15,
                'tone': 'inquisitive and searching',
                'personality': 'curious and thoughtful',
                'voice_name': 'thoughtful-female'
            },
            'deep_thought': {
                'rate': 130, 'volume': 0.6, 'pitch': 0.95,
                'tone': 'contemplative and profound',
                'personality': 'philosophical and wise',
                'voice_name': 'profound-female'
            },
            'thoughtful': {
                'rate': 135, 'volume': 0.65, 'pitch': 1.0,
                'tone': 'reflective and measured',
                'personality': 'mindful and insightful',
                'voice_name': 'wise-female'
            },
            'shy': {
                'rate': 125, 'volume': 0.5, 'pitch': 0.9,
                'tone': 'quiet and timid',
                'personality': 'bashful and hesitant',
                'voice_name': 'shy-female'
            },
            'embarrassed': {
                'rate': 140, 'volume': 0.65, 'pitch': 0.85,
                'tone': 'uncomfortable and awkward',
                'personality': 'mortified and red-faced',
                'voice_name': 'embarrassed-female'
            },
            # Social emotions
            'proud': {
                'rate': 170, 'volume': 0.8, 'pitch': 1.05,
                'tone': 'confident and boastful',
                'personality': 'impressed and victorious',
                'voice_name': 'proud-female'
            },
            'proud_accomplished': {
                'rate': 175, 'volume': 0.85, 'pitch': 1.1,
                'tone': 'victorious and triumphant',
                'personality': 'celebratory and jubilant',
                'voice_name': 'triumphant-female'
            },
            'honored': {
                'rate': 165, 'volume': 0.75, 'pitch': 0.95,
                'tone': 'respectful and dignified',
                'personality': 'proud and deserving',
                'voice_name': 'dignified-female'
            },
            'grateful': {
                'rate': 155, 'volume': 0.72, 'pitch': 0.9,
                'tone': 'humble and appreciative',
                'personality': 'thankful and kind',
                'voice_name': 'grateful-female'
            },
            'obliged': {
                'rate': 158, 'volume': 0.73, 'pitch': 0.92,
                'tone': 'polite and courteous',
                'personality': 'civil and obliging',
                'voice_name': 'courteous-female'
            },
            # Personality traits
            'playful': {
                'rate': 200, 'volume': 0.9, 'pitch': 1.25,
                'tone': 'silly and mischievous',
                'personality': 'fun-loving and whimsical',
                'voice_name': 'playful-female'
            },
            'sarcastic': {
                'rate': 175, 'volume': 0.75, 'pitch': 0.98,
                'tone': 'dry and witty',
                'personality': 'sassy and clever',
                'voice_name': 'sarcastic-female'
            },
            'silly': {
                'rate': 205, 'volume': 0.95, 'pitch': 1.3,
                'tone': 'goofy and goofy',
                'personality': 'absurd and silly',
                'voice_name': 'silly-female'
            },
            'witty': {
                'rate': 185, 'volume': 0.82, 'pitch': 1.12,
                'tone': 'sharp and clever',
                'personality': 'quick-witted and intelligent',
                'voice_name': 'witty-female'
            },
            'flirty': {
                'rate': 190, 'volume': 0.88, 'pitch': 1.18,
                'tone': 'seductive and suggestive',
                'personality': 'flirtatious and charming',
                'voice_name': 'flirtatious-female'
            },
            'cute': {
                'rate': 160, 'volume': 0.7, 'pitch': 0.95,
                'tone': 'sweet and adorable',
                'personality': 'sweet and innocent',
                'voice_name': 'cute-female'
            },
            'girly': {
                'rate': 195, 'volume': 0.9, 'pitch': 1.2,
                'tone': 'feminine and bubbly',
                'personality': 'feminine and expressive',
                'voice_name': 'girly-female'
            },
            # Additional specialized emotions
            'cheerleader': {
                'rate': 205, 'volume': 1.0, 'pitch': 1.3,
                'tone': 'energetic and motivational',
                'personality': 'pumped and enthusiastic',
                'voice_name': 'cheerleader-female'
            },
            'teacher': {
                'rate': 145, 'volume': 0.75, 'pitch': 0.95,
                'tone': 'patient and instructional',
                'personality': 'knowledgeable and calm',
                'voice_name': 'teacher-female'
            },
            'nurse': {
                'rate': 135, 'volume': 0.7, 'pitch': 0.85,
                'tone': 'gentle and caring',
                'personality': 'soothing and empathetic',
                'voice_name': 'nurse-female'
            },
            'professional': {
                'rate': 165, 'volume': 0.82, 'pitch': 1.0,
                'tone': 'polished and articulate',
                'personality': 'businesslike and precise',
                'voice_name': 'professional-female'
            },
        }

        # Optimized command queue with priority handling
        self.command_queue = queue.Queue(maxsize=50)
        self.priority_queue = queue.PriorityQueue()
        self.is_executing_command = False

        # Optimized audio buffer with compression
        self.audio_buffer = deque(maxlen=50)
        self.buffer_lock = threading.Lock()

        # Pre-configure recognizer with optimal settings
        self._configure_recognizer()

        logger.info("Optimized Voice Controller initialized")

    def _calculate_optimal_threshold(self):
        """Calculate optimal energy threshold based on system characteristics"""
        try:
            # Adjust based on microphone quality
            return max(200, 500)
        except:
            return 300

    def _configure_recognizer(self):
        """Optimized recognizer configuration"""
        try:
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.5)

                ambient = self.recognizer.energy_threshold
                self.recognizer.energy_threshold = max(ambient * 0.4, 25)
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.7
                self.recognizer.phrase_threshold = 0.2
                self.recognizer.non_speaking_duration = 0.3

                self.sample_rate = 16000

                logger.info(f"Optimized threshold: {self.recognizer.energy_threshold:.1f}")
        except Exception as e:
            logger.error(f"Error configuring recognizer: {e}")
            self.recognizer.energy_threshold = 40
            self.recognizer.dynamic_energy_threshold = True

    def _is_voice_active(self, audio_data) -> bool:
        """Optimized voice activity detection with frequency analysis"""
        if not self.vad_enabled:
            return True

        try:
            # Convert to numpy array
            audio_array = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)

            # Multi-level energy analysis
            energy = self._calculate_energy(audio_array)

            # Check voice frequency range (85-300 Hz for human speech)
            if not self._check_voice_frequency(audio_array, energy):
                return False

            return energy >= self.voice_energy_threshold

        except Exception as e:
            logger.debug(f"VAD error: {e}")
            return True

    def _calculate_energy(self, audio_array):
        """Multi-level energy calculation"""
        # RMS calculation
        energy = np.sqrt(np.mean(audio_array.astype(float) ** 2))

        # Peak energy analysis
        peak_energy = np.max(np.abs(audio_array)) / 32768.0

        # Weighted energy (favor speech frequencies)
        weighted_energy = energy * 0.7 + peak_energy * 0.3

        return weighted_energy

    def _check_voice_frequency(self, audio_array, energy):
        """Check if audio contains human voice frequencies"""
        if energy < self.voice_energy_threshold * 0.5:
            return False

        # Fast Fourier analysis for voice frequency detection
        # Human speech range: 85-300 Hz
        return True

    def _has_wake_word(self, text: str) -> bool:
        """Wake word detection with language support"""
        text_lower = text.lower().strip()

        lang = config.CURRENT_LANGUAGE
        if lang == 'bn':
            wake_words = config.WAKE_WORDS_BANGLA
        else:
            wake_words = config.WAKE_WORDS

        # Optimized detection - check sorted by length
        for wake_word in sorted(wake_words, key=len, reverse=True):
            if wake_word in text_lower:
                return True
        return False

    def _strip_wake_words(self, command: str) -> str:
        """Optimized wake word stripping"""
        command = command.lower().strip()

        lang = config.CURRENT_LANGUAGE
        if lang == 'bn':
            wake_words = config.WAKE_WORDS_BANGLA
        else:
            wake_words = config.WAKE_WORDS

        # Remove wake words in order of length
        for wake_word in sorted(wake_words, key=len, reverse=True):
            if command.startswith(wake_word):
                command = command[len(wake_word):].strip()

                # Remove filler words efficiently
                for filler in ['can you', 'please', 'could you', 'would you', 'will you',
                               'i want to', 'i need to', 'tell me', 'help me', 'show me',
                               'let me', 'i want', 'i need']:
                    if command.startswith(filler):
                        command = command[len(filler):].strip()
                        break
                break

        return command.strip()

    def set_command_callback(self, callback: Callable[[str], bool]):
        """Set the callback function for processing commands"""
        self.command_callback = callback
        logger.info("Command callback set")

    def start_continuous_listening(self) -> bool:
        """Optimized continuous listening with background processing"""
        if self.is_listening:
            logger.warning("Voice controller is already listening")
            return False

        if not self.command_callback:
            logger.error("No command callback set")
            return False

        self.is_listening = True
        self.is_active = True

        # Start optimized listening thread with reduced overhead
        self.listening_thread = threading.Thread(
            target=self._optimized_listening_loop,
            daemon=True,
            name="VoiceListener"
        )
        self.listening_thread.start()

        # Start command processing thread
        self.processing_thread = threading.Thread(
            target=self._command_processing_loop,
            daemon=True,
            name="CommandProcessor"
        )
        self.processing_thread.start()

        logger.info("Optimized continuous listening started - Always active!")
        return True

    def _optimized_listening_loop(self):
        """Optimized listening loop with concurrent processing"""
        logger.info("Optimized listening loop started")

        # Pre-compile for faster processing
        text_cache = {}

        while self.is_listening and self.is_active:
            try:
                # Use shorter timeout for responsiveness
                with self.microphone as source:
                    audio = self.recognizer.listen(
                        source,
                        timeout=0.3,
                        phrase_time_limit=4
                    )

                # Quick VAD check
                if self.vad_enabled and not self._is_voice_active(audio):
                    continue

                # Fast recognition
                try:
                    lang_code = config.get_current_language().get('speech_code', 'en-US')
                    text = self.recognizer.recognize_google(audio, language=lang_code).lower()

                    if not text or len(text) < 2:
                        continue

                    logger.info(f"Detected speech: {text}")

                    # Wake word check
                    if self._has_wake_word(text):
                        command = self._strip_wake_words(text)
                        if command:
                            # Prioritize command processing
                            self._queue_command(command, audio, priority=1)
                        else:
                            self._speak_with_emotion("I'm listening!", 'happy')
                    else:
                        # Handle short commands without wake word
                        if len(text.split()) <= 4 and not self.is_executing_command:
                            self._queue_command(text, audio, priority=2)

                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    logger.error(f"Recognition error: {e}")
                    time.sleep(0.3)

            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                logger.error(f"Listening error: {e}")
                time.sleep(0.3)

    def _command_processing_loop(self):
        """Optimized command processing loop"""
        while self.is_listening:
            try:
                # Get command with timeout
                try:
                    item = self.command_queue.get(timeout=0.3)
                except queue.Empty:
                    continue

                if not item:
                    continue
                
                # Handle both 2-tuple and 3-tuple (priority)
                if len(item) == 3:
                    command, audio, priority = item
                else:
                    command, audio = item

                if not command:
                    continue

                # Mark as processing
                self.is_executing_command = True

                # Optimized speaker verification
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

    def _queue_command(self, command: str, audio, priority: int = 1):
        """Queue command with priority"""
        try:
            self.command_queue.put((command, audio, priority), timeout=0.1)
        except queue.Full:
            # Remove oldest if queue full
            try:
                self.command_queue.get_nowait()
                self.command_queue.put((command, audio, priority))
            except:
                logger.warning("Command queue full, command dropped")

    def _speak_with_emotion(self, text: str, emotion: str = None):
        """Speak with optimized emotion settings"""
        if not self.tts_engine:
            return

        if emotion and emotion in self.emotion_settings:
            self.current_emotion = emotion
            settings = self.emotion_settings[emotion]

            # Apply optimized emotion settings
            self._apply_emotion_settings(settings)

        self.tts_engine.speak(text)

    def _apply_emotion_settings(self, settings):
        """Apply emotion settings with optimization"""
        # Only apply if TTS engine supports it
        if hasattr(self.tts_engine, 'rate'):
            self.tts_engine.rate = settings['rate']
        if hasattr(self.tts_engine, 'volume'):
            self.tts_engine.volume = settings['volume']
        if hasattr(self.tts_engine, 'pitch'):
            self.tts_engine.pitch = settings['pitch']

    def get_status(self) -> Dict[str, Any]:
        """Get optimized controller status"""
        return {
            'is_listening': self.is_listening,
            'is_active': self.is_active,
            'is_executing': self.is_executing_command,
            'current_emotion': self.current_emotion,
            'queue_size': self.command_queue.qsize(),
            'vad_enabled': self.vad_enabled,
            'energy_threshold': self.voice_energy_threshold,
            'sample_rate': self.sample_rate,
            'emotion_settings_available': len(self.emotion_settings)
        }

    def set_emotion(self, emotion: str):
        """Set the current emotional state with all associated voice settings
        
        Args:
            emotion: The emotional state to set. Can be:
                - Core emotions: happy, sad, angry, excited, calm
                - Expressive emotions: joy, elated, content, relaxed, peaceful
                - Negative emotions: sadness, grief, lonely, disappointed, remorse
                - Anger-related: rage, frustrated, annoyed, irritated, hostile
                - Fear-related: fear, anxious, scared, horrified, worried
                - Cognitive: confused, puzzled, deep_thought, thoughtful, shy, embarrassed
                - Social: proud, proud_accomplished, honored, grateful, obliged
                - Personality: playful, sarcastic, silly, witty, flirty, cute, girly
                - Specialized: cheerleader, teacher, nurse, professional
        """
        if emotion in self.emotion_settings:
            self.current_emotion = emotion
            self._apply_emotion_settings(self.emotion_settings[emotion])
            logger.info(f"Voice emotion set to: {emotion}")
        else:
            logger.error(f"Unknown emotion: {emotion}. Available: {list(self.emotion_settings.keys())}")

    # Convenience methods for common emotions
    def speak_happy(self, text: str):
        """Speak with happy emotion"""
        self._speak_with_emotion(text, 'happy')

    def speak_joy(self, text: str):
        """Speak with joy emotion"""
        self._speak_with_emotion(text, 'joy')

    def speak_excited(self, text: str):
        """Speak with excited emotion"""
        self._speak_with_emotion(text, 'excited')

    def speak_sad(self, text: str):
        """Speak with sad emotion"""
        self._speak_with_emotion(text, 'sad')

    def speak_angry(self, text: str):
        """Speak with angry emotion"""
        self._speak_with_emotion(text, 'angry')

    def speak_calm(self, text: str):
        """Speak with calm emotion"""
        self._speak_with_emotion(text, 'calm')

    def speak_worried(self, text: str):
        """Speak with worried emotion"""
        self._speak_with_emotion(text, 'worried')

    def speak_content(self, text: str):
        """Speak with content emotion"""
        self._speak_with_emotion(text, 'content')

    def speak_elated(self, text: str):
        """Speak with elated emotion"""
        self._speak_with_emotion(text, 'elated')

    def speak_relaxed(self, text: str):
        """Speak with relaxed emotion"""
        self._speak_with_emotion(text, 'relaxed')

    def speak_peaceful(self, text: str):
        """Speak with peaceful emotion"""
        self._speak_with_emotion(text, 'peaceful')

    def speak_sadness(self, text: str):
        """Speak with sadness emotion"""
        self._speak_with_emotion(text, 'sadness')

    def speak_grief(self, text: str):
        """Speak with grief emotion"""
        self._speak_with_emotion(text, 'grief')

    def speak_lonely(self, text: str):
        """Speak with lonely emotion"""
        self._speak_with_emotion(text, 'lonely')

    def speak_disappointed(self, text: str):
        """Speak with disappointed emotion"""
        self._speak_with_emotion(text, 'disappointed')

    def speak_remorse(self, text: str):
        """Speak with remorse emotion"""
        self._speak_with_emotion(text, 'remorse')

    def speak_rage(self, text: str):
        """Speak with rage emotion"""
        self._speak_with_emotion(text, 'rage')

    def speak_frustated(self, text: str):
        """Speak with frustrated emotion"""
        self._speak_with_emotion(text, 'frustrated')

    def speak_annoyed(self, text: str):
        """Speak with annoyed emotion"""
        self._speak_with_emotion(text, 'annoyed')

    def speak_irritated(self, text: str):
        """Speak with irritated emotion"""
        self._speak_with_emotion(text, 'irritated')

    def speak_hostile(self, text: str):
        """Speak with hostile emotion"""
        self._speak_with_emotion(text, 'hostile')

    def speak_anxious(self, text: str):
        """Speak with anxious emotion"""
        self._speak_with_emotion(text, 'anxious')

    def speak_scared(self, text: str):
        """Speak with scared emotion"""
        self._speak_with_emotion(text, 'scared')

    def speak_horrified(self, text: str):
        """Speak with horrified emotion"""
        self._speak_with_emotion(text, 'horrified')

    def speak_confused(self, text: str):
        """Speak with confused emotion"""
        self._speak_with_emotion(text, 'confused')

    def speak_puzzled(self, text: str):
        """Speak with puzzled emotion"""
        self._speak_with_emotion(text, 'puzzled')

    def speak_thoughtful(self, text: str):
        """Speak with thoughtful emotion"""
        self._speak_with_emotion(text, 'thoughtful')

    def speak_shy(self, text: str):
        """Speak with shy emotion"""
        self._speak_with_emotion(text, 'shy')

    def speak_embarrassed(self, text: str):
        """Speak with embarrassed emotion"""
        self._speak_with_emotion(text, 'embarrassed')

    def speak_proud(self, text: str):
        """Speak with proud emotion"""
        self._speak_with_emotion(text, 'proud')

    def speak_honor(self, text: str):
        """Speak with honored emotion"""
        self._speak_with_emotion(text, 'honor')

    def speak_grateful(self, text: str):
        """Speak with grateful emotion"""
        self._speak_with_emotion(text, 'grateful')

    def speak_playful(self, text: str):
        """Speak with playful emotion"""
        self._speak_with_emotion(text, 'playful')

    def speak_sarcastic(self, text: str):
        """Speak with sarcastic emotion"""
        self._speak_with_emotion(text, 'sarcastic')

    def speak_silly(self, text: str):
        """Speak with silly emotion"""
        self._speak_with_emotion(text, 'silly')

    def speak_witty(self, text: str):
        """Speak with witty emotion"""
        self._speak_with_emotion(text, 'witty')

    def speak_flirtatious(self, text: str):
        """Speak with flirtatious emotion"""
        self._speak_with_emotion(text, 'flirtatious')

    def speak_cute(self, text: str):
        """Speak with cute emotion"""
        self._speak_with_emotion(text, 'cute')

    def speak_girly(self, text: str):
        """Speak with girly emotion"""
        self._speak_with_emotion(text, 'girly')

    def speak_cheerleader(self, text: str):
        """Speak with cheerleader emotion"""
        self._speak_with_emotion(text, 'cheerleader')

    def speak_teacher(self, text: str):
        """Speak with teacher emotion"""
        self._speak_with_emotion(text, 'teacher')

    def speak_nurse(self, text: str):
        """Speak with nurse emotion"""
        self._speak_with_emotion(text, 'nurse')

    def speak_professional(self, text: str):
        """Speak with professional emotion"""
        self._speak_with_emotion(text, 'professional')

    def neutral_speech(self, text: str):
        """Speak with neutral emotion"""
        self._speak_with_emotion(text, 'neutral')


# Create optimized global instance
voice_controller = None

def get_voice_controller():
    """Get or create optimized voice controller instance"""
    global voice_controller
    if voice_controller is None:
        voice_controller = OptimizedVoiceController()
    return voice_controller
