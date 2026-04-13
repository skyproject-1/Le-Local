"""Order management routes"""

import json
import sqlite3

from flask import Blueprint, request, jsonify
from config.database import get_db_connection

try:
    from services.email import send_order_email
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False

bp = Blueprint('orders', __name__)

@bp.route('/', methods=['GET'])
def get_all_orders():
    """Get all orders, optionally filtered by user_id or status"""
    user_id = request.args.get('user_id')
    
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        if user_id:
            cursor.execute('''
                SELECT * FROM orders 
                WHERE user_id = ? 
                ORDER BY created_at DESC
            ''', (user_id,))
        else:
            cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
        
        orders = [{
            'id': o['id'],
            'userId': o['user_id'],
            'items': json.loads(o['items']),
            'total': float(o['total']),
            'status': o['status'],
            'deliveryAddress': o['delivery_address'],
            'createdAt': o['created_at']
        } for o in cursor.fetchall()]
        
        return jsonify({'orders': orders}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order by ID"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({
            'id': order['id'],
            'userId': order['user_id'],
            'items': json.loads(order['items']),
            'total': float(order['total']),
            'status': order['status'],
            'deliveryAddress': order['delivery_address'],
            'createdAt': order['created_at']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@bp.route('/', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.json
    user_id = data.get('user_id')
    items = data.get('items')
    total = data.get('total')
    delivery_address = data.get('delivery_address')
    
    if not all([items, total]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO orders (user_id, items, total, delivery_address, status)
            VALUES (?, ?, ?, ?, 'pending')
        ''', (user_id, json.dumps(items), total, delivery_address))
        
        order_id = cursor.lastrowid
        
        if user_id:
            cursor.execute('SELECT wallet_balance FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            
            if user and user[0] >= total:
                cursor.execute('''
                    UPDATE users 
                    SET wallet_balance = wallet_balance - ?,
                        loyalty_points = loyalty_points + ?
                    WHERE id = ?
                ''', (total, int(total), user_id))
                
                cursor.execute('''
                    INSERT INTO transactions (user_id, type, amount, description)
                    VALUES (?, 'spend', ?, ?)
                ''', (user_id, total, f'Order #{order_id}'))
        
        conn.commit()
        
        if EMAIL_AVAILABLE and user_id:
            cursor.execute('SELECT email, first_name FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            if user:
                user_email = user[0]
                customer_name = user[1]
                send_order_email(user_email, {
                    'order_id': order_id,
                    'items': items,
                    'total': total,
                    'delivery_address': delivery_address,
                    'customer_name': customer_name,
                    'payment_method': 'card' if data.get('payment') == 'card' else 'cash'
                })
        
        return jsonify({
            'message': 'Order placed successfully',
            'order_id': order_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@bp.route('/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update the status of an order"""
    data = request.json
    status = data.get('status')
    
    if not status:
        return jsonify({'error': 'Status is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE orders 
            SET status = ? 
            WHERE id = ?
        ''', (status, order_id))
        
        conn.commit()
        
        return jsonify({'message': 'Order status updated'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
