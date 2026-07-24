"""
Hypothesis Engine
Generates, evaluates, and tests hypotheses from partial information
"""
import json
import os
import time
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from collections import deque
from logger import logger


class Hypothesis:
    """A single hypothesis with evidence tracking"""
    
    def __init__(self, statement: str, prior: float = 0.5, context: str = ""):
        self.statement = statement
        self.prior = prior
        self.context = context
        self.posterior = prior
        self.evidence_for = []
        self.evidence_against = []
        self.status = "active"  # active, confirmed, rejected, uncertain
        self.created_at = datetime.now().isoformat()
        self.tested_at = None
        self.confidence_history = [prior]
    
    def add_evidence(self, evidence: str, supports: bool, strength: float = 0.1):
        """Add evidence and update posterior probability"""
        entry = {
            "evidence": evidence,
            "supports": supports,
            "strength": strength,
            "timestamp": datetime.now().isoformat()
        }
        
        if supports:
            self.evidence_for.append(entry)
            self.posterior = min(0.95, self.posterior + strength)
        else:
            self.evidence_against.append(entry)
            self.posterior = max(0.05, self.posterior - strength)
        
        self.confidence_history.append(self.posterior)
    
    def confirm(self):
        """Mark hypothesis as confirmed"""
        self.status = "confirmed"
        self.tested_at = datetime.now().isoformat()
    
    def reject(self, reason: str = ""):
        """Mark hypothesis as rejected"""
        self.status = "rejected"
        self.tested_at = datetime.now().isoformat()
        if reason:
            self.evidence_against.append({
                "evidence": f"Rejected: {reason}",
                "supports": False,
                "strength": 1.0,
                "timestamp": datetime.now().isoformat()
            })
    
    def get_strength(self) -> float:
        """Get current strength of hypothesis"""
        total_evidence = len(self.evidence_for) + len(self.evidence_against)
        if total_evidence == 0:
            return self.prior
        return self.posterior
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "statement": self.statement,
            "prior": self.prior,
            "posterior": self.posterior,
            "context": self.context,
            "status": self.status,
            "evidence_for_count": len(self.evidence_for),
            "evidence_against_count": len(self.evidence_against),
            "created_at": self.created_at,
            "tested_at": self.tested_at,
            "confidence_history": self.confidence_history
        }


class HypothesisEngine:
    """
    Generates and tests hypotheses from partial information.
    Uses knowledge graph for evidence gathering and Bayesian-style updating.
    """
    
    def __init__(self, knowledge_graph=None, data_dir: str = None):
        self.kg = knowledge_graph
        self.data_dir = data_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "thinking_data"
        )
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.active_hypotheses = deque(maxlen=20)
        self.confirmed_hypotheses = deque(maxlen=100)
        self.rejected_hypotheses = deque(maxlen=100)
        self.history = self._load("hypothesis_history.json", {
            "total_generated": 0,
            "total_confirmed": 0,
            "total_rejected": 0,
            "accuracy": 0.0,
            "sessions": []
        })
        
        logger.info("Hypothesis Engine initialized")
    
    def _load(self, filename: str, default: Any) -> Any:
        filepath = os.path.join(self.data_dir, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"HypothesisEngine load error: {e}")
        return default
    
    def _save(self, filename: str, data: Any):
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"HypothesisEngine save error: {e}")
    
    # ==================== HYPOTHESIS GENERATION ====================
    
    def generate_hypotheses(self, observation: str, context: Dict[str, Any] = None) -> List[Hypothesis]:
        """
        Given an observation or question, generate 2-4 hypotheses.
        
        Args:
            observation: The input text to form hypotheses about
            context: Optional context dict with keys like 'emotion', 'topics', etc.
        
        Returns:
            List of Hypothesis objects ranked by prior probability
        """
        context = context or {}
        text_lower = observation.lower().strip()
        hypotheses = []
        
        # Pattern 1: "Why" questions → causal hypotheses
        if "why" in text_lower:
            hypotheses.extend(self._generate_causal_hypotheses(text_lower, context))
        
        # Pattern 2: "How" questions → process hypotheses
        elif "how" in text_lower:
            hypotheses.extend(self._generate_process_hypotheses(text_lower, context))
        
        # Pattern 3: Comparison questions → relative hypotheses
        elif any(w in text_lower for w in ["better", "worse", "compare", "versus", "best", "worst"]):
            hypotheses.extend(self._generate_comparison_hypotheses(text_lower, context))
        
        # Pattern 4: Prediction questions → outcome hypotheses
        elif any(w in text_lower for w in ["will", "predict", "future", "expect", "happen"]):
            hypotheses.extend(self._generate_prediction_hypotheses(text_lower, context))
        
        # Pattern 5: Problem statements → solution hypotheses
        elif any(w in text_lower for w in ["problem", "issue", "error", "bug", "broken", "fix"]):
            hypotheses.extend(self._generate_solution_hypotheses(text_lower, context))
        
        # Pattern 6: General → analytical hypotheses
        else:
            hypotheses.extend(self._generate_analytical_hypotheses(text_lower, context))
        
        # Rank by prior probability
        hypotheses.sort(key=lambda h: h.prior, reverse=True)
        
        # Keep only top 4
        hypotheses = hypotheses[:4]
        
        # Store active hypotheses
        for h in hypotheses:
            self.active_hypotheses.append(h)
        
        self.history["total_generated"] += len(hypotheses)
        self._save("hypothesis_history.json", self.history)
        
        logger.info(f"Generated {len(hypotheses)} hypotheses for: {observation[:50]}...")
        return hypotheses
    
    def _generate_causal_hypotheses(self, text: str, context: dict) -> List[Hypothesis]:
        """Generate hypotheses for 'why' questions"""
        hypotheses = []
        
        # Extract the subject of the "why" question
        subject = self._extract_subject(text)
        
        # Common causal patterns
        hypotheses.append(Hypothesis(
            f"There is a direct, identifiable cause for {subject}",
            prior=0.6,
            context="direct_cause"
        ))
        hypotheses.append(Hypothesis(
            f"Multiple factors contribute to {subject}",
            prior=0.3,
            context="multiple_causes"
        ))
        hypotheses.append(Hypothesis(
            f"The cause is systemic or structural rather than immediate",
            prior=0.2,
            context="systemic_cause"
        ))
        
        # If we have knowledge graph, look for causal links
        if self.kg:
            causes = self.kg.query_causes(subject)
            if causes:
                for cause_data in causes[:2]:
                    hypotheses.append(Hypothesis(
                        f"{cause_data['cause'].title()} causes {subject}",
                        prior=cause_data["confidence"],
                        context="knowledge_graph_causal"
                    ))
        
        return hypotheses
    
    def _generate_process_hypotheses(self, text: str, context: dict) -> List[Hypothesis]:
        """Generate hypotheses for 'how' questions"""
        hypotheses = []
        subject = self._extract_subject(text)
        
        hypotheses.append(Hypothesis(
            f"There is a standard, well-documented process for {subject}",
            prior=0.5,
            context="standard_process"
        ))
        hypotheses.append(Hypothesis(
            f"There are multiple valid approaches to {subject}",
            prior=0.4,
            context="multiple_approaches"
        ))
        hypotheses.append(Hypothesis(
            f"{subject} requires creative or non-standard methods",
            prior=0.15,
            context="creative_process"
        ))
        
        return hypotheses
    
    def _generate_comparison_hypotheses(self, text: str, context: dict) -> List[Hypothesis]:
        """Generate hypotheses for comparison questions"""
        hypotheses = []
        
        hypotheses.append(Hypothesis(
            "Option A is clearly superior based on objective criteria",
            prior=0.3,
            context="objective_comparison"
        ))
        hypotheses.append(Hypothesis(
            "Option B is clearly superior based on objective criteria",
            prior=0.3,
            context="objective_comparison"
        ))
        hypotheses.append(Hypothesis(
            "The better choice depends on specific context and priorities",
            prior=0.5,
            context="context_dependent"
        ))
        
        return hypotheses
    
    def _generate_prediction_hypotheses(self, text: str, context: dict) -> List[Hypothesis]:
        """Generate hypotheses for prediction questions"""
        hypotheses = []
        
        hypotheses.append(Hypothesis(
            "Current trends will continue",
            prior=0.4,
            context="trend_continuation"
        ))
        hypotheses.append(Hypothesis(
            "A disruption or change is likely",
            prior=0.3,
            context="disruption"
        ))
        hypotheses.append(Hypothesis(
            "The outcome is too uncertain to predict reliably",
            prior=0.3,
            context="uncertain"
        ))
        
        return hypotheses
    
    def _generate_solution_hypotheses(self, text: str, context: dict) -> List[Hypothesis]:
        """Generate hypotheses for problem statements"""
        hypotheses = []
        subject = self._extract_subject(text)
        
        hypotheses.append(Hypothesis(
            f"The problem has a known solution that can be applied directly",
            prior=0.5,
            context="known_solution"
        ))
        hypotheses.append(Hypothesis(
            f"The problem requires a creative or adapted solution",
            prior=0.3,
            context="creative_solution"
        ))
        hypotheses.append(Hypothesis(
            f"The problem has multiple root causes that need separate fixes",
            prior=0.3,
            context="multiple_roots"
        ))
        
        # Knowledge graph lookup
        if self.kg:
            requirements = self.kg.query_requirements(subject)
            if requirements:
                hypotheses.append(Hypothesis(
                    f"Addressing requirements {[r['required'] for r in requirements[:2]]} will solve it",
                    prior=0.6,
                    context="requirement_based"
                ))
        
        return hypotheses
    
    def _generate_analytical_hypotheses(self, text: str, context: dict) -> List[Hypothesis]:
        """Generate hypotheses for general analytical questions"""
        hypotheses = []
        
        hypotheses.append(Hypothesis(
            "The straightforward interpretation is correct",
            prior=0.5,
            context="straightforward"
        ))
        hypotheses.append(Hypothesis(
            "There is additional context that changes the interpretation",
            prior=0.25,
            context="hidden_context"
        ))
        hypotheses.append(Hypothesis(
            "Multiple valid interpretations exist",
            prior=0.25,
            context="multiple_interpretations"
        ))
        
        return hypotheses
    
    def _extract_subject(self, text: str) -> str:
        """Extract the main subject from a question"""
        # Remove question words and common phrases
        cleaned = re.sub(r'(why|how|what|when|where|who|is|does|do|can|could|would|should)\s+', '', text)
        cleaned = re.sub(r'\?', '', cleaned).strip()
        
        # Take first few words as subject
        words = cleaned.split()
        if len(words) > 4:
            return ' '.join(words[:4])
        return cleaned if cleaned else "this"
    
    # ==================== HYPOTHESIS EVALUATION ====================
    
    def evaluate_evidence(self, hypothesis_idx: int, evidence: str, supports: bool, 
                          strength: float = 0.1) -> Dict[str, Any]:
        """
        Add evidence to a hypothesis and update its ranking.
        
        Returns updated hypothesis state.
        """
        if hypothesis_idx < 0 or hypothesis_idx >= len(self.active_hypotheses):
            return {"error": "Invalid hypothesis index"}
        
        hypothesis = self.active_hypotheses[hypothesis_idx]
        hypothesis.add_evidence(evidence, supports, strength)
        
        # Auto-confirm or reject based on threshold
        if hypothesis.posterior > 0.85:
            hypothesis.confirm()
            self.confirmed_hypotheses.append(hypothesis)
            self.history["total_confirmed"] += 1
        elif hypothesis.posterior < 0.15:
            hypothesis.reject("Evidence strongly contradicts")
            self.rejected_hypotheses.append(hypothesis)
            self.history["total_rejected"] += 1
        
        self._update_accuracy()
        self._save("hypothesis_history.json", self.history)
        
        return {
            "hypothesis": hypothesis.statement,
            "posterior": hypothesis.posterior,
            "status": hypothesis.status,
            "evidence_count": len(hypothesis.evidence_for) + len(hypothesis.evidence_against)
        }
    
    def confirm_hypothesis(self, hypothesis_idx: int, reason: str = "") -> bool:
        """Manually confirm a hypothesis"""
        if 0 <= hypothesis_idx < len(self.active_hypotheses):
            h = self.active_hypotheses[hypothesis_idx]
            h.confirm()
            self.confirmed_hypotheses.append(h)
            self.history["total_confirmed"] += 1
            self._update_accuracy()
            self._save("hypothesis_history.json", self.history)
            logger.info(f"Hypothesis confirmed: {h.statement[:50]}...")
            return True
        return False
    
    def reject_hypothesis(self, hypothesis_idx: int, reason: str = "") -> bool:
        """Manually reject a hypothesis"""
        if 0 <= hypothesis_idx < len(self.active_hypotheses):
            h = self.active_hypotheses[hypothesis_idx]
            h.reject(reason)
            self.rejected_hypotheses.append(h)
            self.history["total_rejected"] += 1
            self._update_accuracy()
            self._save("hypothesis_history.json", self.history)
            logger.info(f"Hypothesis rejected: {h.statement[:50]}... | reason: {reason}")
            return True
        return False
    
    def _update_accuracy(self):
        """Update overall accuracy metric"""
        total = self.history["total_confirmed"] + self.history["total_rejected"]
        if total > 0:
            self.history["accuracy"] = round(self.history["total_confirmed"] / total, 2)
    
    # ==================== HYPOTHESIS QUERIES ====================
    
    def get_most_likely(self) -> Optional[Hypothesis]:
        """Get the highest-ranked active hypothesis"""
        active = [h for h in self.active_hypotheses if h.status == "active"]
        if not active:
            return None
        return max(active, key=lambda h: h.posterior)
    
    def get_all_active(self) -> List[Dict[str, Any]]:
        """Get all active hypotheses"""
        return [h.to_dict() for h in self.active_hypotheses if h.status == "active"]
    
    def get_ranked_hypotheses(self) -> List[Dict[str, Any]]:
        """Get all active hypotheses ranked by posterior"""
        active = [h for h in self.active_hypotheses if h.status == "active"]
        active.sort(key=lambda h: h.posterior, reverse=True)
        return [h.to_dict() for h in active]
    
    def get_hypothesis_report(self) -> Dict[str, Any]:
        """Get statistics on hypothesis generation and testing"""
        return {
            "total_generated": self.history["total_generated"],
            "total_confirmed": self.history["total_confirmed"],
            "total_rejected": self.history["total_rejected"],
            "accuracy": self.history["accuracy"],
            "currently_active": len([h for h in self.active_hypotheses if h.status == "active"]),
            "recent_confirmed": [h.to_dict() for h in list(self.confirmed_hypotheses)[-5:]],
            "recent_rejected": [h.to_dict() for h in list(self.rejected_hypotheses)[-5:]]
        }
    
    def learn_from_outcome(self, hypothesis_idx: int, was_correct: bool):
        """Learn from whether a hypothesis turned out to be correct"""
        if 0 <= hypothesis_idx < len(self.active_hypotheses):
            h = self.active_hypotheses[hypothesis_idx]
            
            if was_correct:
                self.history["total_confirmed"] += 1
            else:
                self.history["total_rejected"] += 1
            
            self._update_accuracy()
            self._save("hypothesis_history.json", self.history)
    
    def clear_active(self):
        """Clear all active hypotheses"""
        self.active_hypotheses.clear()


# Global instance (created on import, KG wired later)
hypothesis_engine = HypothesisEngine()
