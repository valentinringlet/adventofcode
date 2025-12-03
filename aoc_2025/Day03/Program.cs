// Read in the input
var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
var inputLines = File.ReadAllLines(inputFileFullPath);
var joltageMap = inputLines
  .Where(line => !string.IsNullOrWhiteSpace(line))
  .Select(line => line.Select(element => int.Parse(element.ToString())).ToList())
  .ToList();

Console.WriteLine($"Read {joltageMap.Count} battery banks, each with {joltageMap.First().Count} batteries.");

// Part 1 - Find the sum of the maximum voltages in each bank
var totalMaxJoltages = 0;
foreach (var bank in joltageMap)
{
    var maxBatteryTensDigit = bank.Slice(0, bank.Count - 1).Max();
    var maxBatteryTensDigitIndex = bank.IndexOf(maxBatteryTensDigit);
    var maxBatteryOnesDigit = bank.Slice(maxBatteryTensDigitIndex+1, bank.Count - (maxBatteryTensDigitIndex+1)).Max();

    var maxJoltageInBank = (maxBatteryTensDigit * 10) + maxBatteryOnesDigit;

    totalMaxJoltages += maxJoltageInBank;
}

Console.WriteLine("The sum of the maximum voltages in each bank is " + totalMaxJoltages);