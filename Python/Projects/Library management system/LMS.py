"""
library_cli.py
--------------
A menu-driven command-line Library Management System (MySQL backend).

Run with:
    python library_cli.py
"""

from datetime import date
import mysql.connector
from database import get_connection, initialize_database


# ---------------------------------------------------------------------
# BOOK FUNCTIONS
# ---------------------------------------------------------------------

def add_book():
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    copies = input("Enter number of copies: ").strip()

    if not title or not author or not copies.isdigit():
        print(" Invalid input. Book not added.\n")
        return

    copies = int(copies)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, total_copies, available_copies) VALUES (%s, %s, %s, %s)",
        (title, author, copies, copies),
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f" Book '{title}' added successfully.\n")


def view_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, title, author, available_copies, total_copies FROM books")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print(" No books in the library yet.\n")
        return

    print("\n{:<5}{:<30}{:<20}{:<10}".format("ID", "Title", "Author", "Available/Total"))
    print("-" * 65)
    for book_id, title, author, available, total in rows:
        print("{:<5}{:<30}{:<20}{:<10}".format(book_id, title, author, f"{available}/{total}"))
    print()


def search_book():
    keyword = input("Enter title or author keyword to search: ").strip()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT book_id, title, author, available_copies, total_copies FROM books "
        "WHERE title LIKE %s OR author LIKE %s",
        (f"%{keyword}%", f"%{keyword}%"),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print(" No matching books found.\n")
        return

    print("\n{:<5}{:<30}{:<20}{:<10}".format("ID", "Title", "Author", "Available/Total"))
    print("-" * 65)
    for book_id, title, author, available, total in rows:
        print("{:<5}{:<30}{:<20}{:<10}".format(book_id, title, author, f"{available}/{total}"))
    print()


def delete_book():
    book_id = input("Enter Book ID to delete: ").strip()
    if not book_id.isdigit():
        print(" Invalid Book ID.\n")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM books WHERE book_id = %s", (book_id,))
    row = cursor.fetchone()
    if not row:
        print(" Book not found.\n")
        cursor.close()
        conn.close()
        return

    cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f" Book '{row[0]}' deleted.\n")


# ---------------------------------------------------------------------
# MEMBER FUNCTIONS
# ---------------------------------------------------------------------

def add_member():
    name = input("Enter member name: ").strip()
    email = input("Enter member email: ").strip()

    if not name or not email:
        print(" Invalid input. Member not added.\n")
        return

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO members (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        print(f" Member '{name}' registered successfully.\n")
    except mysql.connector.Error as e:
        print(f" Could not add member (maybe email already exists). Error: {e}\n")
    finally:
        cursor.close()
        conn.close()


def view_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT member_id, name, email FROM members")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print(" No members registered yet.\n")
        return

    print("\n{:<5}{:<25}{:<30}".format("ID", "Name", "Email"))
    print("-" * 60)
    for member_id, name, email in rows:
        print("{:<5}{:<25}{:<30}".format(member_id, name, email))
    print()


# ---------------------------------------------------------------------
# TRANSACTION (ISSUE / RETURN) FUNCTIONS
# ---------------------------------------------------------------------

def issue_book():
    book_id = input("Enter Book ID to issue: ").strip()
    member_id = input("Enter Member ID: ").strip()

    if not book_id.isdigit() or not member_id.isdigit():
        print(" Invalid IDs.\n")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT available_copies FROM books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.execute("SELECT name FROM members WHERE member_id = %s", (member_id,))
    member = cursor.fetchone()

    if not book:
        print(" Book ID not found.\n")
        cursor.close()
        conn.close()
        return
    if not member:
        print(" Member ID not found.\n")
        cursor.close()
        conn.close()
        return
    if book[0] <= 0:
        print(" No available copies of this book right now.\n")
        cursor.close()
        conn.close()
        return

    cursor.execute(
        "INSERT INTO transactions (book_id, member_id, issue_date, return_date) VALUES (%s, %s, %s, NULL)",
        (book_id, member_id, date.today()),
    )
    cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f" Book issued to {member[0]} on {date.today()}.\n")


def return_book():
    book_id = input("Enter Book ID being returned: ").strip()
    member_id = input("Enter Member ID: ").strip()

    if not book_id.isdigit() or not member_id.isdigit():
        print(" Invalid IDs.\n")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT transaction_id FROM transactions "
        "WHERE book_id = %s AND member_id = %s AND return_date IS NULL "
        "ORDER BY transaction_id DESC LIMIT 1",
        (book_id, member_id),
    )
    txn = cursor.fetchone()

    if not txn:
        print(" No matching active issue record found.\n")
        cursor.close()
        conn.close()
        return

    cursor.execute(
        "UPDATE transactions SET return_date = %s WHERE transaction_id = %s",
        (date.today(), txn[0]),
    )
    cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE book_id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f" Book returned successfully on {date.today()}.\n")


def view_issued_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.transaction_id, b.title, m.name, t.issue_date
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        JOIN members m ON t.member_id = m.member_id
        WHERE t.return_date IS NULL
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print(" No books currently issued.\n")
        return

    print("\n{:<5}{:<30}{:<20}{:<12}".format("TxnID", "Book", "Member", "Issue Date"))
    print("-" * 70)
    for txn_id, title, name, issue_date in rows:
        print("{:<5}{:<30}{:<20}{:<12}".format(txn_id, title, name, str(issue_date)))
    print()


def view_member_history():
    member_id = input("Enter Member ID: ").strip()
    if not member_id.isdigit():
        print(" Invalid Member ID.\n")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.title, t.issue_date, t.return_date
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        WHERE t.member_id = %s
        ORDER BY t.transaction_id
    """, (member_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print(" No borrowing history found for this member.\n")
        return

    print("\n{:<30}{:<12}{:<12}".format("Book", "Issued", "Returned"))
    print("-" * 55)
    for title, issue_date, return_date in rows:
        print("{:<30}{:<12}{:<12}".format(title, str(issue_date), str(return_date) if return_date else "Not returned"))
    print()


# ---------------------------------------------------------------------
# MENU
# ---------------------------------------------------------------------

MENU = """
========== LIBRARY MANAGEMENT SYSTEM ==========
 1. Add Book
 2. View All Books
 3. Search Book
 4. Delete Book
 5. Register Member
 6. View All Members
 7. Issue Book
 8. Return Book
 9. View Currently Issued Books
10. View Member Borrowing History
 0. Exit
================================================
"""

ACTIONS = {
    "1": add_book,
    "2": view_books,
    "3": search_book,
    "4": delete_book,
    "5": add_member,
    "6": view_members,
    "7": issue_book,
    "8": return_book,
    "9": view_issued_books,
    "10": view_member_history,
}


def main():
    try:
        initialize_database()
    except mysql.connector.Error as e:
        print(f" Could not connect to MySQL: {e}")
        print("   -> Check that MySQL server is running and DB_CONFIG in database.py is correct.\n")
        return

    print("Welcome to the Library Management System!")

    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print(" Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()