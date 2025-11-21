# Library Inventory Manager (CSV storage)

**Course:** Programming for Problem Solving using Python

**Author:** Yokshit Rajora

## Overview
A small command-line library inventory manager that demonstrates object-oriented design, file persistence (CSV), exception handling, and a menu-driven CLI.

## Files
- `library_manager/book.py` — `Book` class
- `library_manager/inventory.py` — `LibraryInventory` class and CSV persistence
- `cli/main.py` — Menu-driven command-line interface
- `data/catalog.csv` — Stored catalog (created on first run)
- `tests/test_library.py` — unit tests using `unittest`

## How to run
1. (Optional) Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Run the CLI:

```bash
python -m cli.main
```

The program stores catalog data in `data/catalog.csv`.

**Folder Structre**

library-inventory-manager-yokshit-csv/
│
├── cli/
│   ├── __init__.py
│   └── main.py
│
├── library_manager/
│   ├── __init__.py
│   ├── book.py
│   └── inventory.py
│
├── tests/
│   ├── __init__.py
│   └── test_library.py
│
├── data/
│   └── catalog.csv
│
├── README.md
├── requirements.txt
├── .gitignore
├── setup.py

**Bibliography**

- `Youtube` = Brocode
- `Google`
- `W3Schools.com`
