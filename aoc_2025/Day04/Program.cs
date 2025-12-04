namespace Day04;

class Program
{
    private static readonly char PaperRoll = '@';
    private static readonly char EmptySpace = '.';

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
        

        // Part 2 - Find the total number of paper rolls that can be removed by forklift
        var currentPaperRollMap = new List<List<char>>(paperRollMap.Count);
        var removablePaperRollMap = new List<List<char>>(paperRollMap.Count);
        paperRollMap.ForEach(row => {
          currentPaperRollMap.Add(new List<char>(row));
          removablePaperRollMap.Add(new List<char>(row));
        });
        var positionsToCheck = new HashSet<(int row, int col)>();
        // Using a HashSet to avoid duplicate positions
        for (int row = 0; row < currentPaperRollMap.Count; row++)
        {
            for (int col = 0; col < currentPaperRollMap[row].Count; col++)
            {
                if (currentPaperRollMap[row][col] == PaperRoll)
                {
                    positionsToCheck.Add((row, col));
                }
            }
        }

        var totalRemovedPaperRolls = 0;
        while (positionsToCheck.Count > 0)
        {
            var (row, col) = positionsToCheck.First();
            positionsToCheck.Remove((row, col));

            if (CanBeAccessedByForklift(currentPaperRollMap, row, col))
            {
                currentPaperRollMap[row][col] = EmptySpace;
                removablePaperRollMap[row][col] = 'x';
                totalRemovedPaperRolls++;

                // Register surrounding paper roll positions to be checked again
                for (int r = row - 1; r <= row + 1; r++)
                {
                    for (int c = col - 1; c <= col + 1; c++)
                    {
                        if (IsOutOfBounds(currentPaperRollMap, r, c))
                            continue;
                        if (r == row && c == col)
                            continue;
                        if (currentPaperRollMap[r][c] == PaperRoll)
                            positionsToCheck.Add((r, c));
                    }
                }
            }
        }

        Console.WriteLine("PART 2 - The total number of paper rolls that can be removed by forklift is " + totalRemovedPaperRolls);
        if (DEBUG)
            DisplayPaperRollMap(removablePaperRollMap);
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