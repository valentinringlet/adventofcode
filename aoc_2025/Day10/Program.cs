using System.Data;

namespace Day10;

class Program
{
    private static readonly char LightOn = '#';

    static void Main(string[] args)
    {
        // Read in the input
        var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
        var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
        var allLines = File.ReadAllLines(inputFileFullPath)
            .Where(line => !string.IsNullOrWhiteSpace(line))
            .Select(SplitInputLine)
            .ToList();
        
        // Part 1 - For each machine (=line) find the minimum number of button presses required to correctly 
        // configure the machine and sum the numbers together
        var sumNumberOfButtonPresses = 0;
        for (var i = 0; i < allLines.Count; i++)
        {
            var (finalState, buttons, _) = allLines[i];
            var startState = Enumerable.Repeat(false, finalState.Count).ToList();

            var minNumberOfButtonPresses = FindMinNumberOfButtonPresses(startState, buttons, finalState);
            if (minNumberOfButtonPresses == -1)
            {
                Console.WriteLine("PART 1 - No solution found for machine " + i);
                return;
            }
            sumNumberOfButtonPresses += minNumberOfButtonPresses;
        }
        Console.WriteLine("PART 1 - The sum of the minimum number of button presses for each machine is " + sumNumberOfButtonPresses);
    }

        /// <summary>
        /// Parses a line of input, splitting it into three parts: 
        /// 1. The final state the lights should be in, 
        /// 2. The effect of the buttons that can be pressed, and
        /// 3. The joltage requirements
        /// 
        /// Input format:
        /// e.g. "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        ///     where [.##.] represents to the final state of the lights,
        ///         (3) (1,3) (2) (2,3) (0,2) (0,1) represents the buttons, and
        ///         {3,5,4,7} represents the joltage requirements
        /// </summary>
        /// <param name="line">The line of input to parse </param>
        /// <returns>
        /// A tuple containing 
        /// 1. The final state of the lights as a boolean list (true if the light should be on), 
        /// 2. The effect of the buttons that can be pressed (as a list of lists of booleans, 
        ///     true if the button flips the light at that position), and 
        /// 3. The joltage requirements
        /// </returns>
    public static (List<bool> finalState, List<List<bool>> buttons, List<int> joltageRequirements) SplitInputLine(string line) 
    {
        var firstPartWithoutBrackets = line.Substring(
                line.IndexOf("[") + 1,
                line.IndexOf("]") - line.IndexOf("[") - 1
            ).Trim();
        var secondPartWithoutBrackets = line.Substring(
                line.IndexOf("(") + 1,
                line.LastIndexOf(")") - line.IndexOf("(") - 1
            ).Replace('(', ' ')
            .Replace(')', ' ')
            .Trim();
        var thirdPartWithoutBrackets = line.Substring(
                line.IndexOf("{") + 1,
                line.IndexOf("}") - line.IndexOf("{") - 1
            ).Trim();

        var parsedFirstPart = firstPartWithoutBrackets
            .Select(c => c == LightOn)
            .ToList();
        
        var preparedSecondPart = secondPartWithoutBrackets
            .Split()
            .Where(buttonWirings => !string.IsNullOrWhiteSpace(buttonWirings))
            .Select(buttonWirings => 
                buttonWirings
                    .Split(",")
                    .Select(int.Parse)
                    .ToList()
            ).ToList();
        var parsedSecondPart = new List<List<bool>>(preparedSecondPart.Count);
        for (var i = 0; i < preparedSecondPart.Count; i ++)
        {
            parsedSecondPart.Add(
                Enumerable.Repeat(false, parsedFirstPart.Count)
                .ToList());
            
            foreach (var indexOfTriggeredLight in preparedSecondPart[i])
            {
                parsedSecondPart[i][indexOfTriggeredLight] = true;
            }
        }
        
        var parsedThirdPart = thirdPartWithoutBrackets
            .Split(",")
            .Select(int.Parse)
            .ToList();

        return (parsedFirstPart, parsedSecondPart, parsedThirdPart);
    }

    public static int FindMinNumberOfButtonPresses(List<bool> startState, List<List<bool>> buttons, List<bool> finalState)
    {
        var searchStates = new Queue<(List<bool>, int)>();
        searchStates.Enqueue((startState, 0));
        while (searchStates.Any())
        {
            var (currentState, numPresses) = searchStates.Dequeue();

            foreach (var button in buttons)
            {
                var newState = ApplyButtonPress(currentState, button);
                if (newState.SequenceEqual(finalState))
                {
                    return numPresses + 1;
                }
                else
                {
                    searchStates.Enqueue((newState, numPresses + 1));
                }
            }
        }

        return -1;
    }

    public static List<bool> ApplyButtonPress(List<bool> currentState, List<bool> buttonPress)
    {
        var newState = new List<bool>(currentState);
        Enumerable.Range(0, newState.Count)
            .ToList()
            .ForEach(i => newState[i] = currentState[i] ^ buttonPress[i]);
        return newState;
    }
}
