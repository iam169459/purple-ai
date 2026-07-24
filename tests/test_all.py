#!/usr/bin/env python3
"""
Test script for the Offline AI Assistant
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from config import config
        print("  Config module imported successfully")
        
        from logger import logger
        print("  Logger module imported successfully")
        
        from core.ai_engine import OfflineAI
        print("  AI Engine module imported successfully")
        
        from utils.memory_manager import MemoryManager
        print("  Memory Manager module imported successfully")
        
        from utils.response_generator import ResponseGenerator
        print("  Response Generator module imported successfully")
        
        from voice.tts_engine import TTSEngine
        print("  TTS Engine module imported successfully")
        
        from voice.voice_controller import VoiceController
        print("  Voice Controller module imported successfully")
        
        from commands.system_commands import SystemCommands
        print("  System Commands module imported successfully")
        
        from commands.entertainment import EntertainmentCommands
        print("  Entertainment Commands module imported successfully")
        
        from utils.learning_engine import LearningEngine
        print("  Learning Engine module imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"  Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of core components"""
    print("\nTesting basic functionality...")
    
    try:
        from utils.memory_manager import MemoryManager
        memory_manager = MemoryManager()
        memory = memory_manager.load_memory()
        print("  Memory manager working")
        
        from utils.response_generator import ResponseGenerator
        response_gen = ResponseGenerator()
        response = response_gen.generate_response("hello", memory)
        print(f"  Response generator working")
        
        from commands.entertainment import EntertainmentCommands
        joke = EntertainmentCommands.get_random_joke()
        print(f"  Entertainment commands working")
        
        return True
        
    except Exception as e:
        print(f"  Functionality test failed: {e}")
        return False

def main():
    print("=" * 50)
    print("Offline AI Assistant - Test Suite")
    print("=" * 50)
    
    if not test_imports():
        print("\nImport tests failed!")
        return False
    
    if not test_basic_functionality():
        print("\nFunctionality tests failed!")
        return False
    
    print("\n" + "=" * 50)
    print("All tests passed!")
    print("Run 'python main.py' to start the AI assistant.")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
