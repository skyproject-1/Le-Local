"""Le Local Off Licence & Grocery - Flask Backend"""

import os

from flask import Flask
from flask_cors import CORS

from routes.users import bp as users_bp
from routes.products import bp as products_bp
from routes.orders import bp as orders_bp
from routes.payments import bp as payments_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'lelocal-secret-key-change-in-production'
)

CORS(app)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(payments_bp, url_prefix='/payments')


@app.route('/')
def index():
    """Health check endpoint"""
    return {'message': 'Le Local API', 'status': 'running'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)