from DB_manage.adding_rows import add_names_to_db
from DB_manage.table_view import use_table
from DB_manage.table_view import *

def main_menu():
    while True:
        print("What do you want to do?")
        print("Option 1: Use table",
              "\nOption 2: Insert values in table",
              "\nOption 3: Delete values in the table")
        option = input("Please enter an option: ")
        if option == "1":
            use_table()
        elif option == "2":
            add_names_to_db()
        elif option == "3":
            print("This option is not yet implemented.")
        else:
            print("Incorrect option")
main_menu()
