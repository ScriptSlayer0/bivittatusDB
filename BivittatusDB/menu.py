from DB_manage.adding_rows import add_names_to_db
from DB_manage.table_view import use_table
from DB_manage.table_view import *
from utils.clean_screan import cleaning_screan
import time

def main_menu():
    cleaning_screan()
    while True:
        print("What do you want to do?")
        print("Option 1: Use table",
              "\nOption 2: Insert values in table",
              "\nOption 3: Delete values in the table",
              "\nOption 4: Exit")
        option = input("Please enter an option: ")
        if option == "1":
            try:
                cleaning_screan()
                use_table()
            except Exception as e:
                print("Exception:",e)

        elif option == "2":
            cleaning_screan()
            add_names_to_db()
            
        elif option == "3":
            print("This option is not yet implemented.")
            time.sleep(1)
            cleaning_screan()

        elif option == "4":
            print("exiting....")
            time.sleep(0.4)
            cleaning_screan()
            break

        else:
            print("Incorrect option")
main_menu()
