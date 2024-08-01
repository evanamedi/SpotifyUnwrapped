#!/bin/bash

REPO_URL="https://github.com/evanamedi/SpotifyUnwrapped.git"
REPO_DIR="SpotifyUnwrapped"

# check if
command_exists() {
	command -v "$1" >/dev/null 2>&1
}

# clone repo
if [ ! -d "$REPO_DIR" ]; then
	git clone $REPO_URL $REPO_DIR
fi

cd $REPO_DIR

# check if Python 3.12 is installed - will install if not
if ! command_exists python3.12; then
	echo "Python 3.12 is not installed. Installing Python 3.12..."
	if [[ "$OSTYPE" == "linux-gnu"* ]]; then
		sudo apt-get update
		sudo apt-get install -y wget builid-essential zlib1g-dev libssl-dev libncurses-dev libffi-dev libsqlite3-dev libreadline-dev libbz2-dev liblzma-dev
		wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
		tar xzf Python-3.12.0.tgz
		cd Python-3.12.0
		./configure --enable-optimizations
		make -j$(nproc)
		sudo make altinstall
		cd ..
		rm -rf Python-3.12.0 Python-3.12.0.tgz
	elif [[ "$OSTYPE" == "darwin"* ]]; then
		curl -O https://www.python.org/ftp/python/3.12.0/python-3.12.0-macosx10.9.pkg
		sudo installer -pkg python-3.12.0-macosx10.9.pkg -target /
		rm python-3.12.0-macosx10.9.pkg
	else
		echo "Unsupported OS. Please install Python 3.12 manually."
		exit 1
	fi
fi

# set up venv
if [ ! -d "venv" ]; then
	python3.12 -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt

# create script to run analysis
cat <<EOL > run_analysis.sh
#!/bin/bash
source venv/bin/activate
python spotifyAnalysis.py
deactivate
EOL
chmod +x run_analysis.sh

echo "Setup is complete. To run analysis, place JSON files in the 'Spotify_Extended_Streaming_History' directory and run './run_analysis.sh' "
