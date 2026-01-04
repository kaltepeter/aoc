using System.Diagnostics;

namespace y2025.day_8;

using System.Data;
using System.Linq;
using Shared;
using y2025.util;

using Result = List<Shared.Point>;
using PuzzleResult = long;
using DistanceTracker = Dictionary<Shared.Point, Dictionary<Shared.Point, double>>;

public static class Day
{
    public static Result ProcessInput(string path, string filename)
    {
        Result result = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            result = Util.ReadLines(sr)
                .Where(line => !string.IsNullOrWhiteSpace(line))
                .Select(line => line.Split(',').Select(double.Parse).ToArray())
                .Select(parts => new Point(parts[0], parts[1], parts[2]))
                .ToList();
        }
        return result;
    }

    public static DistanceTracker GetDistances(Result input)
    {
        var distances = new Dictionary<Point, Dictionary<Point, double>>();
        foreach (var (point, index) in input.Select((point, index) => (point, index)))
        {
            distances[point] = new Dictionary<Point, double>();
            foreach (var (otherPoint, otherIndex) in input.Select((point, index) => (point, index)))
            {
                if (point == otherPoint)
                {
                    continue;
                }

                distances[point][otherPoint] = Util.CalculateEuclideanDistanceThreeDimensional(point, otherPoint);
            }
        }

        var orderedDistances = distances.ToDictionary(
            kvp => kvp.Key,
            kvp => kvp.Value.OrderBy(innerKvp => innerKvp.Value).ToDictionary(innerKvp => innerKvp.Key, innerKvp => innerKvp.Value)
        );

        return orderedDistances;
    }

    public static UnionFind<Point> CreateUnionFind(Result input)
    {
        var uf = new UnionFind<Point>();
        foreach (var point in input)
        {
            uf.MakeSet(point);
        }
        return uf;
    }

    public static PuzzleResult Part1(DistanceTracker orderedDistances, UnionFind<Point> uf, int numConnections)
    {
        // Generate all pairs from all points, normalize, deduplicate, and get 10 shortest
        var pairs = orderedDistances
            .SelectMany(kvp => kvp.Value.Select(innerKvp => (kvp.Key, innerKvp.Key, innerKvp.Value)))
            .Select(pair => {
                // Normalize pairs so (A,B) and (B,A) are treated as the same
                var (p1, p2, dist) = pair;
                return p1 <= p2 ? (p1, p2, dist) : (p2, p1, dist);
            })
            .GroupBy(pair => (pair.Item1, pair.Item2)) // Group by normalized pair
            .Select(g => g.First()) // Take first from each group (removes duplicates)
            .OrderBy(pair => pair.Item3)
            .Take(numConnections); // Get the 10 shortest connections


        foreach (var (pair1, pair2, distance) in pairs)
        {
            Point p1 = uf.Find(pair1);
            Point p2 = uf.Find(pair2);

            uf.Union(p1, p2);
        }

        var result = uf.GetRootSizes()
        .Where(p => p.Value > 1)
        .OrderByDescending(p => p.Value)
        .Take(3)
        .Aggregate(1L, (acc, p) => acc * p.Value);

        // Debug.WriteLine($"UnionFind: {uf}");

        return result;
    }

    public static void RenderNetwork(string inputPath, UnionFind<Point> uf) {
        var dotPath = Path.Join(inputPath, "graph.dot");

        if (File.Exists(dotPath))
        {
            File.Delete(dotPath);
        }
        Debug.Assert(!File.Exists(dotPath), "graph.dot should exist after RenderNetwork");

        var dotContent = new RenderNetwork().ToGraphvizDot(uf);
        File.WriteAllText(dotPath, dotContent);
        Debug.Assert(File.Exists(dotPath), "graph.dot should exist after RenderNetwork");
        Console.WriteLine($"Graphviz DOT file saved to {dotPath}");
        Console.WriteLine($"To render: dot -Tpng {dotPath} -o {Path.Join(inputPath)}graph.png");
    }

    public static PuzzleResult Part2(DistanceTracker orderedDistances, UnionFind<Point> uf)
    {
        // Generate all pairs from all points, normalize, deduplicate, and get 10 shortest
        var pairs = orderedDistances
            .SelectMany(kvp => kvp.Value.Select(innerKvp => (kvp.Key, innerKvp.Key, innerKvp.Value)))
            .Select(pair => {
                // Normalize pairs so (A,B) and (B,A) are treated as the same
                var (p1, p2, dist) = pair;
                return p1 <= p2 ? (p1, p2, dist) : (p2, p1, dist);
            })
            .GroupBy(pair => (pair.Item1, pair.Item2)) // Group by normalized pair
            .Select(g => g.First()) // Take first from each group (removes duplicates)
            .OrderBy(pair => pair.Item3);

        Point? point1 = null;
        Point? point2 = null;

        foreach (var (pair1, pair2, distance) in pairs)
        {
            Point p1 = uf.Find(pair1);
            Point p2 = uf.Find(pair2);

            if (p1 == p2) {
                continue;
            }

            uf.Union(p1, p2);
    
            // Check if all networks are connected (only one root remaining)
            if (uf.GetRoots().Count() == 1)
            {
                point1 = pair1;
                point2 = pair2;
                break;
            }
            
        }

        var result = (long)(point1!.Value.X * point2!.Value.X);
        return result;
    }

    public static void Run(string inputPath = "dotnet/y2025/day_8", string inputFilename = "input.txt")
    {
        var input = ProcessInput(inputPath, inputFilename);
        var orderedDistances = GetDistances(input);
        var uf = CreateUnionFind(input);

        long part1Result = Part1(orderedDistances, uf, 1000);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result == 164475);
        RenderNetwork(inputPath, uf);

        long part2Result = Part2(orderedDistances, uf);
        Console.WriteLine($"Part II: {part2Result}");
        Debug.Assert(part2Result == 169521198);
    }
}
