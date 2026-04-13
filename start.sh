# Le Local - Start Development Servers

echo "Starting Le Local Off Licence..."

# Start Flask backend (port 5000)
echo "Starting Flask API on port 5000..."
cd backend
python3 app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start static file server (port 8080)
echo "Starting Static Server on port 8080..."
cd ..
python3 -m http.server 8080 &
STATIC_PID=$!

echo ""
echo "=========================================="
echo "Le Local is running!"
echo "=========================================="
echo "Home:        http://localhost:8080/index.html"
echo "Shop:        http://localhost:8080/shop.html"
echo "Account:     http://localhost:8080/le-local-account.html"
echo "Admin:       http://localhost:8080/admin.html"
echo "API:         http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "=========================================="

# Wait for Ctrl+C
trap "kill $BACKEND_PID $STATIC_PID 2>/dev/null; exit" INT TERM
wait
