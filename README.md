# list-manager


A lightweight command-line "List Manager" that stores tasks in an "SQLite" database.


## Purpose


This tool helps you manage short lists (todo items, shopping lists, notes) from the terminal. It supports:


 Adding, removing, updating, and marking tasks completed
 Listing tasks with different output formats
 Searching / filtering tasks with **regular expressions**
 Importing from and exporting to CSV files
 Using a single-file SQLite database (no DB server required)


Why this is useful

 Works on any system with Python 3 — no external DB or heavy setup.
Useful when you want a reproducible, scriptable list manager to integrate with other tools cron jobs, editors, automation.
 Demonstrates CLI argument handling, input validation, regex filtering, and persistent storage.


 Notes This project intentionally differs from a simple bash exercise or earlier class projects by focusing on a single-file Python CLI with a SQLite-backed persistent store, regex filtering, CSV import/export, and clear error handling.


## Requirements


Python 3.8+


No extra Python packages required — uses the standard library (argparse, sqlite3, re, csv, `datetime`, `sys`, `pathlib`).


## How to install


1. You will need to copy "list_manager.py" to a directory.
2. Then you will need to make it executable like this: `chmod +x list_manager.py` (optional)
3. Run: `./list_manager.py --help` or `python3 list_manager.py --help`


## Usage