"""
Self-Repair Module - Auto-detects and fixes issues
"""
import os
import sys
import subprocess
import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("OfflineAI")

class SelfRepair:
    def __init__(self, project_root=None):
        self.project_root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.repair_log = os.path.join(self.project_root, "logs", "repairs.json")
        self.repairs_applied = []
    
    def run_diagnostics(self):
        """Run all diagnostics and fix issues"""
        issues = []
        fixes = []
        
        # Check 1: Duplicate log handlers
        result = self._check_duplicate_handlers()
        if result['fixed']:
            fixes.append(result)
        
        # Check 2: Lock file stuck
        result = self._check_stuck_lock()
        if result['fixed']:
            fixes.append(result)
        
        # Check 3: Corrupted memory file
        result = self._check_memory_file()
        if result['fixed']:
            fixes.append(result)
        
        # Check 4: Missing directories
        result = self._check_directories()
        if result['fixed']:
            fixes.append(result)
        
        # Check 5: Python syntax errors
        result = self._check_syntax_errors()
        if result['issues']:
            issues.extend(result['issues'])
        
        # Check 6: Import errors
        result = self._check_imports()
        if result['issues']:
            issues.extend(result['issues'])
        
        # Check 7: TTS engine health
        result = self._check_tts_health()
        if result['fixed']:
            fixes.append(result)
        
        # Check 8: Voice recognition health
        result = self._check_voice_health()
        if result['fixed']:
            fixes.append(result)
        
        # Log repairs
        if fixes:
            self._log_repairs(fixes)
        
        return {
            'issues': issues,
            'fixes': fixes,
            'healthy': len(issues) == 0
        }
    
    def _check_duplicate_handlers(self):
        """Check and fix duplicate log handlers"""
        result = {'check': 'duplicate_handlers', 'fixed': False, 'message': ''}
        
        from logger import logger as main_logger
        
        if len(main_logger.handlers) > 2:
            # Remove duplicate handlers
            file_handlers = [h for h in main_logger.handlers if isinstance(h, logging.FileHandler)]
            stream_handlers = [h for h in main_logger.handlers if isinstance(h, logging.StreamHandler)]
            
            # Keep only one of each type
            main_logger.handlers = []
            if file_handlers:
                main_logger.addHandler(file_handlers[0])
            if stream_handlers:
                main_logger.addHandler(stream_handlers[0])
            
            result['fixed'] = True
            result['message'] = f"Removed {len(main_logger.handlers) - 2} duplicate handlers"
        
        return result
    
    def _check_stuck_lock(self):
        """Check and remove stuck lock files"""
        result = {'check': 'stuck_lock', 'fixed': False, 'message': ''}
        
        lock_file = "/tmp/purple_ai.lock"
        if os.path.exists(lock_file):
            # Check if the process is still running
            try:
                with open(lock_file, 'r') as f:
                    pid = f.read().strip()
                    if pid:
                        # Check if process exists
                        try:
                            os.kill(int(pid), 0)
                            # Process exists, don't remove
                            result['message'] = "Lock file exists with active process"
                        except (ProcessLookupError, ValueError):
                            # Process doesn't exist, remove lock
                            os.remove(lock_file)
                            result['fixed'] = True
                            result['message'] = "Removed stuck lock file"
                    else:
                        os.remove(lock_file)
                        result['fixed'] = True
                        result['message'] = "Removed empty lock file"
            except Exception:
                os.remove(lock_file)
                result['fixed'] = True
                result['message'] = "Removed corrupted lock file"
        
        return result
    
    def _check_memory_file(self):
        """Check and fix corrupted memory file"""
        result = {'check': 'memory_file', 'fixed': False, 'message': ''}
        
        memory_file = os.path.join(self.project_root, "ai_memory.json")
        
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r') as f:
                    data = json.load(f)
                result['message'] = "Memory file is valid"
            except json.JSONDecodeError:
                # Corrupted file, backup and recreate
                backup = f"{memory_file}.bak.{int(datetime.now().timestamp())}"
                os.rename(memory_file, backup)
                
                # Create default memory
                default_memory = {
                    "user_name": "Rifat",
                    "setup_complete": True,
                    "interaction_count": 0,
                    "conversation_history": [],
                    "reminders": [],
                    "learned_info": [],
                    "mood_patterns": {"current_mood": "neutral"}
                }
                with open(memory_file, 'w') as f:
                    json.dump(default_memory, f, indent=2)
                
                result['fixed'] = True
                result['message'] = f"Fixed corrupted memory file (backup: {backup})"
        else:
            # Create default memory
            default_memory = {
                "user_name": "Rifat",
                "setup_complete": True,
                "interaction_count": 0,
                "conversation_history": [],
                "reminders": [],
                "learned_info": [],
                "mood_patterns": {"current_mood": "neutral"}
            }
            with open(memory_file, 'w') as f:
                json.dump(default_memory, f, indent=2)
            
            result['fixed'] = True
            result['message'] = "Created missing memory file"
        
        return result
    
    def _check_directories(self):
        """Check and create missing directories"""
        result = {'check': 'directories', 'fixed': False, 'message': ''}
        
        required_dirs = ['logs', 'utils', 'voice', 'core', 'scripts', 'tests']
        missing = []
        
        for d in required_dirs:
            path = os.path.join(self.project_root, d)
            if not os.path.exists(path):
                os.makedirs(path)
                missing.append(d)
        
        if missing:
            result['fixed'] = True
            result['message'] = f"Created missing directories: {', '.join(missing)}"
        
        return result
    
    def _check_syntax_errors(self):
        """Check Python files for syntax errors"""
        result = {'check': 'syntax_errors', 'issues': []}
        
        python_files = list(Path(self.project_root).glob("**/*.py"))
        
        for file_path in python_files:
            if "venv" in str(file_path):
                continue
            
            try:
                with open(file_path, 'r') as f:
                    compile(f.read(), str(file_path), 'exec')
            except SyntaxError as e:
                result['issues'].append({
                    'file': str(file_path),
                    'error': str(e),
                    'line': e.lineno
                })
        
        return result
    
    def _check_imports(self):
        """Check for import errors"""
        result = {'check': 'import_errors', 'issues': []}
        
        # Test critical imports
        critical_imports = [
            'config',
            'logger',
            'voice.tts_engine',
            'voice.voice_controller',
            'core.ai_engine',
            'utils.response_generator',
            'utils.system_controller'
        ]
        
        for module in critical_imports:
            try:
                __import__(module)
            except ImportError as e:
                result['issues'].append({
                    'module': module,
                    'error': str(e)
                })
        
        return result
    
    def _check_tts_health(self):
        """Check TTS engine health"""
        result = {'check': 'tts_health', 'fixed': False, 'message': ''}
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            if engine:
                del engine
                result['message'] = "TTS engine is healthy"
            else:
                result['message'] = "TTS engine returned None"
        except Exception as e:
            result['message'] = f"TTS engine error: {e}"
        
        return result
    
    def _check_voice_health(self):
        """Check voice recognition health"""
        result = {'check': 'voice_health', 'fixed': False, 'message': ''}
        
        try:
            import speech_recognition
            result['message'] = "Voice recognition is available"
        except ImportError:
            result['message'] = "Speech recognition not installed"
        
        return result
    
    def _log_repairs(self, repairs):
        """Log repairs to file"""
        try:
            os.makedirs(os.path.dirname(self.repair_log), exist_ok=True)
            
            log_data = []
            if os.path.exists(self.repair_log):
                with open(self.repair_log, 'r') as f:
                    log_data = json.load(f)
            
            log_data.append({
                'timestamp': datetime.now().isoformat(),
                'repairs': repairs
            })
            
            # Keep only last 100 entries
            log_data = log_data[-100:]
            
            with open(self.repair_log, 'w') as f:
                json.dump(log_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to log repairs: {e}")
    
    def auto_fix_all(self):
        """Automatically fix all detected issues"""
        results = self.run_diagnostics()
        
        if results['fixes']:
            logger.info(f"Auto-repair: Fixed {len(results['fixes'])} issues")
            for fix in results['fixes']:
                logger.info(f"  - {fix['check']}: {fix.get('message', 'Fixed')}")
        
        return results


# Global instance
self_repair = SelfRepair()
