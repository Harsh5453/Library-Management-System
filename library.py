import sqlite3
import os
from datetime import date

# Use full path for mobile compatibility (Pydroid 3)
db_path = os.path.expanduser("~") + "/library.db"
db = sqlite3.connect(db_path)
cursor = db.cursor()

# Create tables if not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    available INTEGER DEFAULT 1
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    book_id INTEGER,
    issue_date TEXT,
    FOREIGN KEY(book_id) REFERENCES books(id)
)''')

db.commit()

# Function to add a book
def add_book(title, author):
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    db.commit()
    print("\n✅ Book added!")

# Function to show all books
def show_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if books:
        print("\n📚 All Books:")
        for book in books:
            status = "Available" if book[3] == 1 else "Issued"
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {status}")
    else:
        print("\n❌ No books found.")

# Function to show available books only
def show_available_books():
    cursor.execute("SELECT * FROM books WHERE available = 1")
    books = cursor.fetchall()
    if books:
        print("\n✅ Available Books:")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}")
    else:
        print("\n❌ No available books.")

# Function to show issued books
def show_issued_books():
    cursor.execute("SELECT students.id, students.name, books.title, students.issue_date FROM students JOIN books ON students.book_id = books.id")
    records = cursor.fetchall()
    if records:
        print("\n📖 Issued Books:")
        for rec in records:
            print(f"Issue ID: {rec[0]}, Student: {rec[1]}, Book: {rec[2]}, Date: {rec[3]}")
    else:
        print("\n❌ No books currently issued.")

# Function to issue a book
def issue_book(student_name, book_id):
    cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
    result = cursor.fetchone()
    if result and result[0] == 1:
        cursor.execute("INSERT INTO students (name, book_id, issue_date) VALUES (?, ?, ?)",
                       (student_name, book_id, date.today().isoformat()))
        cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
        db.commit()
        print("\n✅ Book issued!")
    else:
        print("\n❌ Book not available or does not exist.")

# Function to return a book
def return_book(student_id):
    cursor.execute("SELECT book_id FROM students WHERE id = ?", (student_id,))
    result = cursor.fetchone()
    if result:
        book_id = result[0]
        cursor.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        db.commit()
        print("\n✅ Book returned!")
    else:
        print("\n❌ Student ID not found.")

# Main menu interface
while True:
    print("\n================= LIBRARY MENU =================")
    print("1. Add Book")
    print("2. Show All Books")
    print("3. Show Available Books")
    print("4. Show Issued Books")
    print("5. Issue Book")
    print("6. Return Book")
    print("7. Exit")
    print("===============================================")
    choice = input("Enter your choice: ")

    if choice == '1':
        title = input("Title: ")
        author = input("Author: ")
        add_book(title, author)

    elif choice == '2':
        show_books()

    elif choice == '3':
        show_available_books()

    elif choice == '4':
        show_issued_books()

    elif choice == '5':
        name = input("Student Name: ")
        book_id = int(input("Book ID: "))
        issue_book(name, book_id)

    elif choice == '6':
        sid = int(input("Issue ID (Student Record ID): "))
        return_book(sid)

    elif choice == '7':
        print("\n👋 Exiting. Have a great day!")
        break

    else:
        print("\n❌ Invalid choice. Please try again.")
