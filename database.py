import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import json
import os

from contextlib import contextmanager

class Database:
    """Database management for file organization system"""
    def __init__(self, db_path: str = "file_organizer.db"):
        self.db_path = db_path
        self._connection = None
        self.init_database()

    @contextmanager
    def connect(self):
        """Create a database connection context manager"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn.cursor()
            conn.commit()
        finally:
            conn.close()

    def init_database(self):
        """Initialize database tables"""
        with self.connect() as cursor:
            # Create files table to track processed files
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_path TEXT UNIQUE,
                    current_path TEXT,
                    file_type TEXT,
                    metadata TEXT,
                    last_processed TIMESTAMP,
                    hash TEXT
                )
            ''')

            # Create operations table to track file operations
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER,
                    operation_type TEXT,
                    source_path TEXT,
                    destination_path TEXT,
                    timestamp TIMESTAMP,
                    status TEXT,
                    error_message TEXT,
                    FOREIGN KEY (file_id) REFERENCES files (id)
                )
            ''')

            # Create cache table for AI processing results
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER,
                    model_version TEXT,
                    processing_type TEXT,
                    result TEXT,
                    timestamp TIMESTAMP,
                    FOREIGN KEY (file_id) REFERENCES files (id)
                )
            ''')

            # Create user preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    preference_key TEXT UNIQUE,
                    preference_value TEXT,
                    last_updated TIMESTAMP
                )
            ''')

    def add_file(self, file_path: str, file_type: str, metadata: Dict) -> int:
        """Add or update a file entry"""
        with self.connect() as cursor:
            now = datetime.now()
            
            cursor.execute('''
                INSERT OR REPLACE INTO files 
                (original_path, current_path, file_type, metadata, last_processed)
                VALUES (?, ?, ?, ?, ?)
            ''', (file_path, file_path, file_type, json.dumps(metadata), now))
            
            return cursor.lastrowid

    def log_operation(self, file_id: int, operation_type: str, source: str, 
                     destination: str, status: str, error: Optional[str] = None):
        """Log a file operation"""
        with self.connect() as cursor:
            now = datetime.now()
            
            cursor.execute('''
                INSERT INTO operations 
                (file_id, operation_type, source_path, destination_path, 
                 timestamp, status, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (file_id, operation_type, source, destination, now, status, error))

    def cache_ai_result(self, file_id: int, model_version: str, 
                       processing_type: str, result: Dict):
        """Cache AI processing result"""
        with self.connect() as cursor:
            now = datetime.now()
            
            cursor.execute('''
                INSERT INTO ai_cache 
                (file_id, model_version, processing_type, result, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (file_id, model_version, processing_type, json.dumps(result), now))

    def get_cached_result(self, file_id: int, model_version: str, 
                         processing_type: str) -> Optional[Dict]:
        """Retrieve cached AI processing result"""
        with self.connect() as cursor:
            cursor.execute('''
                SELECT result FROM ai_cache 
                WHERE file_id = ? AND model_version = ? AND processing_type = ?
                ORDER BY timestamp DESC LIMIT 1
            ''', (file_id, model_version, processing_type))
            
            result = cursor.fetchone()
            return json.loads(result[0]) if result else None

    def set_preference(self, key: str, value: str):
        """Set user preference"""
        with self.connect() as cursor:
            now = datetime.now()
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_preferences 
                (preference_key, preference_value, last_updated)
                VALUES (?, ?, ?)
            ''', (key, value, now))

    def get_preference(self, key: str) -> Optional[str]:
        """Get user preference"""
        with self.connect() as cursor:
            cursor.execute('''
                SELECT preference_value FROM user_preferences 
                WHERE preference_key = ?
            ''', (key,))
            
            result = cursor.fetchone()
            return result[0] if result else None

    def get_file_history(self, file_path: str) -> List[Dict]:
        """Get operation history for a file"""
        with self.connect() as cursor:
            cursor.execute('''
                SELECT o.* FROM operations o
                JOIN files f ON o.file_id = f.id
                WHERE f.original_path = ?
                ORDER BY o.timestamp DESC
            ''', (file_path,))
            
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def cleanup_old_cache(self, days: int = 30):
        """Clean up old cache entries"""
        with self.connect() as cursor:
            cleanup_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            cursor.execute('''
                DELETE FROM ai_cache 
                WHERE timestamp < ?
            ''', (cleanup_date,))
