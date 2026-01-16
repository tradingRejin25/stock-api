# PowerShell script to install dependencies

Write-Host "Installing Stock API Service Dependencies..." -ForegroundColor Green
Write-Host ""

# Function to try installing with a command
function Install-WithCommand {
    param($Command)
    
    try {
        $version = & $Command --version 2>&1
        if ($LASTEXITCODE -eq 0 -or $version) {
            Write-Host "Using: $Command" -ForegroundColor Yellow
            Write-Host ""
            
            # First, upgrade pip, setuptools, and wheel
            Write-Host "Upgrading pip, setuptools, and wheel..." -ForegroundColor Cyan
            & $Command -m pip install --upgrade pip setuptools wheel
            
            # Try installing requirements
            Write-Host "Installing dependencies..." -ForegroundColor Cyan
            & $Command -m pip install -r requirements.txt
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "Installation complete!" -ForegroundColor Green
                Write-Host ""
                Write-Host "To run the server:" -ForegroundColor Cyan
                Write-Host "  python main.py" -ForegroundColor White
                return $true
            } else {
                Write-Host ""
                Write-Host "Standard installation failed. Trying alternative method..." -ForegroundColor Yellow
                Write-Host ""
                
                # Try installing pandas separately with pre-built wheels
                Write-Host "Installing pandas from pre-built wheel..." -ForegroundColor Cyan
                & $Command -m pip install --only-binary :all: pandas
                
                # Install other dependencies
                Write-Host "Installing other dependencies..." -ForegroundColor Cyan
                & $Command -m pip install fastapi uvicorn[standard] pydantic openpyxl python-multipart
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Host ""
                    Write-Host "Installation complete!" -ForegroundColor Green
                    return $true
                }
            }
        }
    } catch {
        return $false
    }
    return $false
}

# Try different Python commands
$commands = @("python", "py", "python3")

foreach ($cmd in $commands) {
    if (Install-WithCommand $cmd) {
        exit 0
    }
}

# If all failed
Write-Host "ERROR: Python is not installed or not in PATH." -ForegroundColor Red
Write-Host ""
Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
Write-Host ""
Write-Host "Or run manually:" -ForegroundColor Cyan
Write-Host "  python -m pip install -r requirements.txt" -ForegroundColor White
Write-Host "  OR" -ForegroundColor White
Write-Host "  py -m pip install -r requirements.txt" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to exit"

