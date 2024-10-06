class MyMatrix:
    def __init__(self, rows=None, cols=None):
        """
        Initializes a sparse matrix with the specified number of rows and columns.
        Uses a dictionary to store non-zero elements for memory efficiency.
        """
        self.numRows = rows
        self.numCols = cols
        self.elements = {}  # Dictionary to store non-zero elements

    @staticmethod
    def get_matrix(matrixFilePath):
        """ Reads a sparse matrix from the input file. """
        matrix = MyMatrix()
        with open(matrixFilePath, 'r') as f:
            lines = f.readlines()
            matrix.numRows = int(lines[0].split('=')[1])
            matrix.numCols = int(lines[1].split('=')[1])

            for line in lines[2:]:
                line = line.strip()
                if not line or not line.startswith('('):
                    continue
                try:
                    row, col, value = map(int, line.strip('()').split(','))
                    matrix.set_element(row, col, value)
                except ValueError:
                    raise ValueError("Input file has wrong format")
        return matrix

    def set_element(self, row, col, value):
        """ Sets the value in the matrix if non-zero. """
        if row >= self.numRows or col >= self.numCols:
            raise ValueError("Index out of bounds")
        if value != 0:
            self.elements[(row, col)] = value

    def get_element(self, row, col):
        """ Retrieves the element at a given position. """
        return self.elements.get((row, col), 0)

    def add(self, other):
        """ Adds two sparse matrices. """
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions not matching for addition")

        result = MyMatrix(self.numRows, self.numCols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value + other.get_element(row, col))
        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.set_element(row, col, value)
        return result

    def subtract(self, other):
        """ Subtracts another sparse matrix from the current matrix. """
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions not matching for subtraction")

        result = MyMatrix(self.numRows, self.numCols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value - other.get_element(row, col))
        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.set_element(row, col, -value)
        return result

    def multiply(self, other):
        """ Multiplies two sparse matrices. """
        if self.numCols != other.numRows:
            raise ValueError("Matrix dimensions not matching for multiplication")

        result = MyMatrix(self.numRows, other.numCols)
        for (row1, col1), value1 in self.elements.items():
            for col2 in range(other.numCols):
                value2 = other.get_element(col1, col2)
                if value2 != 0:
                    current_val = result.get_element(row1, col2)
                    result.set_element(row1, col2, current_val + value1 * value2)
        return result

    def display(self):
        """ Displays the non-zero elements of the matrix. """
        for (row, col), value in sorted(self.elements.items()):
            print(f"({row}, {col}, {value})")


# Usage example
matrix1 = MyMatrix.get_matrix('../../sample_inputs/easy_sample_01_2.txt')
matrix2 = MyMatrix.get_matrix('../../sample_inputs/easy_sample_01_3.txt')

# Addition, Subtraction, and Multiplication
result_add = matrix1.add(matrix2)
result_sub = matrix1.subtract(matrix2)
result_mul = matrix1.multiply(matrix2)

# Displaying outputs
print("Addition Output:")
result_add.display()

print("\nSubtraction Output:")
result_sub.display()

print("\nMultiplication Output:")
result_mul.display()
