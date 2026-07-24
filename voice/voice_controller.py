"""
Voice Controller
Handles speech recognition, wake word detection, and voice command processing
"""
import speech_recognition as sr
import threading
import time
import logging
from typing import Optional, Callable, Tuple
from config import config
from logger import logger
from voice.speaker_verification import SpeakerVerification

class VoiceController:
    """Advanced voice control system for continuous listening and wake word detection"""
    
    def __init__(self, tts_engine=None):
        self.tts_engine = tts_engine
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.is_active = False
        self.wake_word_detected = False
        self.listening_thread = None
        self.command_callback = None
        self.speaker_verification = SpeakerVerification()
        
        # Configure recognizer settings
        self._configure_recognizer()
        
        logger.info("Voice Controller initialized")
    
    def _strip_wake_words(self, command: str) -> str:
        """Strip wake words from the command"""
        command = command.lower().strip()
        
        # Get current language wake words
        lang = config.CURRENT_LANGUAGE
        if lang == 'bn':
            wake_words = config.WAKE_WORDS_BANGLA
        else:
            wake_words = config.WAKE_WORDS
        
        # Remove wake words from the beginning of the command
        for wake_word in sorted(wake_words, key=len, reverse=True):
            if command.startswith(wake_word):
                command = command[len(wake_word):].strip()
                # Remove common filler words after wake word
                filler_words = ['can you', 'please', 'could you', 'would you', 'will you', 'i want to', 'i need to']
                for filler in filler_words:
                    if command.startswith(filler):
                        command = command[len(filler):].strip()
                        break
                break
        
        return command
    
    def _configure_recognizer(self):
        """Configure the speech recognizer with optimal settings"""
        try:
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(
                    source, 
                    duration=3
                )
                
                ambient = self.recognizer.energy_threshold
                self.recognizer.energy_threshold = max(ambient * 0.6, 25)
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 1.2
                self.recognizer.phrase_threshold = 0.3
                self.recognizer.non_speaking_duration = 0.5
                
                logger.info(f"Ambient noise level: {ambient:.1f}, threshold set to: {self.recognizer.energy_threshold:.1f}")
                logger.info("Voice recognizer configured with high sensitivity")
                
        except Exception as e:
            logger.error(f"Error configuring recognizer: {e}")
            self.recognizer.energy_threshold = 50
            self.recognizer.dynamic_energy_threshold = True
    
    def set_command_callback(self, callback: Callable[[str], bool]):
        """Set the callback function for processing commands"""
        self.command_callback = callback
    
    def start_continuous_listening(self) -> bool:
        """Start continuous listening mode"""
        if self.is_listening:
            logger.warning("Voice controller is already listening")
            return False
        
        if not self.command_callback:
            logger.error("No command callback set")
            return False
        
        self.is_listening = True
        self.is_active = True
        
        # Start listening in a separate thread
        self.listening_thread = threading.Thread(
            target=self._continuous_listening_loop,
            daemon=True
        )
        self.listening_thread.start()
        
        logger.info("Continuous listening started")
        self._speak("I'm now listening for your voice commands!")
        return True
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        self.is_active = False
        self.wake_word_detected = False
        
        if self.listening_thread and self.listening_thread.is_alive():
            self.listening_thread.join(timeout=2)
        
        logger.info("Continuous listening stopped")
    
    def _continuous_listening_loop(self):
        """Main continuous listening loop - Always active, no wake word needed"""
        while self.is_listening and self.is_active:
            try:
                # Directly listen for commands (no wake word required)
                command, audio = self._listen_for_command()
                
                if command and audio:
                    logger.info(f"Command received: {command}")
                    
                    # Verify the speaker
                    if not self.speaker_verification.verify_speaker(audio):
                        logger.warning("Speaker verification failed. Ignoring command.")
                        self._speak("I'm sorry, I don't recognize your voice.")
                        if not config.CONTINUOUS_LISTENING:
                            break
                        continue
                        
                    # Process the command
                    continue_listening = self.command_callback(command)
                    if not continue_listening:
                        break
                else:
                    logger.debug("No speech detected, continuing to listen...")
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in listening loop: {e}")
                time.sleep(1)  # Wait before retrying
    
    def _listen_for_wake_word(self) -> bool:
        """Listen specifically for wake words"""
        try:
            with self.microphone as source:
                logger.debug("Listening for wake word...")
                audio = self.recognizer.listen(
                    source,
                    timeout=config.AUDIO_TIMEOUT,
                    phrase_time_limit=2  # Short timeout for wake words
                )
            
            # Try to recognize the wake word
            try:
                # Use Google's recognizer for wake word detection (more accurate)
                text = self.recognizer.recognize_google(audio).lower()
                logger.debug(f"Detected speech: {text}")
                
                # Check if any wake word is detected
                for wake_word in config.WAKE_WORDS:
                    if wake_word in text:
                        logger.info(f"Wake word '{wake_word}' detected")
                        return True
                        
            except sr.UnknownValueError:
                # No speech detected
                pass
            except sr.RequestError as e:
                logger.error(f"Wake word recognition error: {e}")
                
        except sr.WaitTimeoutError:
            # Normal timeout, continue listening
            pass
        except Exception as e:
            logger.error(f"Error listening for wake word: {e}")
        
        return False
    
    def _listen_for_command(self) -> Tuple[Optional[str], Optional[sr.AudioData]]:
        """Listen for voice command with current language support"""
        try:
            time.sleep(0.5)
            
            with self.microphone as source:
                logger.debug("Listening for command...")
                audio = self.recognizer.listen(
                    source,
                    timeout=config.COMMAND_TIMEOUT,
                    phrase_time_limit=config.AUDIO_PHRASE_LIMIT
                )
            
            # Get language-specific speech code
            lang_code = config.get_current_language().get('speech_code', 'en-US')
            
            # Recognize the command with language support
            try:
                command = self.recognizer.recognize_google(audio, language=lang_code).lower()
                logger.info(f"Command recognized ({lang_code}): {command}")
                
                # Strip wake words from command
                stripped_command = self._strip_wake_words(command)
                if stripped_command:
                    logger.info(f"Stripped command: {stripped_command}")
                    return stripped_command, audio
                else:
                    # Command was just a wake word, ignore it
                    return None, None
                
            except sr.UnknownValueError:
                logger.warning("Could not understand command")
                return None, None
            except sr.RequestError as e:
                logger.error(f"Command recognition error: {e}")
                return None, None
                
        except sr.WaitTimeoutError:
            logger.warning("Command timeout - no speech detected")
            return None, None
        except Exception as e:
            logger.error(f"Error listening for command: {e}")
            return None, None
    
    def process_single_command(self) -> Tuple[Optional[str], Optional[sr.AudioData]]:
        """Process a single voice command with current language support"""
        try:
            with self.microphone as source:
                logger.info("Listening for command...")
                self._speak("I'm listening for your command. Please speak now.")
                audio = self.recognizer.listen(
                    source,
                    timeout=config.AUDIO_TIMEOUT,
                    phrase_time_limit=config.AUDIO_PHRASE_LIMIT
                )
            
            # Get language-specific speech code
            lang_code = config.get_current_language().get('speech_code', 'en-US')
            
            # Recognize speech with language support
            try:
                command = self.recognizer.recognize_google(audio, language=lang_code).lower()
                logger.info(f"Command recognized ({lang_code}): {command}")
                
                # Verify speaker
                if not self.speaker_verification.verify_speaker(audio):
                    logger.warning("Speaker verification failed.")
                    self._speak("I'm sorry, I don't recognize your voice.")
                    return None, None
                    
                return command, audio
                
            except sr.UnknownValueError:
                logger.warning("Could not understand command")
                self._speak("Sorry, I couldn't understand that. Please try again.")
                return None, None
            except sr.RequestError as e:
                logger.error(f"Speech recognition error: {e}")
                self._speak("Sorry, there was an error processing your voice.")
                return None, None
                
        except sr.WaitTimeoutError:
            logger.warning("No speech detected within timeout")
            self._speak("I didn't hear anything. Please try again.")
            return None, None
        except Exception as e:
            logger.error(f"Error processing single command: {e}")
            return None, None
    
    def _speak(self, text: str):
        """Speak text using TTS engine if available"""
        if self.tts_engine and self.tts_engine.is_available():
            self.tts_engine.speak(text)
        else:
            logger.info(f"AI: {text}")