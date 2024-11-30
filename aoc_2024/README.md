# Advent of Code 2024
In this repository, I'll be adding my answers for the challenges of the [2024 Advent of Code](https://adventofcode.com/2024).

## Getting started
After downloading the files from this repo, you can get started by executing the `runner.py` file using the following command:
```
python runner.py
```

The code will then prompt you to input which challenge you would like to execute.


## Solving new challenges
When solving new challenges, I recommend to follow the following structure:

1. Add a new python package under [challenges/](challenges/) named after the challenge, e.g. `01/`
2. Add the subclass of the [Challenge](shared/challenge.py) abstract class in the [variables](shared/variables.py) file