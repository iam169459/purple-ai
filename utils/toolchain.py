"""
Toolchain - Full system access and control
Provides complete computer control capabilities
"""
import os
import sys
import subprocess
import shutil
import json
import platform
import psutil
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from logger import logger

class Toolchain:
    def __init__(self):
        self.os_type = platform.system()
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.temp_dir = os.path.join(self.project_root, "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Command history
        self.command_history = []
        self.max_history = 100
        
        logger.info(f"Toolchain initialized for {self.os_type}")
    
    # ==================== FILE SYSTEM ====================
    def read_file(self, filepath: str) -> Dict[str, Any]:
        """Read file contents"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"success": True, "content": content, "size": len(content)}
        except Exception as e:
            return {"success": False, "message": f"Error reading file: {e}"}
    
    def write_file(self, filepath: str, content: str) -> Dict[str, Any]:
        """Write content to file"""
        try:
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"success": True, "message": f"File written: {filepath}"}
        except Exception as e:
            return {"success": False, "message": f"Error writing file: {e}"}
    
    def append_file(self, filepath: str, content: str) -> Dict[str, Any]:
        """Append content to file"""
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(content)
            return {"success": True, "message": f"Content appended to: {filepath}"}
        except Exception as e:
            return {"success": False, "message": f"Error appending to file: {e}"}
    
    def delete_file(self, filepath: str) -> Dict[str, Any]:
        """Delete file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return {"success": True, "message": f"Deleted: {filepath}"}
            return {"success": False, "message": "File not found"}
        except Exception as e:
            return {"success": False, "message": f"Error deleting file: {e}"}
    
    def move_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Move file"""
        try:
            shutil.move(source, destination)
            return {"success": True, "message": f"Moved {source} to {destination}"}
        except Exception as e:
            return {"success": False, "message": f"Error moving file: {e}"}
    
    def copy_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Copy file"""
        try:
            shutil.copy2(source, destination)
            return {"success": True, "message": f"Copied {source} to {destination}"}
        except Exception as e:
            return {"success": False, "message": f"Error copying file: {e}"}
    
    def create_directory(self, dirpath: str) -> Dict[str, Any]:
        """Create directory"""
        try:
            os.makedirs(dirpath, exist_ok=True)
            return {"success": True, "message": f"Created directory: {dirpath}"}
        except Exception as e:
            return {"success": False, "message": f"Error creating directory: {e}"}
    
    def list_directory(self, dirpath: str = ".") -> Dict[str, Any]:
        """List directory contents"""
        try:
            items = []
            for item in os.listdir(dirpath):
                full_path = os.path.join(dirpath, item)
                items.append({
                    "name": item,
                    "type": "directory" if os.path.isdir(full_path) else "file",
                    "size": os.path.getsize(full_path) if os.path.isfile(full_path) else 0
                })
            return {"success": True, "items": items}
        except Exception as e:
            return {"success": False, "message": f"Error listing directory: {e}"}
    
    def find_files(self, pattern: str, directory: str = ".") -> List[str]:
        """Find files matching pattern"""
        try:
            matches = list(Path(directory).glob(pattern))
            return [str(m) for m in matches]
        except Exception as e:
            logger.error(f"Error finding files: {e}")
            return []
    
    def get_file_info(self, filepath: str) -> Dict[str, Any]:
        """Get file information"""
        try:
            stat = os.stat(filepath)
            return {
                "success": True,
                "name": os.path.basename(filepath),
                "path": filepath,
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "is_file": os.path.isfile(filepath),
                "is_dir": os.path.isdir(filepath)
            }
        except Exception as e:
            return {"success": False, "message": f"Error getting file info: {e}"}
    
    # ==================== PROCESS MANAGEMENT ====================
    def run_command(self, command: str, cwd: str = None, timeout: int = 30) -> Dict[str, Any]:
        """Run shell command"""
        try:
            self.command_history.append({"command": command, "time": time.time()})
            if len(self.command_history) > self.max_history:
                self.command_history.pop(0)
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "message": "Command timed out"}
        except Exception as e:
            return {"success": False, "message": f"Error running command: {e}"}
    
    def run_background(self, command: str) -> Dict[str, Any]:
        """Run command in background"""
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return {"success": True, "pid": process.pid, "message": f"Started background process: {process.pid}"}
        except Exception as e:
            return {"success": False, "message": f"Error starting background process: {e}"}
    
    def kill_process(self, pid: int) -> Dict[str, Any]:
        """Kill process by PID"""
        try:
            process = psutil.Process(pid)
            process.terminate()
            return {"success": True, "message": f"Terminated process: {pid}"}
        except Exception as e:
            return {"success": False, "message": f"Error killing process: {e}"}
    
    def get_processes(self) -> List[Dict[str, Any]]:
        """Get list of running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes
    
    def find_process(self, name: str) -> List[Dict[str, Any]]:
        """Find process by name"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if name.lower() in proc.info['name'].lower():
                    processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes
    
    # ==================== APPLICATION CONTROL ====================
    def open_app(self, app_name: str) -> Dict[str, Any]:
        """Open application"""
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['open', '-a', app_name], check=True)
            elif self.os_type == 'Windows':
                subprocess.run(['start', app_name], shell=True, check=True)
            else:
                subprocess.run([app_name], check=True)
            return {"success": True, "message": f"Opened {app_name}"}
        except Exception as e:
            return {"success": False, "message": f"Error opening app: {e}"}
    
    def close_app(self, app_name: str) -> Dict[str, Any]:
        """Close application"""
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', f'quit app "{app_name}"'], check=True)
            elif self.os_type == 'Windows':
                subprocess.run(['taskkill', '/IM', f'{app_name}.exe', '/F'], check=True)
            else:
                subprocess.run(['pkill', app_name], check=True)
            return {"success": True, "message": f"Closed {app_name}"}
        except Exception as e:
            return {"success": False, "message": f"Error closing app: {e}"}
    
    def focus_app(self, app_name: str) -> Dict[str, Any]:
        """Bring application to front"""
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', f'tell application "{app_name}" to activate'], check=True)
            return {"success": True, "message": f"Focused {app_name}"}
        except Exception as e:
            return {"success": False, "message": f"Error focusing app: {e}"}
    
    # ==================== BROWSER AUTOMATION ====================
    def open_url(self, url: str) -> Dict[str, Any]:
        """Open URL in default browser"""
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['open', url], check=True)
            elif self.os_type == 'Windows':
                subprocess.run(['start', url], shell=True, check=True)
            else:
                subprocess.run(['xdg-open', url], check=True)
            return {"success": True, "message": f"Opened {url}"}
        except Exception as e:
            return {"success": False, "message": f"Error opening URL: {e}"}
    
    def search_google(self, query: str) -> Dict[str, Any]:
        """Search Google"""
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return self.open_url(url)
    
    def search_youtube(self, query: str) -> Dict[str, Any]:
        """Search YouTube"""
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        return self.open_url(url)
    
    def download_file(self, url: str, destination: str) -> Dict[str, Any]:
        """Download file from URL"""
        try:
            import urllib.request
            urllib.request.urlretrieve(url, destination)
            return {"success": True, "message": f"Downloaded to {destination}"}
        except Exception as e:
            return {"success": False, "message": f"Error downloading: {e}"}
    
    # ==================== SYSTEM INFO ====================
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        try:
            info = {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count(),
                "cpu_percent": psutil.cpu_percent(interval=1),
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
                "network": dict(psutil.net_io_counters()._asdict())
            }
            return {"success": True, "info": info}
        except Exception as e:
            return {"success": False, "message": f"Error getting system info: {e}"}
    
    def get_battery(self) -> Dict[str, Any]:
        """Get battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "success": True,
                    "percent": battery.percent,
                    "plugged": battery.power_plugged,
                    "time_left": battery.secsleft
                }
            return {"success": False, "message": "No battery found"}
        except Exception as e:
            return {"success": False, "message": f"Error getting battery: {e}"}
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        try:
            addrs = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            return {"success": True, "interfaces": dict(addrs), "stats": dict(stats)}
        except Exception as e:
            return {"success": False, "message": f"Error getting network info: {e}"}
    
    # ==================== TEXT OPERATIONS ====================
    def type_text(self, text: str) -> Dict[str, Any]:
        """Type text using keyboard"""
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', f'tell application "System Events" to keystroke "{text}"'], check=True)
            elif self.os_type == 'Windows':
                import pyautogui
                pyautogui.typewrite(text, interval=0.05)
            return {"success": True, "message": f"Typed: {text}"}
        except Exception as e:
            return {"success": False, "message": f"Error typing: {e}"}
    
    def press_key(self, key: str) -> Dict[str, Any]:
        """Press keyboard key"""
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', f'tell application "System Events" to key code {key}'], check=True)
            return {"success": True, "message": f"Pressed key: {key}"}
        except Exception as e:
            return {"success": False, "message": f"Error pressing key: {e}"}
    
    def take_screenshot(self, filepath: str = None) -> Dict[str, Any]:
        """Take screenshot"""
        try:
            if not filepath:
                filepath = os.path.join(self.temp_dir, f"screenshot_{int(time.time())}.png")
            
            if self.os_type == 'Darwin':
                subprocess.run(['screencapture', '-x', filepath], check=True)
            elif self.os_type == 'Windows':
                subprocess.run(['powershell', '-Command', 
                    'Add-Type -AssemblyName System.Windows.Forms; '
                    '[System.Windows.Forms.Screen]::PrimaryScreen | ForEach-Object { '
                    '$bmp = New-Object System.Drawing.Bitmap($_.Bounds.Width, $_.Bounds.Height); '
                    '$graphics = [System.Drawing.Graphics]::FromImage($bmp); '
                    '$graphics.CopyFromScreen($_.Location, [System.Drawing.Point]::Empty, $_.Size); '
                    f'$bmp.Save("{filepath}") }}'], check=True)
            
            return {"success": True, "filepath": filepath}
        except Exception as e:
            return {"success": False, "message": f"Error taking screenshot: {e}"}
    
    # ==================== CLIPBOARD ====================
    def get_clipboard(self) -> Dict[str, Any]:
        """Get clipboard contents"""
        try:
            if self.os_type == 'Darwin':
                result = subprocess.run(['pbpaste'], capture_output=True, text=True)
                return {"success": True, "content": result.stdout}
            elif self.os_type == 'Windows':
                result = subprocess.run(['powershell', '-Command', 'Get-Clipboard'], capture_output=True, text=True)
                return {"success": True, "content": result.stdout}
            return {"success": False, "message": "Clipboard not supported on this OS"}
        except Exception as e:
            return {"success": False, "message": f"Error getting clipboard: {e}"}
    
    def set_clipboard(self, text: str) -> Dict[str, Any]:
        """Set clipboard contents"""
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['pbcopy'], input=text.encode(), check=True)
                return {"success": True, "message": "Clipboard updated"}
            elif self.os_type == 'Windows':
                subprocess.run(['powershell', '-Command', f'Set-Clipboard -Value "{text}"'], check=True)
                return {"success": True, "message": "Clipboard updated"}
            return {"success": False, "message": "Clipboard not supported on this OS"}
        except Exception as e:
            return {"success": False, "message": f"Error setting clipboard: {e}"}
    
    # ==================== AUDIO ====================
    def play_audio(self, filepath: str) -> Dict[str, Any]:
        """Play audio file"""
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['afplay', filepath], check=True)
            elif self.os_type == 'Windows':
                subprocess.run(['start', filepath], shell=True, check=True)
            return {"success": True, "message": f"Playing {filepath}"}
        except Exception as e:
            return {"success": False, "message": f"Error playing audio: {e}"}
    
    def get_audio_devices(self) -> List[Dict[str, Any]]:
        """Get audio devices"""
        try:
            # Simple implementation - can be enhanced
            return [{"success": True, "message": "Audio device detection requires additional libraries"}]
        except Exception as e:
            return [{"success": False, "message": f"Error: {e}"}]
    
    # ==================== NETWORK OPERATIONS ====================
    def ping(self, host: str) -> Dict[str, Any]:
        """Ping host"""
        try:
            param = '-n' if self.os_type == 'Windows' else '-c'
            result = subprocess.run(['ping', param, '4', host], capture_output=True, text=True, timeout=10)
            return {"success": result.returncode == 0, "output": result.stdout}
        except Exception as e:
            return {"success": False, "message": f"Error pinging: {e}"}
    
    def get_public_ip(self) -> Dict[str, Any]:
        """Get public IP address"""
        try:
            import urllib.request
            ip = urllib.request.urlopen('https://api.ipify.org').read().decode()
            return {"success": True, "ip": ip}
        except Exception as e:
            return {"success": False, "message": f"Error getting IP: {e}"}
    
    # ==================== UTILITY ====================
    def get_time(self) -> Dict[str, Any]:
        """Get current time"""
        from datetime import datetime
        now = datetime.now()
        return {
            "success": True,
            "time": now.strftime("%I:%M %p"),
            "date": now.strftime("%Y-%m-%d"),
            "datetime": now.isoformat()
        }
    
    def set_timer(self, seconds: int) -> Dict[str, Any]:
        """Set timer"""
        try:
            def timer_callback():
                time.sleep(seconds)
                # Could trigger a notification here
            
            import threading
            timer = threading.Thread(target=timer_callback, daemon=True)
            timer.start()
            return {"success": True, "message": f"Timer set for {seconds} seconds"}
        except Exception as e:
            return {"success": False, "message": f"Error setting timer: {e}"}
    
    def get_weather(self, city: str = "auto") -> Dict[str, Any]:
        """Get weather (requires API key for full functionality)"""
        try:
            import urllib.request
            url = f"https://wttr.in/{city}?format=j1"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": f"Error getting weather: {e}"}
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get command history"""
        return self.command_history[-20:]  # Last 20 commands
    
    def clear_history(self) -> Dict[str, Any]:
        """Clear command history"""
        self.command_history = []
        return {"success": True, "message": "History cleared"}


# Global instance
toolchain = Toolchain()
