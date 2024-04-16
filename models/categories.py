import sqlite3
from .base_model import AbstractBaseClass
from .constants import PATH_TO_DB

class Category(AbstractBaseClass):
    def __init__(self, id=None, name=None):
        super().__init__()  # Initialize the base class
        self.id = id
        self.name = name

    TABLE_NAME = "Category"
        
    
    def save(self):
        table_name = __class__.TABLE_NAME
        #if user exists already
        if self.id:
            query = f"UPDATE {table_name} SET name=? WHERE id=?"

            #establish db connection
            with sqlite3.connect(PATH_TO_DB) as connection:
                cursor = connection.cursor()

                cursor.execute(query,(self.name,self.id))
                connection.commit()
            
            #else store into database
        else:
            query = f"INSERT INTO {table_name} (name) VALUES(?)"

            with sqlite3.connect(PATH_TO_DB) as connection:
                cursor = connection.cursor()
                cursor.execute(query,(self.name,))
                connection.commit()

                statement = f"SELECT MAX(id) FROM {table_name}"
                new_id = cursor.execute(statement).fetchone()[0]
                self.id = new_id
                connection.commit()
            

    def read(id=None,table_name="Category"):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()
            
        if id!=None:
            query = f"SELECT id,name FROM {table_name} WHERE id=?"
            result = cursor.execute(query,(id,)).fetchone()
            if result is None:
                return None
            
            category = __class__(id=result[0],name=result[1])
            return category
            
        else:
            query = f"SELECT * FROM {table_name}"
            results = cursor.execute(query).fetchall()

            categories = []

            for result in results:
                category = __class__(id=result[0],name=result[1])
                categories.append(category)
            return categories
            
    def delete(id=None):
        table_name = __class__.TABLE_NAME
        with sqlite3.connect(PATH_TO_DB) as connection:
                cursor = connection.cursor()

        if id!=None:
            cursor.execute(f"DELETE FROM {table_name} WHERE id=?",(id,))
            connection.commit()
        
        else:
            cursor.execute(f"DELETE FROM {table_name}")
            connection.commit()
    
    def toJSON(self):
        return {
            "name": self.name,
            "id": self.id
        }

    