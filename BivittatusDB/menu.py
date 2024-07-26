import BivittatusDB as bdb
from DB_manage.table_view import use_table
from DB_manage.table_view import *

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

def main_menu():
    while True:
        print("¿Qué quieres hacer?")
        print("Opción 1: Usar tabla",
              "Opción 2: Insertar valores en la tabla",
              "Opción 3: Eliminar valores en la tabla")
        opcion = input("Introduce una opción por favor: ")
        if opcion == "1":
            use_table()
        elif opcion == "2":
            add_names_to_db()
        elif opcion == "3":
            print("Esta opción aún no está implementada.")
        else:
            print("Opción incorrecta")

main_menu()
