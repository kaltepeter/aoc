using System.Diagnostics;

namespace y2025.day_7;

using System.Data;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;
using y2025.util;
using System.Text;

using Result = List<string>;
using Position = (int x, int y);
using BeamTracker = Dictionary<int, List<int>>;

public static class Day
{
    public static Result ProcessInput(string path, string filename)
    {
        Result result = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            result = Util.ReadLines(sr)
                .Where(line => !string.IsNullOrWhiteSpace(line))
                .Select(line => line.Replace(".", " "))
                .ToList();
        }
        return result;
    }


    public static void PrintMap(BeamTracker beams, Result input)
    {
        Result map = input.ToList();
        foreach (var (x, rows) in beams)
        {
            foreach (var y in rows)
            {
                StringBuilder sb = new StringBuilder(map[y]);
                sb[x] = '|';
                map[y] = sb.ToString();
            }
        }
        foreach (var row in map)
        {
            Console.WriteLine(string.Join(" ", row));
        }
    }

    private static void AddToBeam(BeamTracker beams, int x, int y)
    {
        if (!beams.TryGetValue(x, out var list))
        {
            list = new List<int>();
            beams[x] = list;
        }
        list.Add(y);
    }

    public static int CountBeams(BeamTracker beams)
    {
        int count = 0;
        foreach (var (x, rows) in beams)
        {
            count += rows.Count();
        }
        return count;
    }

    public static (int, List<Position>) Part1(Result input)
    {
        Position start = (x: input[0].IndexOf('S'), y: 0);
        BeamTracker beams = new()
        {
            [start.x] = new List<int> { start.y + 1 }
        };
        List<Position> splitters = [];

        var map = input.ToList();

        foreach (var (row, rowIndex) in map.Select((value, rowIndex) => (value, rowIndex)))
        {
            foreach (var (col, colIndex) in row.Select((value, colIndex) => (value, colIndex)))
            {
                bool hasBeam = beams.GetValueOrDefault(colIndex, []).Contains(rowIndex - 1);
                if (hasBeam)
                {
                    if (col == '^')
                    {
                        splitters.Add((colIndex, rowIndex));
                        AddToBeam(beams, colIndex - 1, rowIndex);
                        AddToBeam(beams, colIndex + 1, rowIndex);
                    }
                    else if (col == ' ')
                    {
                        AddToBeam(beams, colIndex, rowIndex);
                    }
                }
            }
        }
        // PrintMap(beams, map);

        return (splitters.Count(), splitters);
    }


    public static long GetTimelineCount(Result map, int x, int y, Dictionary<(int x, int y), long> cache)
    {
        var key = (x, y);
        if (cache.TryGetValue(key, out long cached))
        {
            return cached;
        }

        char c = map[y][x];
        long result = 0;

        if (y >= map.Count - 1)
        {
            result = 1;
        } 
        else if (c == ' ' || c == 'S')
        {
            result = GetTimelineCount(map, x, y + 1, cache);
        }
        else if (c == '^')
        {
            long leftCount = GetTimelineCount(map, x - 1, y, cache);
            long rightCount = GetTimelineCount(map, x + 1, y, cache);
            result = leftCount + rightCount;
        }

        return cache[key] = result;
    }

    public static long Part2(Result input)
    {
        var map = input.ToList();
        Position start = (x: input[0].IndexOf('S'), y: 0);
        var cache = new Dictionary<(int x, int y), long>();

        return GetTimelineCount(map, start.x, start.y, cache);
    }

    public static void Run(string inputPath = "dotnet/y2025/day_7", string inputFilename = "input.txt")
    {
        var input = ProcessInput(inputPath, inputFilename);

        var (splitterCount, _) = Part1(input);
        Console.WriteLine($"Part I: {splitterCount}");
        Debug.Assert(splitterCount < 1688);
        Debug.Assert(splitterCount == 1581);

        var part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
        Debug.Assert(part2Result > 3160);
        Debug.Assert(part2Result == 73007003089792);
    }
}