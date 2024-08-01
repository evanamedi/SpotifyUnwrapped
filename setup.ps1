$REPO_URL = "https://github.com/evanamedi/SpotifyUnwrapped.git"
$REPO_DIR = "SpotifyUnwrapped"

# check if command exists
function CommandExists {
	param (
		[string]$command
		)
	return Get-Command $command -ErrorAction SilentlyContinue
}

# clone repo
if (-not (Test-Path -Path $REPO_DIR)) {
	get clone $REPO_URL $REPO_DIR
}

Set-Location -Path $REPO_DIR

# check if Python 3.12 is installed, install if not
if (-not (CommandExists "python3.12")) {
	Write-Host "Python 3.12 is not installed. Installing Python 3.12..."
	$pythonInstaller = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
	$installerPath = "$env:TEMP\python-3.12.0-amd64.exe"
	Invoke-WebRequest -Uri $pythonInstaller -OutFile $installerPath
	Start-Process -Wait -FilePath $installerPath -ArgumentList "\quiet InstallAllUsers=1 PrependPath=1"
	Remove-Item -Path $installer Path
}

# set up venv
if (-not (Test-Path -Path "venv")) {
	python3.12 -m venv venv
}

& .\venv\Scripts\Activate

pip install -r requirements.txt

# script to run analysis
$scriptContent = @"
@echo off
call venv\Scripts\activate
python spotifyAnalysis.py
call venv\Scripts\deactivate
"@
Set-Content -Path "run_analysis.bat" -Value $scriptContent

Write-Host "Setup is complete. To run analysis, place JSON files in the 'Spotify_Extended_Streaming_History' directory and run './run_analysis.sh' "
