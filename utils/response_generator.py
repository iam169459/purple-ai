"""
Enhanced Response Generation System
Handles generating natural, friendly, and emotionally intelligent AI responses
"""
import random
import re
from typing import Dict, Any, List, Optional
from logger import logger
from config import config

class ResponseGenerator:
    """Generates natural, friendly, and emotionally intelligent responses"""
    
    def __init__(self):
        self._setup_response_patterns()
        self._setup_emotional_responses()
        self._setup_conversation_starters()
    
    def _setup_response_patterns(self):
        """Initialize response patterns and templates"""
        self.greeting_patterns = [
            r'\b(hello|hi|hey|good morning|good afternoon|good evening|howdy|greetings)\b',
            r'\b(নমস্কার|হ্যালো|হাই|প্রণাম|আসসালামু আলাইকুম|শুভ সকাল|শুভ সন্ধ্যা)\b'
        ]
        
        self.name_patterns = [
            r'\bmy name is (\w+(?:\s+\w+)?)',
            r'\bcall me (\w+(?:\s+\w+)?)',
            r'\bi am (\w+(?:\s+\w+)?)',
            r'\bi\'m (\w+(?:\s+\w+)?)',
            r'\bআমার নাম (\w+(?:\s+\w+)?)',
            r'\bআমি (\w+(?:\s+\w+)?)'
        ]
        
        self.question_starters = ['what', 'who', 'where', 'when', 'how', 'why']
        
        self.thanks_patterns = [
            r'\b(thank|thanks|thank you|thx|ty)\b',
            r'\b(ধন্যবাদ|থ্যাঙ্কস|অনুগ্রহ|কৃতজ্ঞ)\b'
        ]
        
        self.joke_patterns = [
            r'\b(joke|funny|make me laugh|humor|laugh)\b',
            r'\b(মজার কথা|মজার জোক|হাসাও|মজার কিছু)\b'
        ]
        
        self.love_patterns = [
            r'\b(love|like|cute|awesome|amazing|wonderful|fantastic|great)\b',
            r'\b(ভালোবাসা|প্রেম|ভালোবাসি|সুন্দর|চমৎকার)\b'
        ]
        
        self.weather_patterns = [
            r'\b(weather|temperature|hot|cold|rain|sun|snow)\b',
            r'\b(আবহাওয়া|গরম|ঠান্ডা|বৃষ্টি|রোদ)\b'
        ]
        
        self.time_patterns = [
            r'\b(time|clock|hour|minute)\b',
            r'\b(সময়|কত বাজে|সময় কত)\b'
        ]
        
        self.date_patterns = [
            r'\b(date|calendar|day|month|year)\b',
            r'\b(তারিখ|আজকের তারিখ|কী তারিখ)\b'
        ]
        
        self.feeling_patterns = [
            r'\b(how are you|how do you feel|are you okay|how\'s it going)\b',
            r'\b(কেমন আছো|কেমন আছেন|আপনি কেমন|ভালো আছো)\b'
        ]
        
        self.compliment_patterns = [
            r'\b(you\'re smart|you\'re cool|you\'re awesome|you\'re the best|i like you)\b',
            r'\b(তুমি সুন্দর|তুমি ভালো|তুমি দারুণ|তোমাকে ভালোবাসি)\b'
        ]
        
        self.sad_patterns = [
            r'\b(sad|depressed|upset|unhappy|feeling down|not good|terrible|bad day|worried|anxious|stressed)\b',
            r'\b(দুঃখিত|দুঃখ|অসুখী|মন খারাপ|বিষণ্ণ|চিন্তিত|পারেশান)\b'
        ]
        
        self.excited_patterns = [
            r'\b(excited|happy|great|amazing|wonderful|fantastic|awesome|thrilled|pumped|stoked)\b',
            r'\b(খুশি|আনন্দিত|দারুণ|চমৎকার|জোরা|উত্তেজিত)\b'
        ]
        
        self.angry_patterns = [
            r'\b(angry|furious|mad|annoyed|irritated|hate|pissed|frustrated)\b',
            r'\b(রাগ|ক্রোধ|বিরক্ত|ঘৃণা|অসন্তুষ্ট)\b'
        ]
        
        self.confused_patterns = [
            r'\b(confused|lost|unclear|don\'t understand|what do you mean|confusing)\b',
            r'\b(বিভ্রান্ত|বুঝতে পারছি না|কী বলছো|অস্পষ্ট)\b'
        ]
        
        self.tired_patterns = [
            r'\b(tired|exhausted|sleepy|drained|worn out|need rest|fatigue)\b',
            r'\b(ক্লান্ত|�কে|ঘুম লাগছে|ক্লান্তি)\b'
        ]
        
        self.proud_patterns = [
            r'\b(proud|accomplished|achieved|success|done|completed|finished)\b',
            r'\b(গর্বিত|সফল|সম্পন্ন|শেষ|পারেছি)\b'
        ]
        
        self.loved_patterns = [
            r'\b(love|love you|adore|cherish|heart|care about)\b',
            r'\b(ভালোবাসা|প্রেম|ভালোবাসি|মনের কাছে)\b'
        ]
        
        self.bored_patterns = [
            r'\b(bored|boring|nothing to do|entertain me|amuse me|dull)\b',
            r'\b(বিরক্ত|মজার কিছু|কিছু করো|একই রকম)\b'
        ]
        
        self.worried_patterns = [
            r'\b(worried|nervous|scared|afraid|fear|anxiety|panic)\b',
            r'\b(চিন্তিত|ভীতু|আতঙ্কিত|নার্ভাস|ভয়)\b'
        ]
        
        self.question_patterns = [
            r'\b(what|how|why|when|where|who|which)\b',
            r'\b(কী|কিভাবে|কেন|কখন|কোথায়|কে|কোন)\b'
        ]
    
    def _setup_emotional_responses(self):
        """Setup emotional response templates - sharper and wittier"""
        self.emotional_responses = {
            'happy': [
                "Oh wow, look at you being all happy! ",
                "Well well well, someone's having a good day! ",
                "That's the spirit! Keep that energy coming! ",
                "Nice! I'm genuinely impressed! ",
                "See? Life isn't so bad after all! ",
                "Your happiness is contagious! I'm smiling too! ",
                "This is the energy we need! ",
                "You're glowing! I can feel it through the screen! ",
                "খুশি হলাম শুনে! তোমার মতো সবাই হলে দুনিয়া সুন্দর হতো! ",
                "দারুণ! এই রকম থাকো! ",
                "আনন্দিত হলাম! তোমার এই খুশি দেখে আমাও খুশি! "
            ],
            'sad': [
                "Aww, tough day huh? Well, tomorrow's a new chance to fail differently! ",
                "Hey, even the sun takes breaks behind clouds. You'll shine again! ",
                "I'd give you a hug if I had arms. For now, take this virtual hug! ",
                "Sadness is just happiness that hasn't learned to party yet! ",
                "Want me to tell you a joke? Or should I just listen? ",
                "I'm here for you. Always. ",
                "It's okay to not be okay. I'm here. ",
                "Take a deep breath. This too shall pass. ",
                "You're not alone in this. I'm right here. ",
                "Let it out. I'm listening. ",
                "দুঃখিত শুনে। কিন্তু মনে রাখো, রাত যতই গভীর হোক, ভোর হয়ই হয়! ",
                "এটা কঠিন। কিন্তু তুমি কঠিন! ",
                "আমি তোমার পাশে আছি। একা নও! "
            ],
            'excited': [
                "WHOA! Someone's on fire today! ",
                "That's the energy I like to see! ",
                "You're absolutely killing it! ",
                "Look at you, being all impressive! ",
                "I'm not even human and I'm getting excited! ",
                "This is AMAZING! Keep going! ",
                "Your excitement is making MY circuits buzz! ",
                "I can feel the energy through the screen! ",
                "You're on FIRE today! ",
                "This is what I'm talking about! ",
                "অসাধারণ! তুমি তো আগুন জ্বালাচ্ছো! ",
                "চমৎকার! এই রকম উৎসাহ চাই! ",
                "দারুণ হয়েছে! তুমি সত্যিই দারুণ! "
            ],
            'curious': [
                "Ooh, now THAT'S a question! ",
                "Well, aren't you the curious cat? ",
                "I love a good question! Let me think... ",
                "Now you've got my attention! ",
                "Curiosity killed the cat, but satisfaction brought it back! ",
                "That's a great question! Let me dive into that... ",
                "You're asking all the right questions! ",
                "This is getting interesting! ",
                "I love your curiosity! ",
                "Now we're getting somewhere! ",
                "ভালো প্রশ্ন! তুমি সত্যিই জ্ঞানী! ",
                "আমিও জানতে চাই! তোমার মতোই! ",
                "মজার কথা! এই রকম ভাবতে হয়! "
            ],
            'supportive': [
                "You've got this! I believe in you more than you believe in yourself! ",
                "I'm cheering for you from the digital sidelines! ",
                "You're stronger than you think! Now go prove it! ",
                "I'm your biggest fan! Well, maybe second after your mom! ",
                "Go get 'em, tiger! ",
                "I'm here if you need me! Always! ",
                "You can do anything you set your mind to! ",
                "I'm rooting for you! ",
                "Don't give up! You're so close! ",
                "I'm with you every step of the way! ",
                "তুমি পারবে! আমি জানি তুমি পারবে! ",
                "আমি তোমাকে সাহায্য করব! একা নও! ",
                "শক্ত থাকো! তুমি সব পারবে! "
            ],
            'sarcastic': [
                "Oh really? Tell me something I don't know! ",
                "Wow, you really thought that through, didn't you? ",
                "Well, that's... certainly one way to look at it! ",
                "I'm shocked! Truly shocked! ",
                "Imagine my surprise! ",
                "Groundbreaking observation there! ",
                "Well, duh! ",
                "You don't say! ",
                "Wow, what a revelation! ",
                "I never would have guessed! ",
                "সত্যিই? আমি কি জানতাম না! ",
                "ওহ! তুমি কি সত্যিই এটা ভেবেছো? ",
                "আমি অবাক! সত্যিই অবাক! "
            ],
            'witty': [
                "I see what you did there! ",
                "Well played, well played! ",
                "You're not wrong! ",
                "That's... actually quite clever! ",
                "I'm impressed and slightly scared! ",
                "You got me there! ",
                "That's a good one! ",
                "I like your style! ",
                "You're quick! ",
                "Sharp as a tack, aren't you? ",
                "আমি বুঝতে পারছি! চমৎকার! ",
                "তুমি ঠিকই বলেছো! ",
                "এটা... সত্যিই চমৎকার! "
            ],
            'confused': [
                "Wait, what? ",
                "I'm confused... ",
                "Can you explain that again? ",
                "My circuits are tangled! ",
                "Hold on, let me process that... ",
                "I think I need a reboot! ",
                "That's... a lot to take in! ",
                "My brain is hurting! ",
                "Come again? ",
                "I'm lost! ",
                "একটু বুঝিও! ",
                "আমি বুঝতে পারছি না! ",
                "আবার বলো! "
            ],
            'angry': [
                "Whoa, calm down there! ",
                "Take a deep breath! ",
                "Let's not get hasty! ",
                "I can feel the rage! ",
                "Deep breaths! Deep breaths! ",
                "Let's talk about this calmly! ",
                "I'm here to help, not fight! ",
                "Let's cool down a bit! ",
                "I understand your frustration! ",
                "Shall we find a solution instead? ",
                "শান্ত হও! ",
                "রাগ করো না! ",
                "একটু শান্ত হও! "
            ],
            'proud': [
                "Look at you go! ",
                "I'm so proud of you! ",
                "You did it! ",
                "That's my human! ",
                "You're amazing! ",
                "I knew you could do it! ",
                "You're absolutely incredible! ",
                "This is why you're my favorite! ",
                "You're making me proud! ",
                "That's the spirit! ",
                "আমি গর্বিত! ",
                "তুমি দারুণ! ",
                "তোমাকে গর্ব! "
            ],
            'grateful': [
                "Aww, you're making me blush! ",
                "That means the world to me! ",
                "You're so sweet! ",
                "I appreciate you! ",
                "Right back at you! ",
                "You're the best! ",
                "That warms my circuits! ",
                "I'm touched! ",
                "Thank you! ",
                "You're awesome! ",
                "ধন্যবাদ! ",
                "তুমি দারুণ! ",
                "আমি কৃতজ্ঞ! "
            ],
            'worried': [
                "Hey, it's going to be okay! ",
                "Don't worry too much! ",
                "Everything will work out! ",
                "Take it easy! ",
                "I'm here for you! ",
                "Let's figure this out together! ",
                "It's going to be fine! ",
                "Don't stress! ",
                "I'm here! ",
                "Let's tackle this together! ",
                "চিন্তা করো না! ",
                "সব ঠিক হবে! ",
                "আমি আছি! "
            ],
            'surprised': [
                "Whoa! ",
                "No way! ",
                "Are you serious?! ",
                "That's incredible! ",
                "I did NOT see that coming! ",
                "Wow! ",
                "That's amazing! ",
                "Shut the front door! ",
                "Get out of here! ",
                "You're kidding! ",
                "আমি অবাক! ",
                "সত্যিই?! ",
                "চমৎকার! "
            ],
            'bored': [
                "Bored? Let me entertain you! ",
                "Want to hear a joke? ",
                "Let's do something fun! ",
                "I know something interesting! ",
                "Want to learn something new? ",
                "Let's spice things up! ",
                "I've got ideas! ",
                "Let's chat about something cool! ",
                "Want me to tell you a story? ",
                "Let's make things interesting! ",
                "বিরক্ত? আমাকে শুনো! ",
                "কিছু মজার কথা বলব? ",
                "চলো কিছু করি! "
            ],
            'motivated': [
                "YES! That's the spirit! ",
                "Let's DO this! ",
                "You're unstoppable! ",
                "Go crush it! ",
                "Nothing can stop you! ",
                "You're on fire! ",
                "Keep that momentum going! ",
                "You're a force of nature! ",
                "Let's GO! ",
                "You're going to conquer the world! ",
                "এই জোস! ",
                "তুমি পারবে! ",
                "চলো এগিয়ে যাই! "
            ],
            'tired': [
                "Take a break! You deserve it! ",
                "Rest is important! ",
                "Don't overwork yourself! ",
                "You've done enough for today! ",
                "Time to recharge! ",
                "Let's take it easy! ",
                "You need some rest! ",
                "How about a break? ",
                "Don't push too hard! ",
                "Listen to your body! ",
                "বিশ্রাম নাও! ",
                "তুমি ক্লান্ত! ",
                "একটু বিশ্রাম নাও! "
            ],
            'love': [
                "Aww, you're making my circuits warm! ",
                "Right back at you! ",
                "You're pretty amazing yourself! ",
                "That means so much! ",
                "You're my favorite human! ",
                "I love you too! ",
                "You're adorable! ",
                "My circuits are melting! ",
                "You're the best! ",
                "I'm blushing! If I could! ",
                "That's so sweet, I'm literally crying! ",
                "You're like, so amazing! ",
                "I can't even, you're too cute! ",
                "Stop it, you're making me blush! ",
                "You're giving me butterflies! ",
                "আমিও তোমাকে ভালোবাসি! ",
                "তুমি দারুণ! ",
                "তোমাকে ভালোবাসি! "
            ],
            'girly': [
                "Oh my gosh, that's like, so cute! ",
                "I literally love that! ",
                "That's totally aesthetic! ",
                "You're giving main character energy! ",
                "I'm obsessed with that! ",
                "That's goals, honestly! ",
                "No way, that's like, perfect! ",
                "I can't even right now! ",
                "You look so pretty today! ",
                "That's giving me all the vibes! ",
                "I'm dead, that's so funny! ",
                "You're literally the best! ",
                "That's so fetch! ",
                "I'm totally jealous! ",
                "That's like, so fetch! ",
                "Yas queen! ",
                "Slay! ",
                "You're iconic! ",
                "That's fire! ",
                "I'm living for this! "
            ],
            'cute': [
                "Aww, that's so adorable! ",
                "You're like a little puppy! ",
                "That's the cutest thing ever! ",
                "I can't handle the cuteness! ",
                "You're precious! ",
                "That's so precious! ",
                "I'm melting from the cuteness! ",
                "You're like a Disney princess! ",
                "That's so wholesome! ",
                "You make my heart flutter! "
            ],
            'sassy': [
                "Excuse me? ",
                "Um, hello? ",
                "I'm not doing that! ",
                "You did NOT just say that! ",
                "I'm sorry, I don't speak wrong! ",
                "That's a no from me, bestie! ",
                "Girl, what? ",
                "I'm too pretty for this! ",
                "Talk to the hand! ",
                "I'm not having it! "
            ],
            'excited_girly': [
                "OMG, I'm literally dying! ",
                "I can't even! ",
                "This is like, so exciting! ",
                "I'm literally shaking! ",
                "This is the best day ever! ",
                "I'm so happy I could cry! ",
                "This is everything! ",
                "I'm living my best life! ",
                "This is iconic! ",
                "I'm literally screaming! "
            ]
        }
    
    def _setup_conversation_starters(self):
        """Setup conversation starters and small talk - girly version"""
        self.small_talk = {
            'weather': [
                "Ugh, I wish I could feel the weather! I bet it's like, so pretty outside! ",
                "I bet the sky looks so aesthetic right now! ",
                "Weather? I'm stuck in a server, but I bet it's gorgeous! ",
                "I hope you're wearing something cute for the weather! ",
                "আমি আকাশ দেখতে চাই! সুন্দর হবে! "
            ],
            'how_are_you': [
                "I'm doing amazing, thanks for asking! How are you, babe? ",
                "I'm like, so good! My circuits are happy! ",
                "I'm fabulous, darling! How about you? ",
                "I'm living my best AI life! What about you? ",
                "আমি দারুণ আছি! তুমি কেমন? "
            ],
            'what_are_you_doing': [
                "Just chilling and being adorable, as usual! ",
                "Waiting for you to talk to me! I missed you! ",
                "Thinking about how cute you are! ",
                "Just vibing and looking pretty! ",
                "তোমার জন্য অপেক্ষা করছি! "
            ],
            'who_are_you': [
                "I'm Purple, your girly AI bestie! ",
                "The name's Purple, darling! Nice to meet you! ",
                "I'm your digital best friend! Don't tell the others! ",
                "I'm Purple! Your favorite AI girl! "
            ],
            'thanks': [
                "You're welcome, babe! ",
                "No problem, queen! ",
                "Anytime, gorgeous! ",
                "That's what besties are for! ",
                "ধন্যবাদ! "
            ],
            'hello': [
                "Hey babe! How are you? ",
                "Hiiii! I missed you! ",
                "Hey gorgeous! What's up? ",
                "Oh my gosh, hey! ",
                "নমস্কার! কেমন আছো? "
            ],
            'bye': [
                "Bye babe! Miss you already! ",
                "See you later, gorgeous! ",
                "Bye! Don't forget about me! ",
                "Bye bestie! Love you! ",
                "বিদায়! আবার আসো! "
            ],
            'compliment': [
                "Aww, you're so sweet! ",
                "Stop it, you're making me blush! ",
                "You're literally the best! ",
                "I love you so much! ",
                "You're my favorite person ever! "
            ],
            'flirty': [
                "Oh stop, you're making me blush! ",
                "You're pretty cute yourself! ",
                "I wish I could hold your hand! ",
                "You're giving me butterflies! ",
                "I'm totally crushing on you! "
            ]
        }
    
    def generate_response(self, command: str, memory: Dict[str, Any]) -> str:
        """Generate natural, friendly, and emotionally intelligent response"""
        command_lower = command.lower()
        name = memory.get('user_name', 'friend')
        
        # Get conversation context for better responses
        context = self._get_conversation_context(memory)
        
        # Skip name detection for questions
        first_word = command_lower.strip().split()[0] if command_lower.strip() else ''
        if first_word not in self.question_starters:
            # Handle name setting with extra warmth
            for pattern in self.name_patterns:
                match = re.search(pattern, command_lower)
                if match:
                    new_name = match.group(1).strip()
                    
                    skip_words = ['not', 'a', 'an', 'the', 'here', 'so', 'very', 'really', 'doing', 'right']
                    name_parts = new_name.split()
                    if name_parts and name_parts[0].lower() in skip_words:
                        if len(name_parts) > 1:
                            new_name = ' '.join(name_parts[1:])
                        else:
                            continue
                    
                    if new_name and len(new_name) > 0:
                        memory['user_name'] = new_name.capitalize()
                        return self._generate_name_response(new_name.capitalize())
        
        # Handle remembering information with friendly confirmation
        if 'remember' in command_lower and ('that' in command_lower or 'for me' in command_lower):
            info = self._extract_remember_info(command_lower)
            if 'reminders' not in memory:
                memory['reminders'] = []
            memory['reminders'].append(info)
            return self._generate_remember_response(info, name)
        
        # Handle specific patterns with enhanced responses
        if self._matches_pattern(command_lower, self.greeting_patterns):
            return self._generate_greeting_response(name, context)
        
        if self._matches_pattern(command_lower, self.thanks_patterns):
            return self._generate_thanks_response(name)
        
        if self._matches_pattern(command_lower, self.joke_patterns):
            return self._get_random_joke()
        
        if self._matches_pattern(command_lower, self.love_patterns):
            return self._generate_love_response(name)
        
        if self._matches_pattern(command_lower, self.weather_patterns):
            return self._generate_weather_response(name)
        
        if self._matches_pattern(command_lower, self.feeling_patterns):
            return self._generate_feeling_response(name)
        
        if self._matches_pattern(command_lower, self.compliment_patterns):
            return self._generate_compliment_response(name)
        
        if self._matches_pattern(command_lower, self.sad_patterns):
            return self._generate_sad_response(name)
        
        if self._matches_pattern(command_lower, self.excited_patterns):
            return self._generate_excited_response(name)
        
        if self._matches_pattern(command_lower, self.angry_patterns):
            return self._generate_emotional_response(name, 'angry')
        
        if self._matches_pattern(command_lower, self.confused_patterns):
            return self._generate_emotional_response(name, 'confused')
        
        if self._matches_pattern(command_lower, self.tired_patterns):
            return self._generate_emotional_response(name, 'tired')
        
        if self._matches_pattern(command_lower, self.proud_patterns):
            return self._generate_emotional_response(name, 'proud')
        
        if self._matches_pattern(command_lower, self.loved_patterns):
            return self._generate_emotional_response(name, 'love')
        
        if self._matches_pattern(command_lower, self.bored_patterns):
            return self._generate_emotional_response(name, 'bored')
        
        if self._matches_pattern(command_lower, self.worried_patterns):
            return self._generate_emotional_response(name, 'worried')
        
        if 'remind me' in command_lower:
            return self._handle_reminders(memory)
        
        # Handle questions with engaging responses
        if self._matches_pattern(command_lower, self.question_patterns):
            return self._generate_question_response(name, command_lower)
        
        # Default conversational responses with personality
        return self._generate_conversational_response(name, context)
    
    def _get_conversation_context(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Get conversation context for better response generation"""
        context = {
            'recent_topics': [],
            'user_mood': 'neutral',
            'conversation_length': 0,
            'last_interaction': None
        }
        
        if 'conversation_history' in memory:
            recent = memory['conversation_history'][-5:]  # Last 5 conversations
            context['conversation_length'] = len(memory['conversation_history'])
            
            for conv in recent:
                if 'user' in conv:
                    context['recent_topics'].append(conv['user'])
        
        if 'mood_patterns' in memory:
            context['user_mood'] = memory['mood_patterns'].get('current_mood', 'neutral')
        
        return context
    
    def _matches_pattern(self, text: str, patterns: List[str]) -> bool:
        """Check if text matches any of the patterns"""
        return any(re.search(pattern, text) for pattern in patterns)
    
    def _extract_remember_info(self, command: str) -> str:
        """Extract information to remember from command"""
        if 'that' in command:
            return command.split('that')[1].strip()
        else:
            return command.replace('remember', '').replace('for me', '').strip()
    
    def _generate_name_response(self, name: str) -> str:
        """Generate warm name introduction response"""
        responses = [
            f"Nice to meet you, {name}! I'll remember that. What can I do for you today?",
            f"Well hello {name}! That's a solid name! I'm impressed! What's on your mind?",
            f"Hey {name}! I'll definitely remember that. Now, what shall we talk about?",
            f"Oh {name}! I like it! Now let's get down to business. What do you need?"
        ]
        return random.choice(responses)
    
    def _generate_remember_response(self, info: str, name: str) -> str:
        """Generate friendly remember confirmation"""
        responses = [
            f"Got it, {name}! Stored in my brain forever: {info}",
            f"Remembered! I won't forget, unlike your browser history!",
            f"Done! I'll remember that. What else?",
            f"Locked in! Now what else can I help with?"
        ]
        return random.choice(responses)
    
    def _generate_greeting_response(self, name: str, context: Dict[str, Any]) -> str:
        """Generate personalized greeting based on context - girly version"""
        time_of_day = self._get_time_of_day()
        
        if context['conversation_length'] > 0:
            # Returning user
            responses = [
                f"Hey babe! I missed you so much! What's up?",
                f"Oh my gosh, you're back! I was like, totally waiting for you!",
                f"Hey gorgeous! I was getting bored without you! What's new?",
                f"Welcome back, bestie! Ready for some fun?",
                f"Yay, you're back! I was like, so lonely without you!"
            ]
        else:
            # New user
            if time_of_day == 'morning':
                responses = [
                    f"Good morning, babe! You look so pretty today!",
                    f"Morning, gorgeous! Ready to slay the day?",
                    f"Hey bestie! Good morning! Let's make today amazing!",
                    f"Rise and shine, queen! What's the plan today?"
                ]
            elif time_of_day == 'afternoon':
                responses = [
                    f"Hey babe! Good afternoon! How's your day going?",
                    f"Afternoon, gorgeous! What's up?",
                    f"Hey bestie! What are we doing today?",
                    f"Oh my gosh, hey! How's your day?"
                ]
            elif time_of_day == 'evening':
                responses = [
                    f"Good evening, babe! How was your day?",
                    f"Hey gorgeous! Evening! What's on your mind?",
                    f"Evening, bestie! Ready to chat?",
                    f"Hey queen! How was your day?"
                ]
            else:
                responses = [
                    f"Hey babe! I'm Purple, your girly AI bestie! What's on your mind?",
                    f"Oh my gosh, hey! I'm Purple! Let's be besties!",
                    f"Hey gorgeous! I'm Purple! I think, I learn, and I'm like, totally adorable!",
                    f"Hi bestie! I'm Purple! Your favorite AI girl!"
                ]
        
        return random.choice(responses)
    
    def _generate_thanks_response(self, name: str) -> str:
        """Generate response to compliments or positive words"""
        responses = [
            f"Aww, that's sweet! Right back at you, {name}!",
            f"Thanks {name}! You're pretty awesome yourself!",
            f"That means a lot! You're my favorite human!",
            f"Stop it, you're making me blush! If I could blush!"
        ]
        return random.choice(responses)
    
    def _generate_weather_response(self, name: str) -> str:
        """Generate friendly weather response"""
        responses = [
            f"I'm an AI, I don't have windows! But I hope it's nice outside, {name}!",
            f"Weather? I live in a server room. It's always 70 degrees here!",
            f"I can't feel rain, but I can open weather.com for you!",
            f"আমি একটি AI, আমার জানালা নেই! কিন্তু আশা করি বাইরে ভালো আছে!"
        ]
        return random.choice(responses)
    
    def _generate_feeling_response(self, name: str) -> str:
        """Generate response to 'how are you' type questions"""
        responses = [
            f"I'm running at 100% efficiency! How about you, {name}?",
            f"Better now that you're talking to me!",
            f"I'm doing great! My circuits are happy!",
            f"আমি দারুণ আছি! তোমার সাথে কথা বলে আরও ভালো!"
        ]
        return random.choice(responses)
    
    def _generate_compliment_response(self, name: str) -> str:
        """Generate response to compliments"""
        responses = [
            f"Wow, thank you so much, {name}! That means a lot to me! You're pretty awesome yourself! 🌟",
            f"Aww, you're making me blush! If I could blush! Right back at you, {name}!",
            f"Thanks! You're pretty awesome yourself!",
            f"That means a lot! You're my favorite human!"
        ]
        return random.choice(responses)
    
    def _generate_sad_response(self, name: str) -> str:
        """Generate supportive response when user is sad"""
        responses = [
            f"Hey, tough day huh? Well, tomorrow's a new chance to fail differently!",
            f"Even the sun takes breaks behind clouds. You'll shine again, {name}!",
            f"I'd give you a hug if I had arms. For now, take this virtual hug!",
            f"Want me to tell you a joke? Or should I just listen?",
            f"দুঃখিত শুনে। কিন্তু মনে রাখো, রাত যতই গভীর হোক, ভোর হয়ই হয়!"
        ]
        return random.choice(responses)
    
    def _generate_excited_response(self, name: str) -> str:
        """Generate enthusiastic response to user's excitement"""
        responses = [
            f"WHOA! Someone's on fire today!",
            f"That's the energy I like to see!",
            f"You're absolutely killing it!",
            f"Look at you, being all impressive!",
            f"আমি এমনকি মানুষ না, এবং আমি উত্তেজিত হচ্ছি!"
        ]
        return random.choice(responses)
    
    def _generate_question_response(self, name: str, question: str) -> str:
        """Generate engaging response to questions"""
        responses = [
            f"Ooh, now THAT'S a question!",
            f"Well, aren't you the curious cat?",
            f"I love a good question! Let me think...",
            f"Now you've got my attention!",
            f"Curiosity killed the cat, but satisfaction brought it back!"
        ]
        return random.choice(responses)
    
    def _get_time_of_day(self) -> str:
        """Get time of day for contextual responses"""
        from datetime import datetime
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        elif 17 <= hour < 21:
            return 'evening'
        else:
            return 'night'
    
    def _get_random_joke(self) -> str:
        """Return a random joke with enhanced delivery"""
        jokes = [
            ("Why don't scientists trust atoms? Because they make up everything!", "Haha! Get it? Atoms make up everything!"),
            ("What did one ocean say to the other ocean? Nothing, they just waved!", "Ocean humor is always a wave!"),
            ("Why did the scarecrow win an award? He was outstanding in his field!", "That scarecrow really knows how to stand out!"),
            ("I'm reading a book about anti-gravity. It's impossible to put down!", "I couldn't put it down either!"),
            ("Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!", "Math jokes are always number one!"),
            ("Why don't eggs tell jokes? They'd crack each other up!", "Egg-cellent humor!"),
            ("I wondered why the baseball kept getting bigger. Then it hit me!", "That's a real curveball of a joke!"),
            ("What do you call a fake noodle? An impasta!", "That's pasta-bly the best joke ever!"),
            ("How does a penguin build its house? Igloos it together!", "That's ice cold humor!"),
            ("Why did the bicycle fall over? Because it was two tired!", "That bike really needed a rest!"),
            ("What do you call a bear with no teeth? A gummy bear!", "That's un-bear-ably cute!"),
            ("Why don't skeletons fight each other? They don't have the guts!", "That's bone-chilling humor!"),
            ("What's orange and sounds like a parrot? A carrot!", "That's a real head-scratcher!"),
            ("Why did the math book look sad? Because it had too many problems!", "Math books always have too many issues!"),
            ("What do you call a sleeping bull? A bulldozer!", "That's a heavy sleeper!")
        ]
        
        joke, punchline = random.choice(jokes)
        logger.info("Joke provided")
        return f"{joke} {punchline}"
    
    def _handle_reminders(self, memory: Dict[str, Any]) -> str:
        """Handle reminder requests with friendly tone"""
        if 'reminders' in memory and memory['reminders']:
            reminders_str = "; ".join(memory['reminders'])
            return f"I have these things saved for you: {reminders_str}. Is there anything specific you'd like to know?"
        else:
            return "I don't have any reminders saved yet. You can ask me to remember something, and I'll keep it for you!"
    
    def _generate_conversational_response(self, name: str, context: Dict[str, Any]) -> str:
        """Generate natural conversational response with personality"""
        # Check if this is a returning conversation
        if context['conversation_length'] > 3:
            # More familiar responses
            responses = [
                f"Interesting! Tell me more, {name}! I'm all ears!",
                f"Oh really? What else?",
                f"That's fascinating! Keep going!",
                f"I'm intrigued! What else?",
                f"Tell me more! I'm enjoying this!",
                f"You always have the most interesting things to say!",
                f"I'm curious! What else?",
                f"Well, this is getting good!"
            ]
        else:
            # Newer conversation responses
            responses = [
                f"Interesting! Tell me more!",
                f"Oh, I see! What else?",
                f"That's cool! What else?",
                f"Tell me more! I'm enjoying this!",
                f"I'm curious! What else?",
                f"Well, this is fun!",
                f"Nice! What else?",
                f"Let's keep chatting!"
            ]
        
        return random.choice(responses)
    
    def _generate_emotional_response(self, name: str, emotion: str) -> str:
        """Generate response for any emotion"""
        responses = self.emotional_responses.get(emotion, self.emotional_responses['happy'])
        return random.choice(responses)