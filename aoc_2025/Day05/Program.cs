

var DEBUG = false;

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
            if (DEBUG) Console.WriteLine($"Ingredient ID {ingredientId} is fresh (in range {Start}-{End})");
            freshIngredientCount++;
            break;
        }
    }
}

Console.WriteLine("PART 1 - The number of available ingredients that are fresh is " + freshIngredientCount);

// Part 2 - Find the total number of ingredient IDs that are fresh
long totalNumberOfFreshIngredients = 0;
var orderedFreshIngredientIdRanges = freshIngredientIdRanges
    .OrderBy(range => range.Start)
    .ToList();

if (DEBUG)
{
    Console.WriteLine("###############################################\nOrdered fresh ingredient ID ranges:");
    foreach (var (Start, End) in orderedFreshIngredientIdRanges)
    {
        Console.WriteLine($"  {Start}-{End}");
    }
    Console.WriteLine("###############################################");
}

int currentIdx = 0;
int nextIdx = 0;
while (currentIdx < orderedFreshIngredientIdRanges.Count)
{
    var (currentStart, currentEnd) = orderedFreshIngredientIdRanges[currentIdx];
    if (DEBUG) Console.WriteLine($"Processing range {currentStart}-{currentEnd}");

    nextIdx = currentIdx + 1;
    while (nextIdx < orderedFreshIngredientIdRanges.Count)
    {
        var (nextStart, nextEnd) = orderedFreshIngredientIdRanges[nextIdx];
        if (nextStart <= currentEnd + 1)
        {
            // Ranges overlap or are contiguous, merge them
            currentEnd = Math.Max(currentEnd, nextEnd);
            if (DEBUG) Console.WriteLine($"  Merging with range {nextStart}-{nextEnd} to form {currentStart}-{currentEnd}");
            nextIdx++;
        }
        else
        {
            if (DEBUG) Console.WriteLine($"  No overlap with range {nextStart}-{nextEnd}, moving to next range.");
            break;
        }
    }

    if (DEBUG) Console.WriteLine($"Final merged range {currentStart}-{currentEnd}, adding {(currentEnd - currentStart + 1)} to total.");
    totalNumberOfFreshIngredients += currentEnd - currentStart + 1;
    currentIdx = nextIdx;
}

Console.WriteLine("PART 2 - The total number of fresh ingredient IDs is " + totalNumberOfFreshIngredients);