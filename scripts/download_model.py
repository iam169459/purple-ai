"""
Script to download the Vosk speech recognition model
"""
import os
import sys
import urllib.request
import zipfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

def download_vosk_model():
    """Download the Vosk English model"""
    print("Downloading Vosk English speech recognition model...")
    
    # URL for the small English model
    model_url = config.MODEL_URL
    model_filename = f"{config.MODEL_NAME}.zip"
    
    try:
        # Download the model
        print("Downloading model file...")
        urllib.request.urlretrieve(model_url, model_filename)
        print("Model downloaded successfully!")
        
        # Extract the model
        print("Extracting model...")
        with zipfile.ZipFile(model_filename, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Rename the extracted folder to 'model'
        extracted_folder = config.MODEL_NAME
        if os.path.exists(extracted_folder):
            if os.path.exists(config.MODEL_PATH):
                shutil.rmtree(config.MODEL_PATH)  # Remove old model folder if exists
            os.rename(extracted_folder, config.MODEL_PATH)
            print(f"Model extracted and renamed to '{config.MODEL_PATH}' folder.")
        
        # Clean up the zip file
        os.remove(model_filename)
        print("Cleaned up temporary files.")
        
        print("\nVosk model setup complete!")
        print("The offline AI can now operate without internet connection.")
        
    except Exception as e:
        print(f"Error downloading or extracting model: {e}")
        print("Please manually download the model from:")
        print("https://alphacephei.com/vosk/models")
        print(f"Extract it to a folder named '{config.MODEL_PATH}' in this directory.")

if __name__ == "__main__":
    download_vosk_model()