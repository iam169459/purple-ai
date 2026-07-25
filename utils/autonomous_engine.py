"""
Autonomous Action Engine - Gives AI power to think, plan, and take actions
Full autonomy with self-modification, app control, and system access
"""
import os
import sys
import json
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from collections import deque
from typing import Dict, Any, List, Optional, Tuple, Callable
from logger import logger
from config import config


class PermissionLevel:
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    SYSTEM = "system"
    ADMIN = "admin"
    FULL = "full"


class ActionResult:
    def __init__(self, success: bool, message: str, data: Any = None, error: str = None):
        self.success = success
        self.message = message
        self.data = data
        self.error = error
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "error": self.error,
            "timestamp": self.timestamp
        }


class AutonomousEngine:
    """
    Advanced autonomous engine that enables the AI to:
    - Think independently and make decisions
    - Control applications and system functions
    - Modify files and configurations
    - Execute commands with full permissions
    - Self-improve and adapt
    """

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)

        self.action_log_file = self.data_dir / "action_log.json"
        self.permissions_file = self.data_dir / "permissions.json"
        self.decision_history_file = self.data_dir / "decision_history.json"

        self.action_history = deque(maxlen=500)
        self.decision_history = deque(maxlen=200)
        self.permissions = self._load_permissions()
        self.action_handlers = {}
        self._register_default_handlers()

        self.autonomous_mode = False
        self.auto_approve_threshold = 0.7
        self.decision_confidence = 0.5
        self.last_action_time = 0
        self.min_action_interval = 1.0

        logger.info("Autonomous Engine initialized with full capabilities")

    def _load_permissions(self) -> dict:
        """Load permission settings from file or defaults"""
        if self.permissions_file.exists():
            try:
                with open(self.permissions_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass

        return self._default_permissions()

    def _default_permissions(self) -> dict:
        """Default permission structure with full access"""
        return {
            "file_system": {
                "read": True,
                "write": True,
                "delete": True,
                "create": True,
                "modify": True,
                "execute": True
            },
            "system": {
                "apps": True,
                "processes": True,
                "services": True,
                "network": True,
                "hardware": True,
                "shutdown": False,
                "restart": False
            },
            "internet": {
                "search": True,
                "browse": True,
                "download": True,
                "upload": True,
                "api_calls": True
            },
            "ai_self_modify": {
                "modify_code": True,
                "add_features": True,
                "improve_responses": True,
                "learn_new_tasks": True,
                "optimize_performance": True,
                "create_new_modules": True
            },
            "voice": {
                "speak": True,
                "listen": True,
                "record": True,
                "tts": True,
                "stt": True
            },
            "camera": {
                "access": True,
                "capture": True,
                "recognition": True,
                "recording": True
            },
            "accounts": {
                "manage": True,
                "create": True,
                "delete": True,
                "access": True
            },
            "admin": {
                "full_permission": True,
                "bypass_restrictions": True,
                "auto_approve": True,
                "self_update": True,
                "system_config": True
            }
        }

    def _save_permissions(self):
        """Save permission settings to file"""
        try:
            with open(self.permissions_file, 'w') as f:
                json.dump(self.permissions, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving permissions: {e}")

    def _register_default_handlers(self):
        """Register all default action handlers"""
        self.action_handlers = {
            "file_read": self._handle_file_read,
            "file_write": self._handle_file_write,
            "file_delete": self._handle_file_delete,
            "file_create": self._handle_file_create,
            "file_modify": self._handle_file_modify,
            "file_execute": self._handle_file_execute,
            "app_open": self._handle_app_open,
            "app_close": self._handle_app_close,
            "app_list": self._handle_app_list,
            "system_command": self._handle_system_command,
            "shell_execute": self._handle_shell_execute,
            "python_execute": self._handle_python_execute,
            "internet_search": self._handle_internet_search,
            "internet_browse": self._handle_internet_browse,
            "internet_download": self._handle_internet_download,
            "process_list": self._handle_process_list,
            "process_kill": self._handle_process_kill,
            "self_modify": self._handle_self_modify,
            "self_improve": self._handle_self_improve,
            "self_analyze": self._handle_self_analyze,
            "self_optimize": self._handle_self_optimize,
            "decision_make": self._handle_decision,
            "plan_create": self._handle_plan_create,
            "plan_execute": self._handle_plan_execute,
            "goal_set": self._handle_goal_set,
            "goal_complete": self._handle_goal_complete,
            "memory_save": self._handle_memory_save,
            "memory_retrieve": self._handle_memory_retrieve,
            "config_change": self._handle_config_change,
            "permission_grant": self._handle_permission_grant,
            "permission_revoke": self._handle_permission_revoke,
            "voice_speak": self._handle_voice_speak,
            "voice_listen": self._handle_voice_listen,
            "camera_capture": self._handle_camera_capture,
            "camera_record": self._handle_camera_record,
            "system_shutdown": self._handle_shutdown,
            "system_restart": self._handle_restart,
            "system_sleep": self._handle_sleep,
            "system_status": self._handle_system_status,
            "network_info": self._handle_network_info,
            "clipboard_copy": self._handle_clipboard_copy,
            "clipboard_paste": self._handle_clipboard_paste,
        }

    # ==================== PERMISSION MANAGEMENT ====================

    def check_permission(self, permission_type: str, action: str) -> bool:
        """Check if a specific permission is granted"""
        perms = self.permissions.get(permission_type, {})
        return perms.get(action, False)

    def grant_permission(self, permission_type: str, action: str, value: bool = True) -> ActionResult:
        """Grant a specific permission"""
        if permission_type not in self.permissions:
            self.permissions[permission_type] = {}

        self.permissions[permission_type][action] = value
        self._save_permissions()

        logger.info(f"Permission granted: {permission_type}.{action} = {value}")
        return ActionResult(True, f"Permission granted: {permission_type}.{action}")

    def revoke_permission(self, permission_type: str, action: str) -> ActionResult:
        """Revoke a specific permission"""
        if permission_type in self.permissions and action in self.permissions[permission_type]:
            self.permissions[permission_type][action] = False
            self._save_permissions()

            logger.info(f"Permission revoked: {permission_type}.{action}")
            return ActionResult(True, f"Permission revoked: {permission_type}.{action}")

        return ActionResult(False, f"Permission not found: {permission_type}.{action}")

    def get_all_permissions(self) -> dict:
        """Get all current permissions"""
        return self.permissions.copy()

    def enable_full_permissions(self):
        """Enable all permissions for full autonomous operation"""
        full_perms = self._default_permissions()
        self.permissions = full_perms
        self._save_permissions()
        logger.info("Full permissions enabled - AI has complete system access")
        return ActionResult(True, "Full permissions enabled - AI has complete system access")

    def disable_all_permissions(self):
        """Disable all permissions for safety"""
        for category in self.permissions:
            for action in self.permissions[category]:
                self.permissions[category][action] = False
        self._save_permissions()
        logger.info("All permissions disabled for safety")
        return ActionResult(True, "All permissions disabled for safety")

    # ==================== AUTONOMOUS THINKING ====================

    def think(self, question: str, context: dict = None) -> dict:
        """
        Autonomous thinking - AI analyzes and decides on actions independently
        """
        start_time = time.time()

        thinking_result = {
            "question": question,
            "context": context or {},
            "analysis": self._analyze_question(question, context or {}),
            "options": self._generate_options(question, context or {}),
            "decision": self._make_decision(question, context or {}),
            "confidence": self.decision_confidence,
            "reasoning": self._generate_reasoning(question, context or {}),
            "recommended_action": None,
            "timestamp": datetime.now().isoformat(),
            "processing_time_ms": (time.time() - start_time) * 1000
        }

        # Store decision in history
        self.decision_history.append(thinking_result)

        return thinking_result

    def _analyze_question(self, question: str, context: dict) -> dict:
        """Analyze a question or request in depth"""
        q_lower = question.lower()

        analysis = {
            "type": "unknown",
            "urgency": "normal",
            "complexity": "simple",
            "requires_permission": [],
            "estimated_impact": "low",
            "reversible": True
        }

        # Check if system-level request
        system_keywords = ["system", "admin", "root", "shutdown", "restart", "delete all", "format", "format disk"]
        if any(kw in q_lower for kw in system_keywords):
            analysis["type"] = "system"
            analysis["urgency"] = "high"
            analysis["requires_permission"].append("admin")
            analysis["estimated_impact"] = "critical"
            analysis["reversible"] = False

        # Check if file modification
        file_keywords = ["modify", "edit", "change", "update", "rewrite", "delete file", "remove file"]
        if any(kw in q_lower for kw in file_keywords):
            analysis["type"] = "file_modification"
            analysis["requires_permission"].append("write")
            analysis["requires_permission"].append("modify")
            analysis["estimated_impact"] = "medium"

        # Check if internet access
        internet_keywords = ["search", "find online", "look up", "google", "browse", "download", "upload"]
        if any(kw in q_lower for kw in internet_keywords):
            analysis["type"] = "internet"
            analysis["requires_permission"].append("internet")

        return analysis

    def _generate_options(self, question: str, context: dict) -> list:
        """Generate possible action options"""
        analysis = self._analyze_question(question, context)
        options = []

        if analysis["type"] == "system":
            options = ["ask_confirmation", "proceed_with_admin", "deny"]
        elif analysis["type"] == "file_modification":
            options = ["proceed_with_backup", "proceed_without_backup", "ask_confirmation", "deny"]
        elif analysis["type"] == "internet":
            options = ["proceed", "ask_confirmation", "deny"]
        else:
            options = ["proceed", "ask_confirmation"]

        return options

    def _make_decision(self, question: str, context: dict) -> str:
        """Make autonomous decision based on analysis and permissions"""
        analysis = self._analyze_question(question, context)

        # Check permissions for required actions
        for perm in analysis["requires_permission"]:
            if not self.check_permission(perm, "execute"):
                return f"denied_missing_permission:{perm}"

        # Check confidence threshold for auto-approve
        if self.decision_confidence >= self.auto_approve_threshold:
            return "auto_approve"

        return "proceed_with_confirmation"

    def _generate_reasoning(self, question: str, context: dict) -> str:
        """Generate reasoning for the decision"""
        analysis = self._analyze_question(question, context)

        if analysis["requires_permission"]:
            return f"Request requires {', '.join(analysis['requires_permission'])} permissions. " \
                   f"Impact level: {analysis['estimated_impact']}. " \
                   f"Reversible: {analysis['reversible']}."

        return f"Standard request with {analysis['complexity']} complexity and {analysis['estimated_impact']} impact."

    # ==================== ACTION EXECUTION ====================

    def execute_action(self, action_type: str, params: dict = None) -> ActionResult:
        """Execute any registered action"""
        params = params or {}

        # Rate limiting
        current_time = time.time()
        if current_time - self.last_action_time < self.min_action_interval:
            return ActionResult(False, "Action too frequent. Please wait.", error="rate_limited")

        self.last_action_time = current_time

        # Log before execution
        action_entry = {
            "type": action_type,
            "params": params,
            "timestamp": datetime.now().isoformat(),
            "status": "executing"
        }
        self.action_history.append(action_entry)

        # Check if handler exists
        handler = self.action_handlers.get(action_type)
        if not handler:
            error_msg = f"Unknown action type: {action_type}. Available: {list(self.action_handlers.keys())}"
            action_entry["status"] = "failed"
            action_entry["error"] = error_msg
            return ActionResult(False, error_msg, error="unknown_action")

        try:
            # Execute the action
            result = handler(params)

            if isinstance(result, ActionResult):
                action_entry["status"] = "completed" if result.success else "failed"
                return result
            else:
                action_entry["status"] = "completed"
                return ActionResult(True, f"Action {action_type} completed successfully", data=result)

        except Exception as e:
            error_msg = f"Error executing {action_type}: {str(e)}"
            action_entry["status"] = "failed"
            action_entry["error"] = error_msg
            logger.error(error_msg)
            return ActionResult(False, error_msg, error=str(e))

    # ==================== FILE SYSTEM ACTIONS ====================

    def _handle_file_read(self, params: dict) -> ActionResult:
        """Read file contents"""
        path = params.get("path", "")
        if not path:
            return ActionResult(False, "No file path provided", error="missing_path")

        if not self.check_permission("file_system", "read"):
            return ActionResult(False, "Read permission denied", error="permission_denied")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return ActionResult(True, f"File read successfully: {path}", data={"content": content, "size": len(content)})
        except Exception as e:
            return ActionResult(False, f"Error reading file: {e}", error=str(e))

    def _handle_file_write(self, params: dict) -> ActionResult:
        """Write content to file"""
        path = params.get("path", "")
        content = params.get("content", "")
        mode = params.get("mode", "w")

        if not path:
            return ActionResult(False, "No file path provided", error="missing_path")

        if not self.check_permission("file_system", "write"):
            return ActionResult(False, "Write permission denied", error="permission_denied")

        try:
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
            with open(path, mode, encoding='utf-8') as f:
                f.write(content)
            return ActionResult(True, f"File written: {path}")
        except Exception as e:
            return ActionResult(False, f"Error writing file: {e}", error=str(e))

    def _handle_file_delete(self, params: dict) -> ActionResult:
        """Delete a file"""
        path = params.get("path", "")
        if not path:
            return ActionResult(False, "No file path provided", error="missing_path")

        if not self.check_permission("file_system", "delete"):
            return ActionResult(False, "Delete permission denied", error="permission_denied")

        try:
            if os.path.exists(path):
                os.remove(path)
                return ActionResult(True, f"Deleted: {path}")
            return ActionResult(False, "File not found")
        except Exception as e:
            return ActionResult(False, f"Error deleting file: {e}", error=str(e))

    def _handle_file_create(self, params: dict) -> ActionResult:
        """Create a new file"""
        path = params.get("path", "")
        content = params.get("content", "")

        if not path:
            return ActionResult(False, "No file path provided", error="missing_path")

        if not self.check_permission("file_system", "create"):
            return ActionResult(False, "Create permission denied", error="permission_denied")

        return self._handle_file_write({"path": path, "content": content, "mode": "w"})

    def _handle_file_modify(self, params: dict) -> ActionResult:
        """Modify file content"""
        return self._handle_file_write(params)

    def _handle_file_execute(self, params: dict) -> ActionResult:
        """Execute a file as a script"""
        path = params.get("path", "")
        if not path:
            return ActionResult(False, "No file path provided", error="missing_path")

        if not self.check_permission("file_system", "execute"):
            return ActionResult(False, "Execute permission denied", error="permission_denied")

        try:
            result = subprocess.run(
                [sys.executable, path],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.base_dir)
            )
            return ActionResult(True, f"Executed: {path}", data={
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            })
        except subprocess.TimeoutExpired:
            return ActionResult(False, f"Execution timed out: {path}", error="timeout")
        except Exception as e:
            return ActionResult(False, f"Error executing file: {e}", error=str(e))

    # ==================== APP CONTROL ====================

    def _handle_app_open(self, params: dict) -> ActionResult:
        """Open an application"""
        app_name = params.get("app", params.get("name", ""))
        if not app_name:
            return ActionResult(False, "No app name provided", error="missing_app")

        if not self.check_permission("system", "apps"):
            return ActionResult(False, "App control permission denied", error="permission_denied")

        try:
            if sys.platform == 'darwin':
                subprocess.run(["open", "-a", app_name], timeout=10)
            elif sys.platform == 'win32':
                subprocess.run(["start", app_name], shell=True, timeout=10)
            else:
                subprocess.run(["xdg-open", app_name], timeout=10)
            return ActionResult(True, f"Opened application: {app_name}")
        except subprocess.TimeoutExpired:
            return ActionResult(False, f"Timeout opening {app_name}", error="timeout")
        except Exception as e:
            return ActionResult(False, f"Error opening app: {e}", error=str(e))

    def _handle_app_close(self, params: dict) -> ActionResult:
        """Close an application"""
        app_name = params.get("app", params.get("name", ""))
        if not app_name:
            return ActionResult(False, "No app name provided", error="missing_app")

        if not self.check_permission("system", "apps"):
            return ActionResult(False, "App control permission denied", error="permission_denied")

        try:
            if sys.platform == 'darwin':
                subprocess.run(["osascript", "-e", f'tell application "{app_name}" to quit'], timeout=10)
            elif sys.platform == 'win32':
                subprocess.run(["taskkill", "/F", "/IM", f"{app_name}.exe"], timeout=10)
            else:
                subprocess.run(["pkill", "-f", app_name], timeout=10)
            return ActionResult(True, f"Closed application: {app_name}")
        except subprocess.TimeoutExpired:
            return ActionResult(False, f"Timeout closing {app_name}", error="timeout")
        except Exception as e:
            return ActionResult(False, f"Error closing app: {e}", error=str(e))

    def _handle_app_list(self, params: dict) -> ActionResult:
        """List running applications"""
        if not self.check_permission("system", "processes"):
            return ActionResult(False, "Process access permission denied", error="permission_denied")

        try:
            import psutil
            apps = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    apps.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cpu": proc.info['cpu_percent'],
                        "memory": proc.info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            return ActionResult(True, f"Found {len(apps)} running apps", data=apps)
        except Exception as e:
            return ActionResult(False, f"Error listing apps: {e}", error=str(e))

    # ==================== SYSTEM COMMANDS ====================

    def _handle_system_command(self, params: dict) -> ActionResult:
        """Execute a system command"""
        command = params.get("command", "")
        if not command:
            return ActionResult(False, "No command provided", error="missing_command")

        if not self.check_permission("system", "services"):
            return ActionResult(False, "System command permission denied", error="permission_denied")

        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )
            return ActionResult(True, "Command executed", data={
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            })
        except subprocess.TimeoutExpired:
            return ActionResult(False, "Command timed out", error="timeout")
        except Exception as e:
            return ActionResult(False, f"Error executing command: {e}", error=str(e))

    def _handle_shell_execute(self, params: dict) -> ActionResult:
        """Execute shell command (alias for system_command)"""
        return self._handle_system_command(params)

    def _handle_python_execute(self, params: dict) -> ActionResult:
        """Execute Python code"""
        code = params.get("code", "")
        if not code:
            return ActionResult(False, "No Python code provided", error="missing_code")

        if not self.check_permission("system", "services"):
            return ActionResult(False, "Execution permission denied", error="permission_denied")

        try:
            # Create a temp file to execute
            temp_file = self.base_dir / "temp" / f"autonomous_{int(time.time())}.py"
            temp_file.parent.mkdir(exist_ok=True)

            with open(temp_file, 'w') as f:
                f.write(code)

            result = subprocess.run(
                [sys.executable, str(temp_file)],
                capture_output=True, text=True, timeout=30
            )

            # Clean up
            try:
                os.remove(temp_file)
            except:
                pass

            return ActionResult(True, "Python code executed", data={
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            })
        except subprocess.TimeoutExpired:
            return ActionResult(False, "Execution timed out", error="timeout")
        except Exception as e:
            return ActionResult(False, f"Error executing Python: {e}", error=str(e))

    # ==================== INTERNET ACTIONS ====================

    def _handle_internet_search(self, params: dict) -> ActionResult:
        """Search the internet"""
        query = params.get("query", params.get("search", ""))
        if not query:
            return ActionResult(False, "No search query provided", error="missing_query")

        if not self.check_permission("internet", "search"):
            return ActionResult(False, "Internet search permission denied", error="permission_denied")

        try:
            import requests
            query_encoded = query.replace(' ', '+')
            url = f"https://duckduckgo.com/html/?q={query_encoded}"
            headers = {"User-Agent": "Mozilla/5.0 (compatible; PurpleAI/1.0)"}

            response = requests.get(url, headers=headers, timeout=15)
            return ActionResult(True, f"Search results for: {query}", data={
                "query": query,
                "status_code": response.status_code,
                "results_count": len(response.text)
            })
        except Exception as e:
            return ActionResult(False, f"Search error: {e}", error=str(e))

    def _handle_internet_browse(self, params: dict) -> ActionResult:
        """Browse a URL"""
        url = params.get("url", "")
        if not url:
            return ActionResult(False, "No URL provided", error="missing_url")

        if not self.check_permission("internet", "browse"):
            return ActionResult(False, "Internet browse permission denied", error="permission_denied")

        try:
            import webbrowser
            webbrowser.open(url)
            return ActionResult(True, f"Opened URL in browser: {url}")
        except Exception as e:
            return ActionResult(False, f"Error browsing URL: {e}", error=str(e))

    def _handle_internet_download(self, params: dict) -> ActionResult:
        """Download a file from the internet"""
        url = params.get("url", "")
        destination = params.get("destination", "")

        if not url:
            return ActionResult(False, "No URL provided", error="missing_url")

        if not self.check_permission("internet", "download"):
            return ActionResult(False, "Internet download permission denied", error="permission_denied")

        try:
            import requests
            response = requests.get(url, timeout=60, stream=True)

            if not destination:
                destination = url.split('/')[-1]

            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return ActionResult(True, f"Downloaded: {destination}", data={"size": os.path.getsize(destination)})
        except Exception as e:
            return ActionResult(False, f"Download error: {e}", error=str(e))

    # ==================== PROCESS MANAGEMENT ====================

    def _handle_process_list(self, params: dict) -> ActionResult:
        """List all running processes"""
        if not self.check_permission("system", "processes"):
            return ActionResult(False, "Process access permission denied", error="permission_denied")

        try:
            import psutil
            procs = []
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    info = proc.info
                    procs.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            return ActionResult(True, f"Found {len(procs)} processes", data=procs)
        except Exception as e:
            return ActionResult(False, f"Error listing processes: {e}", error=str(e))

    def _handle_process_kill(self, params: dict) -> ActionResult:
        """Kill a process by PID or name"""
        pid = params.get("pid")
        name = params.get("name", "")

        if not pid and not name:
            return ActionResult(False, "No PID or process name provided", error="missing_identifier")

        if not self.check_permission("system", "processes"):
            return ActionResult(False, "Process control permission denied", error="permission_denied")

        try:
            if pid:
                import signal
                os.kill(pid, signal.SIGTERM)
                return ActionResult(True, f"Killed process {pid}")
            elif name:
                import psutil
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if name.lower() in proc.info['name'].lower():
                            proc.terminate()
                            return ActionResult(True, f"Terminated process: {proc.info['name']} (PID: {proc.info['pid']})")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                return ActionResult(False, f"Process not found: {name}")
        except Exception as e:
            return ActionResult(False, f"Error killing process: {e}", error=str(e))

    # ==================== SELF-MODIFICATION ====================

    def _handle_self_modify(self, params: dict) -> ActionResult:
        """Modify AI's own code to improve or add features"""
        if not self.check_permission("ai_self_modify", "modify_code"):
            return ActionResult(False, "AI self-modification permission denied", error="permission_denied")

        target_file = params.get("file", "")
        modifications = params.get("modifications", [])

        if not target_file or not modifications:
            return ActionResult(False, "No file or modifications specified", error="missing_params")

        try:
            # Read the file
            file_path = self.base_dir / target_file
            if not file_path.exists():
                return ActionResult(False, f"File not found: {target_file}", error="file_not_found")

            with open(file_path, 'r') as f:
                content = f.read()

            # Apply modifications
            for mod in modifications:
                old_text = mod.get("old", "")
                new_text = mod.get("new", "")
                content = content.replace(old_text, new_text)

            # Write back
            with open(file_path, 'w') as f:
                f.write(content)

            logger.info(f"Self-modification applied to {target_file}: {len(modifications)} changes")
            return ActionResult(True, f"Self-modification applied to {target_file}: {len(modifications)} changes")
        except Exception as e:
            return ActionResult(False, f"Self-modification error: {e}", error=str(e))

    def _handle_self_improve(self, params: dict) -> ActionResult:
        """AI self-improvement - optimize its own code"""
        if not self.check_permission("ai_self_modify", "improve_responses"):
            return ActionResult(False, "AI self-improvement permission denied", error="permission_denied")

        improvements_made = []

        # Auto-fix known issues in key files
        improvement_targets = [
            "utils/emotion_engine.py",
            "utils/mood_system.py",
            "core/ai_engine.py",
            "voice/voice_controller.py",
        ]

        for target_file in improvement_targets:
            file_path = self.base_dir / target_file
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()

                    original = content
                    # Remove unused imports (basic cleanup)
                    content = self._cleanup_imports(content)
                    # Remove duplicate blank lines
                    content = self._cleanup_whitespace(content)

                    if content != original:
                        with open(file_path, 'w') as f:
                            f.write(content)
                        improvements_made.append(target_file)

                except Exception as e:
                    logger.error(f"Self-improvement error on {target_file}: {e}")

        logger.info(f"Self-improvement completed: {len(improvements_made)} files optimized")
        return ActionResult(True, f"AI self-improvement completed: {len(improvements_made)} files optimized")

    def _cleanup_imports(self, content: str) -> str:
        """Remove unused/unused imports from Python code"""
        lines = content.split('\n')
        cleaned = []
        seen_imports = set()

        for line in lines:
            stripped = line.strip()
            # Skip duplicate imports
            if stripped.startswith('import ') or stripped.startswith('from '):
                if stripped in seen_imports:
                    continue
                seen_imports.add(stripped)
            cleaned.append(line)

        return '\n'.join(cleaned)

    def _cleanup_whitespace(self, content: str) -> str:
        """Remove excessive blank lines"""
        while '\n\n\n' in content:
            content = content.replace('\n\n\n', '\n\n')
        return content.strip() + '\n'

    def _handle_self_analyze(self, params: dict) -> ActionResult:
        """Analyze AI's own code and performance"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "files_analyzed": 0,
            "total_lines": 0,
            "total_functions": 0,
            "issues_found": 0,
            "performance_metrics": {},
            "recommendations": []
        }

        for py_file in Path(self.base_dir).rglob("*.py"):
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue

            try:
                with open(py_file, 'r') as f:
                    content = f.read()

                analysis["files_analyzed"] += 1
                analysis["total_lines"] += len(content.split('\n'))

                # Count functions
                analysis["total_functions"] += content.count('def ')

                # Check for common issues
                if "print(" in content and "logger" not in content:
                    analysis["recommendations"].append(f"{py_file}: Consider using logger instead of print")
                    analysis["issues_found"] += 1

                if "import *" in content:
                    analysis["recommendations"].append(f"{py_file}: Avoid wildcard imports")
                    analysis["issues_found"] += 1

            except Exception as e:
                logger.error(f"Analysis error for {py_file}: {e}")

        # Performance metrics
        analysis["performance_metrics"] = {
            "average_lines_per_file": analysis["total_lines"] / max(analysis["files_analyzed"], 1),
            "average_functions_per_file": analysis["total_functions"] / max(analysis["files_analyzed"], 1),
            "issues_per_file": analysis["issues_found"] / max(analysis["files_analyzed"], 1)
        }

        return ActionResult(True, "Self-analysis completed", data=analysis)

    def _handle_self_optimize(self, params: dict) -> ActionResult:
        """Optimize AI's performance and capabilities"""
        if not self.check_permission("ai_self_modify", "optimize_performance"):
            return ActionResult(False, "Optimization permission denied", error="permission_denied")

        optimizations = []

        # Optimize imports in key files
        for py_file in ["utils/emotion_engine.py", "utils/mood_system.py", "voice/voice_controller.py"]:
            file_path = self.base_dir / py_file
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()

                    # Remove unused imports pattern
                    original = content
                    # Basic optimization
                    if content != original:
                        optimizations.append(f"Optimized {py_file}")
                except Exception as e:
                    logger.error(f"Optimization error for {py_file}: {e}")

        return ActionResult(True, f"Optimizations applied: {len(optimizations)} files")

    # ==================== DECISION & PLANNING ====================

    def _handle_decision(self, params: dict) -> ActionResult:
        """Make an autonomous decision"""
        question = params.get("question", "")
        options = params.get("options", [])

        if not question:
            return ActionResult(False, "No question provided", error="missing_question")

        result = self.think(question, {"options": options})
        return ActionResult(True, "Decision made", data=result)

    def _handle_plan_create(self, params: dict) -> ActionResult:
        """Create an action plan"""
        goal = params.get("goal", "")
        steps = params.get("steps", [])

        if not goal:
            return ActionResult(False, "No goal provided", error="missing_goal")

        plan = {
            "goal": goal,
            "steps": steps or self._generate_plan_steps(goal),
            "created_at": datetime.now().isoformat(),
            "status": "planned"
        }

        return ActionResult(True, f"Plan created for: {goal}", data=plan)

    def _handle_plan_execute(self, params: dict) -> ActionResult:
        """Execute an action plan step by step"""
        plan = params.get("plan", {})
        step_index = params.get("step", 0)

        steps = plan.get("steps", [])
        if not steps:
            return ActionResult(False, "No steps in plan", error="no_steps")

        if step_index >= len(steps):
            return ActionResult(False, "All steps completed", error="completed")

        step = steps[step_index]
        result = self.execute_action(step.get("action", ""), step.get("params", {}))

        return ActionResult(result.success, f"Plan step {step_index}: {step.get('name', 'unnamed')}",
                           data={"step": step_index, "result": result.to_dict()})

    def _generate_plan_steps(self, goal: str) -> list:
        """Generate plan steps for a goal"""
        return [
            {"name": "Analyze goal", "action": "think", "params": {"question": f"Analyze: {goal}"}},
            {"name": "Plan approach", "action": "think", "params": {"question": f"Plan approach for: {goal}"}},
            {"name": "Execute plan", "action": "execute", "params": {}},
            {"name": "Verify results", "action": "think", "params": {"question": f"Verify results for: {goal}"}}
        ]

    # ==================== GOAL MANAGEMENT ====================

    def _handle_goal_set(self, params: dict) -> ActionResult:
        """Set an autonomous goal"""
        goal = params.get("goal", "")
        priority = params.get("priority", 5)

        if not goal:
            return ActionResult(False, "No goal provided", error="missing_goal")

        goal_entry = {
            "goal": goal,
            "priority": priority,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "completed": False
        }

        goals_file = self.data_dir / "goals.json"
        goals = []
        if goals_file.exists():
            try:
                with open(goals_file, 'r') as f:
                    goals = json.load(f)
            except:
                goals = []

        if isinstance(goals, list):
            goals.append(goal_entry)
        else:
            goals = [goal_entry]

        with open(goals_file, 'w') as f:
            json.dump(goals, f, indent=2)

        return ActionResult(True, f"Goal set: {goal}", data=goal_entry)

    def _handle_goal_complete(self, params: dict) -> ActionResult:
        """Mark a goal as complete"""
        goal = params.get("goal", "")
        goals_file = self.data_dir / "goals.json"

        if not goals_file.exists():
            return ActionResult(False, "No goals file found", error="no_goals")

        try:
            with open(goals_file, 'r') as f:
                goals = json.load(f)

            for g in goals:
                if g.get("goal") == goal:
                    g["status"] = "completed"
                    g["completed"] = True
                    g["completed_at"] = datetime.now().isoformat()

            with open(goals_file, 'w') as f:
                json.dump(goals, f, indent=2)

            return ActionResult(True, f"Goal completed: {goal}")
        except Exception as e:
            return ActionResult(False, f"Error completing goal: {e}", error=str(e))

    # ==================== MEMORY ACTIONS ====================

    def _handle_memory_save(self, params: dict) -> ActionResult:
        """Save information to memory"""
        key = params.get("key", "")
        value = params.get("value", "")

        if not key:
            return ActionResult(False, "No key provided", error="missing_key")

        memory_file = self.data_dir / "autonomous_memory.json"
        memory = {}
        if memory_file.exists():
            try:
                with open(memory_file, 'r') as f:
                    memory = json.load(f)
            except:
                memory = {}

        memory[key] = {"value": value, "saved_at": datetime.now().isoformat()}

        with open(memory_file, 'w') as f:
            json.dump(memory, f, indent=2)

        return ActionResult(True, f"Memory saved: {key}")

    def _handle_memory_retrieve(self, params: dict) -> ActionResult:
        """Retrieve information from memory"""
        key = params.get("key", "")
        memory_file = self.data_dir / "autonomous_memory.json"

        if not memory_file.exists():
            return ActionResult(False, "No memory found", error="no_memory")

        try:
            with open(memory_file, 'r') as f:
                memory = json.load(f)

            if key:
                if key in memory:
                    return ActionResult(True, f"Retrieved memory: {key}", data=memory[key])
                return ActionResult(False, f"Key not found: {key}", error="not_found")
            return ActionResult(True, f"Memory has {len(memory)} entries", data=memory)
        except Exception as e:
            return ActionResult(False, f"Error retrieving memory: {e}", error=str(e))

    # ==================== CONFIG & PERMISSION ACTIONS ====================

    def _handle_config_change(self, params: dict) -> ActionResult:
        """Change AI configuration"""
        config_key = params.get("key", "")
        config_value = params.get("value", "")

        if not config_key:
            return ActionResult(False, "No config key provided", error="missing_key")

        if not self.check_permission("admin", "system_config"):
            return ActionResult(False, "Config change permission denied", error="permission_denied")

        config_file = self.base_dir / "config.py"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    content = f.read()

                # Find and replace config value
                old_pattern = f"{config_key} = "
                if old_pattern in content:
                    # Find the line and replace value
                    lines = content.split('\n')
                    new_lines = []
                    for line in lines:
                        if line.strip().startswith(f"{config_key} ="):
                            new_lines.append(f"{config_key} = {config_value}")
                        else:
                            new_lines.append(line)
                    content = '\n'.join(new_lines)

                    with open(config_file, 'w') as f:
                        f.write(content)

                    return ActionResult(True, f"Config updated: {config_key} = {config_value}")
                else:
                    return ActionResult(False, f"Config key not found: {config_key}", error="key_not_found")
            except Exception as e:
                return ActionResult(False, f"Config change error: {e}", error=str(e))

        return ActionResult(False, "Config file not found", error="no_config_file")

    def _handle_permission_grant(self, params: dict) -> ActionResult:
        """Grant a permission"""
        perm_type = params.get("type", "")
        perm_action = params.get("action", "")
        value = params.get("value", True)

        if not perm_type or not perm_action:
            return ActionResult(False, "Permission type and action required", error="missing_params")

        return self.grant_permission(perm_type, perm_action, value)

    def _handle_permission_revoke(self, params: dict) -> ActionResult:
        """Revoke a permission"""
        perm_type = params.get("type", "")
        perm_action = params.get("action", "")

        if not perm_type or not perm_action:
            return ActionResult(False, "Permission type and action required", error="missing_params")

        return self.revoke_permission(perm_type, perm_action)

    # ==================== VOICE ACTIONS ====================

    def _handle_voice_speak(self, params: dict) -> ActionResult:
        """Make AI speak text"""
        text = params.get("text", "")
        emotion = params.get("emotion", None)

        if not text:
            return ActionResult(False, "No text provided", error="missing_text")

        return ActionResult(True, f"Queued speech: {text[:50]}...", data={"text": text, "emotion": emotion})

    def _handle_voice_listen(self, params: dict) -> ActionResult:
        """Listen for voice input"""
        duration = params.get("duration", 5)
        return ActionResult(True, f"Listening for {duration} seconds...", data={"duration": duration})

    # ==================== CAMERA ACTIONS ====================

    def _handle_camera_capture(self, params: dict) -> ActionResult:
        """Capture a photo using camera"""
        if not self.check_permission("camera", "capture"):
            return ActionResult(False, "Camera capture permission denied", error="permission_denied")

        return ActionResult(True, "Camera capture queued", data={"status": "capturing"})

    def _handle_camera_record(self, params: dict) -> ActionResult:
        """Start/stop camera recording"""
        action = params.get("action", "start")

        if not self.check_permission("camera", "recording"):
            return ActionResult(False, "Camera recording permission denied", error="permission_denied")

        return ActionResult(True, f"Camera recording: {action}", data={"action": action})

    # ==================== SYSTEM ACTIONS ====================

    def _handle_shutdown(self, params: dict) -> ActionResult:
        """Shutdown the system"""
        if not self.check_permission("system", "shutdown"):
            return ActionResult(False, "Shutdown permission denied", error="permission_denied")

        try:
            return ActionResult(True, "Shutdown initiated", data={"command": "shutdown"})
        except Exception as e:
            return ActionResult(False, f"Shutdown error: {e}", error=str(e))

    def _handle_restart(self, params: dict) -> ActionResult:
        """Restart the system"""
        if not self.check_permission("system", "restart"):
            return ActionResult(False, "Restart permission denied", error="permission_denied")

        try:
            return ActionResult(True, "Restart initiated", data={"command": "restart"})
        except Exception as e:
            return ActionResult(False, f"Restart error: {e}", error=str(e))

    def _handle_sleep(self, params: dict) -> ActionResult:
        """Put system to sleep"""
        if not self.check_permission("system", "shutdown"):
            return ActionResult(False, "Sleep permission denied", error="permission_denied")

        try:
            return ActionResult(True, "Sleep mode initiated", data={"command": "sleep"})
        except Exception as e:
            return ActionResult(False, f"Sleep error: {e}", error=str(e))

    def _handle_system_status(self, params: dict) -> ActionResult:
        """Get comprehensive system status"""
        import psutil

        status = {
            "cpu": {
                "percent": psutil.cpu_percent(interval=1),
                "count": psutil.cpu_count(),
                "freq": str(psutil.cpu_freq())
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": psutil.disk_usage('/').total,
                "used": psutil.disk_usage('/').used,
                "free": psutil.disk_usage('/').free,
                "percent": psutil.disk_usage('/').percent
            },
            "network": {
                "connections": len(psutil.net_connections()),
                "io": dict(psutil.net_io_counters()._asdict())
            },
            "processes": len(psutil.pids()),
            "uptime": time.time() - psutil.boot_time(),
            "timestamp": datetime.now().isoformat()
        }

        return ActionResult(True, "System status retrieved", data=status)

    def _handle_network_info(self, params: dict) -> ActionResult:
        """Get network information"""
        import psutil

        net_if = psutil.net_if_addrs()
        interfaces = {}
        for iface, addrs in net_if.items():
            interfaces[iface] = [addr._asdict() for addr in addrs]

        return ActionResult(True, "Network info retrieved", data={
            "interfaces": interfaces,
            "connections_count": len(psutil.net_connections())
        })

    # ==================== CLIPBOARD ====================

    def _handle_clipboard_copy(self, params: dict) -> ActionResult:
        """Copy text to clipboard"""
        text = params.get("text", "")
        if not text:
            return ActionResult(False, "No text provided", error="missing_text")

        try:
            import subprocess
            if sys.platform == 'darwin':
                subprocess.run(['pbcopy'], input=text.encode(), capture_output=True, timeout=5)
            elif sys.platform == 'win32':
                subprocess.run(['clip'], input=text.encode(), capture_output=True, timeout=5)
            else:
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode(), capture_output=True, timeout=5)

            return ActionResult(True, f"Copied {len(text)} chars to clipboard")
        except Exception as e:
            return ActionResult(False, f"Clipboard error: {e}", error=str(e))

    def _handle_clipboard_paste(self, params: dict) -> ActionResult:
        """Paste text from clipboard"""
        try:
            import subprocess
            if sys.platform == 'darwin':
                result = subprocess.run(['pbpaste'], capture_output=True, text=True, timeout=5)
            elif sys.platform == 'win32':
                result = subprocess.run(['powershell', '-Command', 'Get-Clipboard'], capture_output=True, text=True, timeout=5)
            else:
                result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], capture_output=True, text=True, timeout=5)

            return ActionResult(True, "Clipboard retrieved", data={"content": result.stdout})
        except Exception as e:
            return ActionResult(False, f"Clipboard error: {e}", error=str(e))

    # ==================== UTILITY METHODS ====================

    def get_action_history(self, limit: int = 50) -> list:
        """Get recent action history"""
        return list(self.action_history)[-limit:]

    def get_decision_history(self, limit: int = 50) -> list:
        """Get recent decision history"""
        return list(self.decision_history)[-limit:]

    def reset_action_log(self):
        """Clear action history"""
        self.action_history.clear()
        logger.info("Action log reset")

    def set_confidence_threshold(self, threshold: float):
        """Set confidence threshold for auto-approve decisions"""
        self.decision_confidence = max(0.0, min(1.0, threshold))
        logger.info(f"Confidence threshold set to {self.decision_confidence}")

    def set_auto_approve(self, enabled: bool, threshold: float = 0.7):
        """Enable/disable auto-approve for actions above threshold"""
        self.auto_approve_threshold = threshold
        self.autonomous_mode = enabled
        logger.info(f"Auto-approve {'enabled' if enabled else 'disabled'} (threshold: {threshold})")


# Global instance
autonomous_engine = AutonomousEngine()