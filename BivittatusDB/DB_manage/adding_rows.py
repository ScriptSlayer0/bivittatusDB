#Be carefull manipulating this module works good for this example of table
import BivittatusDB as bdb

def add_names_to_db():
    #drop pre-existing databases (for best practices and to avoid errors)
    try: bdb.drop("test")
    except: pass

    #initialise the database
    test_db=bdb.database("test").init()

    #create a new table 
    tb1=test_db.New_table("table1", #name "table1")
                        ("id", "name"), #columns are named "id" and "name".
                        (int(), str()), #id contains int, and name contains str
                        "id") #id will be the #primary key

    #initialize id4
    id = 1

    while True:
        #ask for a name
        name = input("Enter a name to add to the table (or 'exit' to end): ")
        
        #break loop if user wants to quit
        if name.lower() == 'exit':
            break

        #add row to table
        tb1+(id, name)
        
        #increment id
        id += 1
    print(tb1)
    bdb.save(tb1)