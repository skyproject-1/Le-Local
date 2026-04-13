# Le Local - Off Licence & Grocery Delivery

## Quick Start

### Local Development

**Option 1: VS Code Live Server (Recommended)**
1. Open the `lelocal-offlicence` folder in VS Code
2. Install "Live Server" extension by Ritwick Dey
3. Right-click `index.html` → "Open with Live Server"

**Option 2: Python Terminal**
```bash
cd /Users/bharat/Desktop/untitled\ folder/lelocal-offlicence/backend
python3 app.py
```

Then in another terminal:
```bash
cd /Users/bharat/Desktop/untitled\ folder/lelocal-offlicence
python3 -m http.server 8080
```

## URLs
- Home: http://localhost:8080/index.html
- Shop: http://localhost:8080/shop.html  
- Account: http://localhost:8080/le-local-account.html
- Admin: http://localhost:8080/admin.html
- API: http://localhost:5000

## Deploy

### Frontend (Netlify)
- Upload folder to Netlify

### Backend (Render)
- Deploy `backend/` folder to Render.com