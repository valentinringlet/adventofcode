namespace Day06;
using System.Globalization;
using System.Text.RegularExpressions;
using Microsoft.VisualBasic;

class Program
{
    static void Main(string[] args)
    {
        // Read in the input
        var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
        var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
        var inputLines = File.ReadAllLines(inputFileFullPath)
            .Where(line => !string.IsNullOrWhiteSpace(line))
            .ToList();

        // Part 1 - Apply the operations to each number and output the final sum
        var operations = inputLines.Last()
            .Split(' ', StringSplitOptions.RemoveEmptyEntries)
            .Select(op => op.Trim())
            .ToList();
        var numbers = inputLines.Take(inputLines.Count - 1)
            .Select(line => line.Split(' ', StringSplitOptions.RemoveEmptyEntries)
                .Select(num => long.Parse(num.Trim()))
                .ToList()
            ).ToList();
        
        long sumResults = SolveAndSumAllProblems(numbers, operations);
        Console.WriteLine("PART 1 - The final sum of the answers of all individual problems is " + sumResults);
    }

    public static long SolveAndSumAllProblems(List<List<long>> numbers, List<string> operations)
    {
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

        return sumResults;
    }
}





