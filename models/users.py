import sqlite3
import json
from base_model import AbstractBaseClass
from exceptions import ModelNotFoundError
from constants import PATH_TO_DB
 
class User(AbstractBaseClass):
    TABLE_NAME = "User"
    def __init__(self,id=None,name=None,email=None,password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
    
    def save(self):
        table_name = __class__.TABLE_NAME
        #if user exists already
        if self.id:
            query = f"UPDATE {table_name} SET name=?,email=?,password=? WHERE id=?"

            #establish db connection
            with sqlite3.connect(PATH_TO_DB) as connection:
                cursor = connection.cursor()

                cursor.execute(query,(self.name,self.email,self.password,self.id))
                connection.commit()
            
        #else store into database
        query = f"INSERT INTO {table_name} (name,email,password) VALUES(?,?,?)"

        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()
            cursor.execute(query,(self.name,self.email,self.password))

            statement = f"SELECT MAX(id) FROM {table_name}"
            new_id = cursor.execute(statement).fetchone()
            self.id = new_id
            connection.commit()

    def read(id=None,table_name="User"):
        # table_name = __class__.TABLE_NAME
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()
            if id !=None:    
                query = f"SELECT id, name, email, password FROM {table_name} WHERE id=?"
                result = cursor.execute(query, (id,)).fetchone()

                if result is None:
                    return None  # User not found in the database

                user = __class__(id=result[0], name=result[1], email=result[2], password=result[3])
                return user
            else:
                query = f"SELECT * FROM {table_name}"
                results = cursor.execute(query).fetchall()
                
                users = []

                for result in results:
                    user = __class__(id = result[0],name=result[1],email=result[2],password=result[3])

                    users.append(user)
                    
                return users
        
    def delete(id=None,):
        table_name = __class__.TABLE_NAME
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()

            if id!=None:
                cursor.execute(f"DELETE FROM {table_name} WHERE id=?",(id,))
                
                
            else:
                cursor.execute(f"DELETE FROM {table_name}")
                
            connection.commit()
        # self.id = None
    

    def toJSON(self):
        return {
            "name": self.name,
            "email":self.email,
            "password":self.password,
            "id": self.id
        }

        