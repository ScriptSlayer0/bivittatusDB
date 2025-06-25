class Table:
    def __init__(self, name, columns, data_types, primary_key):
        """
        Initialize a table with columns, data types, and primary key
        
        :param name: Name of the table
        :param columns: Tuple of column names
        :param data_types: Tuple of corresponding data types
        :param primary_key: Name of the primary key column
        """
        self.name = name
        self.columns = columns
        self.data_types = data_types
        self.primary_key = primary_key
        self.data = []
        
    def add_row(self, row):
        """
        Add a row to the table with type checking
        
        :param row: Tuple of values to add
        """
        # Validate row length and types
        if len(row) != len(self.columns):
            raise ValueError(f"Row must have {len(self.columns)} elements")
        
        for i, (value, expected_type) in enumerate(zip(row, self.data_types)):
            if not isinstance(value, expected_type):
                raise TypeError(f"Column {self.columns[i]} expects {expected_type.__name__}, got {type(value).__name__}")
        
        self.data.append(row)
        return self
    
    def __add__(self, row):
        """
        Operator overloading for adding rows
        """
        return self.add_row(row)
    
    def __str__(self):
        """
        String representation of the table
        """
        # Create header
        header = " | ".join(self.columns)
        separator = "-" * len(header)
        
        # Create rows
        row_strings = [" | ".join(str(val) for val in row) for row in self.data]
        
        return f"{self.name} Table:\n{header}\n{separator}\n" + "\n".join(row_strings)
    
    def left_join(self, other_table):
        """
        Perform left join with another table
        
        :param other_table: Table to join with
        :return: List of joined rows
        """
        pk_index = self.columns.index(self.primary_key)
        other_pk_index = other_table.columns.index(other_table.primary_key)
        
        # Combine columns as a tuple
        joined_columns = self.columns + tuple(col for col in other_table.columns if col != other_table.primary_key)
        
        # Perform join
        joined_rows = []
        for self_row in self.data:
            joined = False
            for other_row in other_table.data:
                if self_row[pk_index] == other_row[other_pk_index]:
                    joined_rows.append(self_row + other_row[:other_pk_index] + other_row[other_pk_index+1:])
                    joined = True
            
            # If no match, add row with None for other table columns
            if not joined:
                joined_rows.append(self_row + (None,) * (len(other_table.columns) - 1))
        
        return joined_rows
    
    def right_join(self, other_table):
        """
        Perform right join with another table
        
        :param other_table: Table to join with
        :return: List of joined rows
        """
        return other_table.left_join(self)
    
    def full_join(self, other_table):
        """
        Perform full outer join with another table
        
        :param other_table: Table to join with
        :return: List of joined rows
        """
        pk_index = self.columns.index(self.primary_key)
        other_pk_index = other_table.columns.index(other_table.primary_key)
        
        # Combine columns as a tuple
        joined_columns = self.columns + tuple(col for col in other_table.columns if col != other_table.primary_key)
        
        # Perform join
        joined_rows = []
        used_self_ids = set()
        used_other_ids = set()
        
        # First do left join
        for self_row in self.data:
            joined = False
            for other_row in other_table.data:
                if self_row[pk_index] == other_row[other_pk_index]:
                    joined_rows.append(self_row + other_row[:other_pk_index] + other_row[other_pk_index+1:])
                    joined = True
                    used_self_ids.add(self_row[pk_index])
                    used_other_ids.add(other_row[other_pk_index])
            
            # If no match, add row with None for other table columns
            if not joined:
                joined_rows.append(self_row + (None,) * (len(other_table.columns) - 1))
                used_self_ids.add(self_row[pk_index])
        
        # Add unmatched rows from other table
        for other_row in other_table.data:
            if other_row[other_pk_index] not in used_other_ids:
                joined_rows.append((None,) * (len(self.columns) - 1) + other_row)
        
        return joined_rows

# Demonstration
def main():
    # Create tables
    table1 = Table("table1", ("id", "name"), (int, str), "id")
    table2 = Table("table2", ("id", "language"), (int, str), "id")
    
    # Add rows
    table1 + (1, "Alice")
    table1 + (2, "Bob")
    table1 + (3, "Cindy")
    
    table2 + (1, "Python")
    table2 + (2, "Java")
    table2 + (4, "C++")
    
    # Print original tables
    print("Table 1:")
    print(table1)
    print("\nTable 2:")
    print(table2)
    
    # Perform joins
    print("\nLeft Join (Table1 << Table2):")
    left_join_result = table1.left_join(table2)
    for row in left_join_result:
        print(row)
    
    print("\nRight Join (Table1 >> Table2):")
    right_join_result = table1.right_join(table2)
    for row in right_join_result:
        print(row)
    
    print("\nFull Join (Table1 ^ Table2):")
    full_join_result = table1.full_join(table2)
    for row in full_join_result:
        print(row)

if __name__ == "__main__":
    main()