namespace MyProject;
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
            if (! IsValidProductId(range[0] + i))
            {
                invalidProductIds.Add(range[0] + i);
            }
          }
        }
        var sumOfInvalidProductIds = invalidProductIds.Sum();

        Console.WriteLine($"PART 1 - The sum of invalid product IDs is {sumOfInvalidProductIds}.");
    }

    public static bool IsValidProductId(long productId)
    {
        // An invalid product ID is made of some sequence of digits repeated twice
        // e.g. "55", "6464", "123123"
        
        var productIdStr = productId.ToString();
        if (productIdStr.Length % 2 != 0)
            return true;
        var halfLength = productIdStr.Length / 2;
        return ! (productIdStr[..halfLength] == productIdStr[halfLength..]);
    }
}
