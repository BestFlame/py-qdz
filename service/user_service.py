from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import re

# 临时模拟数据库
users = {}

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent.parent / 'db' / 'database.db'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# 初始化用户表
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()


def validate_email_format(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def validate_password_strength(password):
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password)

def register_user(email: str, password: str):
    if not validate_email_format(email):
        return {'error': '邮箱格式不正确'}, 400
    
    if not validate_password_strength(password):
        return {'error': '密码需要至少8位且包含大写字母和数字'}, 400

    try:
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return {'error': '邮箱已被注册'}, 409

def authenticate_user(email, password):
    user = users.get(email)
    if not user or not check_password_hash(user['password_hash'], password):
        return {'error': '邮箱或密码错误'}, 401
    
    return {
        'email': user['email'],
        'created_at': '2024-01-01'  # 示例数据
    }, 200