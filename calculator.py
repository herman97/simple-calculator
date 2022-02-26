import sys

registers = dict()  # All registers are unique
valid_operators = ['add', 'subtract', 'multiply']


class Register:
    """
    A Register contains a name, its current value and a list of 
    operations.
    It also contains functions to add operations to the register
    and perform all operations in the operations-list.
    """

    def __init__(self, name: str) -> None:
        """ 
        Init a register. A register needs a name and during construction 
        it is given a list for operations and a starting value 
        """
        self.name = name
        self.value = 0
        self.operations = []

    def add_operation(self, operator: str, value: str) -> None:
        """ 
        Adds a operation and a value as a tuple to the operation list 
        """
        self.operations.append((operator, value))

    def perform_operations(self) -> int:
        """ 
        Calculates the value of this register based on the operations in 
        the operations list 
        """
        while(self.operations):
            # Remove the operations so it is not performed again
            operation = self.operations.pop(0)
            operator = operation[0]
            val = operation[1]

            # val is not a register, so it does not need to be further
            # evaluated
            if isinstance(val, int):
                self.value = calculate(self.value, operator, val)

            # val is a register and needs to be evaluated before performing an
            # operation with it
            else:
                register = get_register(val)
                if (register):
                    self.value = calculate(
                        self.value, operator, register.perform_operations())
                else:
                    self.value = calculate(self.value, operator, int(val))

        return self.value


def calculate(val1: int, operator: str, val2: int) -> int:
    """
    Calcluates and returns a value depending on the operator, if operator does
    not exist it returns the old value.
    Can easily be extended with more operators.
    """
    if not operator in valid_operators:
        print(operator, " is not a valid operator.")
    return {'add': val1+val2,
            'subtract': val1-val2,
            'multiply': val1*val2}.get(operator, val1)


def get_register(register_name: str) -> Register or None:
    """
    Returns a register if it exists, else return false
    """
    return registers[register_name] \
        if register_name in registers.keys() \
        else None


def evaluate_operation(operation: list) -> None:
    """
    operation: [print, register]. Print the register by calling its evaluation
            function.

    operation: [register, operator, value]. If register exists, add the new 
            operation to it, else create register and add the operation.
    """

    if operation[0] == 'print' and len(operation) == 2:
        register = get_register(operation[1])
        if register:
            print(register.perform_operations())
        else:
            print("Register does not exist, cant print value of: " +
                  operation[1])

    elif len(operation) == 3:
        register = get_register(operation[0])
        if register:
            register.add_operation(operation[1], operation[2])
        else:
            new_register = Register(operation[0])
            new_register.add_operation(operation[1], operation[2])
            registers[operation[0]] = new_register

    else:
        print("Invalid line: ", operation)


def read_from_file(file: str) -> list:
    """ 
    Read input from file and return a list of [register, operator, value]
    """
    operations = []
    try:
        with open(file) as f:
            operations = [(x.lower().split()) for x in f.readlines()]
    except FileNotFoundError:
        print("No file with name '", file, "' found")

    return operations


def read_from_input() -> list:
    """ 
    Reads input from command line and returns a list of 
    [register, operator, value]
    """
    operations = []
    while True:
        line = input().lower()

        if line == 'quit':
            break
        else:
            operations.append(line.split())

    return operations


def main():
    """
    Handles input reading and goes through all read operations
    """
    operations = []

    # File input as argument
    if len(sys.argv) > 1:
        operations = read_from_file(sys.argv[1])

    # Read from input
    else:
        operations = read_from_input()

    for operation in operations:
        if not operation:
            continue
        if operation[0] == 'quit':
            break
        else:
            evaluate_operation(operation)


if __name__ == "__main__":
    main()
