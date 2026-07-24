"""
Account Manager - Manages user accounts with browser automation
"""
import json
import time
from pathlib import Path
from datetime import datetime
import webbrowser

class AccountManager:
    """Manages user accounts - login, logout, status"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.memory_dir = self.base_dir / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.accounts_file = self.memory_dir / "user_accounts.json"
        self.accounts = self._load_accounts()
        self.browser = None
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        import logging
        logger = logging.getLogger("AccountManager")
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            logger.propagate = False
        return logger
    
    def _load_accounts(self) -> dict:
        if self.accounts_file.exists():
            try:
                with open(self.accounts_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {"accounts": {}, "last_updated": None}
        return {"accounts": {}, "last_updated": None}
    
    def _save_accounts(self):
        try:
            self.accounts["last_updated"] = datetime.now().isoformat()
            with open(self.accounts_file, 'w') as f:
                json.dump(self.accounts, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save accounts: {e}")
    
    def add_account(self, platform: str, username: str, url: str = None) -> dict:
        """Add an account to track"""
        platform = platform.lower()
        
        default_urls = {
            "facebook": "https://facebook.com",
            "instagram": "https://instagram.com",
            "twitter": "https://twitter.com",
            "x": "https://x.com",
            "youtube": "https://youtube.com",
            "gmail": "https://mail.google.com",
            "google": "https://google.com",
            "github": "https://github.com",
            "linkedin": "https://linkedin.com",
            "tiktok": "https://tiktok.com",
            "reddit": "https://reddit.com",
            "discord": "https://discord.com",
            "slack": "https://slack.com",
            "notion": "https://notion.so",
            "netflix": "https://netflix.com",
            "spotify": "https://spotify.com",
            "amazon": "https://amazon.com",
            "ebay": "https://ebay.com",
            "fiverr": "https://fiverr.com",
            "upwork": "https://upwork.com"
        }
        
        if not url:
            url = default_urls.get(platform, f"https://{platform}.com")
        
        self.accounts["accounts"][platform] = {
            "username": username,
            "url": url,
            "added_at": datetime.now().isoformat(),
            "last_accessed": None,
            "status": "active"
        }
        
        self._save_accounts()
        
        return {
            "success": True,
            "message": f"Account added: {platform} ({username})",
            "platform": platform
        }
    
    def remove_account(self, platform: str) -> dict:
        """Remove an account"""
        platform = platform.lower()
        
        if platform in self.accounts["accounts"]:
            del self.accounts["accounts"][platform]
            self._save_accounts()
            return {"success": True, "message": f"Account removed: {platform}"}
        
        return {"success": False, "message": f"Account not found: {platform}"}
    
    def open_account(self, platform: str) -> dict:
        """Open account in browser"""
        platform = platform.lower()
        
        if platform in self.accounts["accounts"]:
            account = self.accounts["accounts"][platform]
            url = account.get("url", f"https://{platform}.com")
            
            try:
                webbrowser.open(url)
                
                account["last_accessed"] = datetime.now().isoformat()
                self._save_accounts()
                
                return {
                    "success": True,
                    "message": f"Opening {platform}",
                    "url": url,
                    "username": account.get("username", "")
                }
            except Exception as e:
                return {"success": False, "message": str(e)}
        
        return {"success": False, "message": f"Account not found: {platform}"}
    
    def get_accounts(self) -> dict:
        """List all accounts"""
        accounts = self.accounts.get("accounts", {})
        
        if not accounts:
            return {"success": True, "message": "No accounts saved", "accounts": []}
        
        account_list = []
        for platform, data in accounts.items():
            account_list.append({
                "platform": platform,
                "username": data.get("username", ""),
                "url": data.get("url", ""),
                "status": data.get("status", "active"),
                "last_accessed": data.get("last_accessed", "Never")
            })
        
        return {
            "success": True,
            "accounts": account_list,
            "count": len(account_list)
        }
    
    def get_account_status(self, platform: str) -> dict:
        """Get status of a specific account"""
        platform = platform.lower()
        
        if platform in self.accounts["accounts"]:
            account = self.accounts["accounts"][platform]
            return {
                "success": True,
                "platform": platform,
                "username": account.get("username", ""),
                "status": account.get("status", "active"),
                "url": account.get("url", ""),
                "last_accessed": account.get("last_accessed", "Never")
            }
        
        return {"success": False, "message": f"Account not found: {platform}"}
    
    def search_accounts(self, query: str) -> dict:
        """Search accounts by platform name"""
        results = []
        for platform, data in self.accounts.get("accounts", {}).items():
            if query.lower() in platform.lower():
                results.append({
                    "platform": platform,
                    "username": data.get("username", ""),
                    "url": data.get("url", "")
                })
        
        return {
            "success": True,
            "results": results,
            "count": len(results)
        }


account_manager = AccountManager()
