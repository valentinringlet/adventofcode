import os

from sphinx.ext.todo import TodoList

# Define input file
filename = "input.txt"
filepath = os.path.join(
    os.path.realpath(os.path.dirname(__file__)),
    filename)

# Read and parse contents of input file
with open(filepath, 'r') as file:
    all_lines = file.readlines()
values = []
for line in all_lines:
    direction = line[0]
    value = int(line[1:])
    if direction == 'L':
        values.append(-value)
    elif direction == 'R':
        values.append(value)
    else:
        raise ValueError(f"Found invalid direction in line {line}")

print(f"Parsed {len(values)} rows of input")

# Calculate the number of times the dial stops at zero
position = 50
totalTimesStoppedAtZero = 0
for value in values:
    position = (position + value) % 100
    totalTimesStoppedAtZero += int(position == 0)

print(f"PART 1 - The dial stopped {totalTimesStoppedAtZero} times at zero")
