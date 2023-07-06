import oracledb
import prettytable
import datetime

oracledb.init_oracle_client()

username = "DARSHNI"
password = "darshni_1912"
host = "localhost"
port = 1521
service_name = "XE"

dsn = f"{username}/{password}@{host}:{port}/{service_name}"
connection = oracledb.connect(dsn=dsn)
connection.autocommit = True
cursor = connection.cursor()

while 1:
    print("1. ADD BOOK")
    print("2. ADD MEMBER")
    print("3. ADD PUBLISHER")
    print("4. ISSUE A BOOK")
    print("5. LIST ALL BOOKS")
    print("6. EXIT")
    ch = int(input("Enter choice (1-5): "))

    if (ch == 1):

        bookid = int(input("Enter book ID: "))
        row = [int(i[0]) for i in cursor.execute("select bookid from books")]
        if bookid in row:
            print("Book ID already exists")
            continue
        title = input("Enter title of the book: ")
        author = input("Enter author's name: ")
        quantity = int(input("Enter the number of books: "))
        price = int(input("Enter the price: "))
        pubid = int(input("Enter Publisher ID: "))

        cursor.execute(f"INSERT INTO BOOKS VALUES ({bookid}, '{title}', '{author}', {quantity}, {price}, {pubid})")

    elif (ch == 2):
        membid = int(input("Enter member ID: "))
        row = [int(i[0]) for i in cursor.execute("select membid from member")]
        if bookid in row:
            print("Member ID already exists")
            continue
        name = input("Enter member's name: ")
        email = input("Enter member's Email: ")
        phnum = int(input("Enter phone number: "))
        bookid = 0
        cursor.execute(f"INSERT INTO MEMBER VALUES ({membid}, '{name}', '{email}', {phnum}, {bookid})")
    elif (ch == 3):
        pubid = int(input("Enter publisher ID: "))
        row = [int(i[0]) for i in cursor.execute("select pubid from publisher")]
        if pubid in row:
            print("Publisher ID already exists")
            continue
        address = input("Enter address: ")
        name = input("Enter publisher's name: ")
    elif (ch == 4):
        membid = int(input("Enter your member ID: "))
        # check if member already has any pending issues
        bookid = int(input("Enter book ID: "))
        row = [i for i in cursor.execute(f"select * from books where bookid={bookid}")][0]
        print(f'''BOOK ID: {row[0]}\nBOOK TITLE: {row[1]}\nBOOK AUTHOR: {row[2]}\nAVAILABLE: {row[3]}\nPRICE: {row[4]}\nPUBLISHER ID: {row[5]}''')
        chh = input("Is this the book you requested for ? (y/n): ")
        chh = chh.lower()[0]
        if chh == 'y':
            cursor.execute(f"INSERT INTO BORROWED VALUES({row[0], })")
        else:
            continue

    elif (ch == 5):
        myTable = prettytable.PrettyTable(["BOOK ID", "BOOK TITLE", "BOOK AUTHOR", "AVAILABLE", "PRICE", "PUBLISHER_ID"])
        for i in cursor.execute("select * from books"):
            myTable.add_row(i)
        print(myTable)
    elif (ch == 6):
        print("THANK YOU")
        break
    else:
        print("Wrong choice.")

cursor.close()
connection.close()