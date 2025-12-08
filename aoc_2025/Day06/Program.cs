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


        // Part 2 - Find the sum of the individual problems, but parsing the numbers differently
        char[] digitChars = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };
        var numbersToParse = inputLines.Take(inputLines.Count - 1).ToList();
        var numbersGroupedByProblemPart2 = new List<List<long>>();
        var currentNumbers = new List<long>();
        var col2 = 0;
        while (col2 < numbersToParse[0].Length)
        {
            var currentNumber = 0L;
            for (var row2 = 0; row2 < numbersToParse.Count; row2++)
            {
                if (digitChars.Contains(numbersToParse[row2][col2]))
                {
                    var digit = long.Parse(numbersToParse[row2].Substring(col2, 1));
                    currentNumber = currentNumber * 10 + digit;
                }
                else
                {
                    // No digit at this row, skip to next row
                    continue;
                }
            }

            if (currentNumber == 0)
            {
                // We have hit a column with no numbers, i.e. we finished parsing a problem
                numbersGroupedByProblemPart2.Add(currentNumbers);
                currentNumbers = new List<long>();
                col2 ++;
                continue;
            }

            currentNumbers.Add(currentNumber);
            col2 ++;
        }

        // Add the last problem
        numbersGroupedByProblemPart2.Add(currentNumbers);

        // Now perform the calculations again
        long sumResultsPart2 = SolveAndSumAllProblems(numbersGroupedByProblemPart2, operations);
        Console.WriteLine("PART 2 - The final sum of the answers of all individual problems (parsed differently) is " + sumResultsPart2);
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





