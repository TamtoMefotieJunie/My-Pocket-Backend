import sqlite3
from .base_model import AbstractBaseClass
from .constants import PATH_TO_DB
from .categories import Category
from .users import User

class Expense(AbstractBaseClass):
    def __init__(self, name=None,amount=None,description=None, id=None,user_id=None,cat_id=None):
        self.id = id
        self.name = name
        self.amount = amount
        self.description = description
        self.user_id = user_id
        self.cat_id = cat_id
        # self.category=None
        # self.user=None
        # dict.__init__(self, name=name,amount=amount,description=description, id=id,user_id=None,cat_id=None)
    
        # if self.cat_id:
        #     self.get_category()
        # if self.user_id:
        #     self.get_user()
    TABLE_NAME = "Expense"
        

    def get_category(self):
        self.category = Category.read(self.cat_id)

    def get_user(self):
        self.user = User.read(self.user_id)
    def save(self):
        table_name = __class__.TABLE_NAME
        #if user exists already
        if self.id:
            query = f"UPDATE {table_name} SET name=?,amount=?,description=?,user_id=?,cat_id=? WHERE id=?"

            #establish db connection
            with sqlite3.connect(PATH_TO_DB) as connection:
                cursor = connection.cursor()

                cursor.execute(query,(self.name,self.amount,self.description,self.user_id,self.cat_id,self.id))
                connection.commit()
            #else store into database
        else:
            query = f"INSERT INTO {table_name} (name,amount,description,user_id,cat_id) VALUES(?,?,?,?,?)"

            with sqlite3.connect(PATH_TO_DB) as connection:
                cursor = connection.cursor()
                cursor.execute(query,(self.name,self.amount,self.description,self.user_id,self.cat_id,))
                connection.commit()

                statement = f"SELECT MAX(id) FROM {table_name}"
                new_id = cursor.execute(statement).fetchone()[0]
                self.id = new_id
                connection.commit()

    def read(id=None,table_name="Expense"):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()
            
        if id!=None:
            query = f"SELECT id,name,amount,description,user_id,cat_id FROM {table_name} WHERE id=?"
            result = cursor.execute(query,(id,)).fetchone()
            if result is None:
                return None

            expense = __class__(id=result[0],name=result[1],amount=result[2],description=result[3],user_id=result[4],cat_id=result[5])
            return expense

            
        else:
            query = f"SELECT * FROM {table_name}"
            results = cursor.execute(query).fetchall()

            expenses = []

            for result in results:
                expense = __class__(id=result[0],name=result[1],amount=result[2],description=result[3],user_id=result[4],cat_id=result[5])
                expenses.append(expense)
            
            return expenses
    
    def delete(id=None):
        table_name = __class__.TABLE_NAME
        with sqlite3.connect(PATH_TO_DB) as connection:
                cursor = connection.cursor()

        if id!=None:
            cursor.execute(f"DELETE FROM {table_name} WHERE id=?",(id,))
        
        else:
            cursor.execute(f"DELETE FROM {table_name}")
            connection.commit()
    
    def toJSON(self):
        return {
            "name": self.name,
            "amount":self.amount,
            "description":self.description,
            "user_id":self.user_id,
            "cat_id":self.cat_id,
            "id": self.id
        }
    
        