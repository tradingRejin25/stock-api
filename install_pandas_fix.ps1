# Fix pandas installation on Windows
# Run this script to install pandas and all dependencies

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host " Stock API Service - Pandas Installation Fix " -NoNewline -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Cyan
Write-Host ""

# Find Python executable
$pythonCmd = $null
$commands = @("python", "py", "python3", "python.exe")

foreach ($cmd in $commands) {
    try {
        $result = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0 -or $result -match "Python") {
            $pythonCmd = $cmd
            Write-Host "Found Python: $cmd" -ForegroundColor Green
            Write-Host "Version: $result" -ForegroundColor Gray
            break
        }
    } catch {
        continue
    }
}

if (-not $pythonCmd) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 1: Upgrading pip, setuptools, and wheel..." -ForegroundColor Cyan
Write-Host ""

try {
    & $pythonCmd -m pip install --upgrade pip setuptools wheel
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Warning: pip upgrade had issues, but continuing..." -ForegroundColor Yellow
    } else {
        Write-Host "✓ pip upgraded successfully" -ForegroundColor Green
    }
} catch {
    Write-Host "Warning: Could not upgrade pip, but continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 2: Installing pandas (using pre-built wheels)..." -ForegroundColor Cyan
Write-Host "This may take a few minutes..." -ForegroundColor Gray
Write-Host ""

try {
    & $pythonCmd -m pip install --only-binary :all: pandas
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ pandas installed successfully" -ForegroundColor Green
    } else {
        Write-Host "Trying alternative pandas installation..." -ForegroundColor Yellow
        & $pythonCmd -m pip install pandas
    }
} catch {
    Write-Host "Error installing pandas. Trying alternative method..." -ForegroundColor Yellow
    & $pythonCmd -m pip install pandas
}

Write-Host ""
Write-Host "Step 3: Installing other dependencies..." -ForegroundColor Cyan
Write-Host ""

$packages = @(
    "fastapi==0.104.1",
    "uvicorn[standard]==0.24.0",
    "pydantic==2.5.0",
    "openpyxl>=3.1.0",
    "python-multipart==0.0.6"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Gray
    & $pythonCmd -m pip install $package
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $package installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to install $package" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Step 4: Verifying installation..." -ForegroundColor Cyan
Write-Host ""

try {
    & $pythonCmd -c "import pandas; import fastapi; import pydantic; print('✓ All packages installed successfully!')"
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=" -NoNewline -ForegroundColor Green
        Write-Host "=" -NoNewline -ForegroundColor Green
        Write-Host " Installation Complete! " -NoNewline -ForegroundColor Green
        Write-Host "=" -NoNewline -ForegroundColor Green
        Write-Host "=" -ForegroundColor Green
        Write-Host ""
        Write-Host "To run the server:" -ForegroundColor Cyan
        Write-Host "  $pythonCmd main.py" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "Some packages may not be installed correctly." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Verification failed. Some packages may be missing." -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

