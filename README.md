# Le Local - Visual Studio Code Setup

## Option 1: VS Code Live Server (Recommended)

1. Open the `lelocal-offlicence` folder in VS Code
2. Install "Live Server" extension by Ritwick Dey
3. Right-click `index.html` → "Open with Live Server"

## Option 2: Python (Terminal)

Run these in two separate terminals:

### Terminal 1 - Backend API
```bash
cd /Users/bharat/Desktop/untitled\ folder/lelocal-offlicence/backend
python3 app.py
```

### Terminal 2 - Static Files  
```bash
cd /Users/bharat/Desktop/untitled\ folder/lelocal-offlicence
python3 -m http.server 8080
```

## Option 3: Run Both at Once (Mac/Linux)
```bash
cd /Users/bharat/Desktop/untitled\ folder/lelocal-offlicence
chmod +x start.sh
./start.sh
```

## URLs
- Home Page: http://localhost:8080/index.html
- Shop: http://localhost:8080/shop.html
- Account: http://localhost:8080/le-local-account.html
- Admin: http://localhost:8080/admin.html
- API: http://localhost:5000
