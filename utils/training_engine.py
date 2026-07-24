"""
Auto-Training Engine
Enables AI to continuously learn and improve itself
"""
import json
import os
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from logger import logger

class TrainingEngine:
    def __init__(self):
        self.training_file = "data/training_data.json"
        self.training_data = self._load_training_data()
        self.performance_metrics = {
            'total_conversations': 0,
            'successful_interactions': 0,
            'failed_interactions': 0,
            'topics_mastered': [],
            'improvement_areas': [],
            'last_training': None,
            'training_sessions': 0
        }
    
    def _load_training_data(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.training_file):
                with open(self.training_file, 'r') as f:
                    return json.load(f)
            return {
                'conversations': [],
                'patterns': {},
                'responses': {},
                'learned_facts': {},
                'user_preferences': {},
                'successful_responses': [],
                'failed_responses': [],
                'topic_knowledge': {},
                'conversation_flows': [],
                'last_updated': None
            }
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            return {'conversations': [], 'patterns': {}, 'responses': {}}
    
    def _save_training_data(self) -> bool:
        try:
            os.makedirs(os.path.dirname(self.training_file), exist_ok=True)
            self.training_data['last_updated'] = datetime.now().isoformat()
            with open(self.training_file, 'w') as f:
                json.dump(self.training_data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving training data: {e}")
            return False
    
    def record_conversation(self, user_input: str, ai_response: str, context: Dict[str, Any]):
        conversation_entry = {
            'user_input': user_input,
            'ai_response': ai_response,
            'timestamp': datetime.now().isoformat(),
            'context': context,
            'topics': self._extract_topics(user_input),
            'sentiment': self._analyze_sentiment(user_input),
            'response_quality': None
        }
        
        self.training_data['conversations'].append(conversation_entry)
        
        if len(self.training_data['conversations']) > 1000:
            self.training_data['conversations'] = self.training_data['conversations'][-1000:]
        
        self._update_patterns(user_input, ai_response)
        self._update_topic_knowledge(user_input, ai_response)
        
        self.performance_metrics['total_conversations'] += 1
        
        self._save_training_data()
    
    def _extract_topics(self, text: str) -> List[str]:
        topics = []
        topic_keywords = {
            'technology': ['computer', 'software', 'code', 'programming', 'ai', 'tech'],
            'science': ['science', 'physics', 'chemistry', 'biology', 'research'],
            'personal': ['i feel', 'i think', 'i believe', 'my opinion'],
            'work': ['work', 'job', 'career', 'office', 'project'],
            'learning': ['learn', 'study', 'education', 'school', 'knowledge'],
            'problems': ['problem', 'issue', 'difficulty', 'challenge'],
            'goals': ['goal', 'plan', 'dream', 'future', 'want to']
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                topics.append(topic)
        
        return topics if topics else ['general']
    
    def _analyze_sentiment(self, text: str) -> str:
        positive = ['happy', 'great', 'love', 'like', 'awesome', 'wonderful', 'good']
        negative = ['sad', 'bad', 'hate', 'dislike', 'terrible', 'worst', 'angry']
        
        text_lower = text.lower()
        pos = sum(1 for w in positive if w in text_lower)
        neg = sum(1 for w in negative if w in text_lower)
        
        if pos > neg:
            return 'positive'
        elif neg > pos:
            return 'negative'
        return 'neutral'
    
    def _update_patterns(self, user_input: str, ai_response: str):
        patterns = self.training_data.get('patterns', {})
        
        input_words = set(user_input.lower().split())
        
        for word in input_words:
            if len(word) > 3:
                if word not in patterns:
                    patterns[word] = {'responses': [], 'count': 0}
                patterns[word]['responses'].append(ai_response)
                patterns[word]['count'] += 1
                
                if len(patterns[word]['responses']) > 10:
                    patterns[word]['responses'] = patterns[word]['responses'][-10:]
        
        self.training_data['patterns'] = patterns
    
    def _update_topic_knowledge(self, user_input: str, ai_response: str):
        topics = self._extract_topics(user_input)
        topic_knowledge = self.training_data.get('topic_knowledge', {})
        
        for topic in topics:
            if topic not in topic_knowledge:
                topic_knowledge[topic] = {
                    'interactions': [],
                    'learned_facts': [],
                    'common_questions': []
                }
            
            topic_knowledge[topic]['interactions'].append({
                'input': user_input,
                'response': ai_response,
                'timestamp': datetime.now().isoformat()
            })
            
            if len(topic_knowledge[topic]['interactions']) > 50:
                topic_knowledge[topic]['interactions'] = topic_knowledge[topic]['interactions'][-50:]
        
        self.training_data['topic_knowledge'] = topic_knowledge
    
    def record_response_quality(self, response_index: int, quality: str):
        if 0 <= response_index < len(self.training_data['conversations']):
            self.training_data['conversations'][response_index]['response_quality'] = quality
            
            if quality == 'good':
                self.performance_metrics['successful_interactions'] += 1
            elif quality == 'bad':
                self.performance_metrics['failed_interactions'] += 1
            
            self._save_training_data()
    
    def learn_from_conversation(self, user_input: str, ai_response: str, was_successful: bool):
        if was_successful:
            self.training_data['successful_responses'].append({
                'input': user_input,
                'response': ai_response,
                'timestamp': datetime.now().isoformat()
            })
            
            if len(self.training_data['successful_responses']) > 200:
                self.training_data['successful_responses'] = self.training_data['successful_responses'][-200:]
        else:
            self.training_data['failed_responses'].append({
                'input': user_input,
                'response': ai_response,
                'timestamp': datetime.now().isoformat()
            })
            
            if len(self.training_data['failed_responses']) > 100:
                self.training_data['failed_responses'] = self.training_data['failed_responses'][-100:]
        
        self._save_training_data()
    
    def get_improved_response(self, user_input: str) -> Optional[str]:
        patterns = self.training_data.get('patterns', {})
        
        input_words = set(user_input.lower().split())
        best_response = None
        best_count = 0
        
        for word in input_words:
            if word in patterns and patterns[word]['count'] > best_count:
                if patterns[word]['responses']:
                    best_response = random.choice(patterns[word]['responses'])
                    best_count = patterns[word]['count']
        
        return best_response
    
    def get_topic_expertise(self, topic: str) -> Dict[str, Any]:
        topic_knowledge = self.training_data.get('topic_knowledge', {})
        
        if topic in topic_knowledge:
            return {
                'interaction_count': len(topic_knowledge[topic]['interactions']),
                'has_learned_facts': len(topic_knowledge[topic].get('learned_facts', [])) > 0,
                'common_questions': topic_knowledge[topic].get('common_questions', [])
            }
        
        return {'interaction_count': 0, 'has_learned_facts': False}
    
    def analyze_performance(self) -> Dict[str, Any]:
        total = self.performance_metrics['total_conversations']
        successful = self.performance_metrics['successful_interactions']
        
        success_rate = (successful / total * 100) if total > 0 else 0
        
        return {
            'total_conversations': total,
            'success_rate': round(success_rate, 2),
            'successful_interactions': successful,
            'failed_interactions': self.performance_metrics['failed_interactions'],
            'topics_in_knowledge': len(self.training_data.get('topic_knowledge', {})),
            'patterns_learned': len(self.training_data.get('patterns', {})),
            'last_training': self.training_data.get('last_updated')
        }
    
    def get_learning_suggestions(self) -> List[str]:
        suggestions = []
        
        topic_knowledge = self.training_data.get('topic_knowledge', {})
        
        for topic, data in topic_knowledge.items():
            if len(data['interactions']) < 5:
                suggestions.append(f"More conversations about {topic}")
        
        failed = self.training_data.get('failed_responses', [])
        if len(failed) > 10:
            suggestions.append("Review failed responses for improvement")
        
        return suggestions
    
    def auto_train(self) -> Dict[str, Any]:
        self.performance_metrics['training_sessions'] += 1
        self.performance_metrics['last_training'] = datetime.now().isoformat()
        
        analysis = self.analyze_performance()
        
        improvements = []
        
        if analysis['success_rate'] < 70:
            improvements.append("Focus on more relevant responses")
        
        if analysis['patterns_learned'] < 10:
            improvements.append("Need more conversation patterns")
        
        self._save_training_data()
        
        return {
            'training_completed': True,
            'session_number': self.performance_metrics['training_sessions'],
            'performance': analysis,
            'improvements': improvements,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_training_stats(self) -> Dict[str, Any]:
        return {
            'total_conversations': len(self.training_data.get('conversations', [])),
            'patterns_learned': len(self.training_data.get('patterns', {})),
            'topics_mastered': len(self.training_data.get('topic_knowledge', {})),
            'successful_responses': len(self.training_data.get('successful_responses', [])),
            'failed_responses': len(self.training_data.get('failed_responses', [])),
            'training_sessions': self.performance_metrics['training_sessions'],
            'last_training': self.training_data.get('last_updated')
        }
