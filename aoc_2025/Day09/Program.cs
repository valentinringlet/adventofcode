using System.Drawing;

namespace Day09;

class Program
{
    static void Main(string[] args)
    {
        // Read in the input
        var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
        var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
        var coordinates = File.ReadAllLines(inputFileFullPath)
            .Where(line => !string.IsNullOrWhiteSpace(line))
            .Select(line => line.Split(','))
            .Select(parts => (x: int.Parse(parts[0]), y: int.Parse(parts[1])))
            .ToList();
        
        // Part 1 - Compute the largest area of any rectangle you can make using 2 of the points as corners
        var maxArea = 0L;
        for (var i = 0; i < coordinates.Count; i++)
        {
            for (var j = i + 1; j < coordinates.Count; j++)
            {
                maxArea = Math.Max(maxArea, Area(coordinates[i], coordinates[j]));
            }
        }
        Console.WriteLine("PART 1 - The largest area of any rectangle you can make is " + maxArea);
    }

    public static long Area((int x, int y) pointA, (int x, int y) pointB)
    {
        return (long)Math.Abs(pointA.x - pointB.x + 1) * Math.Abs(pointA.y - pointB.y + 1);
    }
}
