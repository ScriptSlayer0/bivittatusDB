import BivittatusDB as bdb

def add_names_to_db():
    #drop pre-existing databases (for best practice and to prevent errors)
    try: bdb.drop("test")
    except: pass

    #initialize the database
    test_db=bdb.database("test").init()

    #create a new table 
    tb1=test_db.New_table("table1", #name "table1"
                           ("id", "name"), #columns are called "id" and "name"
                           (int(), str()), #id holds int, and name holds str
                           "id") #id will be the primary key

    #add rows to the table
    i = 1
    while True:
        name = input("Enter a name (or 'exit' to finish): ")
        if name.lower() == 'exit':
            break
        tb1+(i, name)
        i += 1

    bdb.save(tb1)
    print(tb1)

# Call the function
add_names_to_db()
