using System.Diagnostics;

namespace y2025.day_2;
using y2025.util;

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
                    var start = parts[0];
                    var end = parts[1];
                    // var isValid = CheckValidInt(long.Parse(start)) && CheckValidInt(long.Parse(end));
                    // if (!isValid)
                    //     throw new InvalidOperationException($"Range {range} is invalid");
                    result.Add((long.Parse(start), long.Parse(end)));
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
            var numbers = Util.Range(start, end - start + 1)
                .Where(x => x.ToString().Length % 2 == 0);
            foreach (var number in numbers) {
                if (IsInvalidNumber(number)) {
                    invalidNumbers.Add(number);
                }
            }
        }
        return invalidNumbers.Sum();
    }

    public static long Part2(List<(long, long)> input)
    {
        return 0;
    }

    public static void Run()
    {
        // Path is relative to workspace root
        List<(long, long)> input = ProcessInput("dotnet/y2025/day_2", "input.txt");

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result > 2101246486);
        Debug.Assert(part1Result < 273626394091585);
        Debug.Assert(part1Result == 29940924880);

        long part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
    }
}