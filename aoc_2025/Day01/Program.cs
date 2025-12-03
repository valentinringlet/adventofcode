// Read in the input
var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
var inputLines = File.ReadAllLines(inputFileFullPath);
var parsedInstructions = new List<(char Dir, int Value)>();
foreach (var line in inputLines)
{
    var s = line.Trim();
    if (s.Length == 0) continue;
    var dir = s[0];
    if (dir != 'L' && dir != 'R')
        throw new FormatException($"Invalid direction in line: {line}");
    if (!int.TryParse(s.Substring(1), out var value))
        throw new FormatException($"Invalid number in line: {line}");
    
    parsedInstructions.Add((dir, value));
}
Console.WriteLine($"Read {parsedInstructions.Count} instructions.");

// Part 1 - How many times did the dial point at zero?
var startPos = 50;
var pointedAtZeroTimes = 0;
foreach (var (dir, value) in parsedInstructions)
{
    if (dir == 'L')
        startPos -= value;
    else if (dir == 'R')
        startPos += value;
    startPos %= 100;

    if (startPos == 0)
        pointedAtZeroTimes++;
}

Console.WriteLine($"PART 1 - The dial pointed at zero {pointedAtZeroTimes} times.");

// Part 2 - How many times does the dial point at zero, including passing over it?
startPos = 50;
pointedAtZeroTimes = 0;
foreach (var (dir, value) in parsedInstructions)
{
    var oldStartPos = startPos;
    if (dir == 'L')
        startPos -= value;
    else if (dir == 'R')
        startPos += value;
    
    var oldHundredsDigit = oldStartPos / 100;
    var newHundredsDigit = startPos / 100;
    pointedAtZeroTimes += Math.Abs(newHundredsDigit - oldHundredsDigit);
    
    if (Math.Sign(oldStartPos) != Math.Sign(startPos) && Math.Sign(oldStartPos) != 0)
        pointedAtZeroTimes++;
    // This covers different edge cases:
    // 1. We passed over zero from positive to negative or negative to positive
    //    --> then the hundreds digit is 0 for both, so we need to add one more count
    // 2. We ended exactly at zero from a negative or positive position
    //    --> then the hundreds digit remains the same (for a number in -99 <= and <= 99), 
    //        so we need to add one more count
    // 3. We started exactly at zero and moved away from it
    //    --> then we should not count it as we already counted it when we ended at zero (see previous case)

    startPos = (startPos % 100 + 100) % 100; // Ensure the result is between 0 and 99 as specified in the assignment
}

Console.WriteLine($"PART 2 - The dial pointed at zero {pointedAtZeroTimes} times.");