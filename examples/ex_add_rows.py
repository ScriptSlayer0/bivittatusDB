#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except bdb.BDBException.DeletionError: pass

#initialize the database
test_db=bdb.Database("test").init()

#create a new table 
tb1=test_db.new_table("table1", #name "table1"
                       ("id", "name"), #columns are called "id" and "name"
                       (int, str), #id holds int, and name holds str
                       "id") #id will be the primary key

#add rows to the table
tb1+(1, "Alice") 
tb1+(2, "Bob")
print((3, "Cindy"), file=tb1) # tables are now writable too!