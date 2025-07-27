# 📚 Booklog CLI

**Booklog CLI** is a simple and lightweight command-line tool to help you track your reading progress. Built with Python and [Click](https://click.palletsprojects.com/), it allows you to manage books, export them to CSV, and view them in a clean tabular format.

---

## 🔧 Features

- ✅ Add a new book with title, author, status, and more
- 📖 List all books in a readable table
- ✏️ Update existing book details
- ❌ Delete books
- 📁 Export your data to CSV format
- 🧠 Data stored locally in a JSON file

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:mhmdmnthsr/Booklog-CLI.git
cd Booklog-CLI
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the Project (Editable Mode)

```bash
pip install -e .
```

---

## 📝 Usage

Once installed, you can use the CLI tool via the `booklog` command:

### ➕ Add a Book

```bash
booklog add --title "Atomic Habits" --author "James Clear" --status "reading"
```

### 📃 List All Books

```bash
booklog list
```

### ✏️ Update a Book

```bash
booklog update 1 --status "completed"
```

### ❌ Delete a Book

```bash
booklog delete 1
```

### 📤 Export to CSV

```bash
booklog export --format csv
```

---

## 🗂️ File Structure

```
Booklog-CLI/
├── booklog/           # Python package containing CLI logic
│   ├── __init__.py
│   └── main.py
├── books.json         # Local data store (auto-created)
├── README.md
├── .gitignore
└── setup.py
```

---

## 🧰 Tech Stack

- **Python 3.10+**
- **Click** for command-line interface
- **JSON** for local data storage
- **CSV** for export
- **Tabulate** for table display
