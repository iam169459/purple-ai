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

    # ==================== YOUTUBE / VIDEO ====================
    "youtube_play": {"patterns": ["play youtube", "play video", "play on youtube", "youtube play"], "handler": "_web_handle_youtube_play", "priority": 85},
    "youtube_shorts": {"patterns": ["play shorts", "youtube shorts", "play short"], "handler": "_web_handle_youtube_shorts", "priority": 84},
    "youtube_music": {"patterns": ["play music", "youtube music", "play song youtube", "music on youtube"], "handler": "_web_handle_youtube_music", "priority": 84},
    "youtube_live": {"patterns": ["play live", "youtube live", "live stream", "live on youtube"], "handler": "_web_handle_youtube_live", "priority": 84},
    "youtube_playlist": {"patterns": ["play playlist", "youtube playlist", "playlist play"], "handler": "_web_handle_youtube_playlist", "priority": 83},
    "vimeo_play": {"patterns": ["play vimeo", "vimeo video"], "handler": "_web_handle_vimeo_play", "priority": 82},
    "twitch_play": {"patterns": ["play twitch", "twitch stream", "watch twitch", "twitch live"], "handler": "_web_handle_twitch_play", "priority": 82},
    "twitch_clips": {"patterns": ["twitch clips", "play clips", "watch clips"], "handler": "_web_handle_twitch_clips", "priority": 81},

    # ==================== STREAMING SERVICES ====================
    "netflix_play": {"patterns": ["play netflix", "netflix", "watch netflix"], "handler": "_web_handle_netflix_play", "priority": 80},
    "hulu_play": {"patterns": ["play hulu", "hulu", "watch hulu"], "handler": "_web_handle_hulu_play", "priority": 80},
    "prime_video": {"patterns": ["play amazon prime", "prime video", "amazon video"], "handler": "_web_handle_prime_video_play", "priority": 80},
    "disney_plus": {"patterns": ["play disney plus", "disney plus", "disney+"], "handler": "_web_handle_disney_plus_play", "priority": 80},
    "spotify_play": {"patterns": ["play spotify", "spotify", "play music spotify", "spotify music"], "handler": "_web_handle_spotify_play", "priority": 80},

    # ==================== SOCIAL MEDIA ====================
    "tiktok_open": {"patterns": ["open tiktok", "tiktok", "play tiktok", "tiktok open"], "handler": "_web_handle_tiktok_open", "priority": 78},
    "instagram_open": {"patterns": ["open instagram", "instagram", " Insta", " insta "], "handler": "_web_handle_instagram_open", "priority": 78},
    "twitter_open": {"patterns": ["open twitter", "open x", "twitter", "x.com", "twitter open"], "handler": "_web_handle_twitter_open", "priority": 78},
    "post_tweet": {"patterns": ["post a tweet", "tweet this", "tweet about", "send tweet"], "handler": "_web_handle_post_tweet", "priority": 77},
    "post_video": {"patterns": ["post video", "upload video", "share video"], "handler": "_web_handle_post_video", "priority": 77},

    # ==================== GOOGLE & SEARCH ====================
    "google_search": {"patterns": ["google search", "google it", "search google"], "handler": "_handle_google_search", "priority": 75},
    "google_maps": {"patterns": ["google maps", "open maps", "navigate to"], "handler": "_web_handle_google_maps", "priority": 75},
    "google_translate": {"patterns": ["translate", "google translate", "translate this"], "handler": "_web_handle_google_translate", "priority": 74},
    "web_search": {"patterns": ["search the web", "search online", "look up online"], "handler": "_web_handle_web_search", "priority": 70},

    # ==================== VIDEO CONTROLS ====================
    "video_pause": {"patterns": ["pause", "pause video", "pause playing"], "handler": "_web_handle_video_pause", "priority": 60},
    "video_resume": {"patterns": ["resume", "resume video", "continue playing"], "handler": "_web_handle_video_resume", "priority": 60},
    "video_stop": {"patterns": ["stop", "stop video", "stop playing", "stop video"], "handler": "_web_handle_video_stop", "priority": 60},
    "volume_set": {"patterns": ["set volume", "volume to", "volume level"], "handler": "_web_handle_volume_set", "priority": 59},
    "video_next": {"patterns": ["next video", "skip", "next", "forward"], "handler": "_web_handle_video_next", "priority": 58},
    "video_previous": {"patterns": ["previous video", "previous", "back"], "handler": "_web_handle_video_previous", "priority": 58},

    # ==================== PLAYLIST MANAGEMENT ====================
    "create_playlist": {"patterns": ["create playlist", "new playlist", "make playlist"], "handler": "_web_handle_create_playlist", "priority": 55},
    "add_to_playlist": {"patterns": ["add to playlist", "playlist add"], "handler": "_web_handle_add_to_playlist", "priority": 55},
    "play_playlist": {"patterns": ["play playlist", "playlist play", "start playlist"], "handler": "_web_handle_play_playlist", "priority": 55},
    "list_playlists": {"patterns": ["show playlists", "list playlists", "my playlists"], "handler": "_web_handle_list_playlists", "priority": 54},

    # ==================== BOOKMARKS ====================
    "add_bookmark": {"patterns": ["bookmark", "save bookmark", "add bookmark"], "handler": "_web_handle_add_bookmark", "priority": 50},
    "open_bookmark": {"patterns": ["open bookmark", "go to bookmark"], "handler": "_web_handle_open_bookmark", "priority": 50},
    "list_bookmarks": {"patterns": ["show bookmarks", "list bookmarks", "my bookmarks"], "handler": "_web_handle_list_bookmarks", "priority": 50},

    # ==================== DOWNLOADS ====================
    "download_video": {"patterns": ["download video", "download youtube", "save video"], "handler": "_web_handle_download_video", "priority": 45},
    "download_audio": {"patterns": ["download audio", "download mp3", "extract audio"], "handler": "_web_handle_download_audio", "priority": 45},

    # ==================== WEB HISTORY ====================
    "web_history": {"patterns": ["history", "web history", "browsing history"], "handler": "_web_handle_web_history", "priority": 40},
    "close_browser": {"patterns": ["close browser", "close tab", "close all tabs"], "handler": "_web_handle_close_browser", "priority": 35},

    # ==================== AUTONOMOUS ACTIONS ====================
    "think": {"patterns": ["think about", "what do you think", "analyze this", "consider", "reflect on"], "handler": "_handle_autonomous_think", "priority": 95},
    "autonomous_decision": {"patterns": ["decide", "make decision", "choose between", "what should i do", "help me decide"], "handler": "_handle_autonomous_decision", "priority": 94},
    "create_plan": {"patterns": ["make a plan", "create plan", "plan for", "action plan", "step by step"], "handler": "_handle_create_plan", "priority": 93},
    "execute_plan": {"patterns": ["execute plan", "run plan", "start plan"], "handler": "_handle_execute_plan", "priority": 92},
    "set_goal": {"patterns": ["set goal", "add goal", "new goal", "i want you to", "objective"], "handler": "_handle_set_goal", "priority": 91},
    "complete_goal": {"patterns": ["goal complete", "goal done", "finish goal", "completed goal"], "handler": "_handle_complete_goal", "priority": 90},
    "self_modify": {"patterns": ["modify code", "edit code", "change code", "update code", "rewrite code"], "handler": "_handle_self_modify", "priority": 89},
    "self_improve": {"patterns": ["improve yourself", "auto improve", "optimize", "optimize yourself", "get better", "self improve"], "handler": "_handle_self_improve", "priority": 88},
    "self_analyze": {"patterns": ["self analyze", "analyze yourself", "how smart", "your abilities", "self review"], "handler": "_handle_self_analyze", "priority": 87},
    "self_optimize": {"patterns": ["self optimize", "optimize performance", "speed up", "improve speed"], "handler": "_handle_self_optimize", "priority": 86},

    # System control
    "shutdown": {"patterns": ["shutdown", "shut down", "turn off the system", "power off"], "handler": "_handle_shutdown", "priority": 15},
    "restart": {"patterns": ["restart", "reboot", "restart the system"], "handler": "_handle_restart", "priority": 15},
    "sleep": {"patterns": ["sleep", "suspend", "hibernate"], "handler": "_handle_sleep", "priority": 15},
    "system_status": {"patterns": ["system status", "computer status", "system info detailed"], "handler": "_handle_system_status", "priority": 14},
    "network_info": {"patterns": ["network info", "network details", "ip address", "wifi info"], "handler": "_handle_network_info", "priority": 13},

    # Process control
    "list_processes": {"patterns": ["list processes", "running processes", "what processes", "all processes"], "handler": "_handle_list_processes", "priority": 12},
    "kill_process": {"patterns": ["kill process", "stop process", "end process", "terminate"], "handler": "_handle_kill_process", "priority": 12},

    # App control
    "open_app": {"patterns": ["open app", "launch app", "start app", "open application"], "handler": "_handle_open_app", "priority": 11},
    "close_app": {"patterns": ["close app", "quit app", "close application"], "handler": "_handle_close_app", "priority": 11},
    "list_apps": {"patterns": ["list apps", "all apps", "installed apps", "app list"], "handler": "_handle_list_apps", "priority": 10},

    # Shell commands
    "run_shell": {"patterns": ["run command", "execute shell", "terminal", "shell command"], "handler": "_handle_run_shell", "priority": 8},
    "run_python": {"patterns": ["run python", "execute python", "python script"], "handler": "_handle_run_python", "priority": 8},

    # Clipboard
    "clipboard_copy": {"patterns": ["copy to clipboard", "clipboard copy", "copy this"], "handler": "_handle_clipboard_copy", "priority": 7},
    "clipboard_paste": {"patterns": ["paste clipboard", "clipboard paste", "paste this"], "handler": "_handle_clipboard_paste", "priority": 7},

    # Permission management
    "grant_permission": {"patterns": ["grant permission", "allow", "enable", "give permission"], "handler": "_handle_grant_permission", "priority": 6},
    "revoke_permission": {"patterns": ["revoke permission", "deny", "block", "remove permission"], "handler": "_handle_revoke_permission", "priority": 6},
    "show_permissions": {"patterns": ["show permissions", "list permissions", "what permissions", "current permissions"], "handler": "_handle_show_permissions", "priority": 5},
    "enable_all_permissions": {"patterns": ["enable all", "full access", "grant all", "full permissions"], "handler": "_handle_enable_all_permissions", "priority": 4},

    # Internet
    "internet_search": {"patterns": ["search the web", "search internet", "look up online"], "handler": "_handle_internet_search", "priority": 3},
    "browse_website": {"patterns": ["browse", "visit website", "open website", "go to website"], "handler": "_handle_browse_website", "priority": 3},
    "download_file": {"patterns": ["download", "download file", "get file"], "handler": "_handle_download_file", "priority": 3},

    # Autonomous memory
    "memory_save": {"patterns": ["remember this", "save memory", "store memory", "note this"], "handler": "_handle_memory_save", "priority": 2},
    "memory_retrieve": {"patterns": ["recall memory", "check memory", "what do you remember", "retrieve memory"], "handler": "_handle_memory_retrieve", "priority": 2},
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
