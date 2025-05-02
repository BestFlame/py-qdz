from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import re

# 临时模拟数据库
users = {}

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent.parent / 'db' / 'database.db'


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
        with sqlite3.connect(str(db_path), check_same_thread=False) as conn:
            cursor = conn.cursor()
            password_hash = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, password_hash)
            )
            conn.commit()
            return {'success': True}, 201
    except sqlite3.IntegrityError:
        return {'error': '邮箱已被注册', 'success': False}, 409

def authenticate_user(email, password):
    try:
        with sqlite3.connect(str(db_path), check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            
            if not user or not check_password_hash(user[2], password):
                return {'error': '邮箱或密码错误'}, 401

            return {
                'id': user[0],
                'email': user[1],
                'created_at': user[3]
            }, 200
    except Exception as e:
        return {'error': '服务器内部错误'}, 500