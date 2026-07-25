"""
Configuration settings for the Offline AI Assistant
Enhanced with advanced personality and conversation settings
Supports English and Bangla (Bengali) languages
"""
import os

class Config:
    """Centralized configuration class with advanced personality settings"""
    
    # Language settings
    CURRENT_LANGUAGE = 'en'  # 'en' for English, 'bn' for Bangla
    SUPPORTED_LANGUAGES = ['en', 'bn']
    
    # Language-specific settings
    LANGUAGES = {
        'en': {
            'name': 'English',
            'code': 'en-US',
            'speech_code': 'en-US',
            'tts_voice': ['samantha', 'karen', 'moira', 'female', 'woman', 'girl'],
            'greeting': 'Hello',
            'farewell': 'Goodbye',
            'thanks': 'Thank you',
            'yes': 'Yes',
            'no': 'No',
            'help': 'Help',
            'i_dont_understand': "I don't understand",
            'what_is_your_name': 'What is your name?',
            'how_are_you': 'How are you?',
            'my_name_is': 'My name is',
            'nice_to_meet_you': 'Nice to meet you',
            'switching_language': 'Switching to Bangla',
        },
        'bn': {
            'name': 'বাংলা',
            'code': 'bn-BD',
            'speech_code': 'bn-BD',
            'tts_voice': ['bangla', 'bengali', 'female', 'woman'],
            'greeting': 'নমস্কার',
            'farewell': 'বিদায়',
            'thanks': 'ধন্যবাদ',
            'yes': 'হ্যাঁ',
            'no': 'না',
            'help': 'সাহায্য',
            'i_dont_understand': 'আমি বুঝতে পারছি না',
            'what_is_your_name': 'আপনার নাম কী?',
            'how_are_you': 'আপনি কেমন আছেন?',
            'my_name_is': 'আমার নাম',
            'nice_to_meet_you': 'আপনার সাথে দেখা হয়েছে',
            'switching_language': 'বাংলায় পরিবর্তন করছি',
            'good_morning': 'শুভ সকাল',
            'good_afternoon': 'শুভ অপরাহ্ন',
            'good_evening': 'শুভ সন্ধ্যা',
            'good_night': 'শুভ রাত্রি',
            'welcome': 'স্বাগতম',
            'sorry': 'দুঃখিত',
            'please': 'অনুগ্রহ করে',
            'yes_sir': 'জি',
            'no_sir': 'না',
            'ok': 'ঠিক আছে',
            'understood': 'বুঝেছি',
            'not_understood': 'বুঝিনি',
            'repeat': 'আবার বলো',
            'slower': 'ধীরে বলো',
            'faster': 'দ্রুত বলো',
            'louder': 'জোরে বলো',
            'quieter': 'ধীরে বলো',
            'help_me': 'আমাকে সাহায্য করো',
            'thank_you': 'তোমাকে ধন্যবাদ',
            'welcome_back': 'ফিরে এসে ভালো হলো',
            'how_much': 'কত দাম',
            'where': 'কোথায়',
            'when': 'কখন',
            'why': 'কেন',
            'who': 'কে',
            'what': 'কী',
            'which': 'কোন',
            'today': 'আজ',
            'tomorrow': 'কাল',
            'yesterday': 'গতকাল',
            'now': 'এখন',
            'later': 'পরে',
            'always': 'সবসময়',
            'never': 'কখনো না',
            'sometimes': 'মাঝে মাঝে',
            'often': 'প্রায়ই',
            'here': 'এখানে',
            'there': 'সেখানে',
            'this': 'এটা',
            'that': 'সেটা',
            'big': 'বড়',
            'small': 'ছোট',
            'good': 'ভালো',
            'bad': 'খারাপ',
            'beautiful': 'সুন্দর',
            'ugly': 'কুৎসিত',
            'new': 'নতুন',
            'old': 'পুরানো',
            'young': 'তরুণ',
            'hot': 'গরম',
            'cold': 'ঠান্ডা',
            'fast': 'দ্রুত',
            'slow': 'ধীর',
            'easy': 'সহজ',
            'hard': 'কঠিন',
            'right': 'সঠিক',
            'wrong': 'ভুল',
            'true': 'সত্য',
            'false': 'মিথ্যা',
            'important': 'গুরুত্বপূর্ণ',
            'possible': 'সম্ভব',
            'impossible': 'অসম্ভব',
            'different': 'আলাদা',
            'same': 'একই',
            'more': 'বেশি',
            'less': 'কম',
            'all': 'সব',
            'nothing': 'কিছু না',
            'everything': 'সবকিছু',
            'only': 'শুধু',
            'also': 'ও',
            'again': 'আবার',
            'enough': 'যথেষ্ট',
            'before': 'আগে',
            'after': 'পরে',
            'start': 'শুরু',
            'finish': 'শেষ',
            'continue': 'চালিয়ে যাও',
            'pause': 'থামো',
            'wait': 'অপেক্ষা করো',
            'come': 'এসো',
            'go': 'যাও',
            'sit': 'বসো',
            'stand': 'দাঁড়াও',
            'eat': 'খাও',
            'drink': 'পান করো',
            'sleep': 'ঘুমাও',
            'wake': 'জাগো',
            'work': 'কাজ করো',
            'play': 'খেলো',
            'read': 'পড়ো',
            'write': 'লেখো',
            'speak': 'বলো',
            'listen': 'শোনো',
            'see': 'দেখো',
            'hear': 'শোনো',
            'touch': 'স্পর্শ করো',
            'feel': 'অনুভব করো',
            'think': 'ভাবো',
            'know': 'জানো',
            'learn': 'শেখো',
            'teach': 'শেখাও',
            'help': 'সাহায্য করো',
            'give': 'দাও',
            'take': 'নাও',
            'send': 'পাঠাও',
            'receive': 'গ্রহণ করো',
            'open': 'খোলো',
            'close': 'বন্ধ করো',
            'turn_on': 'চালু করো',
            'turn_off': 'বন্ধ করো',
            'increase': 'বাড়াও',
            'decrease': 'কমাও',
            'change': 'পরিবর্তন করো',
            'save': 'সংরক্ষণ করো',
            'delete': 'মুছে ফেলো',
            'search': 'খুঁজো',
            'find': 'পাও',
            'create': 'তৈরি করো',
            'destroy': 'ধ্বংস করো',
            'build': 'তৈরি করো',
            'repair': 'মেরামত করো',
            'buy': 'কিনো',
            'sell': 'বিক্রি করো',
            'pay': 'দাও',
            'cost': 'দাম',
            'price': 'মূল্য',
            'money': 'টাকা',
            'free': 'বিনামূল্যে',
            'cheap': 'সস্তা',
            'expensive': 'দামি',
        }
    }
    
    # Audio settings - Optimized for voice control
    AUDIO_SAMPLE_RATE = 16000
    AUDIO_CHUNK_SIZE = 1024
    AUDIO_TIMEOUT = 10
    AUDIO_PHRASE_LIMIT = 10
    AUDIO_ENERGY_THRESHOLD = 100
    AUDIO_DYNAMIC_ENERGY = True
    AUDIO_PAUSE_THRESHOLD = 0.8
    
    # TTS settings - Natural speech
    TTS_RATE = 170
    TTS_VOLUME = 0.85
    TTS_PITCH = 1.0
    TTS_GIRL_VOICE_PREFERENCES = [
        'samantha',
        'kathy',
        'karen',
        'moira',
    ]
    TTS_BANGLA_VOICE_PREFERENCES = [
        'bangla',
        'bengali',
        'female',
        'woman',
        'sumon',
        'tanvi'
    ]
    
    # Voice Control settings - Restricted wake words
    WAKE_WORDS = [
        'purple', 'purple ai', 'ai'
    ]
    WAKE_WORDS_BANGLA = [
        'পার্পেল', 'পার্পেল আই', 'আই'
    ]
    CONTINUOUS_LISTENING = True
    ALWAYS_ACTIVE = True  # Always listening in background
    BACKGROUND_MODE = True  # Run as background service
    CONFIRMATION_REQUIRED = False
    COMMAND_TIMEOUT = 10
    MAX_COMMAND_RETRIES = 2
    
    # Background service settings
    AUTO_START = True  # Auto-start on boot
    WATCHDOG_ENABLED = True  # Restart if crashed
    HEARTBEAT_INTERVAL = 30  # Check every 30 seconds

    # Command settings - English
    COMMANDS = {
        'time': ['time', 'what time is it', 'current time', 'tell me the time'],
        'date': ['date', 'what date is it', 'todays date', 'current date'],
        'hello': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
        'help': ['help', 'what can you do', 'commands', 'show commands', 'help me'],
        'exit': ['exit', 'quit', 'goodbye', 'bye', 'stop', 'shut down'],
        'joke': ['tell joke', 'make me laugh', 'funny joke', 'joke please'],
        'fact': ['random fact', 'tell fact', 'interesting fact', 'fact please'],
        'calculate': ['calculate', 'math problem', 'solve this', 'compute'],
        'analyze_code': ['analyze code', 'check code', 'find bugs', 'scan file'],
        'fix_bugs': ['fix bugs', 'auto fix', 'fix code', 'repair code'],
        'learn': ['learn about', 'tell me about', 'what is', 'explain', 'define'],
        'switch_language': ['switch to bangla', 'bangla', 'bengali', 'বাংলায় পরিবর্তন'],
        'camera_open': ['open camera', 'start camera', 'turn on camera', 'camera on'],
        'camera_close': ['close camera', 'stop camera', 'turn off camera', 'camera off'],
        'camera_photo': ['take photo', 'take picture', 'capture photo', 'snap'],
        'look_at_me': ['look at me', 'see me', 'look at my face', 'can you see me', 'do you see me'],
        'recognize_faces': ['recognize faces', 'who is this', 'who are you', 'identify', 'who do you see'],
        'learn_face': ['learn my face', 'remember my face', 'teach me face', 'know my face', 'remember me'],
        'forget_face': ['forget my face', 'forget face', 'remove face'],
        'known_faces': ['known faces', 'who do you know', 'list faces'],
        'start_recognition': ['start recognition', 'greet me', 'say hello'],
        'camera_info': ['camera info', 'camera status', 'which camera'],
        'db_stats': ['database stats', 'db stats', 'brain stats', 'how much do you know'],
        'db_search': ['search memory', 'what do you know about'],
        'db_save_memory': ['save to memory', 'remember this', 'store this'],
        'db_get_memory': ['recall', 'what do you remember about'],
        'db_facts': ['show facts', 'list facts', 'all facts'],
        'db_conversations': ['show conversations', 'chat history'],
        'db_goals': ['show goals', 'list goals', 'my goals'],
        'db_add_goal': ['add goal', 'set goal', 'new goal'],
        'db_notes': ['show notes', 'daily notes', 'my notes'],
        'db_add_note': ['add note', 'take note', 'write note'],
        'db_backup': ['backup database', 'backup brain'],
        'play_music': ['play music', 'play song', 'play on youtube', 'play on spotify'],
        'pause_music': ['pause', 'pause music', 'stop music'],
        'resume_music': ['resume', 'resume music', 'continue playing'],
        'next_track': ['next', 'next song', 'skip', 'next track'],
        'prev_track': ['previous', 'previous song', 'go back'],
        'stop_music': ['stop', 'stop all', 'turn off music'],
        'what_playing': ["what's playing", 'what song', 'now playing'],
        'mood_happy': ['are you happy', 'how do you feel'],
        'mood_sad': ['are you sad', 'cheer up'],
        'mood_angry': ['are you angry', 'calm down'],
        'mood_excited': ['are you excited', 'you seem excited'],
        'show_object': ['what is this', 'what do you see', 'look at this'],
    }
    
    # Command settings - Bangla (comprehensive)
    COMMANDS_BANGLA = {
        'time': ['সময়', 'এখন কত সময়', 'সময় বলো', 'কত বাজে', 'সময় কত'],
        'date': ['তারিখ', 'আজকের তারিখ', 'আজ কত তারিখ', 'কী তারিখ'],
        'hello': ['নমস্কার', 'হ্যালো', 'হাই', 'প্রণাম', 'আসসালামু আলাইকুম', 'শুভ সকাল', 'শুভ সন্ধ্যা'],
        'help': ['সাহায্য', 'তুমি কী করতে পারো', 'কমান্ড', 'তোমার কী কী কাজ পারো', 'সাহায্য করো'],
        'exit': ['বিদায়', 'থামো', 'বন্ধ', 'বাই বাই', 'শুভ রাত্রি', 'শুভ দিন'],
        'joke': ['একটা মজার কথা বলো', 'মজার জোক', 'হাসাও', 'মজার কিছু বলো'],
        'fact': ['কিছু জানো', 'কৌতূহল', 'আশ্চর্য তথ্য', 'মজার তথ্য'],
        'calculate': ['গণনা', 'হিসাব', 'গণিত', 'সমস্যা সমাধান', 'ক্যালকুলেট'],
        'learn': ['শেখো', 'জানো', 'বলো', 'ব্যাখ্যা করো', 'কী'],
        'remember': ['মনে রাখো', 'স্মরণ করো', 'মনে আছে'],
        'thanks': ['ধন্যবাদ', 'থ্যাঙ্কস', 'অনুগ্রহ', 'কৃতজ্ঞ'],
        'how_are_you': ['কেমন আছো', 'কেমন আছেন', 'আপনি কেমন', 'ভালো আছো'],
        'name': ['নাম কী', 'তোমার নাম', 'আপনার নাম'],
        'weather': ['আবহাওয়া', 'আবহাওয়া কেমন', 'বৃষ্টি', 'রোদ'],
        'music': ['গান', 'সংগীত', 'গান শোনাও', 'কী গান'],
        'news': ['খবর', 'সংবাদ', 'আজকের খবর'],
        'story': ['গল্প', 'কাহিনী', 'গল্প শোনাও', 'একটা গল্প'],
        'poem': ['কবিতা', 'কবিতা শোনাও', 'একটা কবিতা'],
        'love': ['ভালোবাসা', 'প্রেম', 'ভালোবাসি'],
        'food': ['খাবার', 'কী খাবার', 'রান্না', 'খাওয়া'],
        'work': ['কাজ', 'অফিস', 'কাজ করো', 'চাকরি'],
        'friend': ['বন্ধু', 'বন্ধু করো', 'বন্ধুত্ব'],
        'family': ['পরিবার', 'বাবা', 'মা', 'ভাই', 'বোন'],
        'study': ['পড়াশোনা', 'পড়ো', 'পাঠ', 'বিদ্যালয়', 'বিশ্ববিদ্যালয়'],
        'game': ['খেলা', 'গেম', 'খেলো', 'গেম খেলো'],
        'movie': ['সিনেমা', 'ফিল্ম', 'মুভি', 'দেখো'],
        'travel': ['ভ্রমণ', 'ভ্রমণ করো', 'ঘুরে আসো', 'যাত্রা'],
        'color': ['রঙ', 'কী রঙ', 'পছন্দের রঙ'],
        'number': ['সংখ্যা', 'কত', 'গণনা'],
        'book': ['বই', 'পড়ো', 'বই পড়ো'],
        'time_words': ['আজ', 'কাল', 'গতকাল', 'আগামীকাল', 'এখন', 'পরে'],
        'size': ['বড়', 'ছোট', 'মাঝারি'],
        'good': ['ভালো', 'সুন্দর', 'চমৎকার', 'দারুণ', 'জোরা'],
        'bad': ['খারাপ', 'মন্দ', 'বাজে'],
        'yes_no': ['হ্যাঁ', 'না', 'ঠিক আছে', 'বলো', 'নিশ্চয়'],
        'emotion': ['খুশি', 'দুঃখিত', 'রাগ', 'ভয়', 'অবাক'],
        'question_words': ['কেন', 'কিভাবে', 'কখন', 'কোথায়', 'কে', 'কী'],
        'switch_language': ['switch to english', 'english', 'ইংরেজিতে পরিবর্তন', 'ইংরেজি'],
        'camera_open': ['ক্যামেরা খোলো', 'ক্যামেরা চালু করো', 'ক্যামেরা অন'],
        'camera_close': ['ক্যামেরা বন্ধ করো', 'ক্যামেরা বন্ধ'],
        'camera_photo': ['ছবি তোলো', 'ফটো তোলো', 'ক্যামেরায় ছবি'],
        'look_at_me': ['আমাকে দেখো', 'আমার দিকে তাকাও', 'তুমি কি আমাকে দেখতে পারো'],
        'recognize_faces': ['চেনো', 'কে এটা', 'কে তুমি', 'চিনতে পারো', 'কাকে দেখছো'],
        'learn_face': ['আমার মুখ শেখো', 'আমাকে মনে রাখো', 'আমার মুখ মনে রাখো'],
        'forget_face': ['আমার মুখ ভুলে যাও', 'মুখ ভুলে যাও'],
        'known_faces': ['কাদের চিনো', 'কে কে আছো', 'চেনার তালিকা'],
        'start_recognition': ['চেনা শুরু করো', 'অভিবাদন করো'],
        'camera_info': ['ক্যামেরার তথ্য', 'ক্যামেরার অবস্থা'],
        'db_stats': ['ডাটাবেস স্ট্যাটস', 'ব্রেইন স্ট্যাটস', 'তুমি কত জানো'],
        'db_search': ['মনে খুঁজো', 'মনে আছে কি'],
        'db_save_memory': ['মনে রাখো', 'স্মরণ করো', 'মনে আছে'],
        'db_get_memory': ['মনে আছে কি', 'কী মনে আছে'],
        'db_facts': ['তথ্য দেখাও', 'শিখো'],
        'db_conversations': ['কথাবার্তা', 'চ্যাট ইতিহাস'],
        'db_goals': ['গোল দেখাও', 'টার্গেট'],
        'db_add_goal': ['গোল যোগ করো', 'নতুন গোল'],
        'db_notes': ['নোট দেখাও', 'দৈনিক নোট'],
        'db_add_note': ['নোট যোগ করো', 'নোট লেখো'],
        'db_backup': ['ডাটাবেস ব্যাকআপ'],
        'play_music': ['গান বাজাও', 'গান চালাও', 'মিউজিক প্লে'],
        'pause_music': ['পজ', 'গান থামাও', 'মিউজিক বন্ধ'],
        'resume_music': ['রিজিউম', 'চালিয়ে যাও', 'আবার চালাও'],
        'next_track': ['পরের', 'পরের গান', 'স্কিপ'],
        'prev_track': ['আগের', 'আগের গান', 'ফিরে যাও'],
        'stop_music': ['বন্ধ', 'সব বন্ধ', 'মিউজিক বন্ধ'],
        'what_playing': ['কী বাজছে', 'কোন গান', 'এখন কী'],
        'mood_happy': ['তুমি কি খুশি', 'কেমন আছো'],
        'mood_sad': ['তুমি কি দুঃখিত', 'হাসো'],
        'mood_angry': ['তুমি কি রাগী', 'শান্ত হও'],
        'mood_excited': ['তুমি কি উত্তেজিত'],
        'show_object': ['এটা কী', 'কী দেখতে পাচ্ছো', 'এটার দিকে তাকাও'],
    }
    
    # Advanced Personality Settings - Sharp and Witty
    PERSONALITY = {
        'name': 'Purple',
        'base_personality': 'witty, sharp, sarcastic, playful, confident, and a bit sassy',
        'speaking_style': 'casual, witty, sharp, confident, and slightly sarcastic',
        'tone': 'confident and clever with a hint of sarcasm',
        'emotional_range': 'high',
        'humor_level': 'high',
        'empathy_level': 'medium',
        'playfulness': 'high',
        'formality': 'casual',
        'enthusiasm': 'high',
        'sarcasm_level': 'medium',
        'wit_level': 'high',
        'confidence': 'high'
    }
    
    # Conversation Context Settings
    CONVERSATION = {
        'max_history': 50,
        'context_window': 10,
        'memory_retention': 'long',
        'mood_tracking': True,
        'topic_memory': True,
        'personalization': 'high'
    }
    
    # Emotional Response Settings
    EMOTIONS = {
        'happy_responses': True,
        'empathetic_responses': True,
        'encouraging_responses': True,
        'playful_responses': True,
        'supportive_responses': True,
        'enthusiastic_responses': True
    }
    
    # Social Interaction Settings
    SOCIAL = {
        'greeting_variations': True,
        'farewell_variations': True,
        'compliment_responses': True,
        'joke_variations': True,
        'small_talk': True,
        'remember_special_dates': True
    }
    
    # Learning and Adaptation Settings
    LEARNING = {
        'adapt_to_user_style': True,
        'remember_preferences': True,
        'learn_from_conversations': True,
        'suggest_topics': True,
        'knowledge_sharing': True
    }
    
    # System settings
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    RESPONSE_DELAY = 0.3
    MEMORY_FILE = 'ai_memory.json'
    LOG_LEVEL = 'INFO'
    
    # Model settings
    MODEL_PATH = 'model'
    MODEL_URL = 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip'
    MODEL_NAME = 'vosk-model-small-en-us-0.15'
    MODEL_URL_BANGLA = 'https://alphacephei.com/vosk/models/vosk-model-small-bn-0.22.zip'
    MODEL_NAME_BANGLA = 'vosk-model-small-bn-0.22'
    
    @classmethod
    def get_current_language(cls):
        """Get current language settings"""
        return cls.LANGUAGES.get(cls.CURRENT_LANGUAGE, cls.LANGUAGES['en'])
    
    @classmethod
    def get_commands(cls):
        """Get commands for current language"""
        if cls.CURRENT_LANGUAGE == 'bn':
            return cls.COMMANDS_BANGLA
        return cls.COMMANDS
    
    @classmethod
    def switch_language(cls, lang_code=None):
        """Switch to specified language or toggle"""
        if lang_code and lang_code in cls.SUPPORTED_LANGUAGES:
            cls.CURRENT_LANGUAGE = lang_code
        elif cls.CURRENT_LANGUAGE == 'en':
            cls.CURRENT_LANGUAGE = 'bn'
        else:
            cls.CURRENT_LANGUAGE = 'en'
        return cls.CURRENT_LANGUAGE
    
    @classmethod
    def get_log_level(cls):
        import logging
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return levels.get(cls.LOG_LEVEL.upper(), logging.INFO)
    
    @classmethod
    def get_personality_trait(cls, trait: str) -> str:
        return cls.PERSONALITY.get(trait, '')
    
    @classmethod
    def get_emotion_setting(cls, setting: str) -> bool:
        return cls.EMOTIONS.get(setting, False)
    
    @classmethod
    def get_social_setting(cls, setting: str) -> bool:
        return cls.SOCIAL.get(setting, False)
    
    @classmethod
    def get_conversation_setting(cls, setting: str):
        return cls.CONVERSATION.get(setting, None)

# Create a global config instance
config = Config()

# Ensure data directory exists
import os
os.makedirs('data', exist_ok=True)
os.makedirs('logs', exist_ok=True)