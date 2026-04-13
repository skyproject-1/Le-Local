# Le Local Backend (Python Flask)

## Requirements
- Python 3.10+
- MySQL Server

## Setup

### 1. Install Python dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Database
Create a MySQL database:
```sql
CREATE DATABASE lelocal;
```

Copy `.env.example` to `.env` and update with your MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=lelocal
```

### 3. Initialize Database
Run the database setup:
```python
from config.database import init_db
init_db()
```

Or run:
```bash
python -c "from config.database import init_db; init_db()"
```

### 4. Start Server
```bash
python app.py
```

Server will run at `http://localhost:5000`

## API Endpoints

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Register new user |
| POST | `/users/login` | Login user |
| GET | `/users/profile/<id>` | Get user profile |
| POST | `/users/wallet/topup` | Top up wallet |
| GET | `/users/wallet/transactions/<id>` | Get transactions |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/` | Get all products |
| GET | `/products/?category=Beer` | Filter by category |
| GET | `/products/?search=carlsberg` | Search products |
| GET | `/products/<id>` | Get single product |
| GET | `/products/categories` | Get categories |
| POST | `/products/` | Add product (admin) |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders/` | Get all orders |
| GET | `/orders/?user_id=1` | Get user orders |
| GET | `/orders/<id>` | Get single order |
| POST | `/orders/` | Create order |
| PUT | `/orders/<id>/status` | Update order status |

## Connect Frontend

Update your frontend JavaScript to fetch from the API:

```javascript
const API_URL = 'http://localhost:5000';

// Login
fetch(`${API_URL}/users/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
})

// Get products
fetch(`${API_URL}/products/`)
```

## Production Deployment

1. Change `DB_HOST` to your MySQL server IP
2. Update `SECRET_KEY` with a secure key
3. Use a production WSGI server (gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app
   ```
