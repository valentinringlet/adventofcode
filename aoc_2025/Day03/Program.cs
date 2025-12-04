// Read in the input
var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
var inputLines = File.ReadAllLines(inputFileFullPath);
var joltageMap = inputLines
  .Where(line => !string.IsNullOrWhiteSpace(line))
  .Select(line => line.Select(element => int.Parse(element.ToString())).ToList())
  .ToList();

Console.WriteLine($"Read {joltageMap.Count} battery banks, each with {joltageMap.First().Count} batteries.");

// Part 1 - Find the sum of the maximum joltages in each bank
var totalMaxJoltages = 0;
foreach (var bank in joltageMap)
{
    var maxBatteryTensDigit = bank.Slice(0, bank.Count - 1).Max();
    var maxBatteryTensDigitIndex = bank.IndexOf(maxBatteryTensDigit);
    var maxBatteryOnesDigit = bank.Slice(maxBatteryTensDigitIndex+1, bank.Count - (maxBatteryTensDigitIndex+1)).Max();

    var maxJoltageInBank = (maxBatteryTensDigit * 10) + maxBatteryOnesDigit;

    totalMaxJoltages += maxJoltageInBank;
}

Console.WriteLine("PART 1 - The sum of the 2 maximum joltages in each bank is " + totalMaxJoltages);

// Part 2 - Find the sum of the maximum joltages in each bank, selecting 12 batteries in each bank
long totalMaxJoltagesPart2 = 0;
foreach (var bank in joltageMap)
{
    long maxJoltageInBank = 0;
    var remainingBank = bank.ToList();
    var numberOfBatteriesToSelect = 12;
    for (int i = 0; i < numberOfBatteriesToSelect; i++)
    {
        var maxBattery = remainingBank.Slice(0, remainingBank.Count - (numberOfBatteriesToSelect - i) + 1).Max();
        var maxBatteryIndex = remainingBank.IndexOf(maxBattery);
        remainingBank = remainingBank.Slice(maxBatteryIndex+1, remainingBank.Count - (maxBatteryIndex+1)).ToList();

        maxJoltageInBank = (maxJoltageInBank * 10) + maxBattery;
    }
    
    totalMaxJoltagesPart2 += maxJoltageInBank;
}

Console.WriteLine("PART 2 - The sum of the 12 maximum joltages in each bank is " + totalMaxJoltagesPart2);
