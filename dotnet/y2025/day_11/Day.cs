using System.Diagnostics;

namespace y2025.day_11;

using System.Data;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;
using y2025.util;

using Result = Dictionary<string, List<string>>;

public enum RequiredSeen {
    None, 
    DAC,
    FFT,
    ALL
}

public static class Day
{
    public static Result ProcessInput(string path, string filename)
    {
        Result result = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            result = Util.ReadLines(sr)
                .Where(line => !string.IsNullOrWhiteSpace(line))
                .Select(line => line.Split(':'))
                .ToDictionary(parts => parts[0].Trim(), parts => parts[1].Trim().Split(' ').ToList());
        }
        return result;
    }


    public static long CountPaths(Result input, Dictionary<string, long> memo, string node) {
        if (node == "out") {
            return 1;
        }

        if (memo.ContainsKey(node)) {
            return memo[node];
        }

        long count = 0;
        foreach (var nextNode in input[node]) {
            count += CountPaths(input, memo, nextNode);
        }
        
        return memo[node] = count;
    }


    public static long Part1(Result input)
    {
        Dictionary<string, long> memo = new();

        var count = CountPaths(input, memo, "you");
        return count;
    }

    public static long ExplorePaths(Result input, Dictionary<(string, RequiredSeen), long> memo, string node, RequiredSeen requiredSeen) {
        if (node == "out") {
            if (requiredSeen == RequiredSeen.ALL) {
                return 1;
            }
            return 0;
        }

        if (memo.ContainsKey((node, requiredSeen))) {
            return memo[(node, requiredSeen)];
        }

        if (node == "dac") {
            requiredSeen |= RequiredSeen.DAC;
        }
        if (node == "fft") {
            requiredSeen |= RequiredSeen.FFT;
        }

        long count = 0;
        foreach (var nextNode in input[node]) {
            count += ExplorePaths(input, memo, nextNode, requiredSeen);
        }
        
        return memo[(node, requiredSeen)] = count;
    }

    public static long Part2(Result input)
    {
        Dictionary<(string, RequiredSeen), long> memo = new();
        var result = ExplorePaths(input, memo, "svr", RequiredSeen.None);
        return result;
    }

    public static void Run(string inputPath = "dotnet/y2025/day_11", string inputFilename = "input.txt")
    {
        var input = ProcessInput(inputPath, inputFilename);

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result == 555);

        long part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
        Debug.Assert(part2Result < 52278330597728296);
        Debug.Assert(part2Result < 1110803659982690);
        Debug.Assert(part2Result > 9055);
        Debug.Assert(part2Result == 502447498690860);
    }
}
