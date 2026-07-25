"""
Command Registry - Fast pattern matching for voice commands
Replaces the massive if/elif chain with dictionary lookups
"""

# Command registry: pattern -> (handler_method, priority)
# Priority: higher = checked first
COMMAND_REGISTRY = {
    # Exit commands (highest priority)
    "exit": {"patterns": ["exit", "quit", "goodbye", "bye", "shut down", "stop"], "handler": "_exit_command", "priority": 100},
    
    # Greetings
    "greeting": {"patterns": ["hello", "hi", "hey", "greetings"], "handler": "_greet_user", "priority": 90},
    
    # Help
    "help": {"patterns": ["help", "what can you do", "commands"], "handler": "_show_help", "priority": 85},
    
    # Who am I
    "whoami": {"patterns": ["who am i", "what is my name", "what's my name"], "handler": "_who_am_i", "priority": 80},
    
    # Time/Date
    "time": {"patterns": ["time", "what time", "current time", "clock"], "handler": "_tell_time", "priority": 70},
    "date": {"patterns": ["date", "today", "what date"], "handler": "_tell_date", "priority": 70},
    
    # Language switch
    "language": {"patterns": ["switch to bangla", "bangla", "bengali", "switch to english", "english"], "handler": "_handle_language_switch", "priority": 75},
    
    # Mood commands
    "mood_check": {"patterns": ["your mood", "how are you feeling", "what mood", "mood check", "current mood"], "handler": "_handle_mood_check", "priority": 72},
    "mood_set": {"patterns": ["be happy", "be excited", "be calm", "be silly", "be focused", "be sarcastic", "be playful", "be energetic", "be chill", "be sad", "cheer up", "be annoyed", "be impatient"], "handler": "_handle_set_mood", "priority": 72},
    
    # Name setting
    "name_set": {"patterns": ["my name is", "i am", "call me"], "handler": "_set_name", "priority": 65},
    
    # Learning
    "learn": {"patterns": ["learn about", "tell me about", "what is", "explain"], "handler": "_handle_learning_command", "priority": 60},
    
    # Code analysis
    "analyze_code": {"patterns": ["analyze code", "analyse code", "check code", "find bugs", "scan code"], "handler": "_handle_code_analysis", "priority": 55},
    "fix_bugs": {"patterns": ["fix bugs", "auto fix", "repair"], "handler": "_handle_auto_fix", "priority": 55},
    
    # Remember
    "remember": {"patterns": ["remember", "save this"], "handler": "_handle_remember_command", "priority": 50},
    
    # Opinions
    "opinion": {"patterns": ["i think", "i believe", "i feel", "in my opinion"], "handler": "_handle_user_opinion", "priority": 45},
    
    # Learning
    "learned": {"patterns": ["i learned", "i discovered", "i realized"], "handler": "_handle_user_learning", "priority": 45},
    
    # Training
    "training_stats": {"patterns": ["training stats", "how are you learning", "show training"], "handler": "_show_training_stats", "priority": 40},
    "train_now": {"patterns": ["train now", "start training", "auto train"], "handler": "_manual_train", "priority": 40},
    
    # Open commands
    "open_screenshot": {"patterns": ["open the screenshot", "open screenshot"], "handler": "_handle_screenshot", "priority": 38},
    "open": {"patterns": ["open ", "launch ", "start "], "handler": "_handle_open_app", "priority": 35},
    
    # YouTube
    "youtube": {"patterns": ["youtube", "youtub"], "handler": "_handle_youtube", "priority": 33},
    
    # Play/Search
    "play": {"patterns": ["play "], "handler": "_handle_play_media", "priority": 32},
    "search": {"patterns": ["search ", "google search"], "handler": "_handle_google_search", "priority": 32},
    
    # Browser
    "browser": {"patterns": ["open browser", "open chrome", "open safari", "open firefox"], "handler": "_handle_open_browser", "priority": 30},
    
    # Close
    "close": {"patterns": ["close ", "quit ", "exit "], "handler": "_handle_close_app", "priority": 28},
    
    # System info
    "system_info": {"patterns": ["system info", "computer info", "system status"], "handler": "_show_system_info", "priority": 25},
    
    # Apps
    "installed_apps": {"patterns": ["installed apps", "list apps", "app list", "all apps"], "handler": "_show_installed_apps", "priority": 24},
    "running_apps": {"patterns": ["running apps", "running programs", "active apps", "open apps"], "handler": "_show_running_apps", "priority": 24},
    
    # Active window
    "active_window": {"patterns": ["what app is this", "what application", "which app am i in", "current app", "active window"], "handler": "_handle_active_window", "priority": 23},
    
    # Browser tabs
    "tabs": {"patterns": ["open tabs", "browser tabs", "what tabs"], "handler": "_handle_list_tabs", "priority": 22},
    
    # Volume
    "volume_up": {"patterns": ["volume up", "louder"], "handler": "_handle_volume_up", "priority": 20},
    "volume_down": {"patterns": ["volume down", "quieter"], "handler": "_handle_volume_down", "priority": 20},
    "mute": {"patterns": ["mute"], "handler": "_handle_mute", "priority": 20},
    "unmute": {"patterns": ["unmute"], "handler": "_handle_unmute", "priority": 20},
    "set_volume": {"patterns": ["set volume", "volume to"], "handler": "_handle_set_volume", "priority": 20},
    
    # Screenshot
    "screenshot": {"patterns": ["screenshot", "screen capture", "take screenshot", "capture screen"], "handler": "_handle_screenshot", "priority": 18},
    
    # System control
    "lock_screen": {"patterns": ["lock screen"], "handler": "_handle_lock_screen", "priority": 15},
    "empty_trash": {"patterns": ["empty trash", "clear trash"], "handler": "_handle_empty_trash", "priority": 15},
    "shutdown": {"patterns": ["shutdown", "shut down", "turn off"], "handler": "_handle_shutdown", "priority": 15},
    "restart": {"patterns": ["restart", "reboot"], "handler": "_handle_restart", "priority": 15},
    "sleep": {"patterns": ["sleep", "suspend"], "handler": "_handle_sleep", "priority": 15},
    
    # Files
    "list_files": {"patterns": ["list files", "show files", "files in"], "handler": "_handle_list_files", "priority": 12},
    "disk_space": {"patterns": ["disk space", "storage"], "handler": "_handle_disk_space", "priority": 12},
    "battery": {"patterns": ["battery", "batteries"], "handler": "_handle_battery", "priority": 12},
    "network": {"patterns": ["wifi", "network"], "handler": "_handle_network", "priority": 12},
    
    # Screen vision
    "see_screen": {"patterns": ["see screen", "look at screen", "what on screen", "screen content", "what do you see", "analyze screen"], "handler": "_handle_see_screen", "priority": 10},
    "read_screen": {"patterns": ["read screen", "read text", "what text", "screen text"], "handler": "_handle_read_screen", "priority": 10},
    "describe_screen": {"patterns": ["what is on my screen", "screen status", "describe screen"], "handler": "_handle_describe_screen", "priority": 10},
    
    # Jokes
    "joke": {"patterns": ["tell joke", "make me laugh", "funny joke", "joke please", "tell a joke"], "handler": "_tell_joke", "priority": 8},
    
    # Resume music
    "resume": {"patterns": ["resume", "resume music", "resume the music", "play again"], "handler": "_handle_play_media", "priority": 7},
    
    # Self-thinking
    "self_analysis": {"patterns": ["analyze yourself", "self analysis", "how smart are you", "your abilities"], "handler": "_handle_self_analysis", "priority": 5},
    "think_about": {"patterns": ["think about", "what do you think", "analyze this"], "handler": "_handle_think_about", "priority": 5},
    "auto_improve": {"patterns": ["auto improve", "improve yourself", "get smarter", "learn from mistakes"], "handler": "_handle_auto_improve", "priority": 5},
    
    # Internet learning
    "search_internet": {"patterns": ["search", "google", "find online", "look up", "search for"], "handler": "_handle_search_internet", "priority": 3},
    "learn_internet": {"patterns": ["learn about", "teach me about", "what is", "tell me about"], "handler": "_handle_learn_internet", "priority": 3},
    
    # Screen awareness
    "what_am_i_doing": {"patterns": ["what am i doing", "what am i working on", "what do you see"], "handler": "_handle_what_am_i_doing", "priority": 2},
    "watch_screen": {"patterns": ["watch my screen", "look at my screen", "see my screen", "monitor my screen"], "handler": "_handle_watch_screen", "priority": 2},
    
    # Database commands
    "db_stats": {"patterns": ["database stats", "db stats", "brain stats", "how much do you know", "memory stats"], "handler": "_handle_db_stats", "priority": 30},
    "db_search": {"patterns": ["search memory", "search brain", "find in memory", "what do you know about"], "handler": "_handle_db_search", "priority": 29},
    "db_save_memory": {"patterns": ["save to memory", "remember this", "store this", "save fact"], "handler": "_handle_db_save_memory", "priority": 28},
    "db_get_memory": {"patterns": ["recall", "what do you remember about", "get memory"], "handler": "_handle_db_get_memory", "priority": 27},
    "db_facts": {"patterns": ["show facts", "list facts", "what facts", "all facts"], "handler": "_handle_db_facts", "priority": 26},
    "db_conversations": {"patterns": ["show conversations", "chat history", "conversation history"], "handler": "_handle_db_conversations", "priority": 25},
    "db_goals": {"patterns": ["show goals", "list goals", "my goals", "goal status"], "handler": "_handle_db_goals", "priority": 24},
    "db_add_goal": {"patterns": ["add goal", "set goal", "new goal", "create goal"], "handler": "_handle_db_add_goal", "priority": 23},
    "db_notes": {"patterns": ["show notes", "daily notes", "my notes", "what happened"], "handler": "_handle_db_notes", "priority": 22},
    "db_add_note": {"patterns": ["add note", "take note", "write note", "note this"], "handler": "_handle_db_add_note", "priority": 21},
    "db_backup": {"patterns": ["backup database", "backup brain", "save database"], "handler": "_handle_db_backup", "priority": 20},
    "db_clear_old": {"patterns": ["clear old", "clean database", "purge old"], "handler": "_handle_db_clear_old", "priority": 19},
    
    # Camera commands
    "camera_open": {"patterns": ["open camera", "start camera", "turn on camera", "camera on"], "handler": "_handle_camera_open", "priority": 26},
    "camera_close": {"patterns": ["close camera", "stop camera", "turn off camera", "camera off"], "handler": "_handle_camera_close", "priority": 26},
    "camera_photo": {"patterns": ["take photo", "take picture", "capture photo", "camera photo", "snap"], "handler": "_handle_camera_photo", "priority": 25},
    "look_at_me": {"patterns": ["look at me", "see me", "look at my face", "can you see me", "do you see me"], "handler": "_handle_look_at_me", "priority": 27},
    "recognize_faces": {"patterns": ["recognize faces", "who is this", "who are you", "identify", "who do you see"], "handler": "_handle_recognize_faces", "priority": 28},
    "learn_face": {"patterns": ["learn my face", "remember my face", "teach me face", "know my face", "remember me"], "handler": "_handle_learn_face", "priority": 29},
    "forget_face": {"patterns": ["forget my face", "forget face", "remove face", "don't remember"], "handler": "_handle_forget_face", "priority": 24},
    "known_faces": {"patterns": ["known faces", "who do you know", "list faces", "face list"], "handler": "_handle_known_faces", "priority": 23},
    "start_recognition": {"patterns": ["start recognition", "start recognizing", "greet me", "say hello"], "handler": "_handle_start_recognition", "priority": 22},
    "camera_info": {"patterns": ["camera info", "camera status", "which camera"], "handler": "_handle_camera_info", "priority": 21},
    
    # Media control commands
    "play_music": {"patterns": ["play music", "play song", "play ", "play on youtube", "play on spotify"], "handler": "_handle_play_music", "priority": 35},
    "pause_music": {"patterns": ["pause", "pause music", "stop music", "pause playback"], "handler": "_handle_pause_music", "priority": 35},
    "resume_music": {"patterns": ["resume", "resume music", "continue", "continue playing"], "handler": "_handle_resume_music", "priority": 35},
    "next_track": {"patterns": ["next", "next song", "skip", "skip song", "next track"], "handler": "_handle_next_track", "priority": 34},
    "prev_track": {"patterns": ["previous", "previous song", "go back", "last song"], "handler": "_handle_prev_track", "priority": 34},
    "stop_music": {"patterns": ["stop", "stop all", "stop playing", "turn off music"], "handler": "_handle_stop_music", "priority": 34},
    "what_playing": {"patterns": ["what's playing", "what song", "current song", "now playing"], "handler": "_handle_what_playing", "priority": 33},
    
    # Emotional responses
    "mood_happy": {"patterns": ["are you happy", "how do you feel", "your mood"], "handler": "_handle_mood_happy", "priority": 30},
    "mood_sad": {"patterns": ["are you sad", "you seem sad", "cheer up"], "handler": "_handle_mood_sad", "priority": 30},
    "mood_angry": {"patterns": ["are you angry", "you seem mad", "calm down"], "handler": "_handle_mood_angry", "priority": 30},
    "mood_excited": {"patterns": ["are you excited", "you seem excited"], "handler": "_handle_mood_excited", "priority": 30},
    
    # Show object to camera
    "show_object": {"patterns": ["what is this", "what do you see", "look at this", "what am i showing"], "handler": "_handle_show_object", "priority": 28},
}


def get_command_handler(command: str) -> tuple:
    """
    Find the best matching handler for a command.
    Returns: (handler_method_name, matched_patterns) or (None, None)
    """
    command_lower = command.lower().strip()
    
    # Sort by priority (highest first)
    sorted_commands = sorted(COMMAND_REGISTRY.items(), key=lambda x: x[1]['priority'], reverse=True)
    
    for cmd_name, cmd_info in sorted_commands:
        for pattern in cmd_info['patterns']:
            if pattern in command_lower:
                return cmd_info['handler'], pattern
    
    return None, None


def get_command_priority(command: str) -> int:
    """Get the priority of a command"""
    handler, _ = get_command_handler(command)
    if handler:
        for cmd_info in COMMAND_REGISTRY.values():
            if cmd_info['handler'] == handler:
                return cmd_info['priority']
    return 0
