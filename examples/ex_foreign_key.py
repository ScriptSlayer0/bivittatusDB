#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except bdb.BDBException.DeletionError: pass

#initialize the database
test_db=bdb.Database("test").init()

#create a new table 
tb2=test_db.new_table("table2", 
                       ("id", "name"), 
                       (int, str), 
                       "id")

tb2@bdb.ON # Necissary for the referenced table or the refrencer reads wrong data

#create a new table 
tb1=test_db.new_table("table1", 
                       ("id", "name"), 
                       (int, str), 
                       "id",
                       ["table2", bdb.PRIMARY, bdb.PRIMARY]) #"id" of table1 is a foreign key to "id" of "table2"

tb1@bdb.ON # Necissary for the referenced table or the refrencer reads wrong data


tb2+(3, "Cindy")
tb1+(3, None)

#Set the name change id 3 to 2
tb2["id"] = (tb2["id"]==3, 2)

#refresh and print 
print(~tb1)
print(~tb2)

#uncomment the lines below to see an example error for 
#tb1+(1, "Python")
#tb1+(2, "Java")