# Spotify Unwrapped

This project analyzes Spotify extended streaming history data and provides insights through visualizations.

## Prerequisites

Before you begin, ensure you have the following:

-   Git installed on your system. [Download Git](https://git-scm.com/downloads)
-   An internet connection to download Python and project dependencies.

## Setup

### Unix-like Systems (Linux, macOS)

1. Open a Terminal:

2. Run the Setup Script:

    ```sh
    curl -s https://raw.githubusercontent.com/evanamedi/SpotifyUnwrapped/main/setup.sh | bash
    ```

### Windows

1. Open PowerShell on your system:

2. Run the Setup Script:

    ```sh
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/evanamedi/SpotifyUnwrapped/main/setup.ps1" -OutFile "setup.ps1"
    .\setup.ps1
    ```

## Running the Analysis

1. Place your JSON files in the **Spotify_Extended_Streaming_History** directory within the cloned repository.

2. Run the following command to activate the virtual environment and execute the analysis script:

    ### Unix-like Systems (Linux, macOS)

    ```sh
    ./run_analysis.sh
    ```

    ### Windows

    ```sh
    .\run_analysis.bat
    ```
