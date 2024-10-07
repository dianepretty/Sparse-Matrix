import sys

class MyMatrix:
    def __init__(self, rows=None, cols=None):
        self.numRows = rows
        self.numCols = cols
        self.elements = {}  # dictionary to store non-zero elements (rows, col): value

    @staticmethod
    def readFile(matrixFilePath):
        """ Reads the sparse matrix from the input file """
        matrix = MyMatrix()
        with open(matrixFilePath, 'r') as f:
            lines = f.readlines()
            matrix.numRows = int(lines[0].split('=')[1])
            matrix.numCols = int(lines[1].split('=')[1])

            for line in lines[2:]:
                line = line.strip()
                if not line or not line.startswith('(')     :
                    print(f"Unkown formart on line: {line}")
                    sys.exit()
                try:
                    row, col, value = map(int, line.strip('()').split(','))
                    matrix.set_element(row, col, value)
                except ValueError:
                    raise ValueError("Unkown formart on line: {line}")
        return matrix

    def set_element(self, row, col, value):
        """ Setting the value in the matrix"""
        try:
            if row >= self.numRows or col >= self.numCols:
                return
            if value != 0:
                self.elements[(row, col)] = value
        except Exception as e:
            print(f"An error occurred while setting the element: {e}")

    def get_element(self, row, col):
        """ Retrieves the element at a given position """
        return self.elements.get((row, col), 0)

    def matrixAddition(self, other):
        """ Addition of matrices """
        if self.numRows != other.numRows or self.numCols != other.numCols:
            print("Matrix dimensions not matching for addition.")
            return None

        result = MyMatrix(self.numRows, self.numCols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value + other.get_element(row, col))
        for (row, col), value in other.elements.items():
            result.set_element(row, col, value)
        return result

    def subtraction(self, other):
        """ Subtraction of matrices """
        if self.numRows != other.numRows or self.numCols != other.numCols:
            print("Matrix dimensions not matching for subtraction.")
            return None

        result = MyMatrix(self.numRows, self.numCols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value - other.get_element(row, col))
        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.set_element(row, col, -value)
        return result

    def multiply(self, other):
        """ Multiplication of matrices """
        if self.numCols != other.numRows:
            print("Matrix dimensions not matching for multiplication.")
            return None

        result = MyMatrix(self.numRows, other.numCols)
        for (row1, col1), value1 in self.elements.items():
            for col2 in range(other.numCols):
                value2 = other.get_element(col1, col2)
                if value2 != 0:
                    current_val = result.get_element(row1, col2)
                    result.set_element(row1, col2, current_val + value1 * value2)
        return result

    def writeResults(self, filePath):
        try:
            with open(filePath, 'w') as f:
                f.write(f"rows={self.numRows}\n")
                f.write(f"cols={self.numCols}\n")
                for (row, col), value in sorted(self.elements.items()):
                    f.write(f"({row},{col},{value})\n")
            print(f"Results written to the results file")
        except Exception as e:
            print(f"Error occured while writing to file: {e}")

try:
    matrixA = MyMatrix.readFile('../../sample_inputs/easy_sample_01_2.txt')
    matrixB = MyMatrix.readFile('../../sample_inputs/easy_sample_01_3.txt')
    result_path = '../../sample_results/results.txt'

    operation = input("Which operation do you want to perform?  add, subtract or multiply :  ").strip().lower()

    if operation == 'add':
        result = matrixA.matrixAddition(matrixB)
        if result:
            result.writeResults(result_path)
    elif operation == 'subtract':
        result = matrixA.subtraction(matrixB)
        if result:
            result.writeResults(result_path)
    elif operation == 'multiply':
        result = matrixA.multiply(matrixB)
        if result:
            result.writeResults(result_path)
    else:
        print("Uknown Operation.")
except Exception as e:
    print(f"An error occurred: {e}")