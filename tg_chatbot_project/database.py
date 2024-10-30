import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            requests_today INTEGER DEFAULT 0,
            request_limit INTEGER DEFAULT 12,
            last_request_date DATE DEFAULT CURRENT_DATE
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id: int):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id) VALUES (?)
    ''', (user_id,))
    conn.commit()
    conn.close()

def update_request_count(user_id: int):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT requests_today, request_limit, last_request_date
        FROM users WHERE user_id = ?
    ''', (user_id,))
    user_data = cursor.fetchone()
    
    if user_data is None:
        add_user(user_id)
        user_data = (0, 12, datetime.now().strftime('%Y-%m-%d'))
    
    requests_today, request_limit, last_request_date = user_data

    if last_request_date != datetime.now().strftime('%Y-%m-%d'):
        reset_user_requests(user_id)
        requests_today = 0

    if requests_today >= request_limit:
        conn.close()
        return False
    
    cursor.execute('''
        UPDATE users SET requests_today = requests_today + 1
        WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()
    
    return True

def get_user_profile(user_id: int) -> dict:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT requests_today, request_limit, last_request_date
        FROM users WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        return None
    
    requests_today, request_limit, last_request_date = result

    if last_request_date != datetime.now().strftime('%Y-%m-%d'):
        reset_user_requests(user_id)
        requests_today = 0

    return {
        "requests_today": requests_today,
        "request_limit": request_limit,
        "remaining_requests": request_limit - requests_today
    }

def reset_user_requests(user_id: int):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET requests_today = 0, last_request_date = CURRENT_DATE
        WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()
