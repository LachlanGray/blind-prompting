from .prompts import new_pattern_function
from .prompts import run_python_function, fix_python_error


# sanity checks during developent #####################################

def create():
    program = new_pattern_function("int", "List[Tuple[int, int]]")
    print("program:")
    print(program + "\n\n")

def create_and_exec():
    program = new_pattern_function("int, int, int", "List[Tuple[int, int]]")
    length = 10
    num1 = 5
    num2 = 11
    num3 = 14
    _, output = run_python_function(program, [length, num1, num2, num3])
    print("program:")
    print(program + "\n")
    print("output:")
    print(output)

def test_error_correction():
    program = "def add_numbers(num1, num2):\n    return nu1m + num2)"
    error = '''Traceback (most recent call last):
      File "/Users/lachlangray/dev/prompt_evolution/outputs.py", line 41, in <module>
        add_numbers(5,6)
      File "/Users/lachlangray/dev/prompt_evolution/outputs.py", line 39, in add_numbers
        return nu1m + num2
    NameError: name 'nu1m' is not defined'''
    corrected_program = fix_python_error(program, error)
    print(corrected_program)



# actual tests ######################################################

# tests will go here

tests = []

def all():
    # iterate over list of function, and execute each one
    # print the name of the function, and the result 
    # red if it fails, green if it passes
    for test in tests:
        status = test()
        print(f"{status} - {test.__name__}")










