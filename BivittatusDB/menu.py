import BivittatusDB as bdb
from DB_manage.adding_rows import add_names_to_db
from DB_manage.table_view import use_table
from DB_manage.table_view import *

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
