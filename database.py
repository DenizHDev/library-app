import sqlite3

from flask import session


def create_tables():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            pages INTEGER,
            checked INTEGER,
            user_id INTEGER,
            UNIQUE(title, user_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
    """)
    connection.commit()
    connection.close()


def register_user(username,email,password):
    connection = sqlite3.connect("library.db")

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO users (username,email,password)
            VALUES (?,?,?)       
        """,(username,email,password))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"The user is already in the database!")
        return False
    finally:
        connection.close()


def get_user(username):
    connection = sqlite3.connect("library.db")
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM users where username = ?
        """,(username,))
        user = cursor.fetchone()
        return user
    finally:
        connection.close()

def get_available_books(user_id):
    connection = sqlite3.connect("library.db")
    try:

        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT * FROM books where checked = 0 AND user_id = ?
        """,(user_id,))
        books = cursor.fetchall()
        return books
    finally:
        connection.close()

def get_checked_books(user_id):
    connection = sqlite3.connect("library.db")
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM books where checked = 1
        """)
        books = cursor.fetchall()
        return books
    finally:
        connection.close()



def add_book(title,author,pages,user_id):
    connection = sqlite3.connect("library.db")
    try:

        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO books (title,author,pages,checked,user_id)
            VALUES (?,?,?,?,?)
        """,(title,author,pages,0,user_id))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Book {title} is already in the database")
        return False
    finally:
        connection.close()

def checkout_book(title):

    connection = sqlite3.connect("library.db")
    try:
        cursor = connection.cursor()
        cursor.execute(f"UPDATE books SET checked = 1 WHERE title = ?",(title,))
        connection.commit()
    finally:
        connection.close()

def return_book(title):
    connection = sqlite3.connect("library.db")
    try:
        cursor = connection.cursor()
        cursor.execute(f"UPDATE books SET checked = 0 WHERE title =? ",(title,))
        connection.commit()
    finally:
        connection.close()


def find_book(title):
    connection = sqlite3.connect("library.db")
    try:
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT * FROM books where title = ?
        """,(title,))
        book = cursor.fetchall()
        return book
    finally:
        connection.close()

def remove_book(title):
    connection = sqlite3.connect("library.db")
    try:
        cursor = connection.cursor()
        cursor.execute(""" DELETE FROM books WHERE title=?""", (title,))
        connection.commit()
    finally:
        connection.close()