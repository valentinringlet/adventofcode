using System.Diagnostics;

namespace Day11;

class Program
{
    private static readonly bool UseTestInput = true;

    static void Main(string[] args)
    {
        // Part 1 - Find the number of paths leading from the start to the end
        // 1.1 - Read in the input
        var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
        var inputFileFullPath = Path.Combine(parentDirectory, (UseTestInput ? "test-part1.txt" : "input.txt"));
        var deviceConnectionsPart1 = File.ReadAllLines(inputFileFullPath)
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
        
        Console.WriteLine("Parsed " + deviceConnectionsPart1.Count + " device connections.");

        // 1.2 - Find the number of paths
        var startingDevicePart1 = "you";
        var finalDevicePart1 = "out";
        var numberOfPathsPart1 = ComputeNumberOfPathsFromStartNodeToEndNode(startingDevicePart1, finalDevicePart1, deviceConnectionsPart1);

        Console.WriteLine("PART 1 - The number of paths from " + startingDevicePart1 + " to " + finalDevicePart1 + " is " + numberOfPathsPart1);
    }

    /// <summary>
    /// Computes the number of paths from a start node to an end node in a graph,
    /// where each node is connected to a list of other nodes.
    /// </summary>
    /// <param name="startNode">The start node of the path.</param>
    /// <param name="endNode">The end node of the path.</param>
    /// <param name="transitions">A dictionary where the key is a node and the value is a list of nodes that the key node is connected to.</param>
    /// <param name="forbiddenNodes">An optional list of nodes that should not be traversed.</param>
    public static int ComputeNumberOfPathsFromStartNodeToEndNode(string startNode, string endNode, Dictionary<string, List<string>> transitions, List<string>? forbiddenNodes = null)
    {
        forbiddenNodes ??= [];

        var paths = new Queue<List<string>>();
        paths.Enqueue([startNode]);
        var completedPaths = new HashSet<List<string>>();
        while (paths.Count > 0)
        {
            var currentPath = paths.Dequeue();
            var currentNode = currentPath[^1];

            if (forbiddenNodes.Contains(currentNode)) continue;
            if (currentNode == endNode)
            {
                completedPaths.Add(currentPath);
                continue;
            }
            else
            {
                var possibleNextDevices = transitions[currentNode];
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

        return completedPaths.Count;
    }
}
