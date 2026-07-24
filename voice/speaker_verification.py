import os
import torch
import torchaudio
from logger import logger

# Try importing from new speechbrain (>= 1.0) and fallback to older versions
try:
    from speechbrain.inference.speaker import SpeakerRecognition
except ImportError:
    try:
        from speechbrain.pretrained import SpeakerRecognition
    except ImportError:
        SpeakerRecognition = None
        logger.error("speechbrain is not installed or configured correctly.")

class SpeakerVerification:
    def __init__(self, reference_file='data/my_voice_reference.wav'):
        self.reference_file = reference_file
        self.model = None
        self.threshold = 0.08  # Very low threshold for better acceptance
        self._temp_files = []

    def initialize(self):
        """Lazy load the model to speed up fast boots if not needed"""
        if self.model is None and SpeakerRecognition is not None:
            logger.info("Loading Speaker Recognition model (this may take a moment)...")
            try:
                self.model = SpeakerRecognition.from_hparams(
                    source="speechbrain/spkrec-ecapa-voxceleb", 
                    savedir="model/spkrec-ecapa-voxceleb"
                )
                logger.info("Speaker Recognition model loaded.")
            except Exception as e:
                logger.error(f"Failed to load Speaker Recognition model: {e}")

    def is_enrolled(self):
        return os.path.exists(self.reference_file)
    
    def save_audio(self, audio_data, filepath):
        """Save speech_recognition AudioData to a wav file"""
        with open(filepath, "wb") as f:
            f.write(audio_data.get_wav_data())
            
    def enroll_user(self, audio_data):
        """Save the given audio data as the reference profile"""
        os.makedirs(os.path.dirname(self.reference_file), exist_ok=True)
        self.save_audio(audio_data, self.reference_file)
        logger.info("User voice enrolled successfully.")
    
    def enroll_user_multi(self, audio_samples):
        """Enroll user with multiple voice samples for better recognition"""
        if not audio_samples:
            logger.warning("No audio samples provided for enrollment")
            return
        
        os.makedirs(os.path.dirname(self.reference_file), exist_ok=True)
        
        # If only one sample, use simple enrollment
        if len(audio_samples) == 1:
            self.enroll_user(audio_samples[0])
            return
        
        # For multiple samples, save the first one as primary
        # and concatenate others for better coverage
        try:
            self.save_audio(audio_samples[0], self.reference_file)
            
            # Save additional samples for reference
            for i, sample in enumerate(audio_samples[1:], 1):
                ref_dir = os.path.dirname(self.reference_file)
                extra_ref = os.path.join(ref_dir, f"voice_sample_{i}.wav")
                self.save_audio(sample, extra_ref)
                logger.info(f"Saved extra voice sample {i}")
            
            logger.info(f"User voice enrolled with {len(audio_samples)} samples")
        except Exception as e:
            logger.error(f"Error in multi-sample enrollment: {e}")
            # Fallback to single sample
            self.enroll_user(audio_samples[0])
        
    def verify_speaker(self, incoming_audio_data) -> bool:
        """Verify if the incoming audio matches the enrolled reference"""
        if not self.is_enrolled():
            logger.warning("No voice profile enrolled. Bypassing verification.")
            return True
            
        self.initialize()
        if not self.model:
            return True # If model fails to load, allow fallback
            
        temp_file = "data/temp_incoming.wav"
        self.save_audio(incoming_audio_data, temp_file)
        
        try:
            score, prediction = self.model.verify_files(self.reference_file, temp_file)
            match_score = score.item()
            logger.info(f"Speaker verification score: {match_score:.2f} (Threshold: {self.threshold})")
            
            # Also check against extra samples if available
            best_score = match_score
            ref_dir = os.path.dirname(self.reference_file)
            for i in range(1, 10):
                extra_ref = os.path.join(ref_dir, f"voice_sample_{i}.wav")
                if os.path.exists(extra_ref):
                    try:
                        extra_score, _ = self.model.verify_files(extra_ref, temp_file)
                        extra_match = extra_score.item()
                        if extra_match > best_score:
                            best_score = extra_match
                            logger.info(f"Extra sample {i} score: {extra_match:.2f}")
                    except Exception:
                        pass
            
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
            return best_score >= self.threshold
        except Exception as e:
            logger.error(f"Error during speaker verification: {e}")
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return True # Fallback to True so we don't break functionality
