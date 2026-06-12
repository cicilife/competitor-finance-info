import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class NewsDatabase:
    def __init__(self, db_path: str = "data/processed/reports.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS brands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                english_name TEXT,
                category TEXT,
                focus TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                source TEXT,
                brand_name TEXT,
                content TEXT,
                content_type TEXT,
                publish_date TEXT,
                crawl_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                summary TEXT,
                tags TEXT,
                FOREIGN KEY(brand_name) REFERENCES brands(name)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pdf_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_name TEXT,
                filename TEXT NOT NULL,
                file_path TEXT UNIQUE NOT NULL,
                report_type TEXT,
                year TEXT,
                quarter TEXT,
                download_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(brand_name) REFERENCES brands(name)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crawl_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_type TEXT,
                source_url TEXT,
                success BOOLEAN,
                crawled_items INTEGER,
                crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                error_message TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_date TEXT UNIQUE NOT NULL,
                news_count INTEGER,
                pdf_count INTEGER,
                report_path TEXT,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def add_brand(self, name: str, english_name: str = None, category: str = None, focus: str = None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO brands (name, english_name, category, focus)
            VALUES (?, ?, ?, ?)
        ''', (name, english_name, category, focus))
        self.conn.commit()

    def add_news_item(self, title: str, url: str, source: str, brand_name: str = None,
                      content: str = None, content_type: str = None, publish_date: str = None,
                      summary: str = None, tags: List[str] = None):
        cursor = self.conn.cursor()
        tags_json = json.dumps(tags) if tags else None
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO news_items 
                (title, url, source, brand_name, content, content_type, publish_date, summary, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, url, source, brand_name, content, content_type, publish_date, summary, tags_json))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def add_pdf_report(self, brand_name: str, filename: str, file_path: str, 
                       report_type: str = None, year: str = None, quarter: str = None):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO pdf_reports
                (brand_name, filename, file_path, report_type, year, quarter)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (brand_name, filename, file_path, report_type, year, quarter))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def log_crawl(self, source_type: str, source_url: str, success: bool, 
                  crawled_items: int = 0, error_message: str = None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO crawl_history
            (source_type, source_url, success, crawled_items, error_message)
            VALUES (?, ?, ?, ?, ?)
        ''', (source_type, source_url, success, crawled_items, error_message))
        self.conn.commit()

    def add_weekly_report(self, report_date: str, news_count: int, pdf_count: int, report_path: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO weekly_reports
            (report_date, news_count, pdf_count, report_path)
            VALUES (?, ?, ?, ?)
        ''', (report_date, news_count, pdf_count, report_path))
        self.conn.commit()

    def get_news_by_brand(self, brand_name: str, limit: int = 100) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM news_items WHERE brand_name = ? ORDER BY crawl_date DESC LIMIT ?
        ''', (brand_name, limit))
        return [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()]

    def get_news_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM news_items 
            WHERE crawl_date >= ? AND crawl_date <= ? 
            ORDER BY crawl_date DESC
        ''', (start_date, end_date))
        return [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()]

    def get_news_by_type(self, content_type: str, limit: int = 100) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM news_items WHERE content_type = ? ORDER BY crawl_date DESC LIMIT ?
        ''', (content_type, limit))
        return [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()]

    def get_latest_news(self, limit: int = 50) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM news_items ORDER BY crawl_date DESC LIMIT ?
        ''', (limit,))
        return [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()]

    def get_pdf_reports(self, brand_name: str = None) -> List[Dict]:
        cursor = self.conn.cursor()
        if brand_name:
            cursor.execute('''
                SELECT * FROM pdf_reports WHERE brand_name = ? ORDER BY download_date DESC
            ''', (brand_name,))
        else:
            cursor.execute('''
                SELECT * FROM pdf_reports ORDER BY download_date DESC
            ''')
        return [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()]

    def get_weekly_reports(self, limit: int = 10) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM weekly_reports ORDER BY generated_at DESC LIMIT ?
        ''', (limit,))
        return [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()]

    def get_brands(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM brands')
        return [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()]

    def url_exists(self, url: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM news_items WHERE url = ?', (url,))
        return cursor.fetchone() is not None

    def pdf_exists(self, file_path: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM pdf_reports WHERE file_path = ?', (file_path,))
        return cursor.fetchone() is not None

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()