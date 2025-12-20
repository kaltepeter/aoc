using System.Diagnostics;

namespace y2025.day_9;

using System.Data;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;
using y2025.util;
using System.Drawing;

using Result = List<System.Drawing.Point>;

public static class Day
{
    public static Result ProcessInput(string path, string filename)
    {
        Result result = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            result = Util.ReadLines(sr)
                .Where(line => !string.IsNullOrWhiteSpace(line))
                .Select(line => line.Split(',').Select(int.Parse).ToArray())
                .Select(parts => new Point(parts[0], parts[1]))
                .ToList();
        }
        return result;
    }

    public static bool IsDiagonal(Point p1, Point p2) {
        return p1.X != p2.X && p1.Y != p2.Y;
    }

    public static long GetManhattanDistance(Point p1, Point p2) {
        return Math.Abs(p1.X - p2.X) + Math.Abs(p1.Y - p2.Y);
    }

    public static long GetArea(Point p1, Point p2) {
        long width = Math.Abs((long)p2.X - p1.X) + 1;
        long height = Math.Abs((long)p2.Y - p1.Y) + 1;
        return width * height;
    }

    public static long Part1(Result input)
    {
        // var maxX = input.Max(p => p.X);
        // var maxY = input.Max(p => p.Y);
        // var minX = input.Min(p => p.X);
        // var minY = input.Min(p => p.Y);
        // var corners = new List<Point> { new Point(minX, minY), new Point(maxX, minY), new Point(minX, maxY), new Point(maxX, maxY) };

        // var cornerPoints = input
        //     .SelectMany(point => corners.Select(corner => (point: point, corner: corner, dist: GetManhattanDistance(point, corner))))
        //     .OrderBy(tuple => tuple.dist)
        //     .ToList();


        // var pointsToCheck = cornerPoints.GroupBy(tuple => tuple.corner)
        //     .SelectMany(group => {
        //         var sorted = group.OrderBy(t => t.dist).ToList();
        //         return new[] { sorted.First(), sorted.Last() };
        //     })
        //     .Select(tuple => tuple.point)
        //     .Distinct();
        var pointsToCheck = input;

        var areas = pointsToCheck
            .SelectMany((point1, i) => pointsToCheck.Skip(i+1).Select((point2) => (point1, point2)))
            .Select(pair => (p1: pair.point1, p2: pair.point2, dist: GetManhattanDistance(pair.point1, pair.point2), area: GetArea(pair.point1, pair.point2)))
            .OrderByDescending(a => a.area);

        var (_, _, dist, area) = areas.First();

        return area;
    }

    public static long Part2(Result input)
    {
       return 0;
    }

    public static void Run(string inputPath = "dotnet/y2025/day_9", string inputFilename = "input.txt")
    {
        var input = ProcessInput(inputPath, inputFilename);

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result > 2147425684);
        Debug.Assert(part1Result == 4735268538);

        long part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
    }
}
