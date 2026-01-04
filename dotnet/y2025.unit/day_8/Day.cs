namespace y2025.unit.day_8;
using y2025.day_8;
using static y2025.day_8.Day;

using Shared;
using Result = List<Shared.Point>;
using PuzzleResult = long;
using DistanceTracker = Dictionary<Shared.Point, Dictionary<Shared.Point, double>>;

public class Day8Tests
{
    string inputPath = "../../../../y2025.unit/day_8";

    static readonly Result testInput = Day.ProcessInput("../../../../y2025.unit/day_8", "example.txt");
    static readonly DistanceTracker orderedDistances = Day.GetDistances(testInput);
    

    [Fact]
    public void Test_ProcessInput()
    {
        var results = Day.ProcessInput(inputPath, "example.txt");
        Assert.Equal(20, results.Count);
        Assert.Equal(new Point(57, 618, 57), results[1]);
        
    }

    [Fact]
    public void Test_GetDistances()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var distances = Day.GetDistances(input);
        Assert.Equal(20, distances.Count);
        Assert.Equal(19, distances[new Point(162,817,812)].Count);
        Assert.Equal(19, distances[new Point(216,146,977)].Count);
        Assert.Equal(new Point(425,690,689), distances[new Point(162,817,812)].Keys.First());
        Assert.Equal(new Point(162,817,812), distances[new Point(425,690,689)].Keys.First());
    }

    [Fact]
    public void Test_Part1()
    {
        var result = Day.Part1(orderedDistances, CreateUnionFind(testInput), 10);
        Assert.Equal(40, result);
    }


    [Fact]
    public void Test_Part2()
    {
        var result = Day.Part2(orderedDistances, CreateUnionFind(testInput));
        Assert.Equal(25272, result);
    }

    [Fact]
    public void Test_RenderNetwork()
    {
        var testUf = CreateUnionFind(testInput);
        Day.Part1(orderedDistances, testUf, 10);
        
        var dotPath = Path.Join(inputPath, "graph.dot");
        if (File.Exists(dotPath))
        {
            File.Delete(dotPath);
        }
        Assert.False(File.Exists(dotPath), "graph.dot should not exist before RenderNetwork");
        
        // Render the network
        Day.RenderNetwork(inputPath, testUf);
        
        // Assert file exists with bytes after
        Assert.True(File.Exists(dotPath), "graph.dot should exist after RenderNetwork");
        var fileInfo = new FileInfo(dotPath);
        Assert.True(fileInfo.Length > 0, "graph.dot should have content (bytes > 0)");
    }

    [Fact]
    public void Test_RenderNetwork_File_Exists()
    {
        var testUf = CreateUnionFind(testInput);
        Day.Part1(orderedDistances, testUf, 10);
        
        var dotPath = Path.Join(inputPath, "graph.dot");
        var originalWriteTime = File.GetLastWriteTime(dotPath);
        Assert.True(originalWriteTime > DateTime.MinValue, "graph.dot should have a write time");
        Assert.True(File.Exists(dotPath), "graph.dot should exist before RenderNetwork");
        
        // Render the network
        Day.RenderNetwork(inputPath, testUf);
        
        // Assert file exists with bytes after
        Assert.True(File.Exists(dotPath), "graph.dot should exist after RenderNetwork");
         var modifiedWriteTime = File.GetLastWriteTime(dotPath);
         Assert.True(modifiedWriteTime > originalWriteTime, "graph.dot should have a newer write time after RenderNetwork");

    }
}
