"""
Proactive Screen Awareness - Watches screen and asks questions based on what you're doing
"""
import time
import json
from pathlib import Path
from datetime import datetime
import threading
import random

class ScreenAwareness:
    """Continuously monitors screen and proactively helps"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.memory_dir = self.base_dir / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.context_file = self.memory_dir / "screen_context.json"
        self.context = self._load_context()
        self.is_monitoring = False
        self.last_app = None
        self.last_activity = None
        self.last_question_time = 0
        self.question_interval = 60  # Ask question every 60 seconds if idle
        self.idle_threshold = 120  # Consider idle after 120 seconds
        self.last_user_input_time = time.time()
        self.suggestions_given = []
        self.activity_history = []
        self.logger = self._setup_logger()
        self.proactive_callback = None
        self.user_name = "boss"
    
    def _setup_logger(self):
        import logging
        logger = logging.getLogger("ScreenAwareness")
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            logger.propagate = False
        return logger
    
    def _load_context(self) -> dict:
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return self._default_context()
        return self._default_context()
    
    def _default_context(self):
        return {
            "current_app": None,
            "current_activity": None,
            "screen_content": None,
            "active_window": None,
            "browser_tabs": [],
            "running_apps": [],
            "last_updated": None,
            "context_history": []
        }
    
    def _save_context(self):
        try:
            self.context["last_updated"] = datetime.now().isoformat()
            with open(self.context_file, 'w') as f:
                json.dump(self.context, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save context: {e}")
    
    def get_screen_state(self) -> dict:
        """Get current screen state"""
        try:
            from utils.screen_vision import screen_vision
            from utils.system_monitor import system_monitor
            
            # Get active window from system_monitor
            active_info = system_monitor.get_active_window()
            active = active_info.get("title", "Unknown") if isinstance(active_info, dict) else str(active_info)
            
            # Get running apps from system_monitor
            apps_info = system_monitor.get_running_apps()
            apps = apps_info if isinstance(apps_info, list) else []
            
            # Get browser tabs if browser is open
            browser_tabs = []
            if any(browser in active.lower() for browser in ['chrome', 'safari', 'firefox', 'edge']):
                tabs_info = system_monitor.get_browser_tabs()
                browser_tabs = tabs_info if isinstance(tabs_info, list) else []
            
            # Get screen content via OCR from screen_vision
            screen_text = ""
            try:
                ocr_result = screen_vision.read_screen_text()
                if isinstance(ocr_result, dict) and ocr_result.get("success"):
                    screen_text = ocr_result.get("text", "")
            except Exception:
                pass
            
            state = {
                "active_window": active,
                "running_apps": apps[:10],
                "browser_tabs": browser_tabs[:5],
                "screen_text": screen_text[:1000] if screen_text else "",
                "timestamp": datetime.now().isoformat()
            }
            
            return state
            
        except Exception as e:
            self.logger.error(f"Failed to get screen state: {e}")
            return {}
    
    def analyze_activity(self, screen_state: dict) -> dict:
        """Analyze what the user is doing"""
        active = screen_state.get("active_window", "").lower()
        apps = [a.lower() for a in screen_state.get("running_apps", [])]
        tabs = screen_state.get("browser_tabs", [])
        screen_text = screen_state.get("screen_text", "").lower()
        
        activity = {
            "app_type": None,
            "task_type": None,
            "context": None,
            "suggestion": None
        }
        
        # Detect app type
        if any(x in active for x in ['chrome', 'safari', 'firefox', 'edge', 'browser']):
            activity["app_type"] = "browser"
            
            # Detect what they're browsing
            if any(x in active for x in ['youtube', 'youtu.be']):
                activity["task_type"] = "watching_video"
                activity["context"] = "YouTube"
            elif any(x in active for x in ['github', 'gitlab', 'bitbucket']):
                activity["task_type"] = "coding"
                activity["context"] = "GitHub"
            elif any(x in active for x in ['stackoverflow', 'stack overflow']):
                activity["task_type"] = "research"
                activity["context"] = "Stack Overflow"
            elif any(x in active for x in ['docs.google', 'google docs']):
                activity["task_type"] = "writing"
                activity["context"] = "Google Docs"
            elif any(x in active for x in ['mail.google', 'gmail', 'outlook']):
                activity["task_type"] = "email"
                activity["context"] = "Email"
            elif any(x in active for x in ['twitter', 'x.com', 'facebook', 'instagram', 'linkedin']):
                activity["task_type"] = "social_media"
                activity["context"] = "Social Media"
            elif any(x in active for x in ['chat.openai', 'claude', 'chatgpt']):
                activity["task_type"] = "using_ai"
                activity["context"] = "AI Chat"
            else:
                activity["task_type"] = "browsing"
                activity["context"] = "Web"
                
        elif any(x in active for x in ['code', 'visual studio', 'vscode', 'intellij', 'pycharm', 'sublime', 'atom']):
            activity["app_type"] = "code_editor"
            activity["task_type"] = "coding"
            activity["context"] = "Code Editor"
            
        elif any(x in active for x in ['terminal', 'iterm', 'console', 'powershell', 'cmd']):
            activity["app_type"] = "terminal"
            activity["task_type"] = "terminal_work"
            activity["context"] = "Terminal"
            
        elif any(x in active for x in ['slack', 'discord', 'teams', 'zoom', 'meet']):
            activity["app_type"] = "communication"
            activity["task_type"] = "communicating"
            activity["context"] = "Communication"
            
        elif any(x in active for x in ['word', 'pages', 'docs', 'notion', 'obsidian']):
            activity["app_type"] = "document"
            activity["task_type"] = "writing"
            activity["context"] = "Document"
            
        elif any(x in active for x in ['excel', 'numbers', 'sheets', 'calc']):
            activity["app_type"] = "spreadsheet"
            activity["task_type"] = "data_work"
            activity["context"] = "Spreadsheet"
            
        elif any(x in active for x in ['photoshop', 'figma', 'sketch', 'canva', 'illustrator']):
            activity["app_type"] = "design"
            activity["task_type"] = "designing"
            activity["context"] = "Design Tool"
            
        elif any(x in active for x in ['spotify', 'music', 'itunes', 'vlc', 'video']):
            activity["app_type"] = "media"
            activity["task_type"] = "media_playback"
            activity["context"] = "Media"
        
        return activity
    
    def generate_suggestion(self, activity: dict, screen_state: dict) -> str:
        """Generate proactive suggestion based on activity"""
        task_type = activity.get("task_type")
        context = activity.get("context")
        
        suggestions = {
            "coding": [
                f"I see you're coding in {context}. Need help with any functions?",
                f"Working on code? I can analyze it for bugs!",
                f"Coding time! Want me to review your code?",
                f"I can help optimize that code if you want!"
            ],
            "watching_video": [
                "Watching a video? Want me to summarize it?",
                "Learning from YouTube? I can take notes for you!",
                "Need me to save the video link?",
                f"Interesting video! Want me to remember the key points?"
            ],
            "email": [
                "Checking emails? Need help drafting a reply?",
                "I can help you organize your inbox!",
                "Want me to help compose that email?",
                "Email time! Need help with anything?"
            ],
            "research": [
                "Researching? I can help find more info!",
                f"Looking into {context}? Want me to search too?",
                "I can summarize those search results!",
                "Need help with that research?"
            ],
            "social_media": [
                "Scrolling social media? Need a break reminder?",
                "Want me to post something for you?",
                "Social media time! Anything I can help with?",
                "Need help with your social media?"
            ],
            "writing": [
                f"Writing in {context}? Need help with grammar?",
                "I can help you write that!",
                "Want me to proofread that?",
                "Need help with your writing?"
            ],
            "terminal_work": [
                "Working in terminal? Need help with commands?",
                "I can run those commands for you!",
                "Terminal work? I can help automate that!",
                "Want me to help with those commands?"
            ],
            "communicating": [
                "On a call? Need me to take notes?",
                "Chatting? Need help with anything?",
                "Communication time! Anything I can assist with?",
                "Want me to help with that conversation?"
            ],
            "designing": [
                f"Designing in {context}? Need inspiration?",
                "Want me to find design references?",
                "I can help with that design!",
                "Need help with your design?"
            ],
            "data_work": [
                "Working with data? Need help with formulas?",
                "I can help analyze that data!",
                "Need help with spreadsheets?",
                "Want me to help with that data?"
            ],
            "media_playback": [
                "Enjoying media! Need anything?",
                "Want me to control playback?",
                "Media time! Anything I can help with?",
                "Need help with your media?"
            ]
        }
        
        task_suggestions = suggestions.get(task_type, [])
        if task_suggestions:
            import random
            return random.choice(task_suggestions)
        
        return None
    
    def start_monitoring(self, callback=None):
        """Start continuous screen monitoring"""
        if self.is_monitoring:
            return {"success": True, "message": "Already monitoring"}
        
        self.is_monitoring = True
        self.proactive_callback = callback
        
        def monitoring_loop():
            while self.is_monitoring:
                try:
                    # Get screen state
                    screen_state = self.get_screen_state()
                    
                    if screen_state:
                        # Analyze activity
                        activity = self.analyze_activity(screen_state)
                        
                        # Update context
                        self.context["current_app"] = screen_state.get("active_window")
                        self.context["current_activity"] = activity.get("task_type")
                        self.context["running_apps"] = screen_state.get("running_apps", [])
                        self.context["browser_tabs"] = screen_state.get("browser_tabs", [])
                        self.context["screen_content"] = screen_state.get("screen_text", "")[:500]
                        self._save_context()
                        
                        # Track activity history
                        self.activity_history.append({
                            "app": screen_state.get("active_window"),
                            "task": activity.get("task_type"),
                            "timestamp": time.time()
                        })
                        if len(self.activity_history) > 50:
                            self.activity_history.pop(0)
                        
                        current_app = screen_state.get("active_window")
                        current_time = time.time()
                        
                        # Proactive question 1: App changed
                        if current_app != self.last_app:
                            suggestion = self.generate_suggestion(activity, screen_state)
                            if suggestion and callback:
                                callback(suggestion, activity)
                            self.last_app = current_app
                            self.last_question_time = current_time
                        
                        # Proactive question 2: Idle detection - ask questions when idle
                        elif current_time - self.last_user_input_time > self.idle_threshold:
                            if current_time - self.last_question_time > self.question_interval:
                                idle_question = self.generate_idle_question(activity, screen_state)
                                if idle_question and callback:
                                    callback(idle_question, activity)
                                    self.last_question_time = current_time
                        
                        # Proactive question 3: Long task - offer help
                        elif self.is_long_task(activity):
                            if current_time - self.last_question_time > 120:
                                help_offer = self.generate_help_offer(activity, screen_state)
                                if help_offer and callback:
                                    callback(help_offer, activity)
                                    self.last_question_time = current_time
                    
                    time.sleep(20)  # Check every 20 seconds
                    
                except Exception as e:
                    self.logger.error(f"Monitoring error: {e}")
                    time.sleep(10)
        
        thread = threading.Thread(target=monitoring_loop, daemon=True)
        thread.start()
        
        return {"success": True, "message": "Screen monitoring started - I'll watch your screen and ask questions!"}
    
    def stop_monitoring(self):
        """Stop screen monitoring"""
        self.is_monitoring = False
        return {"success": True, "message": "Screen monitoring stopped"}
    
    def update_user_input(self):
        """Update last user input time - call when user interacts"""
        self.last_user_input_time = time.time()
    
    def is_long_task(self, activity: dict) -> bool:
        """Check if user has been doing the same task for a long time"""
        if len(self.activity_history) < 5:
            return False
        
        current_task = activity.get("task_type")
        recent_tasks = [h.get("task") for h in self.activity_history[-5:]]
        
        return all(t == current_task for t in recent_tasks)
    
    def generate_idle_question(self, activity: dict, screen_state: dict) -> str:
        """Generate a question when user appears idle"""
        task_type = activity.get("task_type", "")
        context = activity.get("context", "")
        
        idle_questions = {
            "coding": [
                f"Still coding? Need help with anything?",
                f"Working hard on that code! Need a hand?",
                f"Want me to review what you've written?",
                f"Stuck on something? I can help!"
            ],
            "browsing": [
                f"Still browsing {context}? Found what you need?",
                f"Need me to search for something?",
                f"Want me to summarize what you're reading?",
                f"Looking for something specific?"
            ],
            "writing": [
                f"Still writing? Need help with that?",
                f"Want me to proofread your work?",
                f"Need help organizing your thoughts?",
                f"Stuck on what to write next?"
            ],
            "research": [
                f"Research going well? Need more sources?",
                f"Want me to find additional info?",
                f"Need help summarizing what you found?",
                f"Found what you were looking for?"
            ],
            "email": [
                f"Still on emails? Need help replying?",
                f"Want me to help draft a response?",
                f"Need help with your inbox?",
                f"Any tricky emails I can help with?"
            ]
        }
        
        questions = idle_questions.get(task_type, [
            f"Hey {self.user_name}, still working on {context}? Need help?",
            f"Everything going okay? Let me know if you need anything!",
            f"I'm here if you need help with that!",
            f"Need a break? I can help with something else!"
        ])
        
        return random.choice(questions)
    
    def generate_help_offer(self, activity: dict, screen_state: dict) -> str:
        """Generate help offer for long tasks"""
        task_type = activity.get("task_type", "")
        context = activity.get("context", "")
        
        help_offers = {
            "coding": [
                f"You've been coding for a while! Want me to review your code?",
                f"Need help debugging? I can analyze your code!",
                f"Want me to suggest optimizations?",
                f"Need help with that function?"
            ],
            "writing": [
                f"Writing for a while! Want me to check grammar?",
                f"Need help with that document?",
                f"Want me to help structure your writing?",
                f"Need a fresh perspective on your writing?"
            ],
            "research": [
                f"Deep in research! Want me to help find more sources?",
                f"Need help organizing your research?",
                f"Want me to summarize what you've found?",
                f"Need help with citations?"
            ]
        }
        
        offers = help_offers.get(task_type, [
            f"You've been at this for a while! Need any help?",
            f"I can help make that easier! Want me to assist?",
            f"Need a hand with {context}?"
        ])
        
        return random.choice(offers)
    
    def ask_about_screen(self) -> str:
        """Ask a question based on current screen"""
        screen_state = self.get_screen_state()
        activity = self.analyze_activity(screen_state)
        
        suggestion = self.generate_suggestion(activity, screen_state)
        
        if suggestion:
            return suggestion
        
        active = screen_state.get("active_window", "something")
        return f"I see you're working on {active}. Need any help?"
    
    def get_context_summary(self) -> str:
        """Get a summary of current context"""
        screen_state = self.get_screen_state()
        activity = self.analyze_activity(screen_state)
        
        summary = {
            "app": screen_state.get("active_window", "Unknown"),
            "task": activity.get("task_type", "Unknown"),
            "context": activity.get("context", "Unknown"),
            "running_apps": len(screen_state.get("running_apps", [])),
            "browser_tabs": len(screen_state.get("browser_tabs", []))
        }
        
        return summary
    
    def answer_about_screen(self, question: str) -> str:
        """Answer a question about what's on screen"""
        screen_state = self.get_screen_state()
        activity = self.analyze_activity(screen_state)
        
        question_lower = question.lower()
        
        if any(x in question_lower for x in ['what app', 'what application', 'what program']):
            return f"You're using {screen_state.get('active_window', 'an application')}"
        
        if any(x in question_lower for x in ['what am i doing', 'what am i working on']):
            task = activity.get("task_type", "something")
            context = activity.get("context", "")
            return f"You're {task.replace('_', ' ')} in {context}"
        
        if any(x in question_lower for x in ['how many apps', 'running apps']):
            apps = screen_state.get("running_apps", [])
            return f"You have {len(apps)} apps running: {', '.join(apps[:5])}"
        
        if any(x in question_lower for x in ['browser tabs', 'open tabs']):
            tabs = screen_state.get("browser_tabs", [])
            return f"You have {len(tabs)} browser tabs open"
        
        if any(x in question_lower for x in ['what on screen', 'what do you see']):
            text = screen_state.get("screen_text", "")
            if text:
                return f"I can see: {text[:200]}..."
            return "I can see your screen but couldn't read the text"
        
        return "I see your screen. What would you like to know about it?"


screen_awareness = ScreenAwareness()
