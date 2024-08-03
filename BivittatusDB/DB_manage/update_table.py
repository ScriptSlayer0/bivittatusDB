import BivittatusDB as bdb

# Drop pre-existing databases (for best practice and to prevent errors)
# try:
#     bdb.drop("test")
# except:
#     pass

# Initialize the database
def update_tb():
    test_db = bdb.database("test").init()

    # Make a new table
    tb1 = test_db.New_table("table1", 
                            ("id", "name"), 
                            (int(), str()), 
                            "id",
                            None)

    # Add data to the table
    tb1 + (1, "Alice")
    tb1 + (2, "Bob")
    tb1 + (3, "Cindy")

    print(tb1)

    # Example updates
    # Set the name "Cindy" to "Chloe"
    tb1[1] = ("Chloe", tb1["name"] == "Cindy")

    print(tb1)

    # Set all names to "new_name"
    tb1["name"] = ("new_name", bdb.ALL)

    print(tb1)

    # Function to update name and optionally save changes
    def update_name():
        # Print current data
        print("Current data in table:")
        print(tb1)

        # Get user input for the ID of the row to update
        id_to_update = int(input("Enter the ID of the row you want to update: "))

        # Get the new name from user
        new_name = input("Enter the new name: ")

        # Update the name in the table
        tb1[id_to_update] = (new_name, tb1["id"] == id_to_update)

        print("Updated table:")
        print(tb1)

        # Ask user if they want to save changes
        save = input("Do you want to save the changes? (yes/no): ").strip().lower()
        if save == 'yes':
            test_db.save(tb1)  # Save changes to the database
            print("Changes have been saved.")
        else:
            print("Changes have not been saved.")
