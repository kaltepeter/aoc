using System.Diagnostics;

namespace y2025.day_10;

using System.Data;
using System.Linq;
using System.Runtime.InteropServices.Swift;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using y2025.util;

public struct Button
{
    public List<int> Positions { get; set; }
    public int Mask { get; set; }

    public override string ToString()
    {
        return $"B({string.Join(",", Positions), 4} Mask: {Mask, 2})";
    }

    public static int CalculateButtonMask(List<int> button, int length)
    {
        int mask = 0b0;
        int max = button.Max();
        button.ForEach(i =>
        {
            if (i == 0)
            {
                mask |= 1 << (length - 1);
            }
            else
            {
                mask |= 1 << (length - 1 - i);
            }
        });
        return mask;
    }
}

public struct Result
{
    public string Pattern { get; set; }
    public List<Button> Buttons { get; set; }
    public List<int> Joltages { get; set; }

    public int LowestClicks { get; set; }

    public override string ToString()
    {
        const int padding = 14;
        var stringBuilder = new StringBuilder();
        stringBuilder.Append($"{Convert.ToString(GetLights(), 2).PadLeft(Pattern.Length, '0'),padding} {Pattern,padding}\t");
        stringBuilder.Append("Pos: ".PadLeft(2) + $"{string.Join(",", GetLightPositions()),padding}\t");
        stringBuilder.Append("Counts: ".PadLeft(2) + $"{Buttons.Count(),2} / {FilteredButtons().Count(),2},\t");
        stringBuilder.Append($"Lowest: {LowestClicks,2}");
        // stringBuilder.Append($"Joltages({Joltages.Count()}): {string.Join(", ", Joltages)}");
        return stringBuilder.ToString();
    }

    public string ToIntString()
    {
        var stringBuilder = new StringBuilder();
        var light = GetLights();
        stringBuilder.Append($"{light,4}\t");
        var buttonValues = FilteredButtons().Select(button => light ^ button.Mask);
        stringBuilder.Append($"{string.Join(",", buttonValues),4}\t");
        return stringBuilder.ToString();
    }

    public int GetLights()
    {
        return Pattern.Aggregate(0, (acc, c) => (acc << 1) | (c == '#' ? 1 : 0));
    }

    public List<int> GetLightPositions()
    {
        return Pattern.Select((c, i) => (c == '#' ? i : -1)).Where(i => i != -1).ToList().OrderBy(i => i).ToList();
    }

    public List<Button> FilteredButtons()
    {
        var lightPositions = GetLightPositions().ToHashSet();
        return Buttons.Where(buttonList => buttonList.Positions.ToHashSet().Intersect(lightPositions).Count() > 0).ToList();
    }

}

public static class Day
{
    public static List<List<Button>> CombinationsOfSize(List<Button> items, int k)
    {
        if (k == 0) return new List<List<Button>> { new List<Button>() };
        if (k > items.Count) return new List<List<Button>>();

        var result = new List<List<Button>>();

        // Include first item
        var withFirst = CombinationsOfSize(items.Skip(1).ToList(), k - 1);
        foreach (var combo in withFirst)
        {
            combo.Insert(0, items[0]);
            result.Add(combo);
        }

        // Exclude first item
        var withoutFirst = CombinationsOfSize(items.Skip(1).ToList(), k);
        result.AddRange(withoutFirst);

        return result;
    }

    public static List<Result> ProcessInput(string path, string filename)
    {
        List<Result> results = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            results = Util.ReadLines(sr)
                .Where(line => !string.IsNullOrWhiteSpace(line))
                .Select(line => line
                    .Replace("[", "")
                    .Replace("]", "")
                    .Replace("(", "")
                    .Replace(")", "")
                    .Replace("{", "")
                    .Replace("}", "")
                    .Trim().Split(' '))
                .Select(parts => (Pattern: parts.First(),
                    Buttons: parts.Skip(1).Take(parts.Count() - 2).Select(btn => btn.Split(',').Select(int.Parse).ToList()).ToList(),
                    Joltages: parts.Last().Split(',').Select(int.Parse).ToList()))
                .Select(parts => new Result
                {
                    Pattern = parts.Pattern,
                    Buttons = parts.Buttons.Select(btn =>
                        new Button
                        {
                            Positions = btn,
                            Mask = Button.CalculateButtonMask(btn, parts.Pattern.Length)
                        }).ToList(),
                    Joltages = parts.Joltages,
                    LowestClicks = int.MaxValue
                })
                .ToList();

            // lines.ForEach(line => Debug.WriteLine(line.ToString()));

        }
        return results;
    }

    public static int ClickButton(int light, Button button)
    {
        var mask = button.Mask;
        var val = light ^ mask;
        return val;
    }

    public static int Part1(List<Result> input)
    {
        List<Result> results = input.ToList();
        for (int i = 0; i < input.Count; i++)
        {
            var result = results[i];

            var buttons = result.Buttons;
            var light = result.GetLights();
            if (buttons.Count() == 0)
            {
                throw new Exception("No buttons found");
            }

            if (light == 0)
            {
                result.LowestClicks = 0;
                results[i] = result;
                continue;
            }

            var rounds = 1;
            var maxRounds = 1000;
            bool found = false;

            while (!found && rounds < maxRounds) {
                List<List<Button>> combos = CombinationsOfSize(
                    buttons.ToList(), rounds
                );
                foreach (var combo in combos) {
                    var value = combo.Select(button => button.Mask)
                        .Aggregate(light, (acc, mask) => acc ^ mask);
                    
                    if (value == 0) {
                        result.LowestClicks = Math.Min(result.LowestClicks, rounds);
                        results[i] = result;
                        found = true;
                        break;
                    }
                }
                rounds += 1;
            }
        }
        results.ForEach(result => Debug.WriteLine(result.ToString()));
        return results.Select(result => result.LowestClicks).Sum();
    }

    public static int Part2(List<Result> input)
    {
        return 0;
    }

    public static void Run(string inputPath = "dotnet/y2025/day_10", string inputFilename = "input.txt")
    {
        var input = ProcessInput(inputPath, inputFilename);

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result == 396);

        long part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
    }
}
