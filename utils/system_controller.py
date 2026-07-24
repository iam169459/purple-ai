"""
System Controller - Full Computer Control
Handles opening/closing apps, file system, volume, screen, and more
"""
import os
import subprocess
import platform
import psutil
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from logger import logger

class SystemController:
    def __init__(self):
        self.os_type = platform.system()
        self.app_paths = self._get_app_paths()
        logger.info(f"System Controller initialized for {self.os_type}")
    
    def _get_app_paths(self) -> Dict[str, str]:
        if self.os_type == 'Darwin':  # macOS
            return {
                'safari': 'open -a Safari',
                'chrome': 'open -a "Google Chrome"',
                'firefox': 'open -a Firefox',
                'finder': 'open -a Finder',
                'terminal': 'open -a Terminal',
                'calculator': 'open -a Calculator',
                'calendar': 'open -a Calendar',
                'notes': 'open -a Notes',
                'music': 'open -a Music',
                'photos': 'open -a Photos',
                'messages': 'open -a Messages',
                'facetime': 'open -a FaceTime',
                'mail': 'open -a Mail',
                'maps': 'open -a Maps',
                'weather': 'open -a Weather',
                'news': 'open -a News',
                'stocks': 'open -a Stocks',
                'reminders': 'open -a Reminders',
                'pages': 'open -a Pages',
                'numbers': 'open -a Numbers',
                'keynote': 'open -a Keynote',
                'imovie': 'open -a iMovie',
                'garageband': 'open -a GarageBand',
                'xcode': 'open -a Xcode',
                'vscode': 'open -a "Visual Studio Code"',
                'spotify': 'open -a Spotify',
                'slack': 'open -a Slack',
                'discord': 'open -a Discord',
                'zoom': 'open -a Zoom',
                'teams': 'open -a Microsoft Teams',
                'word': 'open -a "Microsoft Word"',
                'excel': 'open -a "Microsoft Excel"',
                'powerpoint': 'open -a "Microsoft PowerPoint"',
                'preview': 'open -a Preview',
                'textedit': 'open -a TextEdit',
                'activity_monitor': 'open -a "Activity Monitor"',
                'system_preferences': 'open -a "System Preferences"',
                'app_store': 'open -a "App Store"',
            }
        elif self.os_type == 'Windows':
            return {
                'chrome': 'start chrome',
                'firefox': 'start firefox',
                'edge': 'start msedge',
                'explorer': 'explorer',
                'notepad': 'notepad',
                'calculator': 'calc',
                'paint': 'mspaint',
                'word': 'start winword',
                'excel': 'start excel',
                'powerpoint': 'start powerpnt',
                'teams': 'start teams',
                'spotify': 'start spotify',
                'discord': 'start discord',
                'vscode': 'start code',
                'settings': 'start ms-settings:',
                'task_manager': 'taskmgr',
                'control_panel': 'control',
            }
        return {}
    
    def open_application(self, app_name: str) -> Dict[str, Any]:
        app_lower = app_name.lower().strip()
        
        # Special handling for YouTube - open in browser
        if 'youtube' in app_lower:
            return self.open_youtube()
        
        # Special handling for Google search
        if 'google' in app_lower and 'search' in app_lower:
            # Extract search query
            query = app_lower.replace('google', '').replace('search', '').strip()
            return self.open_google_search(query)
        
        if app_lower in self.app_paths:
            cmd = self.app_paths[app_lower]
        else:
            if self.os_type == 'Darwin':
                cmd = f'open -a "{app_name}"'
            elif self.os_type == 'Windows':
                cmd = f'start {app_name}'
            else:
                cmd = app_name
        
        try:
            subprocess.Popen(cmd, shell=True)
            return {'success': True, 'message': f'Opened {app_name}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to open {app_name}: {e}'}
    
    def close_application(self, app_name: str) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', f'quit app "{app_name}"'], 
                             capture_output=True, timeout=5)
            elif self.os_type == 'Windows':
                subprocess.run(['taskkill', '/IM', f'{app_name}.exe', '/F'], 
                             capture_output=True, timeout=5)
            return {'success': True, 'message': f'Closed {app_name}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to close {app_name}: {e}'}
    
    def get_installed_apps(self) -> List[str]:
        if self.os_type == 'Darwin':
            try:
                result = subprocess.run(['ls', '/Applications'], capture_output=True, text=True, timeout=5)
                apps = [f.replace('.app', '') for f in result.stdout.strip().split('\n') if f.endswith('.app')]
                return apps
            except Exception:
                return list(self.app_paths.keys())
        elif self.os_type == 'Windows':
            try:
                result = subprocess.run(['dir', 'C:\\Program Files\\', '/b'], capture_output=True, text=True, timeout=5)
                return result.stdout.strip().split('\n')
            except Exception:
                return list(self.app_paths.keys())
        return list(self.app_paths.keys())
    
    def get_running_apps(self) -> List[str]:
        try:
            running = []
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name']
                    if name and name not in running:
                        running.append(name)
                except Exception:
                    pass
            return sorted(set(running))
        except Exception:
            return []
    
    def get_system_info(self) -> Dict[str, Any]:
        try:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'cpu_count': psutil.cpu_count(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_total': round(psutil.virtual_memory().total / (1024**3), 2),
                'memory_used': round(psutil.virtual_memory().used / (1024**3), 2),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': round(psutil.disk_usage('/').percent if self.os_type != 'Windows' else psutil.disk_usage('C:\\').percent, 2),
                'battery': self._get_battery_info(),
                'hostname': platform.node(),
            }
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def _get_battery_info(self) -> Dict[str, Any]:
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percent': battery.percent,
                    'power_plugged': battery.power_plugged,
                    'time_left': battery.secsleft if battery.secsleft > 0 else 'Unknown'
                }
        except Exception:
            pass
        return {'percent': 'N/A', 'power_plugged': 'N/A'}
    
    def get_volume(self) -> int:
        try:
            if self.os_type == 'Darwin':
                result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], 
                                       capture_output=True, text=True, timeout=5)
                return int(result.stdout.strip())
            elif self.os_type == 'Windows':
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                return int(volume.GetMasterVolumeLevelScalar() * 100)
        except Exception:
            pass
        return 50
    
    def set_volume(self, level: int) -> Dict[str, Any]:
        level = max(0, min(100, level))
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', f'set volume output volume {level}'], 
                             capture_output=True, timeout=5)
                return {'success': True, 'message': f'Volume set to {level}%'}
            elif self.os_type == 'Windows':
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                volume.SetMasterVolumeLevelScalar(level / 100, None)
                return {'success': True, 'message': f'Volume set to {level}%'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to set volume: {e}'}
        return {'success': False, 'message': 'Volume control not available'}
    
    def volume_up(self) -> Dict[str, Any]:
        current = self.get_volume()
        return self.set_volume(min(100, current + 10))
    
    def volume_down(self) -> Dict[str, Any]:
        current = self.get_volume()
        return self.set_volume(max(0, current - 10))
    
    def mute(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', 'set volume output muted true'], 
                             capture_output=True, timeout=5)
                return {'success': True, 'message': 'Muted'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to mute: {e}'}
        return {'success': False, 'message': 'Mute not available'}
    
    def unmute(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', 'set volume output muted false'], 
                             capture_output=True, timeout=5)
                return {'success': True, 'message': 'Unmuted'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to unmute: {e}'}
        return {'success': False, 'message': 'Unmute not available'}
    
    def screenshot(self, filename: str = None) -> Dict[str, Any]:
        try:
            if not filename:
                from datetime import datetime
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            if self.os_type == 'Darwin':
                filepath = os.path.join(os.path.expanduser('~/Desktop'), filename)
                subprocess.run(['screencapture', filepath], timeout=10)
                return {'success': True, 'message': f'Screenshot saved to {filepath}'}
            elif self.os_type == 'Windows':
                filepath = os.path.join(os.path.expanduser('~/Desktop'), filename)
                subprocess.run(['snippingtool', '/clip', filepath], timeout=10)
                return {'success': True, 'message': f'Screenshot saved to {filepath}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to take screenshot: {e}'}
        return {'success': False, 'message': 'Screenshot not available'}
    
    def lock_screen(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', 'tell application "System Events" to keystroke "q" using {command down, control down}'], 
                             timeout=5)
                return {'success': True, 'message': 'Screen locked'}
            elif self.os_type == 'Windows':
                subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'], timeout=5)
                return {'success': True, 'message': 'Screen locked'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to lock screen: {e}'}
        return {'success': False, 'message': 'Lock not available'}
    
    def empty_trash(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', 'tell application "Finder" to empty the trash'], 
                             timeout=30)
                return {'success': True, 'message': 'Trash emptied'}
            elif self.os_type == 'Windows':
                subprocess.run(['rd', '/s', '/q', '%SystemDrive%\\$Recycle.bin'], 
                             shell=True, timeout=30)
                return {'success': True, 'message': 'Recycle Bin emptied'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to empty trash: {e}'}
        return {'success': False, 'message': 'Empty trash not available'}
    
    def shutdown(self, delay: int = 0) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                if delay > 0:
                    subprocess.run(['osascript', '-e', f'delay {delay}', '-e', 
                                   'tell application "System Events" to shut down'], timeout=delay+10)
                else:
                    subprocess.run(['osascript', '-e', 'tell application "System Events" to shut down'], 
                                 timeout=10)
                return {'success': True, 'message': 'Shutting down'}
            elif self.os_type == 'Windows':
                subprocess.run(['shutdown', '/s', '/t', str(delay)], timeout=10)
                return {'success': True, 'message': 'Shutting down'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to shutdown: {e}'}
        return {'success': False, 'message': 'Shutdown not available'}
    
    def restart(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', 'tell application "System Events" to restart'], 
                             timeout=10)
                return {'success': True, 'message': 'Restarting'}
            elif self.os_type == 'Windows':
                subprocess.run(['shutdown', '/r', '/t', '0'], timeout=10)
                return {'success': True, 'message': 'Restarting'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to restart: {e}'}
        return {'success': False, 'message': 'Restart not available'}
    
    def cancel_shutdown(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['killall', 'shutdown'], timeout=5)
                return {'success': True, 'message': 'Shutdown cancelled'}
            elif self.os_type == 'Windows':
                subprocess.run(['shutdown', '/a'], timeout=5)
                return {'success': True, 'message': 'Shutdown cancelled'}
        except Exception:
            return {'success': False, 'message': 'No shutdown to cancel'}
    
    def sleep(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['pmset', 'sleepnow'], timeout=5)
                return {'success': True, 'message': 'Computer sleeping'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to sleep: {e}'}
        return {'success': False, 'message': 'Sleep not available'}
    
    def wake(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['caffeinate', '-u', '-t', '1'], timeout=5)
                return {'success': True, 'message': 'Waking up'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to wake: {e}'}
        return {'success': False, 'message': 'Wake not available'}
    
    def list_files(self, path: str = '~') -> Dict[str, Any]:
        try:
            path = os.path.expanduser(path)
            items = os.listdir(path)
            files = []
            dirs = []
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    dirs.append(item + '/')
                else:
                    files.append(item)
            return {'success': True, 'directories': sorted(dirs), 'files': sorted(files), 'path': path}
        except Exception as e:
            return {'success': False, 'message': f'Failed to list files: {e}'}
    
    def get_file_info(self, filepath: str) -> Dict[str, Any]:
        try:
            filepath = os.path.expanduser(filepath)
            if os.path.exists(filepath):
                stat = os.stat(filepath)
                return {
                    'success': True,
                    'name': os.path.basename(filepath),
                    'size': round(stat.st_size / 1024, 2),
                    'modified': stat.st_mtime,
                    'is_dir': os.path.isdir(filepath),
                }
            return {'success': False, 'message': 'File not found'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {e}'}
    
    def open_file(self, filepath: str) -> Dict[str, Any]:
        try:
            filepath = os.path.expanduser(filepath)
            if os_type == 'Darwin':
                subprocess.run(['open', filepath], timeout=10)
            elif os_type == 'Windows':
                os.startfile(filepath)
            return {'success': True, 'message': f'Opened {filepath}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to open file: {e}'}
    
    def create_folder(self, path: str) -> Dict[str, Any]:
        try:
            path = os.path.expanduser(path)
            os.makedirs(path, exist_ok=True)
            return {'success': True, 'message': f'Created folder: {path}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to create folder: {e}'}
    
    def delete_file(self, filepath: str) -> Dict[str, Any]:
        try:
            filepath = os.path.expanduser(filepath)
            if os.path.isfile(filepath):
                os.remove(filepath)
                return {'success': True, 'message': f'Deleted {filepath}'}
            elif os.path.isdir(filepath):
                import shutil
                shutil.rmtree(filepath)
                return {'success': True, 'message': f'Deleted folder {filepath}'}
            return {'success': False, 'message': 'File not found'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to delete: {e}'}
    
    def copy_file(self, src: str, dst: str) -> Dict[str, Any]:
        try:
            import shutil
            src = os.path.expanduser(src)
            dst = os.path.expanduser(dst)
            shutil.copy2(src, dst)
            return {'success': True, 'message': f'Copied to {dst}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to copy: {e}'}
    
    def move_file(self, src: str, dst: str) -> Dict[str, Any]:
        try:
            import shutil
            src = os.path.expanduser(src)
            dst = os.path.expanduser(dst)
            shutil.move(src, dst)
            return {'success': True, 'message': f'Moved to {dst}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to move: {e}'}
    
    def search_files(self, pattern: str, path: str = '~') -> List[str]:
        try:
            path = os.path.expanduser(path)
            matches = []
            for root, dirs, files in os.walk(path):
                for f in files:
                    if pattern.lower() in f.lower():
                        matches.append(os.path.join(root, f))
                if len(matches) >= 20:
                    break
            return matches
        except Exception:
            return []
    
    def get_wifi_info(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                result = subprocess.run(['networksetup', '-getairportnetwork', 'en0'], 
                                       capture_output=True, text=True, timeout=5)
                return {'connected': 'not associated' not in result.stdout, 'network': result.stdout.strip()}
        except Exception:
            pass
        return {'connected': 'Unknown', 'network': 'Unknown'}
    
    def get_battery(self) -> Dict[str, Any]:
        return self._get_battery_info()
    
    def get_disk_space(self) -> Dict[str, Any]:
        try:
            if self.os_type != 'Windows':
                usage = psutil.disk_usage('/')
            else:
                usage = psutil.disk_usage('C:\\')
            return {
                'total': round(usage.total / (1024**3), 2),
                'used': round(usage.used / (1024**3), 2),
                'free': round(usage.free / (1024**3), 2),
                'percent': round(usage.percent, 2)
            }
        except Exception:
            return {'error': 'Could not get disk info'}
    
    def get_network_info(self) -> Dict[str, Any]:
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': round(net_io.bytes_sent / (1024**2), 2),
                'bytes_recv': round(net_io.bytes_recv / (1024**2), 2),
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
            }
        except Exception:
            return {'error': 'Could not get network info'}
    
    def open_url(self, url: str) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['open', url], timeout=10)
            elif self.os_type == 'Windows':
                subprocess.run(['start', url], shell=True, timeout=10)
            return {'success': True, 'message': f'Opened {url}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to open URL: {e}'}
    
    def open_youtube(self) -> Dict[str, Any]:
        return self.open_url('https://www.youtube.com')
    
    def open_youtube_search(self, query: str) -> Dict[str, Any]:
        search_url = f'https://www.youtube.com/results?search_query={query.replace(" ", "+")}'
        return self.open_url(search_url)
    
    def open_google_search(self, query: str) -> Dict[str, Any]:
        search_url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
        return self.open_url(search_url)
    
    def open_browser(self) -> Dict[str, Any]:
        if self.os_type == 'Darwin':
            return self.open_application('safari')
        else:
            return self.open_application('chrome')
    
    def search_in_browser(self, query: str) -> Dict[str, Any]:
        return self.open_google_search(query)
    
    def type_text(self, text: str) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', f'tell application "System Events" to keystroke "{text}"'], 
                             timeout=10)
            elif self.os_type == 'Windows':
                import pyautogui
                pyautogui.typewrite(text, interval=0.05)
            return {'success': True, 'message': f'Typed: {text}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to type: {e}'}
    
    def press_key(self, key: str) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', f'tell application "System Events" to key code {key}'], 
                             timeout=5)
            return {'success': True, 'message': f'Pressed key: {key}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to press key: {e}'}
    
    def press_enter(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 36'], 
                             timeout=5)
            return {'success': True, 'message': 'Pressed Enter'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to press Enter: {e}'}
    
    def cmd_key(self, key: str) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', f'tell application "System Events" to keystroke "{key}" using command down'], 
                             timeout=5)
            return {'success': True, 'message': f'Pressed Cmd+{key}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to press Cmd+{key}: {e}'}
    
    def cmd_tab(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['osascript', '-e', 'tell application "System Events" to keystroke tab using command down'], 
                             timeout=5)
            return {'success': True, 'message': 'Switched app'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to switch: {e}'}
    
    def click_at(self, x: int, y: int) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                subprocess.run(['cliclick', f'c:{x},{y}'], timeout=5)
            return {'success': True, 'message': f'Clicked at {x},{y}'}
        except Exception:
            return {'success': False, 'message': 'Click not available'}
    
    def get_active_window(self) -> Dict[str, Any]:
        try:
            if self.os_type == 'Darwin':
                result = subprocess.run(['osascript', '-e', 'tell application "System Events" to get name of first application process whose frontmost is true'], 
                                       capture_output=True, text=True, timeout=5)
                return {'success': True, 'app': result.stdout.strip()}
        except Exception:
            pass
        return {'success': False, 'app': 'Unknown'}
    
    def is_app_running(self, app_name: str) -> bool:
        try:
            running = self.get_running_apps()
            app_lower = app_name.lower()
            for app in running:
                if app_lower in app.lower():
                    return True
        except Exception:
            pass
        return False
