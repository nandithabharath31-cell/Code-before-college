# 📚 Library Management System (CLI + MySQL)

A simple, menu-driven **Library Management System** built with **Python** and **MySQL**.
It manages books, members, and book issue/return transactions — a practical mini-project
that demonstrates core DBMS concepts (tables, primary/foreign keys, joins) with a real
relational database server.

## ✨ Features

- **Book management** — add, view, search, and delete books
- **Member management** — register and view library members
- **Issue / Return system** — issue a book to a member (checks availability),
  return a book, and automatically update available copy counts
- **Reports** — view all currently issued books, and a member's full borrowing history
- Data is **persisted** in a MySQL database (`library_db`), created automatically
  the first time you run the program

## 🗂️ Database Schema

| Table          | Columns                                                                 |
|----------------|--------------------------------------------------------------------------|
| `books`        | `book_id (PK)`, `title`, `author`, `total_copies`, `available_copies`   |
| `members`      | `member_id (PK)`, `name`, `email (unique)`                              |
| `transactions` | `transaction_id (PK)`, `book_id (FK)`, `member_id (FK)`, `issue_date`, `return_date` |

`transactions` links `books` and `members` (a many-to-many relationship over time),
a good real-world example of a junction/associative table in relational database design.

## 🛠️ Tech Stack

- Python 3
- MySQL (via the `mysql-connector-python` library)

## ⚙️ Setup

### 1. Install MySQL Server (if you don't already have it)
- Easiest option: install **XAMPP** or **WAMP** (includes MySQL + a GUI called phpMyAdmin)
- Or install MySQL Community Server directly from mysql.com
- Make sure the MySQL service is **running** before you run this program

### 2. Install the Python dependency
```bash
pip install -r requirements.txt
```

### 3. Configure your credentials
Open `database.py` and edit the `DB_CONFIG` dictionary near the top to match your
local MySQL username/password:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_mysql_password",   # <-- put your actual MySQL password here
}
```

> You do **not** need to manually create the database or tables — the program
> creates `library_db` and all required tables automatically on first run.

### 4. Run the program
```bash
python library_cli.py
```

## 📋 Menu Options

```
1. Add Book                        6. View All Members
2. View All Books                  7. Issue Book
3. Search Book                     8. Return Book
4. Delete Book                     9. View Currently Issued Books
5. Register Member                10. View Member Borrowing History
                                    0. Exit
```

## 📁 Project Structure

```
library-management-system/
├── database.py         # MySQL connection + table creation (schema)
├── library_cli.py      # Main program: menu + all feature functions
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

## 🔮 Possible Future Improvements

- Add due dates and fine calculation for late returns
- Add a Flask web interface (HTML/CSS front-end) on top of the same database
- Add admin login / authentication
- Export reports to CSV

## 📝 Author

Built as a first-year B.Tech CSE pre-college project to practice Python, SQL, and
software structuring fundamentals.
