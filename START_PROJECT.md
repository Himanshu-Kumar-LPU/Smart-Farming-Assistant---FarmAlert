# How to Start the Project - Step by Step

## Prerequisites
- **Node.js** (v18+): Download from https://nodejs.org/
- **Python** (3.11+): Download from https://www.python.org/
- **Git**: Download from https://git-scm.com/

## Step 1: Navigate to Project Directory
```powershell
cd "C:\Users\Himanshu Kumar\OneDrive\Desktop\project"
```

## Step 2: Install Node Dependencies
Run this once to install backend Node packages:
```powershell
npm install
```

## Step 3: Verify/Download Model Files (Git LFS)
The trained leaf model is stored in Git LFS. Download it:
```powershell
git lfs pull
```

This downloads the `leaf_model.keras` file (134MB).

## Step 4: Install Python Dependencies
Install Python packages for the prediction API:
```powershell
& "python_api\.venv311\Scripts\python.exe" -m pip install -r python_api/requirements.txt
```

Or if you prefer using the project's venv311:
```powershell
& "python_api\.venv311\Scripts\python.exe" -m pip install flask tensorflow pillow numpy h5py
```

## Step 5: Start Backend Server (Terminal 1)
Open a **new PowerShell terminal** and run:
```powershell
cd "C:\Users\Himanshu Kumar\OneDrive\Desktop\project"
npm run start
```

You should see:
```
🔑 GROQ_API_KEY loaded: YES
✅ Groq client initialized successfully
🚀 Server starting...
Server running on http://localhost:3000
✅ MongoDB connected successfully
```

**Keep this terminal open!**

## Step 6: Start Python API (Terminal 2)
Open a **second PowerShell terminal** and run:
```powershell
cd "C:\Users\Himanshu Kumar\OneDrive\Desktop\project"
& "python_api\.venv311\Scripts\python.exe" python_api/app.py
```

You should see:
```
Loaded leaf model from C:\Users\Himanshu Kumar\OneDrive\Desktop\project\python_api\models\leaf_model.keras
...
Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**Keep this terminal open!**

## Step 7: Access the Application
Once both services are running, open your browser and visit:

### **Login Page:**
```
http://localhost:3000/auth/login.html
```

### **Main App:**
```
http://localhost:3000
```

### **Backend API (Alerts):**
```
http://localhost:3000/alerts
```

### **Python Prediction API:**
```
http://127.0.0.1:5000/predict
```

---

## Quick Checklist
- [ ] Node.js installed (`node --version`)
- [ ] Python 3.11+ installed (`python --version`)
- [ ] Ran `npm install` in project directory
- [ ] Ran `git lfs pull` to download model
- [ ] Backend started with `npm run start` (Terminal 1)
- [ ] Python API started with `python_api/.venv311/Scripts/python.exe python_api/app.py` (Terminal 2)
- [ ] Can access http://localhost:3000/auth/login.html
- [ ] Can access http://127.0.0.1:5000/predict

---

## Troubleshooting

### "Port 3000 already in use"
Stop existing Node process:
```powershell
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
```

### "Port 5000 already in use"
Stop existing Python process:
```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

### "leaf_model.keras not found"
Ensure Git LFS is installed and run:
```powershell
git lfs pull
```

### "TensorFlow not installed"
Run:
```powershell
& "python_api\.venv311\Scripts\python.exe" -m pip install tensorflow
```

---

## Stopping the Project
Press `CTRL+C` in each terminal to stop the services:
- Terminal 1 (Backend): `CTRL+C`
- Terminal 2 (Python API): `CTRL+C`

---

## Environment Variables (Optional)
Create a `.env` file in the project root if you need custom settings:
```
PORT=3000
HTTPS_DEV=false
MONGODB_URI=mongodb://localhost:27017/farm-alert
GROQ_API_KEY=your_key_here
```
