import oracledb

oracledb.init_oracle_client()

username = "DARSHNI"
password = "darshni_1912"
host = "localhost"
port = 1521
service_name = "XE"

dsn = f"{username}/{password}@{host}:{port}/{service_name}"
connection = oracledb.connect(dsn=dsn)
cursor = connection.cursor()

while 1:
    print("1. ADD BOOK")
    print("2. ADD MEMBER")
    print("3. ISSUE A BOOK")
    print("4. LIST ALL BOOKS")
    print("5. EXIT")
    ch = int(input("Enter choice (1-4): "))

    if (ch == 1):

        

        bookid = int(input("Enter book ID: "))
        title = input("Enter title of the book: ")
        author = input("Enter author's name: ")
        price = int(input("Enter the price: "))

        cursor.execute(f"INSERT INTO BOOKS VALUES ({bookid}, '{title}', '{author}', {price})")

    elif (ch == 2):
        pass
    elif (ch == 3):
        pass
    elif (ch == 4):
        pass
    elif (ch == 5):
        print("THANK YOU")
        break
    else:
        print("Wrong choice.")

cursor.close()
connection.close()