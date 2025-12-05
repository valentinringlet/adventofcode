// Read in the input
var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
var inputLines = File.ReadAllLines(inputFileFullPath);
var separationIndex = inputLines.Index()
    .Where(element => string.IsNullOrWhiteSpace(element.Item))
    .Select(element => element.Index)
    .First();
var freshIngredientIdRanges = inputLines.Take(separationIndex)
    .Select(line => line.Split('-'))
    .Select(parts => (Start: long.Parse(parts[0]), End: long.Parse(parts[1])))
    .ToList();
var availableIngredientIds = inputLines.Skip(separationIndex + 1)
    .Select(long.Parse)
    .ToList();

Console.WriteLine($"Found {freshIngredientIdRanges.Count} fresh ingredient ranges and {availableIngredientIds.Count} available ingredients.");


// Part 1 - Find the number of available ingredients that are fresh
var freshIngredientCount = 0;
foreach (var ingredientId in availableIngredientIds)
{
    foreach (var (Start, End) in freshIngredientIdRanges)
    {
        if (Start <= ingredientId && ingredientId <= End)
        {
            freshIngredientCount++;
            break;
        }
    }
}

Console.WriteLine("PART 1 - The number of available ingredients that are fresh is " + freshIngredientCount);