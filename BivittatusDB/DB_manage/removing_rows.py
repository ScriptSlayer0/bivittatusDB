import traceback  # Importamos el módulo traceback
from DB_manage.funtions.common.common_db_operations import get_table_from_db
from DB_manage.funtions.removing.rm_rows import remove_rows_from_table
from DB_manage.funtions.common.saving import save_table

def remove_rows():
    """
    Función principal para eliminar filas de una tabla.
    Obtiene la tabla, elimina filas según los criterios definidos y guarda los cambios.
    """
    try:
        # Obtener la tabla desde la base de datos
        tb1 = get_table_from_db()
        if tb1 is None:
            print("Error: No se pudo obtener la tabla desde la base de datos.")
            return

        # Eliminar filas de la tabla
        remove_rows_from_table(tb1)

        # Mostrar el resultado final
        print("Tabla resultante:")
        print(tb1)

        # Guardar la tabla modificada
        save_table(tb1)
        print("Tabla guardada correctamente.")

    except ValueError as ve:
        # Capturamos el traceback para errores de validación
        traceback_details = traceback.format_exc()
        print(f"Error de validación: {ve}\nTraceback:\n{traceback_details}")
    except IOError as ioe:
        # Capturamos el traceback para errores de E/S
        traceback_details = traceback.format_exc()
        print(f"Error de E/S al guardar la tabla: {ioe}\nTraceback:\n{traceback_details}")
    except Exception as e:
        # Capturamos el traceback para errores inesperados
        traceback_details = traceback.format_exc()
        print(f"Error inesperado: {e}\nTraceback:\n{traceback_details}")

def main():
    """
    Función principal del script.
    """
    print("Iniciando proceso de eliminación de filas...")
    remove_rows()
    print("Proceso completado.")

if __name__ == "__main__":
    main()