from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
from flask import jsonify, session, redirect, url_for, render_template, request
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

def update_user_info(user_id, new_name):
    try:
        with sqlite3.connect(str(db_path), check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET name = ? WHERE id = ?", (new_name, user_id))
            conn.commit()
            return {'message': '个人信息更新成功'}, 200
    except Exception as e:
        return {'error': str(e)}, 500

def change_password(user_id, old_password, new_password):
    try:
        with sqlite3.connect(str(db_path), check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            
            if not user or not check_password_hash(user[0], old_password):
                return {'error': '旧密码错误'}, 400
            
            new_hash = generate_password_hash(new_password)
            cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
            conn.commit()
            return {'message': '密码修改成功'}, 200
    except Exception as e:
        return {'error': str(e)}, 500

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


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['id'])
        self.email = user_data['email']
        self.password_hash = user_data['password_hash']

    def get_id(self):
        return self.id

def get_user_by_email(email):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        if user:
            return User({'id': user[0], 'email': user[1], 'password_hash': user[2]})
        return None


def get_user_by_id(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, password_hash FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return User({'id': user[0], 'email': user[1], 'password_hash': user[2]})
        return None