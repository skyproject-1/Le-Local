"""Product catalog routes"""

import sqlite3

from flask import Blueprint, request, jsonify
from config.database import get_db_connection

bp = Blueprint('products', __name__)

@bp.route('/', methods=['GET'])
def get_all_products():
    """Get all products, optionally filtered by category or search term"""
    category = request.args.get('category')
    search = request.args.get('search')
    
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        query = 'SELECT * FROM products WHERE in_stock = 1'
        params = []
        
        if category and category != 'All':
            query += ' AND category = ?'
            params.append(category)
        
        if search:
            query += ' AND (name LIKE ? OR description LIKE ?)'
            search_term = f'%{search}%'
            params.extend([search_term, search_term])
        
        query += ' ORDER BY name'
        
        cursor.execute(query, params)
        products = [{
            'id': p['id'],
            'name': p['name'],
            'category': p['category'],
            'subcategory': p['subcategory'],
            'price': float(p['price']),
            'originalPrice': float(p['original_price']) if p['original_price'] else None,
            'image': p['image'],
            'description': p['description']
        } for p in cursor.fetchall()]
        
        return jsonify({'products': products}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({
            'id': product['id'],
            'name': product['name'],
            'category': product['category'],
            'subcategory': product['subcategory'],
            'price': float(product['price']),
            'originalPrice': float(product['original_price']) if product['original_price'] else None,
            'image': product['image'],
            'description': product['description'],
            'inStock': product['in_stock']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories with counts"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT DISTINCT category, COUNT(*) as count 
            FROM products 
            GROUP BY category
        ''')
        
        categories = [{
            'name': c['category'],
            'count': c['count']
        } for c in cursor.fetchall()]
        
        return jsonify({'categories': categories}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@bp.route('/', methods=['POST'])
def add_product():
    """Add a new product to the catalog"""
    data = request.json
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO products (name, category, subcategory, price, original_price, image, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['category'], data.get('subcategory'),
              data['price'], data.get('originalPrice'), data.get('image'), 
              data.get('description')))
        
        conn.commit()
        
        return jsonify({'message': 'Product added successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product"""
    data = request.json
    
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Get existing product
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        existing = cursor.fetchone()
        
        if not existing:
            return jsonify({'error': 'Product not found'}), 404
        
        # Update with new values or keep existing
        name = data.get('name') if data.get('name') else existing['name']
        category = data.get('category') if data.get('category') else existing['category']
        subcategory = data.get('subcategory') if data.get('subcategory') else existing['subcategory']
        price = data.get('price') if data.get('price') else existing['price']
        original_price = data.get('originalPrice') if data.get('originalPrice') else existing['original_price']
        image = data.get('image') if data.get('image') else existing['image']
        description = data.get('description') if data.get('description') else existing['description']
        
        cursor.execute('''
            UPDATE products 
            SET name = ?, category = ?, subcategory = ?, price = ?, 
                original_price = ?, image = ?, description = ?
            WHERE id = ?
        ''', (name, category, subcategory, price, original_price, image, description, product_id))
        
        conn.commit()
        
        return jsonify({'message': 'Product updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
