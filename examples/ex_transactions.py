#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except bdb.BDBException.DeletionError: pass

#initialize the database
test_db=bdb.Database("test").init()

#create a new table
tb1=test_db.new_table("table1", 
                       ("id", "name"), 
                       (int, str), 
                       "id")

#add data to the table
tb1+(1, "Alice")
tb1+(2, "Bob")

#set savepoint
bdb.SAVEPOINT@tb1

#edit the table
tb1+(3, "Cindy")
print(tb1)

#rollback change
bdb.ROLLBACK@tb1

print(tb1)
#commit the difference
bdb.COMMIT@tb1