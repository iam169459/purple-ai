#!/usr/bin/env python3
"""
Purple AI Assistant - Main Entry Point
With Auto-Training and Self-Improvement
"""
import sys
import os
import logging
import time
import signal
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from logger import logger
from core.ai_engine import OfflineAI
from voice.tts_engine import TTSEngine
from voice.voice_controller import VoiceController
from utils.self_repair import self_repair

def cleanup(signum=None, frame=None):
    """Cleanup on exit"""
    sys.exit(0)

def print_welcome_banner():
    print("\n" + "=" * 60)
    print("✨ Purple AI - Always Listening ✨")
    print("=" * 60)
    print("Your Self-Improving AI Companion - Always Active!")
    print("=" * 60)
    print("\nFeatures:")
    print("  🎧 Always Listening - Say any wake word")
    print("  📸 Camera Vision - Recognizes your face")
    print("  🧠 Smart Database - Remembers everything")
    print("  🔄 Auto-Training - Learns from every chat")
    print("  💬 Natural Conversations - Chat naturally")
    print("=" * 60)
    print("\nQuick Start:")
    print("  Say 'purple' or 'hey purple' to activate")
    print("  Or just speak naturally - I'm always listening!")
    print("=" * 60)

def print_help_menu():
    print("\n" + "=" * 60)
    print("Purple AI - Voice Commands Guide")
    print("=" * 60)
    print("\nTraining & Learning:")
    print("  'Training stats' - See my improvement progress")
    print("  'Train now' - Start a training session")
    print("  'I think...' - Share your opinion with me")
    print("  'I learned...' - Teach me something new")
    print("\nMood & Personality:")
    print("  'What's your mood' - Check my current mood")
    print("  'Be happy/excited/calm/silly' - Set my mood")
    print("  'Be focused/chill/playful/energetic' - More moods!")
    print("\nCode Analysis:")
    print("  'Analyze code [file.py]' - Find bugs")
    print("  'Fix bugs [file.py]' - Auto-fix issues")
    print("\nInternet Learning:")
    print("  'Learn about [topic]' - Learn from web")
    print("  'What is [concept]' - Get explanations")
    print("\nBasic:")
    print("  'What time is it?' - Current time")
    print("  'What's today's date?' - Current date")
    print("  'Help' - Show this help")
    print("  'Goodbye' - Exit")
    print("\nHow Auto-Training Works:")
    print("  - I analyze every conversation we have")
    print("  - I learn patterns from successful interactions")
    print("  - I improve my responses over time")
    print("  - I auto-train every 10 conversations!")
    print("  - I get smarter with every chat!")
    print("=" * 60)

def main():
    # Register signal handlers for cleanup
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    # Check for background mode
    background_mode = '--background' in sys.argv or '--bg' in sys.argv
    
    try:
        # Run self-diagnostics and auto-fix
        if not background_mode:
            print("\n🔍 Running self-diagnostics...")
        repair_results = self_repair.auto_fix_all()
        
        if not background_mode:
            if repair_results['fixes']:
                print(f"✅ Auto-fixed {len(repair_results['fixes'])} issues:")
                for fix in repair_results['fixes']:
                    print(f"   - {fix.get('message', 'Fixed')}")
            
            if repair_results['issues']:
                print(f"⚠️  Found {len(repair_results['issues'])} issues that need attention:")
                for issue in repair_results['issues']:
                    print(f"   - {issue.get('error', 'Unknown issue')}")
            
            if repair_results['healthy']:
                print("✅ System healthy!")
            
            print_welcome_banner()
        
        logger.info("=" * 60)
        logger.info("Starting Purple AI - Always Listening Mode")
        logger.info("=" * 60)
        
        tts_engine = TTSEngine()
        
        if not tts_engine.is_available():
            logger.error("TTS engine not available")
            if not background_mode:
                print("\n❌ Error: TTS engine not available.")
            sys.exit(1)
        
        logger.info("Initializing AI engine...")
        ai_engine = OfflineAI(tts_engine=tts_engine)
        
        # Check if first-time setup is needed
        if not ai_engine.memory.get('setup_complete', False):
            logger.info("First-time setup needed. Starting setup wizard...")
            
            logger.info("Initializing voice controller for setup...")
            voice_controller = VoiceController(tts_engine)
            
            # Run the setup flow
            ai_engine.setup_owner(voice_controller=voice_controller)
        else:
            logger.info("Setup already complete. Loading owner profile...")
            owner_name = ai_engine.memory.get('user_name', 'friend')
        
        logger.info("Initializing voice controller...")
        voice_controller = VoiceController(tts_engine)
        voice_controller.set_command_callback(ai_engine._process_command)
        
        if not background_mode:
            logger.info("Starting voice-only mode...")
            print("\n" + "=" * 60)
            print("🎧 Purple AI - Always Listening 🎧")
            print("=" * 60)
            print("I'm ALWAYS listening! Say any wake word to activate:")
            print("")
            print("  🔵 Wake Words:")
            print("     purple, hey purple, hello purple")
            print("     ai, hey ai, computer, jarvis")
            print("     wake up, listen, hello, hey")
            print("")
            print("  🎯 Or just speak naturally - I'm always listening!")
            print("")
            print("  📸 Camera: 'Look at me' to recognize you")
            print("  🧠 Database: 'Save to memory' to remember things")
            print("  ❓ 'Help' - Show all commands")
            print("=" * 60)
            print(f"\n⏰ Started at: {datetime.now().strftime('%I:%M %p')}")
            print("Background mode: Always active")
            print("Press Ctrl+C to exit")
            print("=" * 60)
        else:
            logger.info("Starting in background mode - always listening")
        
        if not voice_controller.start_continuous_listening():
            logger.error("Failed to start listening")
            if not background_mode:
                print("\n❌ Error: Failed to start voice listening.")
            sys.exit(1)
        
        try:
            while voice_controller.is_listening:
                time.sleep(0.1)
        except KeyboardInterrupt:
            if not background_mode:
                print("\n\n👋 Shutting down...")
        
        logger.info("Shutting down...")
        voice_controller.stop_listening()
        ai_engine.memory_manager.save_memory(ai_engine.memory)
        
        if not background_mode:
            print("\n" + "=" * 60)
            print("📊 Session Summary")
            print("=" * 60)
            print(f"Conversations: {ai_engine.conversation_stats.get('commands_processed', 0)}")
            print(f"Training sessions: {ai_engine.conversation_stats.get('training_sessions', 0)}")
            print(f"Improvements made: {ai_engine.conversation_stats.get('improvements_made', 0)}")
            print(f"Questions asked: {ai_engine.conversation_stats.get('questions_asked', 0)}")
            print(f"Knowledge gained: {ai_engine.conversation_stats.get('knowledge_gained', 0)}")
            print(f"Bugs found: {ai_engine.conversation_stats.get('bugs_found', 0)}")
            print(f"Bugs fixed: {ai_engine.conversation_stats.get('bugs_fixed', 0)}")
            print("=" * 60)
            
            tts_engine.speak("Goodbye! I've learned and improved from our conversation!")
            print("\n✨ Thank you for helping me improve! ✨\n")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
