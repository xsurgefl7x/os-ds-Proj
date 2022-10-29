from productDB import ProductDB
from userDB import UserDB

#making an object creates the database if a database doesn't already exist
product = ProductDB()
product.create_product('Water', 1200, 5, 2.00)
product.create_product('Sandwich', 1201, 3, 5.00)
print("Database: ")
print(product.fetch_all())

print("Search: Water")
print(product.search_DB('Water'))

print("Remove: Sandwich")
product.remove_product('Sandwich')
print("Edit: Water")
product.edit_product('Water', 'Price', 1.00)

print("New Database:")
print(product.fetch_all())

#always close
product.close_DB()

user = UserDB()
user.create_user('John', 'Doe', 'jd1', 'password', 'user')
user.create_user('Jane', 'Doe', 'jd2', 'password', 'admin')
print("Database: ")
print(user.fetch_all())
print("Search: jd2")
print(user.search_DB('jd2'))
print("Remove: jd1")
user.remove_user('jd1')
print("Database: ")
print(user.fetch_all())
print("Edit: jd2")
user.edit_user('jd2', 'Password', 'pass')
print("Database: ")
print(user.fetch_all())
user.close_DB()
