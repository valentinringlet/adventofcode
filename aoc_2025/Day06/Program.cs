
using System.Text.RegularExpressions;

// Read in the input
var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
var inputLines = File.ReadAllLines(inputFileFullPath)
    .Where(line => !string.IsNullOrWhiteSpace(line))
    .ToList();
var operations = inputLines.Last()
    .Split(' ', StringSplitOptions.RemoveEmptyEntries)
    .Select(op => op.Trim())
    .ToList();
var numbers = inputLines.Take(inputLines.Count - 1)
    .Select(line => line.Split(' ', StringSplitOptions.RemoveEmptyEntries)
        .Select(num => long.Parse(num.Trim()))
        .ToList()
    ).ToList();

// Part 1 - Apply the operations to each number and output the final sum
long sumResults = 0;
for (var col=0; col < numbers[0].Count; col++)
{
    long currentResult = numbers[0][col];
    for (var row=1; row < numbers.Count; row++)
    {
        var number = numbers[row][col];
        var operation = operations[col];
        if (operation == "+")
        {
            currentResult += number;
        }
        else if (operation == "*")
        {
            currentResult *= number;
        }
        else
        {
            throw new Exception($"Unknown operation '{operation}'");
        }
    }

    sumResults += currentResult;
}
Console.WriteLine("PART 1 - The final sum of the answers of all individual problems is " + sumResults);