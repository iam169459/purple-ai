"""
Purple AI Database - Personal memory and knowledge storage
SQLite database for storing conversations, facts, memories, and learned data
"""
import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

class PurpleDatabase:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.db_path = self.data_dir / "purple_brain.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize database with all required tables"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Conversations table - stores chat history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_message TEXT,
                ai_response TEXT,
                command_type TEXT,
                mood TEXT,
                session_id TEXT
            )
        ''')
        
        # Memories table - important things to remember
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                importance INTEGER DEFAULT 5,
                created_at TEXT NOT NULL,
                last_accessed TEXT,
                access_count INTEGER DEFAULT 0
            )
        ''')
        
        # Facts table - learned knowledge
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                fact TEXT NOT NULL,
                source TEXT DEFAULT 'conversation',
                confidence REAL DEFAULT 1.0,
                created_at TEXT NOT NULL,
                times_used INTEGER DEFAULT 0
            )
        ''')
        
        # User info table - user preferences and profile
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Goals table - tracks goals and progress
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                progress INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                completed_at TEXT
            )
        ''')
        
        # Learned patterns - from conversations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT NOT NULL,
                response TEXT,
                context TEXT,
                success_count INTEGER DEFAULT 1,
                last_used TEXT
            )
        ''')
        
        # Commands history - what commands were used
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                handler TEXT,
                success INTEGER DEFAULT 1,
                timestamp TEXT NOT NULL
            )
        ''')
        
        # Face memories - who the AI knows
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS face_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                first_seen TEXT NOT NULL,
                last_seen TEXT,
                times_seen INTEGER DEFAULT 1,
                notes TEXT
            )
        ''')
        
        # Daily notes - what happened each day
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                note TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                created_at TEXT NOT NULL
            )
        ''')
        
        # Settings table - AI settings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _get_conn(self):
        """Get database connection"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    # Conversation methods
    def save_conversation(self, user_msg: str, ai_response: str, command_type: str = None, mood: str = None):
        """Save a conversation exchange"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (timestamp, user_message, ai_response, command_type, mood)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), user_msg, ai_response, command_type, mood))
        conn.commit()
        conn.close()
    
    def get_conversations(self, limit: int = 50) -> List[Dict]:
        """Get recent conversations"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM conversations ORDER BY id DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def search_conversations(self, query: str) -> List[Dict]:
        """Search conversations"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM conversations 
            WHERE user_message LIKE ? OR ai_response LIKE ?
            ORDER BY id DESC LIMIT 50
        ''', (f'%{query}%', f'%{query}%'))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # Memory methods
    def save_memory(self, key: str, value: str, category: str = 'general', importance: int = 5):
        """Save a memory"""
        conn = self._get_conn()
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT OR REPLACE INTO memories (key, value, category, importance, created_at, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (key, value, category, importance, now, now))
        conn.commit()
        conn.close()
    
    def get_memory(self, key: str) -> Optional[str]:
        """Get a memory by key"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('UPDATE memories SET access_count = access_count + 1, last_accessed = ? WHERE key = ?',
                      (datetime.now().isoformat(), key))
        cursor.execute('SELECT value FROM memories WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        return row['value'] if row else None
    
    def search_memories(self, query: str) -> List[Dict]:
        """Search memories"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM memories 
            WHERE key LIKE ? OR value LIKE ?
            ORDER BY importance DESC, access_count DESC
        ''', (f'%{query}%', f'%{query}%'))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_all_memories(self, category: str = None) -> List[Dict]:
        """Get all memories, optionally filtered by category"""
        conn = self._get_conn()
        cursor = conn.cursor()
        if category:
            cursor.execute('SELECT * FROM memories WHERE category = ? ORDER BY importance DESC', (category,))
        else:
            cursor.execute('SELECT * FROM memories ORDER BY importance DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def delete_memory(self, key: str) -> bool:
        """Delete a memory"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM memories WHERE key = ?', (key,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
    
    # Facts methods
    def save_fact(self, topic: str, fact: str, source: str = 'conversation', confidence: float = 1.0):
        """Save a learned fact"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO facts (topic, fact, source, confidence, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (topic, fact, source, confidence, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_facts(self, topic: str = None) -> List[Dict]:
        """Get facts, optionally filtered by topic"""
        conn = self._get_conn()
        cursor = conn.cursor()
        if topic:
            cursor.execute('SELECT * FROM facts WHERE topic LIKE ? ORDER BY confidence DESC', (f'%{topic}%',))
        else:
            cursor.execute('SELECT * FROM facts ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def search_facts(self, query: str) -> List[Dict]:
        """Search facts"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM facts 
            WHERE topic LIKE ? OR fact LIKE ?
            ORDER BY confidence DESC
        ''', (f'%{query}%', f'%{query}%'))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # User info methods
    def save_user_info(self, key: str, value: str):
        """Save user information"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO user_info (key, value, updated_at)
            VALUES (?, ?, ?)
        ''', (key, value, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_user_info(self, key: str) -> Optional[str]:
        """Get user information"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM user_info WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        return row['value'] if row else None
    
    def get_all_user_info(self) -> Dict[str, str]:
        """Get all user information"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT key, value FROM user_info')
        rows = cursor.fetchall()
        conn.close()
        return {row['key']: row['value'] for row in rows}
    
    # Goals methods
    def save_goal(self, goal: str):
        """Save a goal"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO goals (goal, created_at)
            VALUES (?, ?)
        ''', (goal, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def update_goal_progress(self, goal_id: int, progress: int):
        """Update goal progress"""
        conn = self._get_conn()
        cursor = conn.cursor()
        status = 'completed' if progress >= 100 else 'active'
        completed_at = datetime.now().isoformat() if status == 'completed' else None
        cursor.execute('''
            UPDATE goals SET progress = ?, status = ?, completed_at = ?
            WHERE id = ?
        ''', (progress, status, completed_at, goal_id))
        conn.commit()
        conn.close()
    
    def get_goals(self, status: str = None) -> List[Dict]:
        """Get goals"""
        conn = self._get_conn()
        cursor = conn.cursor()
        if status:
            cursor.execute('SELECT * FROM goals WHERE status = ? ORDER BY created_at DESC', (status,))
        else:
            cursor.execute('SELECT * FROM goals ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # Command history methods
    def save_command(self, command: str, handler: str = None, success: bool = True):
        """Save command to history"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO command_history (command, handler, success, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (command, handler, 1 if success else 0, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_command_stats(self) -> Dict:
        """Get command usage statistics"""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM command_history')
        total = cursor.fetchone()['total']
        
        cursor.execute('SELECT command, COUNT(*) as count FROM command_history GROUP BY command ORDER BY count DESC LIMIT 10')
        popular = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute('SELECT handler, COUNT(*) as count FROM command_history WHERE handler IS NOT NULL GROUP BY handler ORDER BY count DESC LIMIT 10')
        handlers = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return {
            'total_commands': total,
            'popular_commands': popular,
            'handler_usage': handlers
        }
    
    # Daily notes methods
    def save_daily_note(self, note: str, category: str = 'general'):
        """Save a daily note"""
        conn = self._get_conn()
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO daily_notes (date, note, category, created_at)
            VALUES (?, ?, ?, ?)
        ''', (today, note, category, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_daily_notes(self, date: str = None) -> List[Dict]:
        """Get daily notes"""
        conn = self._get_conn()
        cursor = conn.cursor()
        if date:
            cursor.execute('SELECT * FROM daily_notes WHERE date = ? ORDER BY created_at DESC', (date,))
        else:
            cursor.execute('SELECT * FROM daily_notes ORDER BY date DESC, created_at DESC LIMIT 50')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # Settings methods
    def save_setting(self, key: str, value: str):
        """Save a setting"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, updated_at)
            VALUES (?, ?, ?)
        ''', (key, value, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        return row['value'] if row else None
    
    # Statistics
    def get_stats(self) -> Dict:
        """Get database statistics"""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        stats = {}
        
        cursor.execute('SELECT COUNT(*) as count FROM conversations')
        stats['conversations'] = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM memories')
        stats['memories'] = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM facts')
        stats['facts'] = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM goals WHERE status = "active"')
        stats['active_goals'] = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM goals WHERE status = "completed"')
        stats['completed_goals'] = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM daily_notes')
        stats['daily_notes'] = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM command_history')
        stats['commands_run'] = cursor.fetchone()['count']
        
        conn.close()
        return stats
    
    def backup_database(self, backup_path: str = None):
        """Backup database"""
        if not backup_path:
            backup_path = str(self.data_dir / f"purple_brain_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        
        import shutil
        shutil.copy2(str(self.db_path), backup_path)
        return backup_path


# Create global instance
purple_db = PurpleDatabase()