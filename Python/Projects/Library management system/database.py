"""
database.py
------------


Tables:
    books        -> catalog of all books in the library
    members      -> registered library members
    transactions -> records of book issue / return activity
"""

import mysql.connector

# ---- EDIT THESE to match your local MySQL setup ----
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",   
}
DB_NAME = "library_db"
# -----------------------------------------------------


def get_connection():
    """Return a connection to the 'library_db' MySQL database."""
    return mysql.connector.connect(database=DB_NAME, **DB_CONFIG)


def initialize_database():
    """Create the database (if it doesn't exist) and all required tables."""

    # Step 1: connect WITHOUT selecting a database, and create it if missing
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()
    conn.close()

    # Step 2: connect to library_db and create tables
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id           INT AUTO_INCREMENT PRIMARY KEY,
            title             VARCHAR(255) NOT NULL,
            author            VARCHAR(255) NOT NULL,
            total_copies      INT NOT NULL DEFAULT 1,
            available_copies  INT NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id   INT AUTO_INCREMENT PRIMARY KEY,
            name        VARCHAR(255) NOT NULL,
            email       VARCHAR(255) UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            book_id        INT NOT NULL,
            member_id      INT NOT NULL,
            issue_date     DATE NOT NULL,
            return_date    DATE,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (member_id) REFERENCES members(member_id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()