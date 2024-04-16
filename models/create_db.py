import os
import sqlite3

from constants import PATH_TO_DB

#check if database exists and delete it
if os.path.exists(PATH_TO_DB):
    os.unlink(PATH_TO_DB)

#if it doesn't exist, a database called db.sqlite will be created with
#the tables below
create_user_table = """CREATE TABLE User(id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT ,email VARCHAR(100),password VARCHAR(50));"""

create_category_table = """ CREATE TABLE Category(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT);"""

create_expense_table = """CREATE TABLE Expense (id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT, amount DECIMAL(10,2), description TEXT,user_id INT,cat_id INT,
FOREIGN KEY(user_id) REFERENCES User(id) ON DELETE CASCADE,
FOREIGN KEY(cat_id) REFERENCES Category(id) ON DELETE CASCADE);"""

#database connection
with sqlite3.connect(PATH_TO_DB) as connection:
    cursor = connection.cursor()

    for query in [create_user_table,create_category_table,create_expense_table]:
        cursor.execute(query)