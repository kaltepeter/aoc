using System.Diagnostics;

namespace y2025.day_6;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;
using y2025.util;

using Result = List<(List<int>, Operation)>;

public enum Operation {
    Add = '+',
    Multiply = '*'
}

public static class Day
{
    public static Result ProcessInput(string path, string filename)
    {
        Result results = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            var rows = Util.ReadLines(sr)
                .Where(line => !string.IsNullOrWhiteSpace(line))
                .Select(line => Regex.Split(line, @"\s+")
                    .Where(s => !string.IsNullOrEmpty(s))
                    .ToList())
                .ToList();

            int numberOfColumns = rows[0].Count();
            
            bool allSameLength = rows.Count == 0 || rows.All(list => list.Count == numberOfColumns);
            if (!allSameLength)
            {
                throw new Exception($"All lists must be the same length: {numberOfColumns}");
            }

            var columns = Enumerable.Range(0, numberOfColumns)
                .Select(colIndex => rows.Select(row => row[colIndex]).ToList())
                .ToList();

            foreach (var column in columns)
            {
                var inputs = column.SkipLast(1).Select(int.Parse).ToList();
                Operation operation = (Operation)column.Last()[0];
                results.Add((inputs, operation));
            }
        }
        return results;
    }


    public static long Part1(Result input)
    {
        List<long> results = [];

        foreach (var (inputs, operation) in input)
        {
            switch (operation)
            {
                case Operation.Add:
                    results.Add(inputs.Sum());
                    break;
                case Operation.Multiply:
                    results.Add(inputs.Select(x => (long)x).Aggregate(1L, (acc, x) => acc * x));
                    break;
            }
        }

        return results.Sum();
    }

    public static long Part2(Result input)
    {
        return 0;
    }

    public static void Run(string inputPath = "dotnet/y2025/day_6", string inputFilename = "input.txt")
    {
        var input = ProcessInput(inputPath, inputFilename);

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result > 25506327850);
        Debug.Assert(part1Result == 6605396225322);

        long part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
    }
}