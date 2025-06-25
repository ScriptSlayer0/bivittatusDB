class BDBException:
    class DeletionError(Exception):
        pass
    
    class ForeignKeyError(Exception):
        pass

class Table:
    def __init__(self, name, columns, data_types, primary_key, foreign_key=None):
        """
        Inicializar una tabla con columnas, tipos de datos, clave primaria y clave foránea opcional
        
        :param name: Nombre de la tabla
        :param columns: Tupla de nombres de columnas
        :param data_types: Tupla de tipos de datos correspondientes
        :param primary_key: Nombre de la columna de clave primaria
        :param foreign_key: Referencia de clave foránea opcional [tabla_referenciada, columna_referenciada, tabla_referenciada]
        """
        self.name = name
        self.columns = columns
        self.data_types = data_types
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.data = []
        self.active = False
    
    def __add__(self, row):
        """
        Agregar una fila a la tabla con validación
        """
        # Validar longitud de la fila
        if len(row) != len(self.columns):
            raise ValueError(f"La fila debe tener {len(self.columns)} elementos")
        
        # Validación de tipos
        for i, (valor, tipo_esperado) in enumerate(zip(row, self.data_types)):
            if valor is not None and not isinstance(valor, tipo_esperado):
                raise TypeError(f"La columna {self.columns[i]} espera {tipo_esperado.__name__}, se obtuvo {type(valor).__name__}")
        
        # Validación de clave foránea si está activa
        if self.foreign_key and self.active:
            ref_tabla, ref_columna, ref_tipo = self.foreign_key
            indice_pk = self.columns.index(self.primary_key)
            indice_ref_pk = ref_tipo.columns.index(ref_columna)
            
            # Verificar si la clave foránea existe en la tabla referenciada
            valor_clave_foranea = row[indice_pk]
            if valor_clave_foranea is not None:
                filas_coincidentes = [r for r in ref_tipo.data if r[indice_ref_pk] == valor_clave_foranea]
                if not filas_coincidentes:
                    raise BDBException.ForeignKeyError(f"La clave foránea {valor_clave_foranea} no existe en {ref_tabla}")
        
        self.data.append(row)
        return self
    
    def __matmul__(self, estado):
        """
        Activar/desactivar la tabla
        """
        self.active = (estado == True)
        return self
    
    def __str__(self):
        """
        Representación en cadena de la tabla
        """
        # Crear encabezado
        encabezado = " | ".join(self.columns)
        separador = "-" * len(encabezado)
        
        # Crear filas
        cadenas_filas = [" | ".join(str(val) for val in fila) for fila in self.data]
        
        return f"Tabla {self.name}:\n{encabezado}\n{separador}\n" + "\n".join(cadenas_filas)
    
    def __invert__(self):
        """
        Refrescar/recargar la tabla (simulado devolviendo el estado actual)
        """
        return self
    
    def __setitem__(self, columna, condicion):
        """
        Actualizar filas basadas en una condición
        
        :param columna: Columna a actualizar
        :param condicion: Tupla de (condicion, nuevo_valor)
        """
        # Encontrar el índice de la columna a actualizar
        indice_columna = self.columns.index(columna)
        
        # Desempaquetar la condición
        funcion_condicion, nuevo_valor = condicion
        
        # Actualizar filas que coincidan
        for i, fila in enumerate(self.data):
            if funcion_condicion(fila):
                # Crear una nueva fila con el valor actualizado
                fila_actualizada = list(fila)
                fila_actualizada[indice_columna] = nuevo_valor
                self.data[i] = tuple(fila_actualizada)
        
        return self

class Database:
    def __init__(self, name):
        """
        Inicializar una base de datos
        
        :param name: Nombre de la base de datos
        """
        self.name = name
        self.tables = {}
    
    def init(self):
        """
        Inicializar la base de datos
        """
        return self
    
    def new_table(self, name, columns, data_types, primary_key, foreign_key=None):
        """
        Crear una nueva tabla en la base de datos
        
        :param name: Nombre de la tabla
        :param columns: Tupla de nombres de columnas
        :param data_types: Tupla de tipos de datos correspondientes
        :param primary_key: Nombre de la columna de clave primaria
        :param foreign_key: Referencia de clave foránea opcional
        """
        # Manejar referencia de clave foránea
        if foreign_key:
            ref_tabla_nombre, ref_columna, ref_tabla = foreign_key
            foreign_key = [ref_tabla_nombre, ref_columna, ref_tabla]
        
        tabla = Table(name, columns, data_types, primary_key, foreign_key)
        self.tables[name] = tabla
        return tabla

def drop(nombre_base_datos):
    """
    Simular la eliminación de una base de datos
    """
    # En una implementación real, esto eliminaría la base de datos
    return True

# Simulación del módulo BivittatusDB
class BivittatusDB:
    ON = True
    PRIMARY = None
    
    @staticmethod
    def drop(nombre_base_datos):
        return drop(nombre_base_datos)
    
    class BDBException:
        DeletionError = BDBException.DeletionError
        ForeignKeyError = BDBException.ForeignKeyError

# Función de demostración
def main():
    # Simular operaciones de base de datos
    bdb = BivittatusDB()
    
    # Eliminar base de datos existente
    try: 
        bdb.drop("test")
    except bdb.BDBException.DeletionError: 
        pass
    
    # Inicializar base de datos
    test_db = Database("test").init()
    
    # Crear tabla2 primero (tabla referenciada)
    tb2 = test_db.new_table("table2", 
                             ("id", "name"), 
                             (int, str), 
                             "id")
    
    # Activar tabla2
    tb2 @ bdb.ON
    
    # Crear tabla1 con referencia de clave foránea a tabla2
    tb1 = test_db.new_table("table1", 
                             ("id", "name"), 
                             (int, str), 
                             "id",
                             ["table2", "id", tb2])
    
    # Activar tabla1
    tb1 @ bdb.ON
    
    # Agregar datos a tabla2
    tb2 + (3, "Cindy")
    
    # Agregar datos a tabla1 con referencia de clave foránea
    tb1 + (3, None)
    
    # Cambiar ID en tabla2
    tb2["id"] = (lambda fila: fila[0] == 3, 2)
    
    # Imprimir tabla
    print(tb1)
    
    # Refrescar e imprimir
    print(~tb1)

# Ejecutar la demostración si se ejecuta como script principal
if __name__ == "__main__":
    main()