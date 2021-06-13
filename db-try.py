import psycopg2

connection = psycopg2.connect(user = "bilalk",
host = "localhost",
port = "5432",
database = "todolist")

cursor = connection.cursor()
postgres_insert_query = """ INSERT INTO users (user_name, first_name, password) VALUES (%s,%s,%s)"""
record_insert = ('bilalkhann', 'Bilal', 'bilal123')  #writing to the database
cursor.execute(postgres_insert_query, record_insert)
connection.commit()
count = cursor.rowcount
print ('rowcount',count)