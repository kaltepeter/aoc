using System.Diagnostics;

namespace y2025.day_4;
using System.Linq;

public static class Day
{
    public static List<(int, int)> neighbor_coords = [(1, 0), (1, -1), (1, 1), (0, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1)];

    public static List<string> ProcessInput(string path, string filename)
    {
        List<string> result = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            string? line;
            while ((line = sr.ReadLine()) != null)
            {
                result.Add(line);
            }
        }
        return result;
    }

    public static List<char> GetNeighborPaperRolls(List<string> input, (int row, int col) position)
    {
        List<char> neighbors = [];
        (int x, int y) = position;
        var maxX = input[0].Length;
        var maxY = input.Count;
        foreach ((int dx, int dy) in neighbor_coords) {
            var neighbor = (x: x + dx, y: y + dy);
            if (neighbor.x < 0 || neighbor.x >= maxX || neighbor.y < 0 || neighbor.y >= maxY) {
                continue;
            }
            var cell = input[neighbor.x][neighbor.y];
            if (cell == '@') {
                neighbors.Add(cell);
            }
        }
        return neighbors.ToList();
    }

    public static int Part1(List<string> input)
    {
        int count = 0;
        foreach (var (row, rowIndex) in input.Select((value, rowIndex) => (value, rowIndex)))
        {
            foreach (var (col, colIndex) in row.Select((value, colIndex) => (value, colIndex)))
            {
                if (col != '@') {
                    continue;
                }
                var neighbors = GetNeighborPaperRolls(input, (rowIndex, colIndex));
                Debug.WriteLine($"row: {rowIndex}, col: {colIndex}, cell: {col}, neighbors: {string.Join(",", neighbors)}");
                if (neighbors.Count < 4)
                {
                    count += 1;
                }
            }
        }
        return count;
    }

    public static int Part2(List<string> input)
    {
        return 0;
    }

    public static void Run(string inputPath = "dotnet/y2025/day_4", string inputFilename = "input.txt")
    {
        List<string> input = ProcessInput(inputPath, inputFilename);

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result == 1505);

        long part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
    }
}