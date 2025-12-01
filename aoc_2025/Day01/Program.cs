// Read in the input
var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
var inputFileFullPath = Path.Combine(parentDirectory, "test.txt");
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
