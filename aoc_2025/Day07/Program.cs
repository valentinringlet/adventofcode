namespace Day07;

class Program
{
    public static readonly char StartSymbol = 'S';
    public static readonly char EmptySpace = '.';
    public static readonly char Splitter = '^';

    static void Main(string[] args)
    {
        // Read in the input
        var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
        var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
        var map = File.ReadAllLines(inputFileFullPath)
            .Where(line => !string.IsNullOrWhiteSpace(line))
            .ToList();
        var startPos = map.First().IndexOf(StartSymbol);

        // Part 1 - Propagate the beam all the way down and count the number of beams
        var beams = new HashSet<(int row, int col)>() { (0, startPos) };
        var numberBeamSplits = 0;
        for (var i = 0; i < map.Count-1; i++)
        {
            var newBeams = new HashSet<(int row, int col)>();
            foreach (var (currentRow, currentCol) in beams)
            {
                var nextRow = currentRow + 1;
                var nextCol = currentCol;

                if (map[nextRow][nextCol] == EmptySpace)
                {
                    newBeams.Add((nextRow, nextCol));
                }
                else if (map[nextRow][nextCol] == Splitter)
                {
                    numberBeamSplits ++;
                    newBeams.Add((nextRow, nextCol - 1));
                    newBeams.Add((nextRow, nextCol + 1));
                }
                else
                {
                    Console.WriteLine("Found unknown map symbol at position (" + nextRow + "," + nextCol + "): " + map[nextRow][nextCol]);
                }
            }

            beams = newBeams;
        }

        Console.WriteLine("PART 1 - The beam will be split " + numberBeamSplits + " times.");
    }
}