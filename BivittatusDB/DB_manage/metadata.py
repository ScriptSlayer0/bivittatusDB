import BivittatusDB as bdb

def print_metadata():
    # Ask the user if he wants to load an existing database
    db_choice = input('Do you want to load an existing database (y/n): ').strip().lower()

    # Request database folder and table name
    db_name = input('Enter the name of the database folder: ').strip()
    table_name = input('Enter the name of the table you want to load or create: ').strip()
    #Input screen cleanup

    # Initialise the database with the provided name
    test_db = bdb.database(db_name).init()

    # If the user wants to load an existing database
    if db_choice == "y":
        tb1 = test_db.load_table(table_name)
        print(f"Table '{table_name}' loaded successfully.")

        # print the table metadata (no additional rows needed)
        print(bdb.metadata(tb1))

        # Ask if the user wants to exit
        exit_choice = input("Do you want to exit (y): ").strip().lower()
        if exit_choice == "y":
            return
    else:
        print("No existing database was loaded.")

    # Additional conditional to check if the table exists
    if test_db.table_exists(table_name):
        print(f"Table “{table_name}” exists in database “{db_name}")
    else:
        print(f"The table “{table_name}” does not exist in database '{db_name}'")