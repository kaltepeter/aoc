using System.Diagnostics;

namespace y2025.day_2;

public static class Day
{
    public static List<int> ProcessInput(string path, string filename)
    {
        List<int> result = [];
        try
        {
            using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
            {
                string? line;
                while ((line = sr.ReadLine()) != null)
                {
                    if (line.StartsWith("L"))
                    {
                        result.Add(-int.Parse(line.Substring(1)));
                    }
                    else if (line.StartsWith("R"))
                    {
                        result.Add(int.Parse(line.Substring(1)));
                    }
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.Message);
        }

        return result;
    }

    public static int Part1(List<int> input)
    {
        return 0;
    }

    public static int Part2(List<int> input)
    {
        return 0;
    }

    public static void Run()
    {
        // Path is relative to workspace root
        List<int> input = ProcessInput("dotnet/y2025/day_2", "input.txt");

        int part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");

        int part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
    }
}