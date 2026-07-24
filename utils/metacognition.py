"""
Metacognition Engine - Think About Thinking
Monitors reasoning quality, calibrates confidence, and selects optimal strategies
"""
import json
import os
import time
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import deque
from logger import logger


class Metacognition:
    """
    Metacognitive system that monitors, evaluates, and improves the AI's own thinking.
    
    Core capabilities:
    - Task assessment: determine problem type and best approach
    - Self-critique: evaluate reasoning quality after the fact
    - Confidence calibration: learn when to be confident vs uncertain
    - Strategy selection: pick the best thinking strategy per task
    - Assumption tracking: log and verify assumptions made during reasoning
    """
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "thinking_data"
        )
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load persistent data
        self.calibration_data = self._load("calibration.json", {
            "predictions": [],  # {predicted_confidence, actual_outcome, timestamp}
            "by_bucket": {}     # confidence_bucket → {total, correct}
        })
        
        self.strategy_performance = self._load("strategy_performance.json", {
            "analytical": {"attempts": 0, "successes": 0, "avg_quality": 0.7},
            "intuitive": {"attempts": 0, "successes": 0, "avg_quality": 0.6},
            "creative": {"attempts": 0, "successes": 0, "avg_quality": 0.5},
            "empathetic": {"attempts": 0, "successes": 0, "avg_quality": 0.65},
            "research_heavy": {"attempts": 0, "successes": 0, "avg_quality": 0.75},
            "step_by_step": {"attempts": 0, "successes": 0, "avg_quality": 0.8}
        })
        
        self.assumptions_log = deque(maxlen=200)
        self.recent_assessments = deque(maxlen=50)
        
        # Task type keywords
        self._task_patterns = {
            "factual": {
                "keywords": ["what", "when", "where", "who", "how many", "how much", 
                             "define", "list", "name", "describe"],
                "strategy": "step_by_step",
                "needs_evidence": True
            },
            "analytical": {
                "keywords": ["why", "how", "explain", "analyze", "compare", "contrast",
                             "evaluate", "assess", "prove", "reason", "because"],
                "strategy": "analytical",
                "needs_evidence": True
            },
            "creative": {
                "keywords": ["imagine", "create", "design", "invent", "what if",
                             "could you", "write", "story", "poem", "brainstorm"],
                "strategy": "creative",
                "needs_evidence": False
            },
            "emotional": {
                "keywords": ["feel", "feeling", "emotion", "sad", "happy", "angry",
                             "worried", "love", "miss", "lonely", "stressed", "anxious"],
                "strategy": "empathetic",
                "needs_evidence": False
            },
            "problem_solving": {
                "keywords": ["solve", "fix", "debug", "error", "problem", "issue",
                             "broken", "wrong", "fail", "crash", "bug"],
                "strategy": "step_by_step",
                "needs_evidence": True
            },
            "opinion": {
                "keywords": ["think", "opinion", "believe", "prefer", "recommend",
                             "suggest", "advice", "should", "best", "worst"],
                "strategy": "analytical",
                "needs_evidence": True
            },
            "procedural": {
                "keywords": ["how to", "steps", "process", "method", "procedure",
                             "tutorial", "guide", "instruction"],
                "strategy": "step_by_step",
                "needs_evidence": False
            },
            "complex": {
                "keywords": ["multi-step", "first.*then", "consequences", "implications",
                             "trade.?offs", "pros.*cons", "if.*then", "scenario"],
                "strategy": "step_by_step",
                "needs_evidence": True
            }
        }
        
        logger.info("Metacognition engine initialized")
    
    # ==================== FILE I/O ====================
    
    def _load(self, filename: str, default: Any) -> Any:
        filepath = os.path.join(self.data_dir, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Metacognition load error ({filename}): {e}")
        return default
    
    def _save(self, filename: str, data: Any):
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Metacognition save error ({filename}): {e}")
    
    # ==================== TASK ASSESSMENT ====================
    
    def assess_task(self, input_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Assess the incoming task to determine the best thinking strategy.
        
        Returns:
            {
                "task_type": str,          # factual|analytical|creative|emotional|...
                "strategy": str,           # Best strategy to use
                "difficulty": float,       # 0.0 (trivial) to 1.0 (very complex)
                "needs_evidence": bool,    # Should we look up facts?
                "needs_hypothesis": bool,  # Should we generate hypotheses?
                "multi_step": bool,        # Does this need decomposition?
                "estimated_steps": int,    # How many reasoning steps needed
                "emotional_weight": float, # How emotionally charged (0-1)
                "complexity_signals": list # What makes this complex
            }
        """
        text_lower = input_text.lower().strip()
        words = text_lower.split()
        
        # Detect task type(s)
        detected_types = []
        for task_type, config in self._task_patterns.items():
            for keyword in config["keywords"]:
                if re.search(keyword, text_lower):
                    detected_types.append(task_type)
                    break
        
        if not detected_types:
            detected_types = ["factual"]  # Default
        
        # Primary task type is the most specific match
        primary_type = detected_types[0]
        if "complex" in detected_types:
            primary_type = "complex"
        elif "analytical" in detected_types:
            primary_type = "analytical"
        elif "problem_solving" in detected_types:
            primary_type = "problem_solving"
        
        # Get strategy for this task type
        strategy = self._task_patterns[primary_type]["strategy"]
        needs_evidence = self._task_patterns[primary_type]["needs_evidence"]
        
        # Analyze complexity
        complexity_signals = []
        difficulty = 0.0
        
        # Word count signals complexity
        if len(words) > 30:
            complexity_signals.append("long_input")
            difficulty += 0.2
        elif len(words) > 15:
            complexity_signals.append("moderate_length")
            difficulty += 0.1
        
        # Multiple questions = multi-step
        question_count = text_lower.count("?")
        if question_count > 2:
            complexity_signals.append("multiple_questions")
            difficulty += 0.3
        elif question_count > 1:
            complexity_signals.append("multi_part_question")
            difficulty += 0.15
        
        # Conditional logic = complex reasoning
        if any(w in text_lower for w in ["if", "then", "else", "unless", "assuming", "suppose"]):
            complexity_signals.append("conditional_logic")
            difficulty += 0.25
        
        # Comparisons = analytical
        if any(w in text_lower for w in ["compare", "versus", "vs", "difference", "better", "worse"]):
            complexity_signals.append("comparison_needed")
            difficulty += 0.15
        
        # Causal reasoning
        if any(w in text_lower for w in ["because", "therefore", "consequently", "results in", "leads to"]):
            complexity_signals.append("causal_reasoning")
            difficulty += 0.2
        
        # Abstraction
        if any(w in text_lower for w in ["concept", "theory", "principle", "philosophy", "abstract"]):
            complexity_signals.append("abstract_concepts")
            difficulty += 0.15
        
        # Multiple clauses (commas suggest complexity)
        if input_text.count(",") > 3:
            complexity_signals.append("complex_sentence")
            difficulty += 0.1
        
        # Technical domain
        technical_terms = ["algorithm", "function", "variable", "class", "method", 
                          "database", "server", "api", "quantum", "neural", "entropy"]
        if any(t in text_lower for t in technical_terms):
            complexity_signals.append("technical_domain")
            difficulty += 0.15
        
        difficulty = min(difficulty, 1.0)
        
        # Determine if multi-step
        multi_step = difficulty > 0.4 or question_count > 1 or len(complexity_signals) > 2
        estimated_steps = max(1, min(int(difficulty * 5) + 1, 8))
        
        # Determine if hypotheses needed (uncertain/ambiguous questions)
        needs_hypothesis = (
            primary_type in ["analytical", "opinion", "complex"] and
            difficulty > 0.3 and
            not any(w in text_lower for w in ["define", "what is the", "how many"])
        )
        
        # Emotional weight
        emotional_weight = 0.0
        emotional_words = ["sad", "happy", "angry", "love", "hate", "worried", 
                          "scared", "excited", "frustrated", "lonely", "miss"]
        for ew in emotional_words:
            if ew in text_lower:
                emotional_weight += 0.15
        emotional_weight = min(emotional_weight, 1.0)
        
        # If emotionally charged, bias toward empathetic strategy
        if emotional_weight > 0.3 and primary_type not in ["emotional"]:
            strategy = "empathetic"
        
        assessment = {
            "task_type": primary_type,
            "all_types": detected_types,
            "strategy": strategy,
            "difficulty": round(difficulty, 2),
            "needs_evidence": needs_evidence,
            "needs_hypothesis": needs_hypothesis,
            "multi_step": multi_step,
            "estimated_steps": estimated_steps,
            "emotional_weight": round(emotional_weight, 2),
            "complexity_signals": complexity_signals,
            "timestamp": datetime.now().isoformat()
        }
        
        self.recent_assessments.append(assessment)
        logger.info(f"Task assessed: {primary_type} | strategy={strategy} | difficulty={difficulty:.2f} | signals={complexity_signals}")
        
        return assessment
    
    def _select_best_strategy(self, task_type: str) -> str:
        """Select the best strategy based on past performance"""
        # Get strategies compatible with this task type
        compatible = {
            "factual": ["step_by_step", "research_heavy"],
            "analytical": ["analytical", "step_by_step"],
            "creative": ["creative", "intuitive"],
            "emotional": ["empathetic", "intuitive"],
            "problem_solving": ["step_by_step", "analytical"],
            "opinion": ["analytical", "creative"],
            "procedural": ["step_by_step"],
            "complex": ["step_by_step", "analytical"]
        }
        
        options = compatible.get(task_type, ["step_by_step", "analytical"])
        
        # Pick the one with highest success rate
        best = max(options, key=lambda s: self.strategy_performance.get(s, {}).get("avg_quality", 0.5))
        return best
    
    # ==================== SELF-CRITIQUE ====================
    
    def self_critique(self, reasoning_trace: Dict[str, Any], response: str = None) -> Dict[str, Any]:
        """
        Review the quality of reasoning after generating a response.
        
        Args:
            reasoning_trace: The chain-of-thought trace from thinking
            response: The final response generated
            
        Returns:
            {
                "quality": float,        # 0.0 (poor) to 1.0 (excellent)
                "issues": list,          # Problems found
                "suggestions": list,     # How to improve
                "assumptions_made": list, # Unverified assumptions
                "evidence_sufficient": bool,
                "reasoning_depth": int   # Number of reasoning steps
            }
        """
        issues = []
        suggestions = []
        assumptions = []
        
        quality = 0.7  # Base quality
        
        # Check reasoning depth
        steps = reasoning_trace.get("steps", [])
        reasoning_depth = len(steps)
        
        if reasoning_depth == 0:
            issues.append("No reasoning steps recorded")
            quality -= 0.2
        elif reasoning_depth == 1:
            issues.append("Only one reasoning step - may be too shallow")
            quality -= 0.1
        elif reasoning_depth >= 3:
            quality += 0.1  # Bonus for deep reasoning
        
        # Check for evidence
        evidence = reasoning_trace.get("evidence", {})
        evidence_for = evidence.get("for", [])
        evidence_against = evidence.get("against", [])
        
        evidence_sufficient = len(evidence_for) >= 2 or (len(evidence_for) >= 1 and len(evidence_against) >= 1)
        
        if not evidence_sufficient and reasoning_trace.get("needs_evidence", False):
            issues.append("Insufficient evidence for claim")
            suggestions.append("Look up more facts before concluding")
            quality -= 0.15
        
        # Check for assumptions
        for step in steps:
            step_text = step.get("step", "").lower()
            if any(marker in step_text for marker in ["assume", "presume", "guess", "probably", "maybe"]):
                assumptions.append(step.get("step", ""))
        
        if assumptions:
            suggestions.append(f"Verify assumptions: {'; '.join(assumptions[:3])}")
            quality -= 0.05 * len(assumptions)
        
        # Check confidence consistency
        confidences = [s.get("confidence", 0.7) for s in steps if "confidence" in s]
        if confidences:
            avg_conf = sum(confidences) / len(confidences)
            variance = sum((c - avg_conf) ** 2 for c in confidences) / len(confidences)
            if variance > 0.1:
                issues.append("Inconsistent confidence across reasoning steps")
                suggestions.append("Re-evaluate steps with wildly different confidence")
                quality -= 0.05
        
        # Check if hypotheses were considered
        hypotheses = reasoning_trace.get("hypotheses", [])
        if reasoning_trace.get("needs_hypothesis", False) and len(hypotheses) < 2:
            suggestions.append("Consider more alternative explanations")
            quality -= 0.05
        
        # Check for backtracking (sign of thorough reasoning)
        if reasoning_trace.get("backtracked", False):
            quality += 0.05  # Bonus for self-correction
        
        # Clamp quality
        quality = max(0.1, min(1.0, quality))
        
        critique = {
            "quality": round(quality, 2),
            "issues": issues,
            "suggestions": suggestions,
            "assumptions_made": assumptions,
            "evidence_sufficient": evidence_sufficient,
            "reasoning_depth": reasoning_depth,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Self-critique: quality={quality:.2f} | issues={len(issues)} | assumptions={len(assumptions)}")
        
        return critique
    
    # ==================== CONFIDENCE CALIBRATION ====================
    
    def calibrate_confidence(self, predicted_confidence: float, actual_outcome: str, context: str = ""):
        """
        Track whether our confidence predictions are well-calibrated.
        
        Args:
            predicted_confidence: The confidence we stated (0.0-1.0)
            actual_outcome: "correct" | "incorrect" | "partial"
            context: Optional description for learning
        """
        bucket = round(predicted_confidence * 10) / 10  # Round to nearest 0.1
        
        if bucket not in self.calibration_data["by_bucket"]:
            self.calibration_data["by_bucket"][bucket] = {"total": 0, "correct": 0}
        
        self.calibration_data["by_bucket"][bucket]["total"] += 1
        if actual_outcome == "correct":
            self.calibration_data["by_bucket"][bucket]["correct"] += 1
        
        self.calibration_data["predictions"].append({
            "predicted": predicted_confidence,
            "outcome": actual_outcome,
            "bucket": bucket,
            "context": context[:100],
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 500 predictions
        if len(self.calibration_data["predictions"]) > 500:
            self.calibration_data["predictions"] = self.calibration_data["predictions"][-500:]
        
        self._save("calibration.json", self.calibration_data)
    
    def get_reliability_score(self, confidence: float) -> float:
        """
        Given a confidence level, return how reliable that confidence typically is.
        E.g., if we say 0.8 and we're right 70% of the time at that level, return 0.7.
        """
        bucket = round(confidence * 10) / 10
        
        if bucket in self.calibration_data["by_bucket"]:
            data = self.calibration_data["by_bucket"][bucket]
            if data["total"] >= 5:  # Need minimum data
                return data["correct"] / data["total"]
        
        # Default: assume well-calibrated (no data yet)
        return confidence
    
    def adjust_confidence(self, raw_confidence: float) -> float:
        """Adjust confidence based on calibration history"""
        reliability = self.get_reliability_score(raw_confidence)
        # Blend raw confidence with reliability
        return round(raw_confidence * 0.6 + reliability * 0.4, 2)
    
    # ==================== STRATEGY TRACKING ====================
    
    def record_strategy_outcome(self, strategy: str, quality: float, success: bool):
        """Record the outcome of using a particular strategy"""
        if strategy not in self.strategy_performance:
            self.strategy_performance[strategy] = {"attempts": 0, "successes": 0, "avg_quality": 0.5}
        
        stats = self.strategy_performance[strategy]
        stats["attempts"] += 1
        if success:
            stats["successes"] += 1
        
        # Update running average quality
        n = stats["attempts"]
        stats["avg_quality"] = round(
            stats["avg_quality"] * ((n - 1) / n) + quality * (1 / n), 3
        )
        
        self._save("strategy_performance.json", self.strategy_performance)
    
    def get_strategy_report(self) -> Dict[str, Any]:
        """Get performance report for all strategies"""
        report = {}
        for strategy, stats in self.strategy_performance.items():
            success_rate = stats["successes"] / max(stats["attempts"], 1)
            report[strategy] = {
                "attempts": stats["attempts"],
                "success_rate": round(success_rate, 2),
                "avg_quality": stats["avg_quality"]
            }
        return report
    
    # ==================== ASSUMPTION TRACKING ====================
    
    def log_assumption(self, assumption: str, context: str = "", verified: bool = False):
        """Log an assumption made during reasoning"""
        entry = {
            "assumption": assumption,
            "context": context[:200],
            "verified": verified,
            "timestamp": datetime.now().isoformat()
        }
        self.assumptions_log.append(entry)
        
        if not verified:
            logger.info(f"Unverified assumption logged: {assumption[:80]}")
    
    def verify_assumption(self, index: int, was_correct: bool):
        """Mark an assumption as verified"""
        if 0 <= index < len(self.assumptions_log):
            self.assumptions_log[index]["verified"] = was_correct
    
    def get_unverified_assumptions(self) -> List[dict]:
        """Get all unverified assumptions"""
        return [a for a in self.assumptions_log if not a["verified"]]
    
    # ==================== REASONING QUALITY TRACKING ====================
    
    def track_reasoning_session(self, assessment: Dict, critique: Dict, strategy_used: str):
        """Track a complete reasoning session for learning"""
        session = {
            "assessment": assessment,
            "critique": critique,
            "strategy": strategy_used,
            "timestamp": datetime.now().isoformat()
        }
        
        # Record strategy outcome
        success = critique["quality"] >= 0.6
        self.record_strategy_outcome(strategy_used, critique["quality"], success)
        
        logger.info(f"Reasoning session tracked: strategy={strategy_used} quality={critique['quality']:.2f}")
    
    # ==================== METACOGNITION REPORT ====================
    
    def get_metacognition_report(self) -> Dict[str, Any]:
        """Get comprehensive metacognition stats"""
        # Calibration stats
        total_predictions = len(self.calibration_data["predictions"])
        correct_predictions = sum(
            1 for p in self.calibration_data["predictions"] if p["outcome"] == "correct"
        )
        calibration_accuracy = correct_predictions / max(total_predictions, 1)
        
        # Recent assessment stats
        recent = list(self.recent_assessments)
        avg_difficulty = sum(a.get("difficulty", 0) for a in recent) / max(len(recent), 1)
        
        # Task type distribution
        type_counts = {}
        for a in recent:
            t = a.get("task_type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
        
        # Unverified assumptions
        unverified = len(self.get_unverified_assumptions())
        
        return {
            "calibration": {
                "total_predictions": total_predictions,
                "calibration_accuracy": round(calibration_accuracy, 2),
                "buckets": self.calibration_data["by_bucket"]
            },
            "strategy_performance": self.get_strategy_report(),
            "recent_assessments": {
                "count": len(recent),
                "avg_difficulty": round(avg_difficulty, 2),
                "task_distribution": type_counts
            },
            "assumptions": {
                "total_logged": len(self.assumptions_log),
                "unverified": unverified
            }
        }
    
    # ==================== INTEGRATION HELPERS ====================
    
    def think_about_complexity(self, input_text: str) -> Tuple[str, int, str]:
        """
        Quick helper: assess input and return (task_type, estimated_steps, strategy).
        For use in tight loops where full assessment isn't needed.
        """
        assessment = self.assess_task(input_text)
        return assessment["task_type"], assessment["estimated_steps"], assessment["strategy"]
    
    def should_use_chain_of_thought(self, assessment: Dict) -> bool:
        """Determine if chain-of-thought reasoning is needed"""
        return (
            assessment["multi_step"] or
            assessment["difficulty"] > 0.3 or
            assessment["needs_hypothesis"] or
            assessment["estimated_steps"] > 2
        )
    
    def get_reasoning_budget(self, assessment: Dict) -> int:
        """Get the maximum number of reasoning steps allowed"""
        base = assessment["estimated_steps"]
        difficulty = assessment["difficulty"]
        
        # More complex tasks get more reasoning budget
        budget = base + int(difficulty * 3)
        return min(max(budget, 2), 10)  # Clamp between 2 and 10


# Global instance
metacognition = Metacognition()
