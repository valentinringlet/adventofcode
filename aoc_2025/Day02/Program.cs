using System.Diagnostics;

namespace Day02;
class Program
{
    static void Main(string[] args)
    {
        // Read in the input
        var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
        var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
        var inputLine = File.ReadAllLines(inputFileFullPath).First();
        var parsedIdRanges = inputLine
          .Split(',')
          .Where(range => ! string.IsNullOrWhiteSpace(range))
          .Select(range => range.Split('-'))
          .Select(range => new[] { long.Parse(range[0]), long.Parse(range[1]) })
          .ToList();

        Console.WriteLine($"Read {parsedIdRanges.Count} product ID ranges.");

        // Part 1 - Find all invalid product ID ranges and sum them
        var invalidProductIds = new List<long>();
        foreach (var range in parsedIdRanges)
        {
          
          foreach (var i in Enumerable.Range(0, (int)(range[1]-range[0]) +1))
          {
            if (! IsValidProductIdPart1(range[0] + i))
            {
                invalidProductIds.Add(range[0] + i);
            }
          }
        }
        var sumOfInvalidProductIds = invalidProductIds.Sum();

        Console.WriteLine($"PART 1 - The sum of invalid product IDs is {sumOfInvalidProductIds}.");

        // Part 2 - Find all invalid product ID ranges and sum them (new criteria for validity)
        var invalidProductIdsPart2 = new List<long>();
        foreach (var range in parsedIdRanges)
        {
          
          foreach (var i in Enumerable.Range(0, (int)(range[1]-range[0]) +1))
          {
            if (! IsValidProductIdPart2(range[0] + i))
            {
                invalidProductIdsPart2.Add(range[0] + i);
            }
          }
        }
        var sumOfInvalidProductIdsPart2 = invalidProductIdsPart2.Sum();

        Console.WriteLine($"PART 2 - The sum of invalid product IDs is {sumOfInvalidProductIdsPart2}.");
    }

    public static bool IsValidProductIdPart1(long productId)
    {
        // An invalid product ID is made of some sequence of digits repeated twice
        // e.g. "55", "6464", "123123"
        
        var productIdStr = productId.ToString();
        if (productIdStr.Length % 2 != 0)
            return true;
        var halfLength = productIdStr.Length / 2;
        return ! (productIdStr[..halfLength] == productIdStr[halfLength..]);
    }

    public static bool IsValidProductIdPart2(long productId)
    {
        // An invalid product ID is made of some sequence of digits repeated twice
        // e.g. "55", "6464", "123123"
        
        var productIdStr = productId.ToString();
        var repeatingSequenceLength = 0;
        while (repeatingSequenceLength < productIdStr.Length / 2)
        {
            repeatingSequenceLength++;
            if (productIdStr.Length % repeatingSequenceLength != 0)
              continue;
            
            var sequence = productIdStr.Substring(0, repeatingSequenceLength);
            var repeatedSequence = string.Concat(Enumerable.Repeat(sequence, productIdStr.Length / repeatingSequenceLength));
            if (repeatedSequence == productIdStr)
                return false;
        }

        return true;
    }
}
