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
        var inputFileFullPath = Path.Combine(parentDirectory, "test.txt");
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
        
        var numbersGroupedByProblem = new List<List<long>>();
        for (var col=0; col < numbers[0].Count; col++)
        {
            var currentProblemNumbers = new List<long>();
            for (var row=0; row < numbers.Count; row++)
            {
                currentProblemNumbers.Add(numbers[row][col]);
            }

            numbersGroupedByProblem.Add(currentProblemNumbers);
        }
        
        long sumResults = SolveAndSumAllProblems(numbersGroupedByProblem, operations);
        Console.WriteLine("PART 1 - The final sum of the answers of all individual problems is " + sumResults);
    }

    public static long SolveAndSumAllProblems(List<List<long>> numbers, List<string> operations)
    {
        var totalSum = 0L;
        for (var i=0; i < numbers.Count; i++)
        {
            var currentProblemOperation = operations[i];
            if (currentProblemOperation == "+")
            {
                totalSum += numbers[i].Sum();
            }
            else if (currentProblemOperation == "*")
            {
                totalSum += numbers[i].Aggregate(1L, (acc, val) => acc * val);
            }
            else
            {
                throw new Exception($"Unknown operation '{currentProblemOperation}'");
            }
        }

        return totalSum;
    }
}





