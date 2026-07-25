"""
Media Controller - Play music on YouTube, Spotify, and other platforms
Controls playback, volume, and manages media state
"""
import os
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

class MediaController:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.state_file = self.data_dir / "media_state.json"
        self.playlist_file = self.data_dir / "playlists.json"
        
        self.current_platform = None
        self.current_song = None
        self.is_playing = False
        self.volume = 50
        
        self._load_state()
    
    def _load_state(self):
        """Load media state"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.current_platform = state.get('platform')
                    self.current_song = state.get('song')
                    self.is_playing = state.get('is_playing', False)
                    self.volume = state.get('volume', 50)
        except Exception:
            pass
    
    def _save_state(self):
        """Save media state"""
        state = {
            'platform': self.current_platform,
            'song': self.current_song,
            'is_playing': self.is_playing,
            'volume': self.volume,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def play_youtube(self, query: str) -> Dict[str, Any]:
        """Play music on YouTube"""
        try:
            # Open YouTube with search query
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            subprocess.run(['open', url])
            
            self.current_platform = 'youtube'
            self.current_song = query
            self.is_playing = True
            self._save_state()
            
            return {
                'success': True,
                'message': f'Playing {query} on YouTube',
                'platform': 'youtube',
                'query': query
            }
        except Exception as e:
            return {'success': False, 'message': f'Error playing YouTube: {str(e)}'}
    
    def play_spotify(self, query: str = None) -> Dict[str, Any]:
        """Play music on Spotify"""
        try:
            # Try to open Spotify
            if query:
                # Search and play on Spotify
                subprocess.run(['open', f'spotify:search:{query.replace(" ", "+")}'])
                self.current_song = query
            else:
                # Just open/continue Spotify
                subprocess.run(['open', '-a', 'Spotify'])
            
            self.current_platform = 'spotify'
            self.is_playing = True
            self._save_state()
            
            msg = f'Playing {query} on Spotify' if query else 'Spotify opened'
            return {
                'success': True,
                'message': msg,
                'platform': 'spotify'
            }
        except Exception as e:
            return {'success': False, 'message': f'Error with Spotify: {str(e)}'}
    
    def play_music(self, query: str, platform: str = 'auto') -> Dict[str, Any]:
        """Play music on specified or best available platform"""
        if platform == 'youtube' or (platform == 'auto' and not self._is_spotify_running()):
            return self.play_youtube(query)
        elif platform == 'spotify' or (platform == 'auto' and self._is_spotify_running()):
            return self.play_spotify(query)
        else:
            return self.play_youtube(query)
    
    def _is_spotify_running(self) -> bool:
        """Check if Spotify is running"""
        try:
            result = subprocess.run(['pgrep', '-x', 'Spotify'], capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def pause(self) -> Dict[str, Any]:
        """Pause current playback"""
        try:
            # Send media key pause
            subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 16'], 
                         capture_output=True)
            
            self.is_playing = False
            self._save_state()
            
            return {'success': True, 'message': 'Paused'}
        except Exception as e:
            return {'success': False, 'message': f'Error pausing: {str(e)}'}
    
    def resume(self) -> Dict[str, Any]:
        """Resume playback"""
        try:
            # Send media key play
            subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 16'], 
                         capture_output=True)
            
            self.is_playing = True
            self._save_state()
            
            return {'success': True, 'message': 'Resumed'}
        except Exception as e:
            return {'success': False, 'message': f'Error resuming: {str(e)}'}
    
    def next_track(self) -> Dict[str, Any]:
        """Skip to next track"""
        try:
            subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 17'], 
                         capture_output=True)
            return {'success': True, 'message': 'Next track'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def previous_track(self) -> Dict[str, Any]:
        """Go to previous track"""
        try:
            subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 20'], 
                         capture_output=True)
            return {'success': True, 'message': 'Previous track'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def volume_up(self) -> Dict[str, Any]:
        """Increase volume"""
        try:
            self.volume = min(100, self.volume + 10)
            subprocess.run(['osascript', '-e', f'set volume output volume {self.volume}'])
            self._save_state()
            return {'success': True, 'message': f'Volume: {self.volume}%', 'volume': self.volume}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def volume_down(self) -> Dict[str, Any]:
        """Decrease volume"""
        try:
            self.volume = max(0, self.volume - 10)
            subprocess.run(['osascript', '-e', f'set volume output volume {self.volume}'])
            self._save_state()
            return {'success': True, 'message': f'Volume: {self.volume}%', 'volume': self.volume}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def set_volume(self, level: int) -> Dict[str, Any]:
        """Set volume to specific level"""
        try:
            self.volume = max(0, min(100, level))
            subprocess.run(['osascript', '-e', f'set volume output volume {self.volume}'])
            self._save_state()
            return {'success': True, 'message': f'Volume set to {self.volume}%', 'volume': self.volume}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def mute(self) -> Dict[str, Any]:
        """Mute audio"""
        try:
            subprocess.run(['osascript', '-e', 'set volume with output muted'])
            return {'success': True, 'message': 'Muted'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def unmute(self) -> Dict[str, Any]:
        """Unmute audio"""
        try:
            subprocess.run(['osascript', '-e', 'set volume without output muted'])
            return {'success': True, 'message': 'Unmuted'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_status(self) -> Dict[str, Any]:
        """Get current media status"""
        return {
            'platform': self.current_platform,
            'song': self.current_song,
            'is_playing': self.is_playing,
            'volume': self.volume
        }
    
    def stop_all(self) -> Dict[str, Any]:
        """Stop all media playback"""
        try:
            # Pause any playing media
            subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 16'], 
                         capture_output=True)
            
            self.is_playing = False
            self.current_song = None
            self._save_state()
            
            return {'success': True, 'message': 'All media stopped'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def play_pause_toggle(self) -> Dict[str, Any]:
        """Toggle play/pause"""
        if self.is_playing:
            return self.pause()
        else:
            return self.resume()


# Create global instance
media_controller = MediaController()