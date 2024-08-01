$REPO_URL = "https://github.com/evanamedi/SpotifyUnwrapped.git"
$REPO_DIR = "SpotifyUnwrapped"

# Function to check if a command exists
function CommandExists {
    param (
        [string]$command
    )
    return Get-Command $command -ErrorAction SilentlyContinue
}

# Step 1: Check if git is installed
if (-not (CommandExists "git")) {
    Write-Host "Git is not installed. Please install Git and rerun the script."
    exit 1
}

# Step 2: Clone the repository
if (-not (Test-Path -Path $REPO_DIR)) {
    git clone $REPO_URL $REPO_DIR
}

Set-Location -Path $REPO_DIR

# Step 3: Check if Python 3.12 is installed and install it if not
if (-not (CommandExists "python3.12")) {
    Write-Host "Python 3.12 is not installed. Installing Python 3.12..."
    $pythonInstaller = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $installerPath = "$env:TEMP\python-3.12.0-amd64.exe"
    Invoke-WebRequest -Uri $pythonInstaller -OutFile $installerPath
    Start-Process -Wait -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1"
    Remove-Item -Path $installerPath
}

# Verify that python3.12 was installed correctly
if (-not (CommandExists "python3.12")) {
    Write-Host "Failed to install Python 3.12. Please install it manually and rerun the script."
    exit 1
}

# Step 4: Set up a virtual environment
if (-not (Test-Path -Path "venv")) {
    python -m venv venv
}

# Step 5: Activate the virtual environment
& .\venv\Scripts\Activate

# Step 6: Install dependencies
pip install -r requirements.txt

# Step 7: Create a script to run the analysis
$scriptContent = @"
@echo off
call venv\Scripts\activate
python spotify_analysis.py
call venv\Scripts\deactivate
"@
Set-Content -Path "run_analysis.bat" -Value $scriptContent

Write-Host "Setup is complete. To run the analysis, place your JSON files in the 'Spotify_Extended_Streaming_History' directory and run 'run_analysis.bat'"
