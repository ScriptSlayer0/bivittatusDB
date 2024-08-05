import BivittatusDB as bdb

# Initialize the database
def update_tb():
    test_db = bdb.database("test").init()
    tb1 = test_db.load_table("table1")

    def get_valid_input(prompt, valid_options=None, convert_func=None):
        while True:
            user_input = input(prompt).strip()
            if user_input.lower() == 'exit':
                return 'exit'
            if valid_options and user_input not in valid_options:
                print(f"Invalid input. Please enter one of the following: {', '.join(valid_options)}")
                continue
            if convert_func:
                try:
                    user_input = convert_func(user_input)
                except ValueError:
                    print(f"Invalid input. Please enter a valid {convert_func.__name__}.")
                    continue
            return user_input

    # Loop to allow user to update data or exit
    while True:
        id_to_update = get_valid_input("Enter the id of the row you want to update or type 'exit' to stop: ", convert_func=int)
        
        if id_to_update == 'exit':
            print("Exiting data entry.")
            break

        new_name = get_valid_input("Enter the new name: ")
        
        if new_name == 'exit':
            print("Exiting data entry.")
            break

        # Update the table based on user input
        tb1["name"] = (new_name, tb1["id"] == id_to_update)

        print("Updated table:")
        print(tb1)

        while True:
            answer = input("Do you want to save this table? (y/n): ").strip().lower()
            if answer == "y":
                bdb.save(tb1)  # Save the table using bdb.save function
                print("Table saved successfully.")
                break  # Exit the loop after saving the table
            elif answer == "n":
                print("You chose not to save this table.")
                break  # Exit the loop after deciding not to save the table
            else:
                print("Choose a correct option (y/n).")