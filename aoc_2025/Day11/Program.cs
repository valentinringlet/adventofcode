using System.Diagnostics;

namespace Day11;

class Program
{
    private static readonly bool DEBUG = true;
    private static readonly string StartingDevice = "you";
    private static readonly string FinalDevice = "out";

    static void Main(string[] args)
    {
        // Read in the input
        var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
        var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
        var deviceConnections = File.ReadAllLines(inputFileFullPath)
            .Where(line => !string.IsNullOrWhiteSpace(line))
            .Select(line => {
                var splitParts = line.Split(':', 2);
                var sourceDevice = splitParts[0].Trim();
                var destinationDevices = splitParts[1].Trim()
                    .Split(' ')
                    .Select(device => device.Trim())
                    .ToList();
                return (sourceDevice, destinationDevices);
            }).ToDictionary();
        
        if (DEBUG) Console.WriteLine("Parsed " + deviceConnections.Count + " device connections.");

        // Part 1 - Find the number of paths leading from the start to the end
        var paths = new Queue<List<string>>();
        paths.Enqueue([StartingDevice]);
        var completedPaths = new HashSet<List<string>>();
        while (paths.Count > 0)
        {
            var currentPath = paths.Dequeue();
            var currentDevice = currentPath[^1];
            if (currentDevice == FinalDevice)
            {
                completedPaths.Add(currentPath);
                continue;
            }
            else
            {
                var possibleNextDevices = deviceConnections[currentDevice];
                foreach (var nextDevice in possibleNextDevices)
                {
                    // avoid loops
                    if (currentPath.Contains(nextDevice)) continue;

                    var newPath = new List<string>(currentPath);
                    newPath.Add(nextDevice);
                    paths.Enqueue(newPath);
                }
            }
        }

        Console.WriteLine("PART 1 - The number of paths from " + StartingDevice + " to " + FinalDevice + " is " + completedPaths.Count);
    }
}
