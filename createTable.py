import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)
user = (1,'vedant','tuwani')
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query,user)

connection.commit()

connection.close()
