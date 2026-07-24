"""
System Monitor - Read open apps, tabs, and system status
"""
import os
import subprocess
import platform
import json
from typing import Dict, Any, List, Optional
from logger import logger

class SystemMonitor:
    def __init__(self):
        self.os_type = platform.system()
        logger.info(f"System Monitor initialized for {self.os_type}")
    
    def get_running_apps(self) -> List[str]:
        """Get list of running applications"""
        apps = []
        
        try:
            if self.os_type == 'Darwin':  # macOS
                # Get running apps using AppleScript
                script = '''
                tell application "System Events"
                    set appList to name of every application process whose background only is false
                end tell
                return appList
                '''
                result = subprocess.run(['osascript', '-e', script], 
                                       capture_output=True, text=True, timeout=10)
                if result.stdout:
                    apps = [app.strip() for app in result.stdout.strip().split(', ') if app.strip()]
            
            elif self.os_type == 'Windows':
                # Get running apps using tasklist
                result = subprocess.run(['tasklist', '/FO', 'CSV'], 
                                       capture_output=True, text=True, timeout=10)
                if result.stdout:
                    lines = result.stdout.strip().split('\n')[1:]  # Skip header
                    for line in lines:
                        parts = line.split(',')
                        if parts:
                            app_name = parts[0].strip('"')
                            if app_name not in apps and not app_name.startswith('Task'):
                                apps.append(app_name)
            
            else:  # Linux
                # Get running apps using ps
                result = subprocess.run(['ps', 'aux'], 
                                       capture_output=True, text=True, timeout=10)
                if result.stdout:
                    for line in result.stdout.strip().split('\n')[1:]:  # Skip header
                        parts = line.split()
                        if len(parts) > 10:
                            cmd = parts[10]
                            if '/' in cmd:
                                app = cmd.split('/')[-1]
                            else:
                                app = cmd
                            if app not in apps and not app.startswith('['):
                                apps.append(app)
        
        except Exception as e:
            logger.error(f"Error getting running apps: {e}")
        
        return apps
    
    def get_active_window(self) -> Dict[str, Any]:
        """Get information about the active window"""
        result = {
            'app': 'Unknown',
            'title': 'Unknown',
            'pid': None
        }
        
        try:
            if self.os_type == 'Darwin':  # macOS
                script = '''
                tell application "System Events"
                    set frontApp to first application process whose frontmost is true
                    set appName to name of frontApp
                    set appPID to unix id of frontApp
                end tell
                    
                tell application "System Events"
                    tell process appName
                        set windowList to every window
                        if (count of windowList) > 0 then
                            set windowTitle to name of first window
                        else
                            set windowTitle to "No Window"
                        end if
                    end tell
                end tell
                    
                return appName & "|||" & windowTitle & "|||" & appPID
                '''
                proc = subprocess.run(['osascript', '-e', script], 
                                     capture_output=True, text=True, timeout=10)
                if proc.stdout:
                    parts = proc.stdout.strip().split('|||')
                    if len(parts) >= 3:
                        result['app'] = parts[0]
                        result['title'] = parts[1]
                        result['pid'] = int(parts[2]) if parts[2].isdigit() else None
            
            elif self.os_type == 'Windows':
                import ctypes
                user32 = ctypes.windll.user32
                hwnd = user32.GetForegroundWindow()
                
                # Get window title
                length = user32.GetWindowTextLengthW(hwnd)
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                result['title'] = buf.value
                
                # Get process ID
                pid = ctypes.c_ulong()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                result['pid'] = pid.value
                
                # Get process name
                import psutil
                try:
                    proc = psutil.Process(pid.value)
                    result['app'] = proc.name()
                except Exception:
                    result['app'] = 'Unknown'
        
        except Exception as e:
            logger.error(f"Error getting active window: {e}")
        
        return result
    
    def get_browser_tabs(self, browser: str = 'safari') -> List[Dict[str, str]]:
        """Get open tabs in browser"""
        tabs = []
        
        try:
            if self.os_type == 'Darwin':  # macOS
                if browser.lower() == 'safari':
                    script = '''
                    tell application "Safari"
                        set tabList to {}
                        repeat with w in every window
                            repeat with t in every tab of w
                                set end of tabList to (name of t & "|||" & URL of t)
                            end repeat
                        end repeat
                        return tabList
                    end tell
                    '''
                    proc = subprocess.run(['osascript', '-e', script], 
                                         capture_output=True, text=True, timeout=15)
                    if proc.stdout:
                        for tab_str in proc.stdout.strip().split(', '):
                            if '|||' in tab_str:
                                parts = tab_str.split('|||')
                                tabs.append({'title': parts[0], 'url': parts[1] if len(parts) > 1 else ''})
                
                elif browser.lower() in ['chrome', 'google chrome']:
                    script = '''
                    tell application "Google Chrome"
                        set tabList to {}
                        repeat with w in every window
                            repeat with t in every tab of w
                                set end of tabList to (title of t & "|||" & URL of t)
                            end repeat
                        end repeat
                        return tabList
                    end tell
                    '''
                    proc = subprocess.run(['osascript', '-e', script], 
                                         capture_output=True, text=True, timeout=15)
                    if proc.stdout:
                        for tab_str in proc.stdout.strip().split(', '):
                            if '|||' in tab_str:
                                parts = tab_str.split('|||')
                                tabs.append({'title': parts[0], 'url': parts[1] if len(parts) > 1 else ''})
            
            elif self.os_type == 'Windows':
                # Windows browser tab reading is more complex
                # Would need to use accessibility APIs
                pass
        
        except Exception as e:
            logger.error(f"Error getting browser tabs: {e}")
        
        return tabs
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            'running_apps': self.get_running_apps(),
            'active_window': self.get_active_window(),
            'browser_tabs': {},
            'system_info': self._get_basic_system_info()
        }
        
        # Get tabs for each running browser
        running_apps = [app.lower() for app in status['running_apps']]
        
        if 'safari' in running_apps:
            status['browser_tabs']['safari'] = self.get_browser_tabs('safari')
        
        if 'google chrome' in running_apps or 'chrome' in running_apps:
            status['browser_tabs']['chrome'] = self.get_browser_tabs('chrome')
        
        return status
    
    def _get_basic_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        info = {
            'platform': self.os_type,
            'cpu_percent': None,
            'memory_percent': None,
            'disk_usage': None
        }
        
        try:
            import psutil
            info['cpu_percent'] = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()
            info['memory_percent'] = memory.percent
            disk = psutil.disk_usage('/')
            info['disk_usage'] = disk.percent
        except ImportError:
            logger.warning("psutil not available for system info")
        
        return info
    
    def describe_screen_state(self) -> str:
        """Generate natural language description of current screen state"""
        status = self.get_system_status()
        
        description = []
        
        # Active window
        active = status['active_window']
        if active['app'] != 'Unknown':
            description.append(f"Currently viewing: {active['app']}")
            if active['title'] != 'No Window':
                description.append(f"Window: {active['title']}")
        
        # Running apps
        apps = status['running_apps']
        if apps:
            description.append(f"Open apps: {', '.join(apps[:5])}")
            if len(apps) > 5:
                description.append(f"and {len(apps) - 5} more")
        
        # Browser tabs
        for browser, tabs in status['browser_tabs'].items():
            if tabs:
                description.append(f"\n{browser.title()} has {len(tabs)} open tab(s):")
                for i, tab in enumerate(tabs[:3], 1):
                    description.append(f"  {i}. {tab['title'][:50]}")
                if len(tabs) > 3:
                    description.append(f"  and {len(tabs) - 3} more tabs")
        
        # System info
        sys_info = status['system_info']
        if sys_info['cpu_percent'] is not None:
            description.append(f"\nSystem: CPU {sys_info['cpu_percent']}%, Memory {sys_info['memory_percent']}%")
        
        return ' '.join(description) if description else "I can see your screen but I'm not sure what to focus on."
    
    def list_open_tabs(self) -> str:
        """List all open browser tabs"""
        status = self.get_system_status()
        
        result = []
        for browser, tabs in status['browser_tabs'].items():
            if tabs:
                result.append(f"\n{browser.title()} ({len(tabs)} tabs):")
                for i, tab in enumerate(tabs, 1):
                    result.append(f"  {i}. {tab['title']}")
        
        return '\n'.join(result) if result else "I don't see any open browser tabs."
    
    def get_app_info(self, app_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific app"""
        info = {
            'name': app_name,
            'is_running': False,
            'pid': None,
            'tabs': [] if app_name.lower() in ['safari', 'chrome', 'google chrome'] else None
        }
        
        running_apps = self.get_running_apps()
        info['is_running'] = any(app_name.lower() in app.lower() for app in running_apps)
        
        # Get tabs if it's a browser
        if info['is_running']:
            if app_name.lower() == 'safari':
                info['tabs'] = self.get_browser_tabs('safari')
            elif app_name.lower() in ['chrome', 'google chrome']:
                info['tabs'] = self.get_browser_tabs('chrome')
        
        return info


# Global instance
system_monitor = SystemMonitor()
