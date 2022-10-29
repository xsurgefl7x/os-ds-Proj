import Pyro4
from productDB import ProductDB

#DBcall: a list of needed parms
def process(db, DBcall):
   function = DBcall[1]
   if function == "Create":
      db.create_product(DBcall[2], DBcall[3], DBcall[4], DBcall[5])
      result = "Product created."
   elif function == "Search":
      result = db.search_DB(DBcall[2])
   elif function == "Remove":
      db.remove_product(DBcall[2])
      result = "Product removed."
   elif function == "Change":
      db.edit_product(DBcall[2], DBcall[3], DBcall[4])
      result = "Product was changed."
   elif function == "DB":
      result = db.fetch_all()
   return result

def main():
   o = Pyro4.Proxy("PYRO:server@ipaddress:55555")
   db = ProductDB()
   print("Getting work from dispatcher.")
   while True:
      try:
         call = o.getWork()
      except ValueError:
         print("no work available yet")
      else:
         result = process(db, call)
         o.putResult(result)

if __name__ == "__main__":
   main()
