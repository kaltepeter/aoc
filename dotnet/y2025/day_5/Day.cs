using System.Diagnostics;

namespace y2025.day_5;
using System.Linq;
using System.Text.Json;

public static class Day
{
    public static (List<(long, long)>, List<long>) ProcessInput(string path, string filename)
    {
        List<(long, long)> ranges = [];
        List<long> ids = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            string? line;
            while ((line = sr.ReadLine()) != null)
            {
                if (string.IsNullOrEmpty(line))
                {
                    continue;
                }

                if (line.Contains("-"))
                {
                    var parts = line.Split('-');
                    var lower = long.Parse(parts[0]);
                    var upper = long.Parse(parts[1]);
                    ranges.Add((lower, upper));
                    // if (lower == upper) {
                    //     Console.WriteLine($"Lower bound is equal to upper bound: {lower} == {upper}");
                    // }
                }
                else
                {
                    ids.Add(long.Parse(line));
                }
            }
        }
        return (ranges, ids);
    }

    public static ((long, long), (long, long)) GetStats(List<(long, long)> ranges, List<long> ids) {
        Console.WriteLine($"range counts: {ranges.Count}, id counts: {ids.Count}");
        var minId = ids.Min();
        var maxId = ids.Max();
        Console.WriteLine($"min id: {minId}, max id: {maxId}, diff: {maxId - minId}");
        var lowestInRanges = ranges.Min(r => r.Item1);
        var highestInRanges = ranges.Max(r => r.Item2);
        Console.WriteLine($"lowest range: {ranges.Min(r => r.Item1)}, highest range: {ranges.Max(r => r.Item2)}, diff: {ranges.Max(r => r.Item2) - ranges.Min(r => r.Item1)}");
        return ((minId, maxId), (lowestInRanges, highestInRanges));
    }

    public static long Part1((List<(long, long)>, List<long>) input)
    {
        int count = 0;
        var (ranges, ids) = input;
        var (_, rangeLimits) = GetStats(ranges, ids);
        var (lowestInRanges, highestInRanges) = rangeLimits;
        foreach (var id in ids) {
            if (id < lowestInRanges || id > highestInRanges) {
                continue;
            }

            foreach (var range in ranges) {
                var (lower, upper) = range;
                if (id >= lower && id <= upper) {
                    count += 1;
                    break;
                }
            }
        }
        return count;
    }

    public static long Part2((List<(long, long)>, List<long>) input)
    {
        return 0;
    }

    public static void Run(string inputPath = "dotnet/y2025/day_5", string inputFilename = "input.txt")
    {
        var input = ProcessInput(inputPath, inputFilename);

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result == 520);

        long part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
    }
}