using System.Diagnostics;
using System.IO.Compression;
using System.Text.RegularExpressions;

namespace Day08;

class Program
{
    private readonly static bool DEBUG = true;
    private readonly static string TEST_FILE_NAME = "test.txt";

    static void Main(string[] args)
    {
        // Read in the input
        var parentDirectory = Directory.GetParent(AppContext.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
        var inputFileFullPath = Path.Combine(parentDirectory, "input.txt");
        var coordinates = File.ReadAllLines(inputFileFullPath)
            .Where(line => !string.IsNullOrWhiteSpace(line))
            .Select(line => line.Split(','))
            .Select(parts => (x: int.Parse(parts[0]), y: int.Parse(parts[1]), z: int.Parse(parts[2])))
            .ToList();
        
        // Part 1 - Connect together the 1000 pairs of junction boxes that are closest to each other
        // and compute the multiplication of the resulting connected components' sizes
        var numberJunctionBoxesToConnect = inputFileFullPath.EndsWith(TEST_FILE_NAME) ? 10 : 1000;

        if (DEBUG) Console.WriteLine("Starting distance computation.");
        
        // 1.1 - Compute all distances
        var orderedCoordinatePairs = new SortedList<double, List<(int, int)>>();
        // Key: distance, Value: pair of coordinate indices
        for (var i = 0; i < coordinates.Count; i++)
        {
            for (var j = i + 1; j < coordinates.Count; j++)
            {
                var distance = ComputeDistance(coordinates[i], coordinates[j]);
                if (!orderedCoordinatePairs.ContainsKey(distance))
                    orderedCoordinatePairs[distance] = new List<(int, int)>();
                
                orderedCoordinatePairs[distance].Add((i, j));
                // by convention, adding only (i,j) where i<j to avoid duplicates
            }
        }

        if (DEBUG) Console.WriteLine("Computed all distances. \nNow computing groups.");

        // 1.2 - Then make the groups
        var groups = new List<HashSet<int>>();
        // each group is a set of coordinate indices
        var groupMembership = new List<int?>();
        for (var i = 0; i < coordinates.Count; i++)
            groupMembership.Add(null);
        // each index contains the index of the group the coordinate belongs to, or null if none
        var idx = 0;
        while (idx < numberJunctionBoxesToConnect)
        {
            var nextPairs = orderedCoordinatePairs.ElementAt(idx).Value;
            foreach (var pair in nextPairs)
            {
                var (coord1Index, coord2Index) = pair;
                var group1Index = groupMembership[coord1Index];
                var group2Index = groupMembership[coord2Index];

                if (group2Index >= groups.Count || group2Index < 0 || group1Index >= groups.Count || group1Index < 0)
                    Console.WriteLine("Group index out of range");

                if (group1Index == null && group2Index == null)
                {
                    // Create a new group
                    var newGroup = new HashSet<int>() { coord1Index, coord2Index };
                    groups.Add(newGroup);

                    var newGroupIndex = groups.Count - 1;
                    groupMembership[coord1Index] = newGroupIndex;
                    groupMembership[coord2Index] = newGroupIndex;
                }
                else if (group1Index != null ^ group2Index != null)
                {
                    // Only one of the 2 coordinates is in a group
                    // --> add the other one to the group
                    var groupIndex = group1Index ?? group2Index;
                    groups[groupIndex!.Value].Add(coord1Index);
                    groups[groupIndex!.Value].Add(coord2Index);
                    // we are using a hashset so adding an existing element is fine
                    groupMembership[coord1Index] = groupIndex;
                    groupMembership[coord2Index] = groupIndex;
                }
                else if (group1Index != null && group2Index != null && group1Index != group2Index)
                {
                    // Merge groups
                    var groupToKeepIndex = group1Index.Value;
                    var groupToMergeIndex = group2Index.Value;
                    var groupToKeep = groups[groupToKeepIndex];
                    var groupToMerge = groups[groupToMergeIndex];
                    foreach (var coordIdx in groupToMerge)
                    {
                        groupToKeep.Add(coordIdx);
                        groupMembership[coordIdx] = groupToKeepIndex;
                    }

                    groups.RemoveAt(groupToMergeIndex);
                    // Update all groupMembership indices greater than groupToMergeIndex
                    for (var k = groupToMergeIndex; k < groups.Count; k++)
                    {
                        foreach (var coordIdx in groups[k])
                        {
                            groupMembership[coordIdx] --;
                        }
                    }
                }

                idx ++;
                if (idx >= numberJunctionBoxesToConnect)
                    break;
            }
        }

        // 1.3 - Compute the multiplication of the sizes of the 3 largest groups and output the result
        int numberOfGroupsToMultiply = 3;
        long multiplicationOfGroupSizes = groups
            .Select(g => (long)g.Count)
            .OrderByDescending(size => size)
            .Take(numberOfGroupsToMultiply)
            .Aggregate(1L, (acc, val) => acc * val);
        Console.WriteLine("PART 1 - The multiplication of the sizes of all connected junction boxes is: " + multiplicationOfGroupSizes);
    }

    public static double ComputeDistance((int x, int y, int z) pointA, (int x, int y, int z) pointB)
    {
        return Math.Sqrt(
            Math.Pow(pointA.x - pointB.x, 2) + 
            Math.Pow(pointA.y - pointB.y, 2) + 
            Math.Pow(pointA.z - pointB.z, 2));
    }
}
