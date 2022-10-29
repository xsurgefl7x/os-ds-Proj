import sqlite3

class ProductDB:
   conn = None
   cursor = None

   #sets up vars
   #sets up table
   def __init__(self):
      self.conn = sqlite3.connect('warehouse.db')
      self.cursor = self.conn.cursor()
      self.create_table()

   #creates table if table does not exist
   ###possibly add DATE to values
   def create_table(self):
      self.cursor.execute('''
         CREATE TABLE IF NOT EXISTS PRODUCTS(
         PRODUCT_NAME CHAR(20) NOT NULL UNIQUE,
         PRODUCT_ID INT,
         PRODUCT_STOCK INT,
         PRODUCT_PRICE FLOAT)''')
      try:
         self.cursor.execute('''
            CREATE UNIQUE INDEX name ON PRODUCTS (PRODUCT_NAME)''')
      except:
         pass

   #inserts data and commits
   def create_product(self, name, id, stock, price):
      try:
         self.cursor.execute('''
            INSERT OR IGNORE
            INTO PRODUCTS
            (PRODUCT_NAME, PRODUCT_ID, PRODUCT_STOCK, PRODUCT_PRICE)
            VALUES ( ?, ?, ?, ?)''', (name, id, stock, price))
         self.conn.commit()
      except:
         print("Item already in database.")

   #searchs table for product(s)
   #name: product name
   #returns a product(s) else returns []
   def search_DB(self, name):
      self.cursor.execute('''
         SELECT *
         FROM PRODUCTS
         WHERE PRODUCT_NAME = ?''', (name,))
      return self.cursor.fetchall()

   #then removes item from table
   def remove_product(self, name):
      self.cursor.execute('''
         DELETE
         FROM PRODUCTS
         WHERE PRODUCT_NAME = ?''', (name,))
      self.conn.commit()

   #name: product name
   #parm_name: parameter to be changed
   #new_val: new value to be updated
   def edit_product(self, name, parm_name, new_val):
      if parm_name == 'Name':
         try:
            self.cursor.execute('''
               UPDATE PRODUCTS
               SET PRODUCT_NAME = ?
               WHERE PRODUCT_NAME = ?
            ''', (new_val, name,))
         except:
            print("Item already in database.")
      elif parm_name == 'ID':
         self.cursor.execute('''
            UPDATE PRODUCTS
            SET PRODUCT_ID = ?
            WHERE PRODUCT_NAME = ?
         ''', (new_val, name,))
      elif parm_name == 'Stock':
         self.cursor.execute('''
            UPDATE PRODUCTS
            SET PRODUCT_STOCK = ?
            WHERE PRODUCT_NAME = ?
         ''', (new_val, name,))
      elif parm_name == 'Price':
         self.cursor.execute('''
            UPDATE PRODUCTS
            SET PRODUCT_PRICE = ?
            WHERE PRODUCT_NAME = ?
         ''', (new_val, name,))
      self.conn.commit()

   def fetch_all(self):
      self.cursor.execute('''
         SELECT *
         FROM PRODUCTS''')
      return self.cursor.fetchall()

   def close_DB(self):
      self.conn.commit()
      self.cursor.close
      self.conn.close()            
