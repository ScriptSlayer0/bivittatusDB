import traceback
import BivittatusDB as bdb
from DB_manage.funtions.common.list_dir_pydb import list_pydb
from DB_manage.funtions.common.saving import save_table
from DB_manage.funtions.common.user_interaction_common import get_db_choice
from bdb_aggregate import delay, pause_and_clean
from typing import List, Any, Callable, Optional

# Function to capture user input with validation
def get_input(prompt: str, valid_options: Optional[List[str]] = None, convert_func: Optional[Callable] = None) -> Any:
    # Infinite loop until the user enters a valid option
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'exit':
            # If the user types ‘exit’, the function exits.
            return 'exit'
        if valid_options and user_input not in valid_options:
            # If the options are valid but the user enters something incorrect, it displays an error message.
            print(f"Invalid input. Please enter one of the following options: {', '.join(valid_options)}")
        else:
            if convert_func:
                try:
                    # Attempts to convert user input according to the function provided.
                    return convert_func(user_input)
                except ValueError:
                    # If the conversion fails, it displays an error message.
                    print(f"Invalid entry. Please enter a valid {convert_func.__name__}.")
            else:
                # If no conversion function is provided, returns the input as it is
                return user_input

# Initialises the database and the selected table
def initialize_table(db_name: str, table_name: str) -> Optional[Any]:
    try:
        print(f"Initializing database: {db_name}")
        db = bdb.Database(db_name).init()
        print(f"Loading table: {table_name}")
        table = db(table_name)
        print(f"Table '{table_name}' successfully loaded.")
        return table
    except Exception as e:
        # If an error occurs during initialisation, displays the error message and returns None
        print(f"Error loading table: {e}")
        traceback.print_exc()
        return None

# Updates a specific row in the table
def update_row(table: List[List[Any]], id_to_update: int, new_name: str) -> bool:
    # Scrolls through each row of the table
    for row in table:
        if row[0] == id_to_update:
            # If it finds the row with the specified ID, it updates the name.
            row[1] = new_name
            return True
    # If row not found, returns False
    return False

# Updates the table with the new name based on the ID
def update_table(table: List[List[Any]]) -> None:
    while True:
        pause_and_clean(0)
        # Displays the current table
        print("Current table:")
        print(table)

        # Asks the user for the ID of the row to be updated
        id_to_update = get_input("Enter the row ID of the row you want to update or type ‘exit’ to stop: ", convert_func=int)
        if id_to_update == 'exit':
            # If the user types ‘exit’, it exits the loop.
            print("Exiting data entry.")
            break

        # Ask the user for the new name
        new_name = get_input("Enter the new name: ")
        if new_name == 'exit':
            # If the user types ‘exit’, it exits the loop.
            print("Exiting data entry.")
            break

        try:
            # Try to update the row with the new name
            if update_row(table, id_to_update, new_name):
                pause_and_clean(0)
                # Displays the updated table
                print("Updated table:")
                print(table)
                pause_and_clean(1.2)
            else:
                # If it does not find the row with the specified ID, it displays an error message.
                print(f"No row found with ID {id_to_update}.")
        except Exception as e:
            # If an error occurs during the update, it displays the error message
            print(f"Error updating the table: {e}")
            traceback.print_exc()
            pause_and_clean(1)

# Manages the update of the database dashboard
def update_database_table() -> None:
    try:
        # Asks the user if he/she wants to continue with the update
        db_choice = get_db_choice()

        if db_choice == "y":
            # Ask the user for the database directory
            db_directory = get_input("Enter the database directory: ")
            if db_directory == 'exit':
                # If the user types ‘exit’, cancels the operation.
                print("Operation cancelled.")
                return

            # Gets the directory and available tables
            db_directory, tables = list_pydb(db_directory)
            if not tables:
                # If no tables are available, cancel the operation.
                print("Transaction cancelled or error when listing tables.")
                return

            # Displays available tables
            print("Available tables:", ", ".join(tables))
            # Asks the user for the name of the table to be loaded
            table_name = get_input("Enter the name of the table you wish to load: ", valid_options=tables)
            if table_name == 'exit':
                # If the user types ‘exit’, cancels the operation.
                print("Operation cancelled.")
                return

            # Displays the selected database and table
            print(f"Selected database: {db_directory}, tabla: {table_name}")
            # Initialises the table
            table = initialize_table(db_directory, table_name)
            if table is None:
                # If the table cannot be initialised, an error message is displayed.
                print("Error: Table could not be initialized.")
                return

            # Update the table
            update_table(table)
            # Save the updated table
            save_table(table)

        else:
            # If the user does not wish to continue, it displays an error message.
            print("Invalid choice. Exiting.")
            return

    except Exception as e:
        # If a general error occurs, it displays the error message
        print(f"General error: {e}")
        traceback.print_exc()
        delay(2)

if __name__ == "__main__":
        # Main entry point
    update_database_table()
