import sys
import traceback
from io import StringIO

from typing import Tuple, List, Any, Callable

from langchain.llms import OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# Adapted from https://gist.github.com/christophmark/60d2cd21a729cd1232e80954eb8de267
class PythonREPL:
    """Simulates a standalone Python REPL."""

    def __init__(self):
        pass        

    def run(self, command: str) -> Tuple[int, str]:
            """Run command and returns anything printed."""
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            try:
                exec(command, globals())
                sys.stdout = old_stdout
                output = mystdout.getvalue()
                status = 0
            except Exception as e:
                sys.stdout = old_stdout
                output = traceback.format_exc()
                status = 1
            return status, output


openaichat = OpenAIChat(model_name="gpt-3.5-turbo")


# Program generation ########################################

new_program_prompt = PromptTemplate(
    input_variables=["input_signature", "output_signature"],
    template = "I need a function that has an input signature of (length: int, {input_signature}) and generate a \
                pattern of type {output_signature}. The length argument is how many times to repeat the pattern. \
                I'm not sure what the pattern is going to be at this time, just its signature. \
                \n\n \
                There is a relationship between the input and the output pattern, but I don't know what it is, \
                and I would like help finding it. \
                \n\n \
                Can you invent a pattern that matches the signature, and write a python function that \
                implements it? Make sure imports are included in the snippet if they are needed. Don't use print statements"
)
                # Can you try a pattern and implement it as a python function ({input_signature}) that returns a \
                # {output_signature} pattern? Make sure imports are included in the snippet."

new_program_chain = LLMChain(llm=openaichat, prompt=new_program_prompt)

def strip_to_code(response: str) -> str:  # utils
    '''remove chatgpt banter'''
    response = response.split("```")[1]
    if response[:6] == "python":
        return response[7:]
    return response

def new_pattern_function(input_signature: str, output_signature: str) -> str:
    # return strip_to_code(new_program_chain.predict(input_signature=input_signature,
                                                   # output_signature=output_signature))
    response = new_program_chain.predict(input_signature=input_signature, output_signature=output_signature)
    return strip_to_code(response)
    


# Program execution ########################################

fix_python_error_prompt = PromptTemplate(
    input_variables=["fn_code", "error"],
    template = "I'm trying to run the following function:\n\n \
                ```\n \
                {fn_code} \
                ```\n\n \
                But I'm getting the following error:\n\n \
                ```\n \
                {error} \
                ```\n\n \
                Can you rewrite the function to solve the issue?"
)

fix_python_error_chain = LLMChain(llm=openaichat, prompt=fix_python_error_prompt)

def fix_python_error(fn_code: str, error: str) -> str:
    return strip_to_code(fix_python_error_chain.predict(fn_code=fn_code,
                                                       error=error))


def string_to_function(fn_code: str) -> Callable:  # utils 
    exec(fn_code)
    return locals()[fn_code.split("(")[0].split()[-1]]

def string_to_function_name(fn_code: str) -> str:  # utils
    return fn_code.split("(")[0].split()[-1]


def run_python_function(fn_code: str, inputs: List, max_depth=3) -> Any:
    '''
    fn_code: a string of python code that defines a function
    inputs: a list of inputs to the function
    max_depth: the maximum number of times to try to fix the function if it fails

    returns: the output of the function, and the code that generated it. 

    Justification for combining execution and correction: execution is meant to be
    flexible like biological DNA; error correction is an integral/intrinsic part 
    of the process and not seperable from it. A slightly broken instruction should 
    execute as if nothing is wrong and correct itself.
    '''
    def try_again(fn_code, output):
        fn_code = fix_python_error(fn_code, output)
        return run_python_function(fn_code, inputs, max_depth=max_depth-1)

    if max_depth == 0:
        return None

    repl = PythonREPL()
    imports, definition = fn_code.split("def")
    definition = "def" + definition

    status, output = repl.run(imports)
    if status == 1:
        return try_again(fn_code, output)

    status, output = repl.run(definition)
    if status == 1:
        return try_again(fn_code, output)

    fn_name = string_to_function_name(fn_code)
    inputs_string = ", ".join([str(i) for i in inputs])
    status, output = repl.run(f"print({fn_name}({inputs_string}))")

    if status == 1:
        # assert False, output
        return try_again(fn_code, output)

    return fn_code, output


# Evaluation ################################################




