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
        var startCol = map.First().IndexOf(StartSymbol);

        // Part 1 - Propagate the beam all the way down and count the number of beams
        var beams = new HashSet<(int row, int col)>() { (0, startCol) };
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
                    if (nextCol > 0) 
                        newBeams.Add((nextRow, nextCol - 1));
                    if (nextCol < map[nextRow].Length - 1)
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

        // Part 2 - Compute the number of possible paths the beam can take to the end
        // = number of beams at the end row if propagating without deduplication of beams on the same position
        var beamsPart2 = new Dictionary<(int, int), long>() { { (0, startCol), 1L } };
        for (var i = 0; i < map.Count-1; i++)
        {
            var newBeamsPart2 = new Dictionary<(int, int), long>();
            foreach (var ((currentRow, currentCol), currentCount) in beamsPart2)
            {
                var nextRow = currentRow + 1;
                var nextCol = currentCol;

                if (map[nextRow][nextCol] == EmptySpace)
                {
                    newBeamsPart2[(nextRow, nextCol)] = currentCount + newBeamsPart2.GetValueOrDefault((nextRow, nextCol), 0);
                }
                else if (map[nextRow][nextCol] == Splitter)
                {
                    if (nextCol > 0)
                        newBeamsPart2[(nextRow, nextCol - 1)] = currentCount + newBeamsPart2.GetValueOrDefault((nextRow, nextCol - 1), 0);
                    if (nextCol < map[nextRow].Length - 1)
                        newBeamsPart2[(nextRow, nextCol + 1)] = currentCount + newBeamsPart2.GetValueOrDefault((nextRow, nextCol + 1), 0);
                }
                else
                {
                    Console.WriteLine("Found unknown map symbol at position (" + nextRow + "," + nextCol + "): " + map[nextRow][nextCol]);
                }
            }

            beamsPart2 = newBeamsPart2;
        }

        var totalNumPaths = beamsPart2.Select(entry => entry.Value).Sum();

        Console.WriteLine("PART 2 - There are " + totalNumPaths + " possible paths of beam splitting.");
    }
}