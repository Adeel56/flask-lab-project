# Backend services for messaging and user management
# Member 1: Backend Lead

import sqlite3
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple

# In-memory message store (resets on app restart)
_messages_store: List[Dict] = []
_message_id_counter = 0


def init_database(db_path: str):
    """Initialize database tables for users only. Messages are stored in memory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Users table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            is_anonymous INTEGER DEFAULT 0,
            avatar TEXT DEFAULT 'default',
            created_at TEXT NOT NULL
        )
        """
    )
    
    conn.commit()
    conn.close()


def get_connection(db_path: str) -> sqlite3.Connection:
    """Get a database connection."""
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def create_user(db_path: str, name: str, is_anonymous: bool = False, avatar: str = 'default') -> Optional[Dict]:
    """Create a new user or return existing."""
    conn = get_connection(db_path)
    created_at = datetime.now(timezone.utc).isoformat()
    
    try:
        # Check if user exists
        existing = conn.execute('SELECT * FROM users WHERE name = ?', (name,)).fetchone()
        if existing:
            conn.close()
            return dict(existing)
        
        # Create new user
        cursor = conn.execute(
            'INSERT INTO users (name, is_anonymous, avatar, created_at) VALUES (?, ?, ?, ?)',
            (name, int(is_anonymous), avatar, created_at)
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None
    except Exception as e:
        conn.close()
        raise e


def get_user_by_id(db_path: str, user_id: int) -> Optional[Dict]:
    """Get user by ID."""
    conn = get_connection(db_path)
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def get_user_by_name(db_path: str, name: str) -> Optional[Dict]:
    """Get user by name."""
    conn = get_connection(db_path)
    user = conn.execute('SELECT * FROM users WHERE name = ?', (name,)).fetchone()
    conn.close()
    return dict(user) if user else None


def update_user_profile(db_path: str, user_id: int, is_anonymous: Optional[bool] = None, avatar: Optional[str] = None) -> Optional[Dict]:
    """Update user profile settings."""
    conn = get_connection(db_path)
    
    updates = []
    params = []
    
    if is_anonymous is not None:
        updates.append('is_anonymous = ?')
        params.append(int(is_anonymous))
    
    if avatar is not None:
        updates.append('avatar = ?')
        params.append(avatar)
    
    if not updates:
        conn.close()
        return get_user_by_id(db_path, user_id)
    
    params.append(user_id)
    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
    
    conn.execute(query, params)
    conn.commit()
    
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def create_message(db_path: str, user_id: int, message: str) -> Optional[Dict]:
    """Create a new message in memory."""
    global _message_id_counter, _messages_store
    
    if not message or len(message) > 500:
        return None
    
    # Get user info from database
    user = get_user_by_id(db_path, user_id)
    if not user:
        return None
    
    _message_id_counter += 1
    created_at = datetime.now(timezone.utc).isoformat()
    
    msg = {
        'id': _message_id_counter,
        'user_id': user_id,
        'message': message,
        'created_at': created_at,
        'name': user['name'],
        'is_anonymous': user['is_anonymous'],
        'avatar': user['avatar']
    }
    
    # Apply anonymous display
    if msg['is_anonymous']:
        msg['display_name'] = 'Anonymous'
    else:
        msg['display_name'] = msg['name']
    
    _messages_store.append(msg)
    return msg


def list_messages(db_path: str, since_id: Optional[int] = None, limit: int = 100) -> List[Dict]:
    """List messages from memory store."""
    global _messages_store
    
    if since_id is not None:
        # Get messages after since_id
        filtered = [msg for msg in _messages_store if msg['id'] > since_id]
        return filtered[:limit]
    else:
        # Get latest messages
        return _messages_store[-limit:] if len(_messages_store) > limit else _messages_store


# Available avatar options
AVATARS = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐸', '🐵', '🐔', '🐧', '🐦', '🦄', '🐝']


def get_available_avatars() -> List[str]:
    """Return list of available avatar emojis."""
    return AVATARS


def clear_all_messages(db_path: str) -> bool:
    """Clear all messages from memory."""
    global _messages_store, _message_id_counter
    try:
        _messages_store = []
        _message_id_counter = 0
        return True
    except Exception as e:
        return False
