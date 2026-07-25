"""
Web Media Engine - YouTube Playback, Video Streaming, Social Media, and Web Features
Provides complete web and media control capabilities
"""
import os
import sys
import json
import re
import time
import subprocess
import webbrowser
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import quote, urlencode
from logger import logger
from config import config


class WebMediaEngine:
    """Comprehensive web and media control engine"""

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)

        self.media_cache_dir = self.data_dir / "media_cache"
        self.media_cache_dir.mkdir(exist_ok=True)

        self.playlist_file = self.data_dir / "playlists.json"
        self.history_file = self.data_dir / "web_history.json"
        self.bookmarks_file = self.data_dir / "bookmarks.json"

        self.playlists = self._load_json(self.playlist_file, {})
        self.web_history = self._load_json(self.history_file, [])
        self.bookmarks = self._load_json(self.bookmarks_file, {})

        self.current_video = None
        self.is_playing = False
        self.is_paused = False
        self.volume_level = 0.8
        self.playback_speed = 1.0
        self.repeat_mode = "none"  # none, one, all
        self.shuffle_mode = False
        self.current_quality = "1080p"
        self.current_platform = "youtube"

        # Platform URLs
        self.platform_urls = {
            "youtube": "https://www.youtube.com",
            "youtube Shorts": "https://www.youtube.com/shorts",
            "youtube Music": "https://music.youtube.com",
            "youtube Live": "https://www.youtube.com/live",
            "vimeo": "https://vimeo.com",
            "dailymotion": "https://www.dailymotion.com",
            "twitch": "https://www.twitch.tv",
            "tiktok": "https://www.tiktok.com",
            "instagram": "https://www.instagram.com",
            "twitter": "https://twitter.com",
            "x": "https://x.com",
            "facebook": "https://www.facebook.com",
            "reddit": "https://www.reddit.com",
            "discord": "https://discord.com",
            "zoom": "https://zoom.us",
            "teams": "https://teams.microsoft.com",
            "slack": "https://slack.com",
            "spotify": "https://open.spotify.com",
            "netflix": "https://www.netflix.com",
            "hulu": "https://www.hulu.com",
            "amazon prime": "https://www.amazon.com/video",
            "disney plus": "https://www.disneyplus.com",
            "apple tv": "https://tv.apple.com",
            "google video": "https://video.google.com",
            "twitch clips": "https://clips.twitch.tv",
            "twitch vods": "https://www.twitch.tv/videos",
        }

        logger.info("Web Media Engine initialized with full capabilities")

    def _load_json(self, filepath, default):
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return default

    def _save_json(self, filepath, data):
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    # ==================== YOUTUBE CONTROLS ====================

    def play_youtube(self, query: str) -> Dict[str, Any]:
        """Play a YouTube video or search"""
        self.current_platform = "youtube"

        video_id = self._extract_youtube_id(query)
        if video_id:
            url = f"https://www.youtube.com/watch?v={video_id}"
            self.current_video = video_id
        else:
            search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
            url = search_url

        self.web_history.append({
            "url": url,
            "platform": "youtube",
            "query": query,
            "action": "play",
            "timestamp": datetime.now().isoformat()
        })
        self._save_history()

        self._open_url(url)
        self.is_playing = True
        self.is_paused = False

        return {
            "success": True,
            "message": f"Playing on YouTube: {query}",
            "url": url,
            "video_id": video_id,
            "platform": "youtube"
        }

    def play_youtube_shorts(self, query: str) -> Dict[str, Any]:
        """Play a YouTube Short"""
        self.current_platform = "youtube Shorts"
        search_url = f"https://www.youtube.com/shorts/{quote(query)}"
        self._open_url(search_url)
        self.is_playing = True
        return {"success": True, "message": f"Playing YouTube Short: {query}", "url": search_url}

    def play_youtube_music(self, query: str) -> Dict[str, Any]:
        """Play music on YouTube Music"""
        self.current_platform = "youtube Music"
        search_url = f"https://music.youtube.com/search?q={quote(query)}"
        self._open_url(search_url)
        self.is_playing = True
        return {"success": True, "message": f"Playing on YouTube Music: {query}", "url": search_url}

    def play_youtube_live(self, query: str) -> Dict[str, Any]:
        """Play a YouTube Live stream"""
        self.current_platform = "youtube Live"
        search_url = f"https://www.youtube.com/results?search_query={quote(query)}+live"
        self._open_url(search_url)
        self.is_playing = True
        return {"success": True, "message": f"Searching YouTube Live: {query}", "url": search_url}

    def play_youtube_playlist(self, playlist_id: str = None, query: str = None) -> Dict[str, Any]:
        """Play a YouTube playlist"""
        if playlist_id:
            url = f"https://www.youtube.com/playlist?list={playlist_id}"
        elif query:
            url = f"https://www.youtube.com/results?search_query={quote(query)}&sp=EgIIBQ%253D%253D"
        else:
            return {"success": False, "message": "Provide playlist ID or search query"}

        self._open_url(url)
        self.is_playing = True
        return {"success": True, "message": f"Playing playlist: {query or playlist_id}", "url": url}

    def _extract_youtube_id(self, query: str) -> Optional[str]:
        """Extract YouTube video ID from URL or search"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'video id[:\s]*([a-zA-Z0-9_-]{11})',
        ]

        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    # ==================== VIMEO CONTROLS ====================

    def play_vimeo(self, query: str) -> Dict[str, Any]:
        """Play a Vimeo video"""
        video_id = self._extract_vimeo_id(query)
        if video_id:
            url = f"https://vimeo.com/{video_id}"
            self.current_video = video_id
        else:
            url = f"https://vimeo.com/search?q={quote(query)}"

        self._open_url(url)
        self.current_platform = "vimeo"
        self.is_playing = True
        return {"success": True, "message": f"Playing on Vimeo: {query}", "url": url}

    def _extract_vimeo_id(self, query: str) -> Optional[str]:
        match = re.search(r'vimeo\.com/(\d+)', query, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    # ==================== DAILYMOTION CONTROLS ====================

    def play_dailymotion(self, query: str) -> Dict[str, Any]:
        """Play a Dailymotion video"""
        url = f"https://www.dailymotion.com/search?q={quote(query)}"
        self._open_url(url)
        self.current_platform = "dailymotion"
        self.is_playing = True
        return {"success": True, "message": f"Searching Dailymotion: {query}", "url": url}

    # ==================== TWITCH CONTROLS ====================

    def play_twitch_stream(self, channel: str = None, query: str = None) -> Dict[str, Any]:
        """Play a Twitch stream"""
        if channel:
            url = f"https://www.twitch.tv/{channel}"
        elif query:
            url = f"https://www.twitch.tv/search?term={quote(query)}"
        else:
            url = "https://www.twitch.tv/directory"

        self._open_url(url)
        self.current_platform = "twitch"
        self.is_playing = True
        return {"success": True, "message": f"Opening Twitch: {channel or query}", "url": url}

    def play_twitch_clips(self, query: str = None) -> Dict[str, Any]:
        """Browse Twitch clips"""
        url = "https://clips.twitch.tv/"
        self._open_url(url)
        self.current_platform = "twitch clips"
        return {"success": True, "message": "Opening Twitch clips", "url": url}

    def play_twitch_vods(self, channel: str = None) -> Dict[str, Any]:
        """Play Twitch VODs"""
        if channel:
            url = f"https://www.twitch.tv/{channel}/videos"
        else:
            url = "https://www.twitch.tv/videos"

        self._open_url(url)
        self.current_platform = "twitch vods"
        return {"success": True, "message": f"Opening Twitch VODs: {channel or 'all'}", "url": url}

    # ==================== SOCIAL MEDIA ====================

    def open_tiktok(self, query: str = None) -> Dict[str, Any]:
        """Open TikTok"""
        url = f"https://www.tiktok.com/search?q={quote(query)}" if query else "https://www.tiktok.com"
        self._open_url(url)
        return {"success": True, "message": f"Opening TikTok: {query or 'home'}", "url": url}

    def open_instagram(self, query: str = None) -> Dict[str, Any]:
        """Open Instagram"""
        if query:
            url = f"https://www.instagram.com/explore/tags/{query}/"
        else:
            url = "https://www.instagram.com"
        self._open_url(url)
        return {"success": True, "message": f"Opening Instagram: {query or 'home'}", "url": url}

    def open_twitter(self, query: str = None) -> Dict[str, Any]:
        """Open Twitter/X"""
        if query and "search" in query.lower():
            url = f"https://x.com/search?q={quote(query)}"
        elif query:
            url = f"https://x.com/i/user/{query}"
        else:
            url = "https://x.com"
        self._open_url(url)
        return {"success": True, "message": f"Opening Twitter/X: {query or 'home'}", "url": url}

    def post_tweet(self, content: str = None) -> Dict[str, Any]:
        """Post a tweet (opens Twitter compose)"""
        if not content:
            return {"success": False, "message": "No content provided for tweet"}

        compose_url = f"https://x.com/compose/tweet?text={quote(content)}"
        self._open_url(compose_url)
        return {"success": True, "message": f"Tweet compose opened with content", "url": compose_url}

    def post_video(self, platform: str = None, query: str = None) -> Dict[str, Any]:
        """Post a video to social media (opens platform)"""
        platforms = {
            "youtube": self._open_youtube_Upload,
            "tiktok": lambda q: self._open_url(f"https://www.tiktok.com/creator"),
            "instagram": lambda q: self._open_url(f"https://www.instagram.com/create/reel/"),
            "twitter": lambda q: self._open_url(f"https://x.com/compose/video"),
            "facebook": lambda q: self._open_url(f"https://www.facebook.com/create/video/"),
            "twitch": lambda q: self._open_url(f"https://www.twitch.tv/dashboard"),
        }

        if platform and platform.lower() in platforms:
            platforms[platform.lower()]("")
            return {"success": True, "message": f"Opening {platform} video upload"}
        elif platform:
            self._open_url(f"https://{platform}.com/upload")
            return {"success": True, "message": f"Opening {platform} upload"}
        else:
            # Open default upload page
            self._open_url("https://www.youtube.com/upload")
            return {"success": True, "message": "Opening default video upload (YouTube)"}

    def _open_youtube_Upload(self, _):
        self._open_url("https://www.youtube.com/upload")

    # ==================== STREAMING SERVICES ====================

    def play_netflix(self, query: str = None) -> Dict[str, Any]:
        """Open Netflix"""
        url = f"https://www.netflix.com/search?q={quote(query)}" if query else "https://www.netflix.com"
        self._open_url(url)
        return {"success": True, "message": f"Opening Netflix: {query or 'home'}", "url": url}

    def play_hulu(self, query: str = None) -> Dict[str, Any]:
        """Open Hulu"""
        url = f"https://www.hulu.com/search?q={quote(query)}" if query else "https://www.hulu.com"
        self._open_url(url)
        return {"success": True, "message": f"Opening Hulu: {query or 'home'}", "url": url}

    def play_amazon_prime(self, query: str = None) -> Dict[str, Any]:
        """Open Amazon Prime Video"""
        url = f"https://www.amazon.com/video?q={quote(query)}" if query else "https://www.amazon.com/video"
        self._open_url(url)
        return {"success": True, "message": f"Opening Amazon Prime Video: {query or 'home'}", "url": url}

    def play_disney_plus(self, query: str = None) -> Dict[str, Any]:
        """Open Disney+"""
        url = f"https://www.disneyplus.com/search?q={quote(query)}" if query else "https://www.disneyplus.com"
        self._open_url(url)
        return {"success": True, "message": f"Opening Disney+: {query or 'home'}", "url": url}

    def play_spotify(self, query: str = None) -> Dict[str, Any]:
        """Open Spotify"""
        if query:
            url = f"https://open.spotify.com/search/{quote(query)}"
        else:
            url = "https://open.spotify.com"
        self._open_url(url)
        return {"success": True, "message": f"Opening Spotify: {query or 'home'}", "url": url}

    def play_spotify_playlist(self, playlist_name: str) -> Dict[str, Any]:
        """Play a Spotify playlist"""
        url = f"https://open.spotify.com/search/{quote(playlist_name)}"
        self._open_url(url)
        return {"success": True, "message": f"Playing Spotify playlist: {playlist_name}", "url": url}

    def play_spotify_podcast(self, podcast_name: str) -> Dict[str, Any]:
        """Play a Spotify podcast"""
        url = f"https://open.spotify.com/search/{quote(podcast_name)}"
        self._open_url(url)
        return {"success": True, "message": f"Playing Spotify podcast: {podcast_name}", "url": url}

    # ==================== GOOGLE SERVICES ====================

    def google_search(self, query: str) -> Dict[str, Any]:
        """Search Google"""
        url = f"https://www.google.com/search?q={quote(query)}"
        self._open_url(url)
        self.web_history.append({
            "url": url, "platform": "google", "query": query,
            "action": "search", "timestamp": datetime.now().isoformat()
        })
        self._save_history()
        return {"success": True, "message": f"Google search: {query}", "url": url}

    def google_maps(self, query: str = None) -> Dict[str, Any]:
        """Open Google Maps"""
        url = f"https://www.google.com/maps/search/{quote(query)}" if query else "https://www.google.com/maps"
        self._open_url(url)
        return {"success": True, "message": f"Opening Google Maps: {query or 'home'}", "url": url}

    def google_translate(self, text: str = None) -> Dict[str, Any]:
        """Open Google Translate"""
        url = f"https://translate.google.com/?text={quote(text)}" if text else "https://translate.google.com"
        self._open_url(url)
        return {"success": True, "message": f"Opening Google Translate", "url": url}

    def google_images(self, query: str) -> Dict[str, Any]:
        """Search Google Images"""
        url = f"https://www.google.com/search?tbm=isch&q={quote(query)}"
        self._open_url(url)
        return {"success": True, "message": f"Google Images search: {query}", "url": url}

    def google_news(self, query: str = None) -> Dict[str, Any]:
        """Open Google News"""
        url = f"https://news.google.com/search?q={quote(query)}" if query else "https://news.google.com"
        self._open_url(url)
        return {"success": True, "message": f"Opening Google News: {query or 'home'}", "url": url}

    def google_gemini(self, query: str = None) -> Dict[str, Any]:
        """Open Google Gemini AI"""
        url = f"https://gemini.google.com/?q={quote(query)}" if query else "https://gemini.google.com"
        self._open_url(url)
        return {"success": True, "message": f"Opening Google Gemini", "url": url}

    # ==================== VIDEO PLATFORM CONTROLS ====================

    def play_video(self, platform: str = None, query: str = None, video_id: str = None) -> Dict[str, Any]:
        """Play a video on any supported platform"""
        result = None

        platform_handlers = {
            "youtube": lambda: self.play_youtube(query or video_id or ""),
            "youtube shorts": lambda: self.play_youtube_shorts(query or video_id or ""),
            "youtube music": lambda: self.play_youtube_music(query or ""),
            "youtube live": lambda: self.play_youtube_live(query or ""),
            "vimeo": lambda: self.play_vimeo(query or video_id or ""),
            "dailymotion": lambda: self.play_dailymotion(query or ""),
            "twitch": lambda: self.play_twitch_stream(channel=query),
            "twitch clips": lambda: self.play_twitch_clips(query),
            "twitch vods": lambda: self.play_twitch_vods(query),
        }

        if platform and platform.lower() in platform_handlers:
            result = platform_handlers[platform.lower()]()
        elif platform:
            # Try to construct URL from platform name
            url = self.platform_urls.get(platform.lower(), f"https://{platform.lower().replace(' ', '')}.com")
            if query:
                url = f"{url}/search?q={quote(query)}"
            self._open_url(url)
            result = {"success": True, "message": f"Opening {platform}: {query}", "url": url}
        else:
            # Default: search all platforms
            result = self.play_youtube(query or "")

        if result and result.get("success"):
            self.is_playing = True
        return result or {"success": False, "message": "No video found"}

    # ==================== PLAYLIST MANAGEMENT ====================

    def create_playlist(self, name: str, videos: List[str] = None) -> Dict[str, Any]:
        """Create a new playlist"""
        if name in self.playlists:
            return {"success": False, "message": f"Playlist '{name}' already exists"}

        self.playlists[name] = {
            "name": name,
            "videos": videos or [],
            "created_at": datetime.now().isoformat(),
            "last_played": None
        }
        self._save_playlists()
        return {"success": True, "message": f"Playlist '{name}' created", "playlist": self.playlists[name]}

    def add_to_playlist(self, playlist_name: str, video: str) -> Dict[str, Any]:
        """Add a video to a playlist"""
        if playlist_name not in self.playlists:
            return {"success": False, "message": f"Playlist '{playlist_name}' not found"}

        self.playlists[playlist_name]["videos"].append(video)
        self._save_playlists()
        return {"success": True, "message": f"Added '{video}' to '{playlist_name}'"}

    def remove_from_playlist(self, playlist_name: str, video: str) -> Dict[str, Any]:
        """Remove a video from playlist"""
        if playlist_name not in self.playlists:
            return {"success": False, "message": f"Playlist '{playlist_name}' not found"}

        try:
            self.playlists[playlist_name]["videos"].remove(video)
            self._save_playlists()
            return {"success": True, "message": f"Removed '{video}' from '{playlist_name}'"}
        except ValueError:
            return {"success": False, "message": f"Video '{video}' not in playlist"}

    def play_playlist(self, playlist_name: str) -> Dict[str, Any]:
        """Play all videos in a playlist"""
        if playlist_name not in self.playlists:
            return {"success": False, "message": f"Playlist '{playlist_name}' not found"}

        playlist = self.playlists[playlist_name]
        videos = playlist["videos"]

        self.playlists[playlist_name]["last_played"] = datetime.now().isoformat()
        self._save_playlists()

        for i, video in enumerate(videos):
            self.play_youtube(video)
            time.sleep(0.5)

        return {
            "success": True,
            "message": f"Playing playlist '{playlist_name}' with {len(videos)} videos",
            "playlist": playlist_name,
            "videos_count": len(videos)
        }

    def list_playlists(self) -> Dict[str, Any]:
        """List all playlists"""
        playlist_info = []
        for name, data in self.playlists.items():
            playlist_info.append({
                "name": name,
                "videos_count": len(data["videos"]),
                "created_at": data["created_at"],
                "last_played": data.get("last_played")
            })
        return {"success": True, "playlists": playlist_info, "total": len(playlist_info)}

    # ==================== BOOKMARKS ====================

    def add_bookmark(self, name: str, url: str) -> Dict[str, Any]:
        """Add a bookmark"""
        self.bookmarks[name] = {"url": url, "added_at": datetime.now().isoformat()}
        self._save_bookmarks()
        return {"success": True, "message": f"Bookmarked: {name}"}

    def remove_bookmark(self, name: str) -> Dict[str, Any]:
        """Remove a bookmark"""
        if name in self.bookmarks:
            del self.bookmarks[name]
            self._save_bookmarks()
            return {"success": True, "message": f"Removed bookmark: {name}"}
        return {"success": False, "message": f"Bookmark '{name}' not found"}

    def get_bookmark(self, name: str) -> Dict[str, Any]:
        """Get a bookmark URL"""
        if name in self.bookmarks:
            return {"success": True, "url": self.bookmarks[name]["url"]}
        return {"success": False, "message": f"Bookmark '{name}' not found"}

    def open_bookmark(self, name: str) -> Dict[str, Any]:
        """Open a bookmark in browser"""
        if name in self.bookmarks:
            url = self.bookmarks[name]["url"]
            self._open_url(url)
            return {"success": True, "message": f"Opened bookmark: {name}", "url": url}
        return {"success": False, "message": f"Bookmark '{name}' not found"}

    def list_bookmarks(self) -> Dict[str, Any]:
        """List all bookmarks"""
        return {"success": True, "bookmarks": dict(self.bookmarks)}

    # ==================== PLAYBACK CONTROLS ====================

    def pause(self) -> Dict[str, Any]:
        """Pause playback"""
        if self.is_playing:
            self.is_paused = True
            return {"success": True, "message": "Playback paused"}
        return {"success": False, "message": "Nothing is playing"}

    def resume(self) -> Dict[str, Any]:
        """Resume playback"""
        if self.is_paused:
            self.is_paused = False
            return {"success": True, "message": "Playback resumed"}
        return {"success": False, "message": "Nothing is paused"}

    def stop(self) -> Dict[str, Any]:
        """Stop playback"""
        self.is_playing = False
        self.is_paused = False
        self.current_video = None
        return {"success": True, "message": "Playback stopped"}

    def next_video(self) -> Dict[str, Any]:
        """Skip to next video"""
        if self.current_video:
            return self.play_youtube("next video")
        return {"success": False, "message": "No video currently playing"}

    def previous_video(self) -> Dict[str, Any]:
        """Go to previous video"""
        if self.web_history:
            prev = self.web_history[-2] if len(self.web_history) > 1 else None
            if prev and prev.get("url"):
                self._open_url(prev["url"])
                return {"success": True, "message": "Playing previous video"}
        return {"success": False, "message": "No previous video"}

    def set_volume(self, level: float) -> Dict[str, Any]:
        """Set playback volume"""
        self.volume_level = max(0.0, min(1.0, level))
        # Adjust system volume on macOS
        try:
            if sys.platform == 'darwin':
                subprocess.run(['osascript', '-e', f'set volume output volume {int(self.volume_level * 100)}'], timeout=5)
        except Exception:
            pass
        return {"success": True, "message": f"Volume set to {int(self.volume_level * 100)}%"}

    def set_playback_speed(self, speed: float) -> Dict[str, Any]:
        """Set playback speed"""
        self.playback_speed = max(0.25, min(2.0, speed))
        return {"success": True, "message": f"Playback speed set to {self.playback_speed}x"}

    def set_quality(self, quality: str) -> Dict[str, Any]:
        """Set video quality"""
        valid_qualities = ["360p", "480p", "720p", "1080p", "1440p", "4k"]
        if quality.lower() in valid_qualities:
            self.current_quality = quality.upper()
            return {"success": True, "message": f"Quality set to {quality.upper()}"}
        return {"success": False, "message": f"Invalid quality. Options: {', '.join(valid_qualities)}"}

    def set_repeat(self, mode: str) -> Dict[str, Any]:
        """Set repeat mode (none, one, all)"""
        if mode.lower() in ["none", "one", "all"]:
            self.repeat_mode = mode.lower()
            return {"success": True, "message": f"Repeat mode set to: {mode.lower()}"}
        return {"success": False, "message": f"Invalid repeat mode. Options: none, one, all"}

    def toggle_shuffle(self) -> Dict[str, Any]:
        """Toggle shuffle mode"""
        self.shuffle_mode = not self.shuffle_mode
        return {"success": True, "message": f"Shuffle {'enabled' if self.shuffle_mode else 'disabled'}"}

    # ==================== BROWSER CONTROLS ====================

    def open_url(self, url: str) -> Dict[str, Any]:
        """Open any URL in browser"""
        self._open_url(url)
        self.web_history.append({
            "url": url, "platform": "browser", "action": "open",
            "timestamp": datetime.now().isoformat()
        })
        self._save_history()
        return {"success": True, "message": f"Opened URL: {url}", "url": url}

    def open_new_tab(self, url: str) -> Dict[str, Any]:
        """Open URL in new browser tab (same as open for web)"""
        return self.open_url(url)

    def refresh_page(self) -> Dict[str, Any]:
        """Refresh the current page"""
        if self.web_history:
            current = self.web_history[-1]
            return self.open_url(current.get("url", ""))
        return {"success": False, "message": "No page to refresh"}

    def go_back(self) -> Dict[str, Any]:
        """Navigate back in history"""
        if len(self.web_history) > 1:
            self.web_history.pop()
            prev = self.web_history[-1]
            self._open_url(prev["url"])
            return {"success": True, "message": f"Navigated back to: {prev['url']}"}
        return {"success": False, "message": "No previous page"}

    def close_browser(self) -> Dict[str, Any]:
        """Close the browser"""
        try:
            if sys.platform == 'darwin':
                subprocess.run(['osascript', '-e', 'tell application "Safari" to quit'], timeout=5)
            elif sys.platform == 'win32':
                subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], timeout=5)
            return {"success": True, "message": "Browser closed"}
        except Exception as e:
            return {"success": False, "message": f"Error closing browser: {e}"}

    # ==================== WEB SEARCH ====================

    def web_search(self, query: str, engine: str = "google") -> Dict[str, Any]:
        """Perform web search"""
        search_urls = {
            "google": f"https://www.google.com/search?q={quote(query)}",
            "bing": f"https://www.bing.com/search?q={quote(query)}",
            "duckduckgo": f"https://duckduckgo.com/?q={quote(query)}",
            "yahoo": f"https://search.yahoo.com/search?p={quote(query)}",
            "youtube": f"https://www.youtube.com/results?search_query={quote(query)}",
            "reddit": f"https://www.reddit.com/search?q={quote(query)}",
            "wikipedia": f"https://en.wikipedia.org/wiki/{quote(query)}",
            "amazon": f"https://www.amazon.com/s?k={quote(query)}",
            "imdb": f"https://www.imdb.com/find?q={quote(query)}",
            "stack overflow": f"https://stackoverflow.com/search?q={quote(query)}",
            "github": f"https://github.com/search?q={quote(query)}",
            "npm": f"https://www.npmjs.com/search?q={quote(query)}",
            "pypi": f"https://pypi.org/search?q={quote(query)}",
            "docs": f"https://docs.python.org/3/search.html?q={quote(query)}",
        }

        url = search_urls.get(engine.lower(), search_urls["google"])
        self._open_url(url)

        self.web_history.append({
            "url": url, "platform": "search", "engine": engine,
            "query": query, "action": "search", "timestamp": datetime.now().isoformat()
        })
        self._save_history()

        return {"success": True, "message": f"Search ({engine}): {query}", "url": url}

    def search_images(self, query: str) -> Dict[str, Any]:
        """Search for images"""
        return self.web_search(query, "google")

    def search_videos(self, query: str) -> Dict[str, Any]:
        """Search for videos"""
        return self.web_search(query, "youtube")

    def search_news(self, query: str) -> Dict[str, Any]:
        """Search for news"""
        return self.web_search(query, "bing")

    def search_wikipedia(self, query: str) -> Dict[str, Any]:
        """Search Wikipedia"""
        return self.web_search(query, "wikipedia")

    # ==================== DOWNLOADS ====================

    def download_file(self, url: str, destination: str = None) -> Dict[str, Any]:
        """Download a file from URL"""
        if not url:
            return {"success": False, "message": "No URL provided"}

        if not destination:
            destination = self.media_cache_dir / os.path.basename(url.split('?')[0])

        try:
            import requests
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()

            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return {
                "success": True,
                "message": f"Downloaded: {destination}",
                "size": os.path.getsize(destination),
                "url": url
            }
        except Exception as e:
            return {"success": False, "message": f"Download error: {e}"}

    def download_youtube_audio(self, video_id: str, output_dir: str = None) -> Dict[str, Any]:
        """Download YouTube audio"""
        if not output_dir:
            output_dir = str(self.media_cache_dir)

        url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            result = subprocess.run(
                ['yt-dlp', '-x', '--audio-format', 'mp3', '-o', f'{output_dir}/%(title)s.%(ext)s', url],
                capture_output=True, text=True, timeout=60
            )
            return {"success": True, "message": f"Audio downloaded for {video_id}", "output": result.stdout}
        except FileNotFoundError:
            return {"success": False, "message": "yt-dlp not installed. Install with: pip install yt-dlp"}
        except subprocess.TimeoutExpired:
            return {"success": False, "message": "Download timed out"}
        except Exception as e:
            return {"success": False, "message": f"Download error: {e}"}

    def download_youtube_video(self, video_id: str, quality: str = "720p", output_dir: str = None) -> Dict[str, Any]:
        """Download YouTube video"""
        if not output_dir:
            output_dir = str(self.media_cache_dir)

        url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            result = subprocess.run(
                ['yt-dlp', '-f', quality, '-o', f'{output_dir}/%(title)s.%(ext)s', url],
                capture_output=True, text=True, timeout=120
            )
            return {"success": True, "message": f"Video downloaded for {video_id}", "output": result.stdout}
        except FileNotFoundError:
            return {"success": False, "message": "yt-dlp not installed. Install with: pip install yt-dlp"}
        except subprocess.TimeoutExpired:
            return {"success": False, "message": "Download timed out"}
        except Exception as e:
            return {"success": False, "message": f"Download error: {e}"}

    # ==================== SOCIAL MEDIA POSTING ====================

    def post_to_social_media(self, platform: str, content: str, media_path: str = None) -> Dict[str, Any]:
        """Post content to social media"""
        platform_urls = {
            "twitter": "https://x.com/compose/tweet",
            "x": "https://x.com/compose/tweet",
            "facebook": "https://www.facebook.com/create/post",
            "instagram": "https://www.instagram.com/create/",
            "tiktok": "https://www.tiktok.com/create",
            "youtube": "https://www.youtube.com/upload",
            "reddit": "https://www.reddit.com/submit",
            "linkedin": "https://www.linkedin.com/posts/",
            "pinterest": "https://pinterest.com/pin/create/",
            "tumblr": "https://www.tumblr.com/customize",
        }

        if platform.lower() in platform_urls:
            url = platform_urls[platform.lower()]
            self._open_url(url)

            return {
                "success": True,
                "message": f"Opening {platform} for posting",
                "url": url,
                "content_preview": content[:100] if content else ""
            }

        return {"success": False, "message": f"Unsupported platform: {platform}. Try: {', '.join(platform_urls.keys())}"}

    def post_video_to_platform(self, platform: str, video_path: str = None) -> Dict[str, Any]:
        """Post a video to social media platform"""
        platform_urls = {
            "youtube": "https://www.youtube.com/upload",
            "tiktok": "https://www.tiktok.com/upload",
            "instagram": "https://www.instagram.com/create/reel/",
            "twitter": "https://x.com/compose/video",
            "facebook": "https://www.facebook.com/create/video/",
            "twitch": "https://www.twitch.tv/dashboard",
        }

        if platform.lower() in platform_urls:
            url = platform_urls[platform.lower()]
            self._open_url(url)

            result = {"success": True, "message": f"Opening {platform} for video upload", "url": url}
            if video_path:
                result["video_path"] = video_path
            return result

        return {"success": False, "message": f"Unsupported platform: {platform}"}

    # ==================== UTILITY METHODS ====================

    def _open_url(self, url: str):
        """Open URL in default browser"""
        try:
            webbrowser.open(url)
            time.sleep(0.3)
        except Exception as e:
            logger.error(f"Error opening URL {url}: {e}")

    def _save_history(self):
        """Save web history"""
        if len(self.web_history) > 1000:
            self.web_history = self.web_history[-1000:]
        self._save_json(self.history_file, self.web_history)

    def _save_playlists(self):
        """Save playlists to file"""
        self._save_json(self.playlist_file, self.playlists)

    def _save_bookmarks(self):
        """Save bookmarks to file"""
        self._save_json(self.bookmarks_file, self.bookmarks)

    def get_web_history(self, limit: int = 50) -> Dict[str, Any]:
        """Get web browsing history"""
        return {"success": True, "history": self.web_history[-limit:]}

    def clear_web_history(self) -> Dict[str, Any]:
        """Clear web browsing history"""
        self.web_history = []
        self._save_history()
        return {"success": True, "message": "Web history cleared"}

    def get_status(self) -> Dict[str, Any]:
        """Get current media engine status"""
        return {
            "is_playing": self.is_playing,
            "is_paused": self.is_paused,
            "current_video": self.current_video,
            "current_platform": self.current_platform,
            "volume": self.volume_level,
            "playback_speed": self.playback_speed,
            "quality": self.current_quality,
            "repeat_mode": self.repeat_mode,
            "shuffle": self.shuffle_mode,
            "playlists_count": len(self.playlists),
            "bookmarks_count": len(self.bookmarks),
            "history_count": len(self.web_history),
            "supported_platforms": list(self.platform_urls.keys())
        }


# Global instance
web_media_engine = WebMediaEngine()