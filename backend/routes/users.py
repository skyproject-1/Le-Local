"""User authentication and wallet management routes"""

import json
import sqlite3

from flask import Blueprint, request, jsonify
from config.database import get_db_connection
import hashlib

bp = Blueprint('users', __name__)

def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(hashed_password, password):
    """Verify a password against its hash"""
    return hashed_password == hash_password(password)


@bp.route('/register', methods=['POST'])
def register():
    """Register a new user account"""
    data = request.json
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id FROM users WHERE email = ?', (data['email'],))
        if cursor.fetchone():
            return jsonify({'error': 'Email already registered'}), 400
        
        hashed_pw = hash_password(data['password'])
        
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, phone, address, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['firstName'], data['lastName'], data['email'], 
              data['phone'], data.get('address', ''), hashed_pw))
        
        conn.commit()
        user_id = cursor.lastrowid
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user_id,
                'firstName': data['firstName'],
                'lastName': data['lastName'],
                'email': data['email']
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user"""
    data = request.json
    
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM users WHERE email = ?', (data['email'],))
        user = cursor.fetchone()
        
        if not user or not check_password(user['password'], data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        return jsonify({
            'user': {
                'id': user['id'],
                'firstName': user['first_name'],
                'lastName': user['last_name'],
                'email': user['email'],
                'phone': user['phone'],
                'address': user['address'],
                'wallet': float(user['wallet_balance']),
                'points': user['loyalty_points']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """Get user profile by ID"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user['id'],
            'firstName': user['first_name'],
            'lastName': user['last_name'],
            'email': user['email'],
            'phone': user['phone'],
            'address': user['address'],
            'wallet': float(user['wallet_balance']),
            'points': user['loyalty_points'],
            'createdAt': user['created_at']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@bp.route('/wallet/topup', methods=['POST'])
def topup_wallet():
    """Add funds to user wallet (called after successful payment)"""
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
    
    if not user_id or not amount:
        return jsonify({'error': 'Missing user_id or amount'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE users 
            SET wallet_balance = wallet_balance + ? 
            WHERE id = ?
        ''', (amount, user_id))
        
        cursor.execute('''
            INSERT INTO transactions (user_id, type, amount, description)
            VALUES (?, 'topup', ?, 'Wallet Top-up')
        ''', (user_id, amount))
        
        conn.commit()
        
        return jsonify({'message': 'Wallet topped up successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@bp.route('/wallet/verify-topup', methods=['POST'])
def verify_wallet_topup():
    """Verify payment and add funds to wallet"""
    data = request.json
    checkout_id = data.get('checkout_id')
    user_id = data.get('user_id')
    amount = data.get('amount')
    
    if not checkout_id or not user_id or not amount:
        return jsonify({'error': 'Missing checkout_id, user_id or amount'}), 400
    
    import os
    api_key = os.environ.get('SUMUP_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'SUMUP_API_KEY not set'}), 500
    
    try:
        import requests
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"https://api.sumup.com/v0.1/checkouts/{checkout_id}", headers=headers)
        
        if response.status_code != 200:
            return jsonify({'error': 'Checkout not found'}), 404
        
        checkout_data = response.json()
        if checkout_data.get('status') == 'PAID':
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET wallet_balance = wallet_balance + ? 
                WHERE id = ?
            ''', (amount, user_id))
            cursor.execute('''
                INSERT INTO transactions (user_id, type, amount, description)
                VALUES (?, 'topup', ?, 'Wallet Top-up')
            ''', (user_id, amount))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Wallet topped up successfully', 'status': 'completed'}), 200
        else:
            return jsonify({'status': checkout_data.get('status')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/wallet/transactions/<int:user_id>', methods=['GET'])
def get_transactions(user_id):
    """Get wallet transaction history for a user"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT * FROM transactions 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 20
        ''', (user_id,))
        
        transactions = [{
            'id': t['id'],
            'type': t['type'],
            'amount': float(t['amount']),
            'description': t['description'],
            'createdAt': t['created_at']
        } for t in cursor.fetchall()]
        
        return jsonify({'transactions': transactions}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@bp.route('/', methods=['GET'])
def get_all_users():
    """Get all users (admin only)"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT id, first_name, last_name, email, phone, address, 
                   wallet_balance, loyalty_points, created_at
            FROM users ORDER BY created_at DESC
        ''')
        
        users = [{
            'id': u['id'],
            'firstName': u['first_name'],
            'lastName': u['last_name'],
            'email': u['email'],
            'phone': u['phone'],
            'address': u['address'],
            'wallet': float(u['wallet_balance']),
            'loyaltyPoints': u['loyalty_points'],
            'createdAt': u['created_at']
        } for u in cursor.fetchall()]
        
        return jsonify({'users': users}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
