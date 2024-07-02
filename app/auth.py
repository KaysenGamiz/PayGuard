import hashlib
import os
import uuid
from db import get_db_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, email):
    password_hash = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s) RETURNING id",
        (username, password_hash, email)
    )
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return user_id

def authenticate_user(username, password):
    password_hash = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username = %s AND password_hash = %s",
        (username, password_hash)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def create_session(user_id):
    session_token = str(uuid.uuid4())
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (user_id, session_token, expires_at) VALUES (%s, %s, NOW() + INTERVAL '1 HOUR') RETURNING id",
        (user_id, session_token)
    )
    session_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return session_token

def validate_session(session_token):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id FROM sessions WHERE session_token = %s AND expires_at > NOW()",
        (session_token,)
    )
    session = cursor.fetchone()
    cursor.close()
    conn.close()
    return session
