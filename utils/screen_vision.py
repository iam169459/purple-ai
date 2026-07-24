"""
Screen Vision Module - See and analyze screen content
Uses OCR to read text, identify UI elements, and ask interactive questions
"""
import os
import subprocess
import platform
from datetime import datetime
from typing import Dict, Any, List, Optional
from logger import logger

class ScreenVision:
    def __init__(self):
        self.os_type = platform.system()
        self._temp_dir = '/tmp'
        self._last_screenshot = None
        self._ocr_available = False
        self._init_ocr()
        logger.info(f"Screen Vision initialized for {self.os_type}")
    
    def _init_ocr(self):
        try:
            import pytesseract
            from PIL import Image
            self._ocr_available = True
            logger.info("OCR engine available")
        except ImportError:
            logger.warning("pytesseract not available - using fallback")
            self._ocr_available = False
    
    def take_screenshot(self, filename: str = None) -> Dict[str, Any]:
        try:
            if not filename:
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            filepath = os.path.join(self._temp_dir, filename)
            
            if self.os_type == 'Darwin':
                subprocess.run(['screencapture', '-x', filepath], 
                             capture_output=True, timeout=10)
            elif self.os_type == 'Windows':
                subprocess.run(['powershell', '-Command', 
                              f'Add-Type -AssemblyName System.Windows.Forms; '
                              f'[System.Windows.Forms.Screen]::PrimaryScreen.Bounds | ForEach-Object {{ '
                              f'$bmp = New-Object System.Drawing.Bitmap($_.Width, $_.Height); '
                              f'$graphics = [System.Drawing.Graphics]::FromImage($bmp); '
                              f'$graphics.CopyFromScreen($_.Location, [System.Drawing.Point]::Empty, $_.Size); '
                              f'$bmp.Save("{filepath}") }}'], 
                             capture_output=True, timeout=15)
            else:
                return {'success': False, 'message': 'Screenshot not supported on this OS'}
            
            if os.path.exists(filepath):
                self._last_screenshot = filepath
                size = os.path.getsize(filepath)
                return {
                    'success': True, 
                    'message': f'Screenshot saved',
                    'filepath': filepath,
                    'size_kb': round(size / 1024, 2)
                }
            else:
                return {'success': False, 'message': 'Failed to create screenshot'}
                
        except Exception as e:
            return {'success': False, 'message': f'Error: {e}'}
    
    def analyze_screen(self) -> Dict[str, Any]:
        result = self.take_screenshot()
        if not result['success']:
            return result
        
        filepath = result['filepath']
        
        analysis = {
            'success': True,
            'filepath': filepath,
            'text_content': [],
            'screen_elements': [],
            'profiles': [],
            'buttons': [],
            'links': [],
            'questions': [],
            'suggestions': [],
            'description': ''
        }
        
        if self._ocr_available:
            try:
                import pytesseract
                from PIL import Image
                
                img = Image.open(filepath)
                text = pytesseract.image_to_string(img)
                analysis['text_content'] = [line.strip() for line in text.split('\n') if line.strip()]
                
                # Analyze UI elements
                analysis['screen_elements'] = self._analyze_ui_elements(text)
                analysis['profiles'] = self._find_profiles(text)
                analysis['buttons'] = self._find_buttons(text)
                analysis['links'] = self._find_links(text)
                
                # Generate questions and suggestions
                analysis['questions'] = self._generate_questions(analysis)
                analysis['suggestions'] = self._generate_suggestions(analysis)
                
                analysis['description'] = self._describe_screen_content(analysis)
                
            except Exception as e:
                logger.error(f"OCR error: {e}")
                analysis['description'] = "I took a screenshot but couldn't read the text."
        else:
            analysis['description'] = "I took a screenshot. OCR is not installed to read text."
        
        return analysis
    
    def _analyze_ui_elements(self, text: str) -> List[Dict]:
        """Analyze text for UI elements"""
        elements = []
        text_lower = text.lower()
        
        ui_patterns = {
            'buttons': ['button', 'btn', 'submit', 'ok', 'cancel', 'close', 'save', 'delete', 'edit', 'open', 'click'],
            'links': ['link', 'href', 'click here', 'read more', 'learn more', 'sign up', 'login', 'register'],
            'inputs': ['input', 'text field', 'search', 'enter', 'type here', 'password', 'email'],
            'profiles': ['profile', 'account', 'user', 'avatar', 'icon', 'picture', 'photo'],
            'navigation': ['menu', 'nav', 'sidebar', 'header', 'footer', 'tab', 'dropdown']
        }
        
        for category, patterns in ui_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    elements.append({
                        'type': category,
                        'pattern': pattern,
                        'context': self._get_context(text, pattern)
                    })
        
        return elements
    
    def _find_profiles(self, text: str) -> List[Dict]:
        """Find profile-related content"""
        profiles = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(p in line_lower for p in ['profile', 'account', 'user', 'avatar', 'who']):
                context = lines[max(0, i-1):min(len(lines), i+2)]
                profiles.append({
                    'text': line.strip(),
                    'context': ' '.join(context)
                })
        
        return profiles
    
    def _find_buttons(self, text: str) -> List[str]:
        """Find button-like elements"""
        buttons = []
        lines = text.split('\n')
        
        button_keywords = ['submit', 'ok', 'cancel', 'save', 'delete', 'edit', 'open', 
                          'click', 'button', 'sign in', 'log in', 'register', 'sign up',
                          'apply', 'confirm', 'yes', 'no', 'next', 'back', 'close',
                          'buy', 'add to cart', 'checkout', 'download', 'install']
        
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and any(k in line_stripped.lower() for k in button_keywords):
                buttons.append(line_stripped)
        
        return buttons
    
    def _find_links(self, text: str) -> List[str]:
        """Find link-like elements"""
        links = []
        lines = text.split('\n')
        
        link_keywords = ['http', 'www', 'click here', 'read more', 'learn more', 
                        'sign up', 'login', 'register', 'download', 'subscribe']
        
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and any(k in line_stripped.lower() for k in link_keywords):
                links.append(line_stripped)
        
        return links
    
    def _get_context(self, text: str, pattern: str, context_words: int = 5) -> str:
        """Get context around a pattern"""
        words = text.split()
        try:
            idx = next(i for i, w in enumerate(words) if pattern in w.lower())
            start = max(0, idx - context_words)
            end = min(len(words), idx + context_words + 1)
            return ' '.join(words[start:end])
        except StopIteration:
            return ''
    
    def _generate_questions(self, analysis: Dict) -> List[str]:
        """Generate questions based on screen analysis"""
        questions = []
        
        # If profiles found
        if analysis['profiles']:
            questions.append(f"I can see {len(analysis['profiles'])} profile(s) on the screen. Which one would you like me to open?")
            for i, profile in enumerate(analysis['profiles'][:3], 1):
                questions.append(f"  {i}. {profile['text']}")
        
        # If buttons found
        if analysis['buttons']:
            questions.append(f"I see these buttons: {', '.join(analysis['buttons'][:3])}. Should I click any of them?")
        
        # If links found
        if analysis['links']:
            questions.append(f"There are {len(analysis['links'])} links visible. Should I open any of them?")
        
        # If no clear action
        if not analysis['profiles'] and not analysis['buttons'] and not analysis['links']:
            questions.append("I can see the screen but I'm not sure what you'd like me to do. Can you tell me more about what you're looking for?")
        
        return questions
    
    def _generate_suggestions(self, analysis: Dict) -> List[str]:
        """Generate suggestions based on screen content"""
        suggestions = []
        
        text_content = ' '.join(analysis.get('text_content', [])).lower()
        
        # Login page detection
        if any(w in text_content for w in ['login', 'sign in', 'log in', 'password']):
            suggestions.append("This looks like a login page. I can help you open a browser or fill in credentials if you'd like.")
        
        # Profile selection
        if analysis['profiles']:
            suggestions.append("I can help you select a profile. Just tell me which one!")
        
        # Shopping page
        if any(w in text_content for w in ['cart', 'checkout', 'buy', 'price', 'add to']):
            suggestions.append("This looks like a shopping page. I can help you add items to cart or checkout.")
        
        # Video player
        if any(w in text_content for w in ['play', 'pause', 'video', 'youtube', 'watch']):
            suggestions.append("I see a video player. I can help you play, pause, or search for videos.")
        
        # Document
        if any(w in text_content for w in ['file', 'edit', 'view', 'document', 'word', 'excel']):
            suggestions.append("This looks like a document editor. I can help you with formatting or navigation.")
        
        # Social media
        if any(w in text_content for w in ['post', 'comment', 'share', 'like', 'follow', 'friend']):
            suggestions.append("This looks like social media. I can help you post, comment, or navigate.")
        
        return suggestions
    
    def _describe_screen_content(self, analysis: Dict) -> str:
        """Generate a natural language description of the screen"""
        description = []
        
        # Main content
        if analysis['text_content']:
            main_text = ' '.join(analysis['text_content'][:3])
            description.append(f"I can see: {main_text[:150]}...")
        
        # Profiles
        if analysis['profiles']:
            profile_names = [p['text'] for p in analysis['profiles'][:3]]
            description.append(f"Found {len(analysis['profiles'])} profile(s): {', '.join(profile_names)}")
        
        # Buttons
        if analysis['buttons']:
            description.append(f"Buttons visible: {', '.join(analysis['buttons'][:3])}")
        
        # Links
        if analysis['links']:
            description.append(f"Found {len(analysis['links'])} link(s)")
        
        # Add questions if any
        if analysis['questions']:
            description.append("\n" + ' '.join(analysis['questions']))
        
        # Add suggestions
        if analysis['suggestions']:
            description.append("\nSuggestions: " + ' '.join(analysis['suggestions']))
        
        return ' '.join(description) if description else "I can see the screen but I'm not sure what to focus on. What would you like me to help with?"
    
    def get_screen_description(self) -> str:
        analysis = self.analyze_screen()
        if analysis['success']:
            return analysis.get('description', 'No description available')
        return "I couldn't analyze the screen."
    
    def find_text_on_screen(self, search_text: str) -> Dict[str, Any]:
        result = self.read_screen_text()
        if not result['success']:
            return result
        
        text = result['text'].lower()
        search_lower = search_text.lower()
        
        found = search_lower in text
        
        context = ''
        if found:
            lines = result['text'].split('\n')
            for line in lines:
                if search_lower in line.lower():
                    context = line.strip()
                    break
        
        return {
            'success': True,
            'found': found,
            'search_text': search_text,
            'context': context
        }
    
    def read_screen_text(self) -> Dict[str, Any]:
        result = self.take_screenshot()
        if not result['success']:
            return result
        
        if not self._ocr_available:
            return {'success': False, 'message': 'OCR not available'}
        
        try:
            import pytesseract
            from PIL import Image
            
            img = Image.open(result['filepath'])
            text = pytesseract.image_to_string(img)
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            return {
                'success': True,
                'text': '\n'.join(lines),
                'line_count': len(lines)
            }
        except Exception as e:
            return {'success': False, 'message': f'OCR error: {e}'}
    
    def get_visible_apps(self) -> List[str]:
        result = self.read_screen_text()
        if not result['success']:
            return []
        
        text = result['text'].lower()
        
        app_indicators = {
            'Safari': ['safari', 'bookmark', 'tab'],
            'Chrome': ['chrome', 'google'],
            'Finder': ['finder', 'applications', 'documents'],
            'Terminal': ['terminal', 'bash', 'zsh', '$'],
            'VS Code': ['vscode', 'visual studio code', 'editor'],
            'Spotify': ['spotify', 'playlist', 'song'],
            'Messages': ['messages', 'imessage'],
            'Mail': ['mail', 'inbox', 'compose'],
            'Calendar': ['calendar', 'event', 'meeting'],
            'Notes': ['notes', 'note'],
            'Photos': ['photos', 'album'],
            'System Preferences': ['preferences', 'settings'],
        }
        
        detected = []
        for app, indicators in app_indicators.items():
            for indicator in indicators:
                if indicator in text:
                    detected.append(app)
                    break
        
        return detected


# Create global instance
screen_vision = ScreenVision()
