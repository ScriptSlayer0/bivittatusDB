import BivittatusDB as bdb
#WIP
def update_tb():
    try:
        # Inicializa la base de datos
        test_db = bdb.database("test").init()
        print("Base de datos inicializada:", test_db)

        # Intentar cargar la tabla
        try:
            tb1 = test_db.load_table("table1")  # Usa load_table para obtener la tabla
            print("Tabla cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar la tabla: {e}")
            return

        # Imprimir el contenido actual de tb1
        print("Contenido actual de tb1:")
        print(tb1)

        # Actualizar el nombre "Cindy" a "Chloe" solo si el nombre actual es "Cindy"
        try:
            for row_id in tb1.keys():  # Itera sobre todos los ids en la tabla
                if tb1[row_id]["name"] == "Cindy":
                    tb1[row_id] = ("Chloe",)  # Actualiza solo el nombre, preservando el ID
            print("Después de actualizar 'Cindy' a 'Chloe':")
        except Exception as e:
            print(f"Error al actualizar 'Cindy' a 'Chloe': {e}")
        
        print(tb1)

        # Establecer todos los nombres a "new_name"
        try:
            for row_id in tb1.keys():  # Itera sobre todos los ids en la tabla
                tb1[row_id] = ("new_name",)  # Actualiza solo el nombre, preservando el ID
            print("Después de actualizar todos los nombres a 'new_name':")
        except Exception as e:
            print(f"Error al actualizar todos los nombres a 'new_name': {e}")
        
        print(tb1)

        # Función para actualizar el nombre y guardar cambios opcionalmente
        def update_name():
            print("Datos actuales en la tabla:")
            print(tb1)

            # Obtener el ID de la fila a actualizar
            try:
                id_to_update = int(input("Introduce el ID de la fila que deseas actualizar: "))
            except ValueError:
                print("Formato de ID inválido.")
                return

            # Obtener el nuevo nombre del usuario
            new_name = input("Introduce el nuevo nombre: ")

            # Actualizar el nombre en la tabla
            try:
                if id_to_update in tb1:
                    # Verificar el nombre actual antes de actualizar
                    current_name = tb1[id_to_update]["name"]
                    if current_name:  # Solo actualiza si el nombre actual existe
                        tb1[id_to_update] = (new_name,)
                        print("Tabla actualizada:")
                        print(tb1)
                    else:
                        print("No se puede actualizar, nombre actual no encontrado.")
                else:
                    print("ID no encontrado en la tabla.")
            except Exception as e:
                print(f"Error al actualizar el nombre: {e}")

            # Preguntar al usuario si desea guardar los cambios
            try:
                save = input("¿Deseas guardar los cambios? (sí/no): ").strip().lower()
                if save == 'sí':
                    test_db.save(tb1)  # Guardar cambios en la base de datos
                    print("Los cambios han sido guardados.")
                else:
                    print("Los cambios no han sido guardados.")
            except Exception as e:
                print(f"Error al guardar: {e}")

        # Llamar a la función de actualización si es necesario
        update_name()

    except Exception as e:
        print(f"Error en la actualización de la tabla: {e}")