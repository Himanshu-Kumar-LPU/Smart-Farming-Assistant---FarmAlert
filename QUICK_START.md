$project = "C:\Users\Himanshu Kumar\OneDrive\Desktop\project"
$py = "$project\python_api\.venv311\Scripts\python.exe"

Set-Location $project

# Clean old processes silently
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Install dependencies (safe to run again)
npm install
& $py -m pip install -r "$project\python_api\requirements.txt"

# Start backend in new terminal window
Start-Process powershell -ArgumentList @(
  "-NoExit",
  "-Command",
  "Set-Location '$project'; npm start"
)

# Start python API in new terminal window
Start-Process powershell -ArgumentList @(
  "-NoExit",
  "-Command",
  "Set-Location '$project'; & '$py' '$project\python_api\app.py'"
)

Write-Host "Starting services..."
Start-Sleep -Seconds 6

# Quick health check
try { (Invoke-WebRequest -UseBasicParsing "http://localhost:3000").StatusCode } catch { $_.Exception.Message }
try { (Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:5000").StatusCode } catch { $_.Exception.Message }