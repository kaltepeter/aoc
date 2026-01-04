using System.Diagnostics;

namespace y2025.day_2;
using y2025.util;
using System.Linq;

public static class Day
{
    public static List<(long, long)> ProcessInput(string path, string filename)
    {
        List<(long, long)> result = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            string? line;
            while ((line = sr.ReadLine()) != null)
            {
                var ranges = line.Split(',');
                foreach (var range in ranges)
                {
                    var parts = range.Split('-');
                    result.Add((long.Parse(parts[0]), long.Parse(parts[1])));
                }
            }
        }
        return result;
    }

    public static bool CheckValidInt(long value) {
        if (value > int.MaxValue || value < int.MinValue)
            return false;
        return true;
    }

    public static bool IsInvalidNumber(long number)
    {
        var strValue = number.ToString();
        var isOdd = strValue.Length % 2 == 1;
        if (isOdd) {
            throw new InvalidOperationException("Number has an odd number of digits");
        }
        var mid = strValue.Length / 2;
        var (left, right) = (strValue[0..mid],strValue[mid..]);
        return left == right;
    }

    public static long Part1(List<(long, long)> input)
    {
        List<long> invalidNumbers = [];
        foreach (var (start, end) in input) {
            var numbers = Util.Range(start, end)
                .Where(x => x.ToString().Length % 2 == 0);
            foreach (var number in numbers) {
                if (IsInvalidNumber(number)) {
                    invalidNumbers.Add(number);
                }
            }
        }
        return invalidNumbers.Sum();
    }

    public static bool IsInvalidNumberPart2(long number)
    {
        var strValue = number.ToString();
        var uniqueChars = new HashSet<char>(strValue);
        if (uniqueChars.Count == 1 && strValue.Length > 1) {
            return true;
        }

        for (int patternLength = 1; patternLength <= strValue.Length / 2; patternLength++) {
            if (strValue.Length % patternLength == 0 && patternLength > 1) {
                var parts = strValue.Chunk(patternLength).Select(chunk => new string(chunk));
                var firstPart = parts.First();
                var remainingParts = parts.Skip(1);
                if (remainingParts.All(part => part == firstPart)) {
                    return true;
                }
            }
        }
        return false;
    }

    public static long Part2(List<(long, long)> input)
    {
        List<long> invalidNumbers = [];
        var invalidSet = new HashSet<long>();
        foreach (var (start, end) in input) {
            var numbers = Util.Range(start, end);
            foreach (var number in numbers) {
                if (IsInvalidNumberPart2(number)) {
                    invalidSet.Add(number);
                }
            }
        }
        return invalidSet.Sum();
    }

    public static void Run(string inputPath = "dotnet/y2025/day_2", string inputFilename = "input.txt")
    {
        List<(long, long)> input = ProcessInput(inputPath, inputFilename);

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result > 2101246486);
        Debug.Assert(part1Result < 273626394091585);
        Debug.Assert(part1Result == 29940924880);

        long part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
        Debug.Assert(part2Result < 48631959042);
        Debug.Assert(part2Result > 18803488789);
        Debug.Assert(part2Result == 48631958998);
    }
}