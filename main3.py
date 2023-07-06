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

for row in cursor.execute("select * from books"):
    print(row)

cursor.close()
connection.close()