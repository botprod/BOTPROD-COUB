# Coub-bot

https://t.me/botpr0d

To get query_id from Pyrogram sessions you should use this repo -> https://github.com/botprod/get_query_id

## Overview
Bot for https://t.me/coub/app?startapp=coub__marker_29720096

## Project Structure
```
project/
|
├── main.py                   # Main script to execute tasks
├── coub.py                   # API interaction logic with Coub
├── utils/                    # Utility modules
│   ├── file_loader.py        # Functions for loading data from files
│   ├── parser.py             # Logic for parsing queries
│   ├── logger.py             # Logging functions
│   └── session_manager.py    # Session management, including proxies and headers
|
├── data/                     # Data storage
│   ├── coub_query.json       # JSON file with Coub queries
│   ├── task.json             # JSON file with tasks
│   ├── proxy.txt             # File with proxy addresses
│   └── sessions.json         # JSON file for storing session details
|
├── requirements.txt          # Project dependencies
└── .gitignore                # Git ignore rules
```

## Setup Instructions
1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```sh
   cd project
   ```
3. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Linux/Mac:
     ```sh
     source venv/bin/activate
     ```
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
5. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
- Before running the script, ensure that all necessary data files are in place, such as `coub_query.json`, `task.json`, and `proxy.txt` in the `data/` folder.
- To start the script, run:
  ```sh
  python main.py
  ```
- During execution, the script will:
   1. Ping a server to verify the proxy is working.
   2. Generate session details, including headers and proxies, and save them in `sessions.json`.
   3. Compare current queries with those stored in `sessions.json` to identify new entries.
   4. Log proxy status, including failure information if proxies are not functioning.

## File Descriptions
- **main.py**: The main file that handles task execution, user interactions, and session verification.
- **coub.py**: Contains the logic for interacting with the Coub API (e.g., logging in, claiming rewards, etc.).
- **file_loader.py**: Utility file for loading data from JSON or text files.
- **parser.py**: Parses user query data to extract meaningful information.
- **logger.py**: Adds timestamped log messages to help with debugging.
- **session_manager.py**: Manages sessions, including generation of headers, proxy verification, and session storage.

## Data Files
- **coub_query.json**: Contains the queries for interacting with the Coub platform.
- **task.json**: JSON file defining various tasks that the script can execute.
- **proxy.txt**: Contains proxy addresses to rotate through during requests.
- **sessions.json**: Stores session details, including proxy, headers, and configuration information.
