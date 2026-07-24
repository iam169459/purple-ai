"""
Enhanced Memory Management System
Handles saving and loading AI memory, user preferences, and conversation context
"""
import json
import os
from typing import Dict, Any, List, Optional
from config import config
from logger import logger
from datetime import datetime, timedelta

class MemoryManager:
    """Enhanced memory manager with advanced conversation context tracking"""
    
    def __init__(self):
        self.memory_file = config.MEMORY_FILE
        self.conversation_file = "data/conversation_history.json"
        self.user_profile_file = "data/user_profile.json"
    
    def load_memory(self) -> Dict[str, Any]:
        """Load the AI's memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    memory = json.load(f)
                logger.debug("Memory loaded successfully")
                
                # Ensure all required fields exist
                memory = self._ensure_memory_structure(memory)
                return memory
            else:
                logger.debug("No memory file found, using default memory")
                return self._get_default_memory()
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            return self._get_default_memory()
    
    def _ensure_memory_structure(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure memory has all required fields"""
        default_memory = self._get_default_memory()
        
        # Add any missing fields from default memory
        for key, value in default_memory.items():
            if key not in memory:
                memory[key] = value
        
        # Ensure conversation_history is a list
        if not isinstance(memory.get('conversation_history'), list):
            memory['conversation_history'] = []
        
        # Ensure reminders is a list
        if not isinstance(memory.get('reminders'), list):
            memory['reminders'] = []
        
        # Add enhanced memory fields
        if 'mood_patterns' not in memory:
            memory['mood_patterns'] = {}
        
        if 'personality_traits' not in memory:
            memory['personality_traits'] = {}
        
        if 'personality_preferences' not in memory:
            memory['personality_preferences'] = {}
        
        if 'user_preferences' not in memory:
            memory['user_preferences'] = {}
        
        if 'conversation_context' not in memory:
            memory['conversation_context'] = {
                'recent_topics': [],
                'emotional_history': [],
                'interaction_count': 0,
                'last_interaction': None
            }
        
        return memory
    
    def save_memory(self, memory: Dict[str, Any]) -> bool:
        """Save the AI's memory to file"""
        try:
            # Update last interaction timestamp
            if 'conversation_context' not in memory:
                memory['conversation_context'] = {}
            memory['conversation_context']['last_interaction'] = self._get_timestamp()
            
            # Increment interaction count
            memory['conversation_context']['interaction_count'] = memory['conversation_context'].get('interaction_count', 0) + 1
            
            with open(self.memory_file, 'w') as f:
                json.dump(memory, f, indent=2)
            logger.debug("Memory saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
            return False
    
    def update_memory(self, key: str, value: Any) -> bool:
        """Update a specific memory key"""
        memory = self.load_memory()
        memory[key] = value
        return self.save_memory(memory)
    
    def get_memory_value(self, key: str, default=None) -> Any:
        """Get a specific memory value"""
        memory = self.load_memory()
        return memory.get(key, default)
    
    def _get_default_memory(self) -> Dict[str, Any]:
        """Return default memory structure with enhanced fields"""
        return {
            'user_name': 'friend',
            'setup_complete': False,
            'conversation_history': [],
            'preferences': {},
            'reminders': [],
            'mood_patterns': {},
            'personality_traits': {},
            'personality_preferences': {},
            'user_preferences': {},
            'conversation_context': {
                'recent_topics': [],
                'emotional_history': [],
                'interaction_count': 0,
                'last_interaction': None
            },
            'interaction_count': 0,
            'special_dates': {},
            'learned_facts': {},
            'conversation_insights': {}
        }
    
    def add_conversation(self, user_input: str, ai_response: str) -> bool:
        """Add conversation to memory with enhanced context tracking"""
        memory = self.load_memory()
        if 'conversation_history' not in memory:
            memory['conversation_history'] = []
        
        conversation_entry = {
            'user': user_input,
            'ai': ai_response,
            'timestamp': self._get_timestamp(),
            'topics': self._extract_topics_from_text(user_input),
            'sentiment': self._analyze_sentiment(user_input)
        }
        
        memory['conversation_history'].append(conversation_entry)
        
        # Keep only last 50 conversations to prevent file bloat
        if len(memory['conversation_history']) > 50:
            memory['conversation_history'] = memory['conversation_history'][-50:]
        
        # Update conversation context
        self._update_conversation_context(memory, user_input, ai_response)
        
        return self.save_memory(memory)
    
    def _extract_topics_from_text(self, text: str) -> List[str]:
        """Extract potential topics from text"""
        topics = []
        
        # Common topic keywords
        topic_keywords = {
            'work': ['work', 'job', 'office', 'meeting', 'project'],
            'family': ['family', 'mom', 'dad', 'sister', 'brother', 'parent'],
            'hobbies': ['hobby', 'hobbies', 'interest', 'enjoy', 'like'],
            'technology': ['computer', 'phone', 'app', 'software', 'technology'],
            'health': ['health', 'exercise', 'diet', 'wellness', 'fitness'],
            'education': ['school', 'university', 'learning', 'study', 'course'],
            'entertainment': ['movie', 'music', 'book', 'game', 'show'],
            'travel': ['travel', 'trip', 'vacation', 'flight', 'hotel'],
            'food': ['food', 'cooking', 'recipe', 'restaurant', 'meal'],
            'weather': ['weather', 'temperature', 'rain', 'sun', 'snow']
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    topics.append(topic)
                    break
        
        return topics if topics else ['general']
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ['happy', 'great', 'awesome', 'love', 'like', 'excited', 'wonderful', 'fantastic', 'amazing']
        negative_words = ['sad', 'bad', 'hate', 'dislike', 'angry', 'upset', 'terrible', 'awful', 'horrible']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _update_conversation_context(self, memory: Dict[str, Any], user_input: str, ai_response: str):
        """Update conversation context with new information"""
        if 'conversation_context' not in memory:
            memory['conversation_context'] = {
                'recent_topics': [],
                'emotional_history': [],
                'interaction_count': 0,
                'last_interaction': None
            }
        
        # Update recent topics
        topics = self._extract_topics_from_text(user_input)
        memory['conversation_context']['recent_topics'].extend(topics)
        
        # Keep only recent topics
        if len(memory['conversation_context']['recent_topics']) > 20:
            memory['conversation_context']['recent_topics'] = memory['conversation_context']['recent_topics'][-20:]
        
        # Update emotional history
        sentiment = self._analyze_sentiment(user_input)
        memory['conversation_context']['emotional_history'].append({
            'sentiment': sentiment,
            'timestamp': self._get_timestamp()
        })
        
        # Keep only recent emotional history
        if len(memory['conversation_context']['emotional_history']) > 30:
            memory['conversation_context']['emotional_history'] = memory['conversation_context']['emotional_history'][-30:]
        
        # Update interaction count
        memory['conversation_context']['interaction_count'] = memory['conversation_context'].get('interaction_count', 0) + 1
    
    def get_conversation_insights(self) -> Dict[str, Any]:
        """Get insights from conversation history"""
        memory = self.load_memory()
        
        if 'conversation_history' not in memory or not memory['conversation_history']:
            return {
                'total_conversations': 0,
                'avg_message_length': 0,
                'most_common_topics': [],
                'sentiment_distribution': {},
                'recent_activity': []
            }
        
        conversations = memory['conversation_history']
        
        # Calculate insights
        total_conversations = len(conversations)
        
        # Average message length
        user_messages = [conv['user'] for conv in conversations if 'user' in conv]
        avg_message_length = sum(len(msg.split()) for msg in user_messages) / len(user_messages) if user_messages else 0
        
        # Most common topics
        all_topics = []
        for conv in conversations:
            if 'topics' in conv:
                all_topics.extend(conv['topics'])
        
        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        most_common_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Sentiment distribution
        sentiments = [conv.get('sentiment', 'neutral') for conv in conversations]
        sentiment_distribution = {}
        for sentiment in sentiments:
            sentiment_distribution[sentiment] = sentiment_distribution.get(sentiment, 0) + 1
        
        # Recent activity
        recent_conversations = conversations[-5:] if len(conversations) >= 5 else conversations
        recent_activity = [
            {
                'user_input': conv.get('user', ''),
                'ai_response': conv.get('ai', ''),
                'timestamp': conv.get('timestamp', '')
            }
            for conv in recent_conversations
        ]
        
        return {
            'total_conversations': total_conversations,
            'avg_message_length': round(avg_message_length, 1),
            'most_common_topics': most_common_topics,
            'sentiment_distribution': sentiment_distribution,
            'recent_activity': recent_activity
        }
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences from memory"""
        memory = self.load_memory()
        return memory.get('user_preferences', {})
    
    def update_user_preference(self, key: str, value: Any) -> bool:
        """Update a user preference"""
        memory = self.load_memory()
        if 'user_preferences' not in memory:
            memory['user_preferences'] = {}
        
        memory['user_preferences'][key] = value
        return self.save_memory(memory)
    
    def get_special_dates(self) -> Dict[str, str]:
        """Get special dates (birthdays, anniversaries, etc.)"""
        memory = self.load_memory()
        return memory.get('special_dates', {})
    
    def add_special_date(self, date_name: str, date_value: str) -> bool:
        """Add a special date"""
        memory = self.load_memory()
        if 'special_dates' not in memory:
            memory['special_dates'] = {}
        
        memory['special_dates'][date_name] = date_value
        return self.save_memory(memory)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about memory usage"""
        memory = self.load_memory()
        
        stats = {
            'total_conversations': len(memory.get('conversation_history', [])),
            'total_reminders': len(memory.get('reminders', [])),
            'has_user_name': 'user_name' in memory,
            'has_personality_data': 'personality_traits' in memory,
            'has_conversation_context': 'conversation_context' in memory,
            'last_interaction': memory.get('conversation_context', {}).get('last_interaction'),
            'interaction_count': memory.get('interaction_count', 0)
        }
        
        return stats