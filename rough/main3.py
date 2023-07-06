import oracledb
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

row = [i[0] for i in cursor.execute("select bookid from books")]
print(row)

cursor.close()
connection.close()