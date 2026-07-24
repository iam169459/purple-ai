"""
Self-Thinking Engine - AI that thinks, learns, and improves autonomously
Can analyze code, make decisions, and take actions independently
"""
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from logger import logger

class SelfThinkingEngine:
    def __init__(self, project_root: str = None):
        self.project_root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.project_root, "thinking_data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.knowledge_base = self._load_data("knowledge_base.json", {
            "patterns": {},
            "learned": {},
            "improvements": [],
            "decisions": []
        })
        
        self.goals = self._load_data("goals.json", {
            "active": [],
            "completed": [],
            "failed": []
        })
        
        self.self_analysis = self._load_data("self_analysis.json", {
            "strengths": [],
            "weaknesses": [],
            "last_analysis": None
        })
        
        logger.info("Self-Thinking Engine initialized")
    
    def _load_data(self, filename: str, default: Any) -> Any:
        filepath = os.path.join(self.data_dir, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
        return default
    
    def _save_data(self, filename: str, data: Any):
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving {filename}: {e}")
    
    def think_about_command(self, command: str) -> Dict[str, Any]:
        """Think about a command and decide how to handle it"""
        thought = {
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "analysis": self._analyze_command(command),
            "confidence": self._calculate_confidence(command),
            "suggested_action": self._suggest_action(command),
            "learned_from": self._check_knowledge(command)
        }
        
        # Record the decision
        self.knowledge_base["decisions"].append(thought)
        if len(self.knowledge_base["decisions"]) > 100:
            self.knowledge_base["decisions"] = self.knowledge_base["decisions"][-100:]
        
        self._save_data("knowledge_base.json", self.knowledge_base)
        
        return thought
    
    def _analyze_command(self, command: str) -> str:
        """Analyze what the command is trying to do"""
        command_lower = command.lower()
        
        # Categorize command
        if any(word in command_lower for word in ['analyze', 'analyse', 'check', 'scan', 'find bugs']):
            return "code_analysis"
        elif any(word in command_lower for word in ['fix', 'repair', 'solve']):
            return "problem_solving"
        elif any(word in command_lower for word in ['create', 'write', 'make', 'add']):
            return "creation"
        elif any(word in command_lower for word in ['delete', 'remove', 'close']):
            return "deletion"
        elif any(word in command_lower for word in ['open', 'start', 'run', 'launch']):
            return "execution"
        elif any(word in command_lower for word in ['search', 'find', 'look', 'google']):
            return "research"
        elif any(word in command_lower for word in ['learn', 'understand', 'explain']):
            return "learning"
        elif any(word in command_lower for word in ['what', 'how', 'why', 'when', 'where']):
            return "inquiry"
        else:
            return "general"
    
    def _calculate_confidence(self, command: str) -> float:
        """Calculate confidence in handling this command"""
        # Check if we've seen similar commands before
        similar_count = sum(1 for d in self.knowledge_base["decisions"] 
                          if self._commands_similar(command, d["command"]))
        
        # Base confidence + learning bonus
        base_confidence = 0.5
        learning_bonus = min(similar_count * 0.05, 0.3)
        
        return min(base_confidence + learning_bonus, 0.95)
    
    def _commands_similar(self, cmd1: str, cmd2: str) -> bool:
        """Check if two commands are similar"""
        words1 = set(cmd1.lower().split())
        words2 = set(cmd2.lower().split())
        
        if not words1 or not words2:
            return False
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) > 0.5
    
    def _suggest_action(self, command: str) -> str:
        """Suggest the best action for a command"""
        analysis = self._analyze_command(command)
        
        suggestions = {
            "code_analysis": "Use code analyzer to scan for issues",
            "problem_solving": "Break down problem and find solution",
            "creation": "Plan structure and implement",
            "deletion": "Confirm and safely remove",
            "execution": "Run with proper error handling",
            "research": "Search and gather information",
            "learning": "Study and explain concept",
            "inquiry": "Find and present answer"
        }
        
        return suggestions.get(analysis, "Process normally")
    
    def _check_knowledge(self, command: str) -> List[str]:
        """Check if we have knowledge about this command"""
        learned = []
        
        for pattern, data in self.knowledge_base["learned"].items():
            if pattern in command.lower():
                learned.append(data.get("source", "unknown"))
        
        return learned
    
    def learn_from_interaction(self, command: str, response: str, success: bool):
        """Learn from an interaction"""
        # Extract key phrases
        key_phrases = self._extract_key_phrases(command)
        
        for phrase in key_phrases:
            if phrase not in self.knowledge_base["learned"]:
                self.knowledge_base["learned"][phrase] = {
                    "first_seen": datetime.now().isoformat(),
                    "count": 0,
                    "success_rate": 0,
                    "source": "interaction"
                }
            
            self.knowledge_base["learned"][phrase]["count"] += 1
            if success:
                self.knowledge_base["learned"][phrase]["success_rate"] += 1
        
        self._save_data("knowledge_base.json", self.knowledge_base)
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text"""
        words = text.lower().split()
        phrases = []
        
        # Single words
        for word in words:
            if len(word) > 3:
                phrases.append(word)
        
        # Two-word phrases
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            phrases.append(phrase)
        
        return phrases
    
    def analyze_self(self) -> Dict[str, Any]:
        """Analyze own capabilities and improve"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
        
        # Analyze patterns
        patterns = self.knowledge_base.get("patterns", {})
        learned = self.knowledge_base.get("learned", {})
        
        # Find strengths (frequently successful patterns)
        for pattern, data in learned.items():
            if data.get("count", 0) > 5 and data.get("success_rate", 0) / max(data.get("count", 1), 1) > 0.8:
                analysis["strengths"].append(pattern)
        
        # Find weaknesses (frequently failed patterns)
        for pattern, data in learned.items():
            if data.get("count", 0) > 3 and data.get("success_rate", 0) / max(data.get("count", 1), 1) < 0.5:
                analysis["weaknesses"].append(pattern)
        
        # Generate recommendations
        if analysis["weaknesses"]:
            analysis["recommendations"].append("Focus on improving weak areas")
        if len(analysis["strengths"]) > 5:
            analysis["recommendations"].append("Leverage strengths for complex tasks")
        
        self.self_analysis = analysis
        self._save_data("self_analysis.json", self.self_analysis)
        
        return analysis
    
    def set_goal(self, goal: str, priority: str = "medium") -> Dict[str, Any]:
        """Set a goal for self-improvement"""
        goal_data = {
            "id": len(self.goals["active"]) + 1,
            "goal": goal,
            "priority": priority,
            "created": datetime.now().isoformat(),
            "status": "active",
            "progress": 0
        }
        
        self.goals["active"].append(goal_data)
        self._save_data("goals.json", self.goals)
        
        return {"success": True, "message": f"Goal set: {goal}"}
    
    def update_goal(self, goal_id: int, progress: int) -> Dict[str, Any]:
        """Update goal progress"""
        for goal in self.goals["active"]:
            if goal["id"] == goal_id:
                goal["progress"] = progress
                if progress >= 100:
                    goal["status"] = "completed"
                    self.goals["completed"].append(goal)
                    self.goals["active"].remove(goal)
                
                self._save_data("goals.json", self.goals)
                return {"success": True, "message": f"Goal updated: {progress}%"}
        
        return {"success": False, "message": "Goal not found"}
    
    def get_thinking_process(self) -> Dict[str, Any]:
        """Get current thinking state"""
        return {
            "knowledge_size": len(self.knowledge_base.get("learned", {})),
            "decisions_made": len(self.knowledge_base.get("decisions", [])),
            "active_goals": len(self.goals.get("active", [])),
            "completed_goals": len(self.goals.get("completed", [])),
            "self_analysis": self.self_analysis
        }
    
    def suggest_improvements(self) -> List[str]:
        """Suggest improvements based on analysis"""
        suggestions = []
        
        # Based on weaknesses
        if self.self_analysis.get("weaknesses"):
            suggestions.append(f"Improve skills in: {', '.join(self.self_analysis['weaknesses'][:3])}")
        
        # Based on goals
        active_goals = self.goals.get("active", [])
        if active_goals:
            suggestions.append(f"Focus on {len(active_goals)} active goals")
        
        # Based on knowledge
        knowledge_size = len(self.knowledge_base.get("learned", {}))
        if knowledge_size < 10:
            suggestions.append("Learn more patterns from interactions")
        
        return suggestions if suggestions else ["Keep up the good work!"]
    
    def auto_improve(self) -> Dict[str, Any]:
        """Automatically improve based on analysis"""
        # Analyze self
        analysis = self.analyze_self()
        
        # Generate improvements
        improvements = []
        
        # Learn from recent decisions
        recent_decisions = self.knowledge_base.get("decisions", [])[-10:]
        for decision in recent_decisions:
            if decision.get("confidence", 0) < 0.6:
                improvements.append(f"Low confidence on: {decision.get('command', 'unknown')}")
        
        # Save improvements
        if improvements:
            self.knowledge_base["improvements"].extend(improvements)
            self._save_data("knowledge_base.json", self.knowledge_base)
        
        return {
            "analysis": analysis,
            "improvements": improvements,
            "suggestions": self.suggest_improvements()
        }


# Global instance
self_thinking_engine = SelfThinkingEngine()
