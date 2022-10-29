import sqlite3

class UserDB:
   cursor = None
   conn = None

   #sets up vars
   def __init__(self):
      self.conn = sqlite3.connect('warehouse.db')
      self.cursor = self.conn.cursor()
      self.create_table()

   #creates table if table does not exist
   ###possibly add DATE to values
   def create_table(self):
      self.cursor.execute('''
          CREATE TABLE IF NOT EXISTS USERS(
          FIRST_NAME CHAR(20) NOT NULL,
          LAST_NAME CHAR(20) NOT NULL,
          USER_ID CHAR(5) NOT NULL UNIQUE,
          USER_PASSWORD CHAR(20) NOT NULL,
          USER_TYPE CHAR(5)
      )''')
      try:
         self.cursor.execute('''
            CREATE UNIQUE INDEX id ON USERS (USER_ID)''')
      except:
         pass

   def create_user(self, firstName, lastName, id, password, type):
      try:
         self.cursor.execute('''
            INSERT OR IGNORE
            INTO USERS
            (FIRST_NAME, LAST_NAME, USER_ID, USER_PASSWORD, USER_TYPE)
            VALUES ( ?, ?, ?, ?, ?)''', (firstName, lastName, id, password, type))
         self.conn.commit()
      except:
         print("Item already in database.")
          
   #searchs table for user
   #id: user id
   #returns a user else returns []
   def search_DB(self, id):
      self.cursor.execute('''
         SELECT *
         FROM USERS
         WHERE USER_ID = ?''', (id,))
      return self.cursor.fetchall()

   #then removes item from table
   def remove_user(self, id):
      self.cursor.execute('''
         DELETE
         FROM USERS
         WHERE USER_ID = ?''', (id,))
      self.conn.commit()

   #id: user id
   #parm_name: parameter to be changed
   #new_val: new value to be updated
   def edit_user(self, id, parm_name, new_val):
      if parm_name == 'User ID':
         try:
            self.cursor.execute('''
               UPDATE USERS
               SET USER_ID = ?
               WHERE USER_ID = ?
            ''', (new_val, id,))
         except:
            print("Item already in database.")
      elif parm_name == 'First Name':
         self.cursor.execute('''
            UPDATE USERS
            SET FIRST_NAME = ?
            WHERE USER_ID = ?
         ''', (new_val, id,))
      elif parm_name == 'Last Name':
         self.cursor.execute('''
            UPDATE USERS
            SET LAST_NAME = ?
            WHERE USER_ID = ?
         ''', (new_val, id,))
      elif parm_name == 'Password':
         self.cursor.execute('''
            UPDATE USERS
            SET USER_PASSWORD = ?
            WHERE USER_ID = ?
         ''', (new_val, id,))
      elif parm_name == 'User Type':
         self.cursor.execute('''
            UPDATE USERS
            SET USER_TYPE = ?
            WHERE USER_ID = ?
         ''', (new_val, id,))
      self.conn.commit()

   def fetch_all(self):
      self.cursor.execute('''
         SELECT *
         FROM USERS''')
      return self.cursor.fetchall()

   def close_DB(self):
      self.conn.commit()
      self.cursor.close
      self.conn.close()
