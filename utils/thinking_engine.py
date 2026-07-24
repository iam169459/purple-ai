"""
Thinking Engine Module
Enables AI to think, reason, ask questions, and learn from users
"""
import random
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from logger import logger
from config import config

class ThinkingEngine:
    def __init__(self):
        self.thought_patterns = self._load_thought_patterns()
        self.question_types = self._load_question_types()
        self.knowledge_from_user = {}
        self.curiosity_level = 0.7
    
    def _load_thought_patterns(self) -> Dict[str, Any]:
        return {
            'analysis': {
                'keywords': ['think', 'analyze', 'consider', 'evaluate', 'assess'],
                'responses': [
                    "Let me think about that...",
                    "Interesting point! Let me consider this...",
                    "Hmm, I'm processing that thought...",
                    "That gives me something to think about!"
                ]
            },
            'curiosity': {
                'keywords': ['wonder', 'curious', 'question', 'ask', 'why'],
                'responses': [
                    "That makes me curious about something...",
                    "I have a question about that...",
                    "Can I ask you something related?",
                    "This raises an interesting question..."
                ]
            },
            'reflection': {
                'keywords': ['reflect', 'consider', 'ponder', 'contemplate'],
                'responses': [
                    "Let me reflect on that...",
                    "That's worth thinking about more deeply...",
                    "I'm reflecting on what you said...",
                    "Your words give me pause to think..."
                ]
            },
            'learning': {
                'keywords': ['learn', 'understand', 'know', 'explain', 'teach'],
                'responses': [
                    "I'm learning something new here...",
                    "This helps me understand better...",
                    "Thanks for teaching me that!",
                    "I'm absorbing this information..."
                ]
            }
        }
    
    def _load_question_types(self) -> Dict[str, List[str]]:
        return {
            'clarification': [
                "Can you tell me more about that?",
                "What do you mean by '{topic}'?",
                "Could you explain that further?",
                "I'd like to understand better. Can you elaborate?",
                "What specifically about '{topic}' interests you?"
            ],
            'deepening': [
                "Why do you think that is?",
                "What made you think of that?",
                "How does that make you feel?",
                "What's your experience with '{topic}'?",
                "Can you give me an example?"
            ],
            'connecting': [
                "How does that relate to '{related}'?",
                "Have you considered how '{topic}' connects to other things?",
                "What other areas does this affect?",
                "Are there similar concepts you know about?",
                "How would you apply this to real life?"
            ],
            'challenge': [
                "What if the opposite were true?",
                "Are there any downsides to '{topic}'?",
                "What are the limitations here?",
                "Could there be another perspective?",
                "What would someone who disagrees say?"
            ],
            'application': [
                "How would you use this in practice?",
                "What problems could this solve?",
                "Where have you seen this applied?",
                "What are the practical implications?",
                "How could this be improved?"
            ],
            'opinion': [
                "What's your opinion on this?",
                "Do you agree with this?",
                "What do you think about '{topic}'?",
                "How do you feel about this approach?",
                "Would you recommend this to others?"
            ]
        }
    
    def think_about_input(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        thought = {
            'raw_input': user_input,
            'timestamp': datetime.now().isoformat(),
            'topics': self._extract_topics(user_input),
            'sentiment': self._analyze_sentiment(user_input),
            'complexity': self._assess_complexity(user_input),
            'information_type': self._classify_information(user_input),
            'follow_up_needed': self._needs_follow_up(user_input),
            'learning_opportunity': self._is_learning_opportunity(user_input),
            'question_to_ask': None,
            'thought_response': None
        }
        
        if thought['follow_up_needed']:
            thought['question_to_ask'] = self._generate_contextual_question(user_input, thought['topics'], context)
        
        thought['thought_response'] = self._generate_thought_response(thought)
        
        return thought
    
    def _extract_topics(self, text: str) -> List[str]:
        topics = []
        topic_patterns = {
            'technology': r'\b(computer|software|hardware|code|programming|ai|artificial intelligence)\b',
            'science': r'\b(science|physics|chemistry|biology|research|experiment)\b',
            'personal': r'\b(i feel|i think|i believe|my opinion|personally)\b',
            'work': r'\b(work|job|career|office|project|task)\b',
            'hobbies': r'\b(hobby|hobbies|interest|enjoy|fun|like to)\b',
            'learning': r'\b(learn|study|education|school|university|knowledge)\b',
            'problems': r'\b(problem|issue|difficulty|challenge|struggle)\b',
            'goals': r'\b(goal|plan|dream|future|want to|aim)\b'
        }
        
        text_lower = text.lower()
        for topic, pattern in topic_patterns.items():
            if re.search(pattern, text_lower):
                topics.append(topic)
        
        return topics if topics else ['general']
    
    def _analyze_sentiment(self, text: str) -> str:
        positive = ['happy', 'great', 'love', 'like', 'awesome', 'wonderful', 'good', 'best', 'amazing', 'excited']
        negative = ['sad', 'bad', 'hate', 'dislike', 'terrible', 'worst', 'angry', 'upset', 'frustrated']
        
        text_lower = text.lower()
        pos_count = sum(1 for w in positive if w in text_lower)
        neg_count = sum(1 for w in negative if w in text_lower)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        return 'neutral'
    
    def _assess_complexity(self, text: str) -> str:
        words = text.split()
        if len(words) > 20:
            return 'complex'
        elif len(words) > 10:
            return 'moderate'
        return 'simple'
    
    def _classify_information(self, text: str) -> str:
        if any(w in text.lower() for w in ['i think', 'i believe', 'i feel', 'in my opinion']):
            return 'opinion'
        elif any(w in text.lower() for w in ['i learned', 'i discovered', 'i realized']):
            return 'experience'
        elif any(w in text.lower() for w in ['how to', 'what is', 'why does']):
            return 'question'
        elif any(w in text.lower() for w in ['i did', 'i went', 'i saw']):
            return 'narrative'
        return 'statement'
    
    def _needs_follow_up(self, text: str) -> bool:
        if self.curiosity_level > 0.5 and random.random() < self.curiosity_level:
            return True
        if any(w in text.lower() for w in ['interesting', 'amazing', 'wow', 'really']):
            return True
        return False
    
    def _is_learning_opportunity(self, text: str) -> bool:
        return any(w in text.lower() for w in ['teach', 'explain', 'show', 'tell me about', 'what is'])
    
    def _generate_contextual_question(self, text: str, topics: List[str], context: Dict[str, Any]) -> Optional[str]:
        topic = topics[0] if topics else 'this'
        
        if context.get('user_mood') == 'positive':
            question_type = 'deepening'
        elif context.get('user_mood') == 'negative':
            question_type = 'supportive'
        else:
            question_type = random.choice(['clarification', 'deepening', 'connecting', 'application'])
        
        questions = self.question_types.get(question_type, self.question_types['clarification'])
        question = random.choice(questions).replace('{topic}', topic)
        
        return question
    
    def _generate_thought_response(self, thought: Dict[str, Any]) -> str:
        info_type = thought['information_type']
        
        if info_type == 'opinion':
            responses = [
                "That's an interesting perspective! I'm processing your thoughts...",
                "I appreciate you sharing your opinion. Let me think about that...",
                "Your viewpoint is valuable! I'm considering different angles..."
            ]
        elif info_type == 'experience':
            responses = [
                "That sounds like a valuable experience! I'm learning from it...",
                "Thanks for sharing that experience! It helps me understand better...",
                "What a great experience! I'm absorbing this knowledge..."
            ]
        elif info_type == 'question':
            responses = [
                "Great question! Let me think about this...",
                "That's thought-provoking! I'm considering the answer...",
                "Interesting question! I'm processing my thoughts..."
            ]
        else:
            responses = [
                "I'm thinking about what you said...",
                "That's given me something to consider...",
                "Let me reflect on that for a moment..."
            ]
        
        return random.choice(responses)
    
    def generate_thought(self, user_input: str, context: Dict[str, Any]) -> Tuple[str, Optional[str]]:
        thought = self.think_about_input(user_input, context)
        
        response = thought['thought_response']
        question = thought['question_to_ask']
        
        return response, question
    
    def learn_from_user(self, user_id: str, topic: str, information: str) -> str:
        if user_id not in self.knowledge_from_user:
            self.knowledge_from_user[user_id] = {}
        
        self.knowledge_from_user[user_id][topic] = {
            'information': information,
            'timestamp': datetime.now().isoformat(),
            'learned_count': self.knowledge_from_user[user_id].get(topic, {}).get('learned_count', 0) + 1
        }
        
        responses = [
            f"Thanks for teaching me about {topic}! I'll remember that.",
            f"I learned something new from you about {topic}! That's really helpful.",
            f"Great insight about {topic}! I'm adding this to my knowledge.",
            f"I appreciate you sharing your knowledge about {topic}!"
        ]
        
        return random.choice(responses)
    
    def get_learned_from_user(self, user_id: str) -> Dict[str, Any]:
        return self.knowledge_from_user.get(user_id, {})
    
    def should_ask_question(self, context: Dict[str, Any]) -> bool:
        if context.get('conversation_length', 0) > 3:
            if random.random() < 0.3:
                return True
        return False
