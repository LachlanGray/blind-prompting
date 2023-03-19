Welcome! I will make a blog post about this soon.

"Blind Prompting" is my name for a technique of large language model prompting that does not involve communicating a specific goal to the LLM.

Instead of asking the LLM for a solution given a premise, the LLM is prompted to gradually discover the nature of the goal and its solution, and approximate it through exploration and exploitation. It is heavily inspired by traditional evolutionary algorithms, but doesn't necessarily have to look like them. 

I think it could be helpful for using LLM's to discover knowledge in domains where humans have an insufficient grasp of the goal, or can't describe what it looks like. Or, in applications where humans *can* describe the goal, but canonical/cliche solutions are undesirable. A few possible examples could be:
- evolving complex control systems
- forming decision making heuristics or policies
- hypothesis mining from experimental data
- developing novel prompt workflows

The point is to impose as few restrictions as possible on what avenues the model will try to explore in accomplishing the task.

## This repository
This is one possible realization of blind prompting, where a goal is accomplished in a workflow similar to a genetic algorithm. Solutions are randomly selected, modified, and recombined according to a fitness metric.

This is a prototype that generates inductive "structures" in the form of pattern-generating python functions. It improves by iteratively inventing, modifying, and merging functions to optimize a signal.

## Usage
**Don't run this stuff outside of the container** because you are executing code straight out of chatGPT, and it's possible that it could try to `import sys` or something and mess with things.

You'll need to set your `OPENAI_API_KEY` system variable.

To start the ai box (container)
```
make build
make start
```

To stop it, `make stop`. 

To run the sanity checks in `tests.py` (no actual tests for now...) 
```
make tests test=function_in_tests_py
```

Currently the most interesting one is `create_and_exec` which generates a python function and executes it. "Damaged" python functions are recursively repaired by ChatGPT to a maximum depth of 3.

Evaluation, solution management, selection coming soon...

## Related work
This list is a work in progress
- [Evolution through Large Models (ELM)](https://arxiv.org/abs/2206.08896)
- [OpenELM](https://carper.ai/openelm-release/)
- [Code4Struct: Code Generation for Few-Shot Structured Prediction from Natural Language](https://arxiv.org/abs/2210.12810)



