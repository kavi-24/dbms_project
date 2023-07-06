import oracledb
import datetime
# import prettytable

oracledb.init_oracle_client()

username = "DARSHNI"
password = "darshni_1912"
host = "localhost"
port = 1521
service_name = "XE"

dsn = f"{username}/{password}@{host}:{port}/{service_name}"
connection = oracledb.connect(dsn=dsn)
connection.autocommit = True

# Function to add a book
def add_book():
    cursor = connection.cursor()
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    quantity = int(input("Enter book quantity: "))
    price = float(input("Enter book price: "))
    pub_id = int(input("Enter publisher ID: "))
    try:
        cursor.execute("INSERT INTO books (bookid, title, author, quantity, price, pubid) VALUES (book_sequence.nextval, :title, :author, :quantity, :price, :pub_id)", title=title, author=author, quantity=quantity, price=price, pub_id=pub_id)
    except:
        cursor.execute("INSERT INTO books (bookid, title, author, quantity, price, pubid) VALUES (1, :title, :author, :quantity, :price, :pub_id)", title=title, author=author, quantity=quantity, price=price, pub_id=pub_id)
    connection.commit()
    print("Book added successfully.")

# Function to add a member
def add_member():
    cursor = connection.cursor()
    name = input("Enter member name: ")
    email = input("Enter member email: ")
    phnum = input("Enter member phone number: ")
    try:
        cursor.execute("INSERT INTO member (membid, name, email, phnum) VALUES (member_sequence.nextval, :name, :email, :phnum)", name=name, email=email, phnum=phnum)
    except:
        cursor.execute("INSERT INTO member (membid, name, email, phnum) VALUES (1, :name, :email, :phnum)", name=name, email=email, phnum=phnum)
    connection.commit()
    print("Member added successfully.")

# Function to add a publisher
def add_publisher():
    cursor = connection.cursor()
    name = input("Enter publisher name: ")
    address = input("Enter publisher address: ")
    try:
        cursor.execute("INSERT INTO publisher (pubid, name, address) VALUES (publisher_sequence.nextval, :name, :address)", name=address, address=name)
    except:
        cursor.execute("INSERT INTO publisher (pubid, name, address) VALUES (1, :name, :address)", name=address, address=name)
    connection.commit()
    print("Publisher added successfully.")

# Function to issue a book
def issue_book():
    cursor = connection.cursor()
    book_id = int(input("Enter book ID: "))
    member_id = int(input("Enter member ID: "))

    # Check if the book is available
    cursor.execute("SELECT quantity FROM books WHERE bookid = :book_id", book_id=book_id)
    result = cursor.fetchone()
    if result is None:
        print("Book does not exist.")
        return

    quantity = result[0]
    if quantity <= 0:
        print("Book is currently not available.")
        return

    # Update the quantity and insert the borrowed record
    cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE bookid = :book_id", book_id=book_id)
    cursor.execute("INSERT INTO borrowed (bookid, duedate, issuedate, membid) VALUES (:book_id, sysdate + 14, sysdate, :member_id)", book_id=book_id, member_id=member_id)
    connection.commit()
    print("Book issued successfully.")

# Function to return a book
def return_book():
    cursor = connection.cursor()
    book_id = int(input("Enter book ID: "))
    member_id = int(input("Enter member ID: "))

    # Check if the book is borrowed by the member
    cursor.execute("SELECT * FROM borrowed WHERE bookid = :book_id AND membid = :member_id", book_id=book_id, member_id=member_id)
    result = cursor.fetchone()
    if result is None:
        print("No such issued book found.")
        return

    # Calculate the fine
    issued_date = result[3].date()
    return_date = datetime.date.today()
    fine_per_day = 10

    days_diff = (return_date - issued_date).days
    fine = fine_per_day * days_diff

    # Update the returned column, calculate fine, and increase quantity
    cursor.execute("UPDATE borrowed SET returned = 1, returndate = :return_date, fine = :fine WHERE bookid = :book_id AND membid = :member_id", return_date=return_date, fine=fine, book_id=book_id, member_id=member_id)
    cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE bookid = :book_id", book_id=book_id)
    connection.commit()
    print("Book returned successfully. Fine: Rs.", fine)

# Function to display all books
def display_books():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    result = cursor.fetchall()
    if not result:
        print("No books found.")
        return

    print("Books:")
    for row in result:
        print(f"Book ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Quantity: {row[3]}, Price: {row[4]}, Publisher ID: {row[5]}")

# Function to display members table
def display_members():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM member")
    result = cursor.fetchall()
    if not result:
        print("No members found.")
        return

    print("Members:")
    for row in result:
        print(f"Member ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Phone Number: {row[3]}")

# Function to display publisher table
def display_publishers():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM publisher")
    result = cursor.fetchall()
    if not result:
        print("No publishers found.")
        return

    print("Publishers:")
    for row in result:
        print(f"Publisher ID: {row[0]}, Name: {row[1]}, Address: {row[2]}")

# Function to display borrowed table
def display_borrowed():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM borrowed")
    result = cursor.fetchall()
    if not result:
        print("No borrowed books found.")
        return

    print("Borrowed Books:")
    for row in result:
        book_id = row[0]
        due_date = row[1]
        return_date = row[2]
        issue_date = row[3]
        fine = row[4]
        member_id = row[5]
        cursor.execute("SELECT title FROM books WHERE bookid = :book_id", book_id=book_id)
        book_title = cursor.fetchone()[0]
        cursor.execute("SELECT name FROM member WHERE membid = :member_id", member_id=member_id)
        member_name = cursor.fetchone()[0]
        print(f"Book ID: {book_id}, Title: {book_title}, Member ID: {member_id}, Member Name: {member_name}")
        print(f"Issue Date: {issue_date}, Due Date: {due_date}, Return Date: {return_date}, Fine: {fine}")

# Main menu
while True:
    print("\nLibrary Management System")
    print("1. Add book")
    print("2. Add member")
    print("3. Add publisher")
    print("4. Issue a book")
    print("5. Return a book")
    print("6. List all books")
    print("7. Display members")
    print("8. Display publishers")
    print("9. Display borrowed books")
    print("10. Exit")

    choice = input("Enter your choice (1-10): ")
    
    if choice == '1':
        add_book()
    elif choice == '2':
        add_member()
    elif choice == '3':
        add_publisher()
    elif choice == '4':
        issue_book()
    elif choice == '5':
        return_book()
    elif choice == '6':
        display_books()
    elif choice == '7':
        display_members()
    elif choice == '8':
        display_publishers()
    elif choice == '9':
        display_borrowed()
    elif choice == '10':
        break
    else:
        print("Invalid choice. Please try again.")

# Close the connection
connection.close()
