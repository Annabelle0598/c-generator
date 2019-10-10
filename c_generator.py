# this file generates simple C Programs for testing Truffle-Pig
import random
import sys
import os
from datetime import datetime


# Global variables
variables = -1
loop_variables = []
functions = []
used_loop_var = []
bool_operators = ["==", "!=", "<", ">", "<=", ">="]


# Main function
def main(arguments):
    global variables
    global loop_variables
    global functions
    global used_loop_var
    global bool_operators

    # Read arguments and init values
    argc = len(arguments)
    if argc == 1:
        # No arguments
        count_generated = 1
        save_directory = "."
        program_name = "program"
    elif argc == 2:
        # Arguments: amount of programs to generate
        try:
            count_generated = int(arguments[1])
            save_directory = "."
            program_name = "program"
        except:
            print("Usage: python c_generator.py [count_generated] [save_directory] [program_name]")
            return
    elif argc == 3:
        # Arguments: amount of programs to generate, directory to save
        try:
            count_generated = int(arguments[1])
            save_directory = str(arguments[2])
            program_name = "program"
        except:
            print("Usage: python c_generator.py [count_generated] [save_directory] [program_name]")
            return
    elif argc == 4:
        # Arguments: amount of programs to generate, directory to save, name of generated programs
        try:
            count_generated = int(arguments[1])
            save_directory = str(arguments[2])
            program_name = str(arguments[3])
        except:
            print("Usage: python c_generator.py [count_generated] [save_directory] [program_name]")
            return
    else:
        # Invalid arguments
        print("Usage: python c_generator.py [count_generated] [save_directory] [program_name]")
        return
    print("Generate " + str(count_generated) + " C programs in directory \"" + str(save_directory) + "\".")

    # Generate save directory is not exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Generate given number of programs
    for i in range(0,count_generated):
        # Init variables
        variables = -1
        loop_variables = []
        functions = []
        used_loop_var = []
        bool_operators = ["==", "!=", "<", ">", "<=", ">="]

        # Generate
        p = init()

        # Save to file
        f = open(save_directory + "/" + str(program_name) + "_" + str(i + 1) + ".c", "w+")
        f.write(p)
        f.close()
        print(str(i + 1) + "/" + str(count_generated))
    print("Finished")


# Generate main and functions
def init():
    global functions
    random.seed(datetime.now())
    functions = []

    # Include stdlib
    program = "#include <stdlib.h>\n"

    # Generate up to 5 functions
    for i in range(0, random.randint(0, 5)):
        # Add function to list
        functions.append("function" + str(i))
        # Add function declaration
        program += "int function" + str(i) + "(int f1, int f2);\n"

    # Generate main function
    program += "\nint main(int argc, char** args){\n int f1 = 0; \n int f2 = 0; \n"
    # Init variables
    program = initialize_variables(random.randint(1, 10), program)
    program = initialize_loop_variables(random.randint(1, 10), program)
    # Generate body
    p = generate_program(random.randint(0, 10))
    program += p + " return 0; \n }"

    # Add function definition
    for f in functions:
        program += "int " + f + "(int f1, int f2){"
        # init variables
        program = initialize_variables(random.randint(1, 10), program)
        program = initialize_loop_variables(random.randint(1, 10), program)
        # Generate body
        p = generate_program(random.randint(0, 10))
        program += p + "return (f1 + f2); \n }"
    return program


# Generate body
def generate_program(length):
    # List of elements to generate
    elements = [generate_arith, generate_fun_call, generate_if, generate_elif, generate_switch, generate_while,
                generate_do_while]
    program = ""
    # Generate "length" random elements
    for i in range(0, length):
        # Pick element
        element = random.choice(elements)
        # Run element
        program = element(program)
    return program


# Create and initialize variables to use in program
def initialize_variables(a, program):
    global variables
    variables = a
    program += "// Variables \n"
    # Generate a random variables
    for i in range(0, a):
        program += "int var" + str(i) + " = " + str(random.randint(0, 100)) + ";\n"
    return program


# Create and initialize variables to use in loops
def initialize_loop_variables(a, program):
    program += "// Loopvariables \n"
    loop_variables.clear()
    # Generate a random loop variables
    for i in range(0, a):
        program += "int varloop" + str(i) + " = " + str(random.randint(0, 100)) + ";\n"
        loop_variables.append("varloop" + str(i))
    return program


# Get a previous generated variable or default variables f1 or f2
def get_var():
    if random.choice([True, False, False, False, False]):
        # 20% choice for default variables
        return random.choice(["f1", "f2"])
    else:
        # Get random variable from previoud generated variables
        if variables > 1:
            return "var" + str(random.randint(0, variables-1))
        elif variables == 1:
            return "var0"
        return "NoVAR"


# Generate arithmetic instruction, return calls or exit calls
def generate_arith(program, index=10):
    # Possible operators
    operators = ["+", "-", "*", "/"]
    program += "// arith \n"
    for i in range(0, index):
        if random.choice([True, False]):
            if random.choice([True, False]):
                if random.choice([True, False]):
                    # Generate return call
                    program += "return " + str(random.randint(-100, 100)) + ";\n"
                else:
                    # Generate exit zero call
                    program += "exit(0);\n"
            else:
                # Generate exit non zero call
                program += "exit(" + str(random.randint(-100, 100)) + ");\n"
        else:
            # Generate arithmetic operation
            program += get_var() + " = " + get_var() + " " + random.choice(operators) + " " + get_var() + "; \n"
    return program


# Generate call to previous declared function
def generate_fun_call(program):
    if len(functions) > 0:
        program += "// function call\n"
        # Random function call
        program += random.choice(functions) + "(" + get_var() + ", " + get_var() + ");\n"
    return program


# Generate if statement
def generate_if(program):
    ifcase = generate_program(random.randint(0, 1))
    elsecase = generate_program(random.randint(0, 1))
    program += "// If-statement \n"
    program += "if(" + get_var() + random.choice(bool_operators) + get_var() + ") \n"
    program += "{" + ifcase + "} else \n"
    program += "{" + elsecase + "}"
    return program


# Generate if statement with elsif case
def generate_elif(program):
    operators = ["==", "!="]
    ifcase = generate_program(random.randint(0, 1))
    elseifcase = generate_program(random.randint(0, 1))
    program += "// If-statement \n"
    program += "if(" + get_var() + random.choice(operators) + get_var() + ") \n"
    program += "{" + ifcase + "} else if (" + get_var() + random.choice(
        operators) + get_var() + ") \n"
    program += "{" + elseifcase + "}"
    return program


# Generate switch statement
def generate_switch(program, cases=3):
    program += "// Switch-statement \n"
    if variables > 1:
        program += "switch (var" + str(random.randint(0, variables-1)) + ") { \n"
    else:
        program += "switch (var0) { \n"

    # Generate cases
    for c in range(0, cases):
        p = generate_program(random.randint(0, 1))
        program += "case " + str(c) + ": " + p + "break; \n"
    # Generate default case
    p = generate_program(random.randint(0, 1))
    program += "default: " + p + " break; \n } \n"
    return program


# Get a previous generated loop variable
def get_loop_var():
    try:
        # Get random first loopvar
        loopvar1 = random.choice(loop_variables)
    except:
        return None, None
    if not loopvar1:
        return None, None
    # Remove first loopvar from free loopvars
    loop_variables.remove(loopvar1)
    try:
        # Get random second loopvar
        loopvar2 = random.choice(loop_variables)
    except:
        return None, None
    if not loopvar2:
        # Undo removing first loopvar
        loop_variables.append(loopvar1)
        return None, None
    # Remove second loopvar from free loopvars
    loop_variables.remove(loopvar2)
    return loopvar1, loopvar2


# Generate while loop
def generate_while(program):
    # Get loopvars
    loopvar1, loopvar2 = get_loop_var()
    if not loopvar1:
        return program
    program += "// While loop \n"

    # Generate body
    p = generate_program(random.randint(0, 1))
    program += "while(" + str(loopvar1) + random.choice(bool_operators) + str(loopvar2) + ") \n"
    program += "{" + p + "}\n"
    return program


def generate_do_while(program):
    # Get loopvars
    loopvar1, loopvar2 = get_loop_var()
    if not loopvar1:
        return program
    program += "// Dowhile loop \n"

    # Generate body
    p = generate_program(random.randint(0, 1))
    program += "do{" + p + "}\n"
    program += "while(" + str(loopvar1) + random.choice(bool_operators) + str(loopvar2) + "); \n"
    return program


main(sys.argv)
