namespace Day04;

class Program
{
    private static readonly char PaperRoll = '@';

    static void Main(string[] args)
    {
        var DEBUG = false;

        // Read in the input
        var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
        var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
        var inputLines = File.ReadAllLines(inputFileFullPath);
        var paperRollMap = inputLines
          .Where(line => !string.IsNullOrWhiteSpace(line))
          .Select(line => line.ToList())
          .ToList();
        
        // Part 1 - Find the number of paper rolls that can be accessed by forklift
        var accessiblePaperRolls = 0;
        var accessiblePaperRollMap = new List<List<char>>(paperRollMap.Count);
        paperRollMap.ForEach(row => accessiblePaperRollMap.Add(new List<char>(row)));
        for (int row = 0; row < paperRollMap.Count; row++)
        {
            accessiblePaperRollMap.Add([]);
            for (int col = 0; col < paperRollMap[row].Count; col++)
            {
                if (paperRollMap[row][col] == PaperRoll && CanBeAccessedByForklift(paperRollMap, row, col))
                {
                    accessiblePaperRolls++;
                    accessiblePaperRollMap[row][col] = 'x';
                }
            }
        }

        Console.WriteLine("PART 1 - The number of paper rolls that can be accessed by forklift is " + accessiblePaperRolls);
        if (DEBUG)
            DisplayPaperRollMap(accessiblePaperRollMap);
}

    public static bool CanBeAccessedByForklift(List<List<char>> paperRollMap, int row, int col)
    {
        var numSurroundingPaperRolls = 0;
        for (int r = row - 1; r <= row + 1; r++)
        {
            for (int c = col - 1; c <= col + 1; c++)
            {
                if (IsOutOfBounds(paperRollMap, r, c))
                    continue;
                if (r == row && c == col)
                    continue;
                if (paperRollMap[r][c] == PaperRoll)
                    numSurroundingPaperRolls++;
            }
        }

        return numSurroundingPaperRolls < 4;
    }

    public static bool IsOutOfBounds(List<List<char>> paperRollMap, int row, int col) =>
        row < 0 || row >= paperRollMap.Count 
        || col < 0 || col >= paperRollMap[row].Count;
    
    public static void DisplayPaperRollMap(List<List<char>> paperRollMap)
    {
        foreach (var line in paperRollMap)
        {
            Console.WriteLine(string.Join("", line));
        }
    }
}