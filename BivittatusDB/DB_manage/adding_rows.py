import BivittatusDB as bdb

def add_names_to_db():
    # Initialize the database
    test_db = bdb.database("test").init()

    # Create a new table 
    tb1 = test_db.New_table(
        "table1",            # Table name
        ("id", "name"),      # Column names
        (int(), str()),      # Column types
        "id"                 # Primary key
    )

    # Start primary key index
    i = 1

    # Add rows to the table
    while True:
        name = input("Enter a name (or 'exit' to finish): ")
        if name.lower() == 'exit':
            break
        
        # Check if the primary key already exists
        if tb1.primary_key_exists(i):
            print(f"Primary key {i} already exists. Skipping entry.")
        else:
            tb1.add((i, name))
            print(f"Added ({i}, {name})")
            i += 1

    # Save the table to the database
    test_db.save(tb1)  # Save using the database instance, not bdb directly
    print("Table saved.")
    print(tb1)