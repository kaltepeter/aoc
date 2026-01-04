using System.Diagnostics;

namespace y2025.day_3;
using y2025.util;
using System.Linq;
using System.Text.Json;

public static class Day
{
    public static List<List<int>> ProcessInput(string path, string filename)
    {
        List<List<int>> result = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            string? line;
            while ((line = sr.ReadLine()) != null)
            {
                result.Add(line.Select(c => int.Parse(c.ToString())).ToList());
            }
        }
        return result;
    }

    public static List<int> GetHighestTwoJoltage(List<int> bank, int numBatteries = 2)
    {
        var found = new List<int>();
        var rightBound = bank.Count - numBatteries + 1;
        var leftBank = bank.ToList()[..rightBound];
        var max = leftBank.Max();
        var maxIndex = bank.IndexOf(max);
        if (maxIndex < rightBound) {
            found.Add(max);
        }
        
        var max_found = bank[maxIndex + 1];

        for (int i = maxIndex + 1; i < bank.Count; i++) {
            if (bank[i] >= max_found) {
                max_found = bank[i];
            }
        }
        found.Add(max_found);
    
        // Debug.WriteLine(JsonSerializer.Serialize(bank));
        // Debug.WriteLine(JsonSerializer.Serialize(found));
        return found;
    }

    public static long Part1(List<List<int>> input)
    {
        long totalJoltage = 0;
        foreach (var bank in input) {
            var top_two_joltage = GetHighestTwoJoltage(bank);
            totalJoltage += long.Parse(string.Join("", top_two_joltage));
        }
        return totalJoltage;
    }

     public static List<int> GetHighestJoltageByNumBatteries(List<int> bank, int numBatteries = 2)
    {
        var found = new List<int>();
        var remainingBatteries = numBatteries;
        var currentIndex = 0;
        var curList = bank.ToList();

        for (int i = currentIndex; i < curList.Count; i++) {
            if (found.Count == numBatteries) {
                break;
            }
            var nextMax = curList[i];
            var nextMaxIndex = i;
            for (int j = i + 1; j < curList.Count; j++) {
                var rightBound = curList.Count - remainingBatteries;
                if (curList[j] > nextMax && j <= rightBound) {
                    nextMax = curList[j];
                    nextMaxIndex = j;
                }
            }
            found.Add(nextMax);
            remainingBatteries -= 1;
            i = nextMaxIndex;
        }
    
        return found;
    }

    public static long Part2(List<List<int>> input)
    {
        long totalJoltage = 0;
        foreach (var bank in input) {
            var topJoltages = GetHighestJoltageByNumBatteries(bank, 12);
            totalJoltage += long.Parse(string.Join("", topJoltages));
        }
        return totalJoltage;
    }

    public static void Run(string inputPath = "dotnet/y2025/day_3", string inputFilename = "input.txt")
    {
        List<List<int>> input = ProcessInput(inputPath, inputFilename);

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result == 17100);

        long part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
        Debug.Assert(part2Result == 170418192256861);
    }
}
