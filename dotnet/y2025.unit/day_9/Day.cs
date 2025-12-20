namespace y2025.unit.day_9;
using y2025.day_9;
using static y2025.day_9.Day;
using System.Drawing;

public class Day9Tests
{
    string inputPath = "../../../../y2025.unit/day_9";

    [Fact]
    public void Test_ProcessInput()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var results = Day.ProcessInput(inputPath, "example.txt");
        Assert.Equal(8, results.Count);
        Assert.Equal(new Point(7, 1), results[0]);
        Assert.Equal(new Point(11, 1), results[1]);
    }

    [Theory]
    [InlineData(new int[] {2, 3}, new int[] {11, 5}, true)]
    [InlineData(new int[] {2, 3}, new int[] {2, 3}, false)]
    [InlineData(new int[] {2, 3}, new int[] {11, 7}, true)]
    [InlineData(new int[] {25, 50}, new int[] {11, 7}, true)]
    public void Test_IsDiagonal(int[] p1, int[] p2, bool expected)
    {
        Assert.Equal(expected, Day.IsDiagonal(new Point(p1[0], p1[1]), new Point(p2[0], p2[1])));
    }

    [Fact]
    public void Test_GetArea()
    {
        Assert.Equal(50, Day.GetArea(new Point(2, 5), new Point(11, 1)));
        Assert.Equal(35, Day.GetArea(new Point(7, 1), new Point(11, 7)));
        Assert.Equal(6, Day.GetArea(new Point(2, 3), new Point(7, 3)));
        Assert.Equal(24, Day.GetArea(new Point(2, 5), new Point(9, 7)));
        Assert.Equal(8, Day.GetArea(new Point(4, 1), new Point(1, 0)));
    }

    [Fact]
    public void Test_GetManhattanDistance()
    {
        Assert.Equal(13, Day.GetManhattanDistance(new Point(2, 5), new Point(11, 1)));
        Assert.Equal(10, Day.GetManhattanDistance(new Point(7, 1), new Point(11, 7)));
        Assert.Equal(5, Day.GetManhattanDistance(new Point(2, 3), new Point(7, 3)));
        Assert.Equal(9, Day.GetManhattanDistance(new Point(2, 5), new Point(9, 7)));
        Assert.Equal(4, Day.GetManhattanDistance(new Point(4, 1), new Point(1, 0)));
        Assert.Equal(0, Day.GetManhattanDistance(new Point(11, 1), new Point(11, 1)));
    }
    
    [Fact]
    public void Test_Part1()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");

        var result = Day.Part1(input);
        Assert.Equal(50, result);
    }


    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(0, result);
    }

    [Fact]
    public void Debug_Day9_Run()
    {
        // Skip unless debugger is attached (allows debugging via code lens)
        if (!System.Diagnostics.Debugger.IsAttached)
        {
            Assert.Skip("Skipped unless debugger is attached. Use debug code lens to run.");
        }

        // Use this to debug Day2.Run() - set breakpoints and run with debugger
        // Pass path relative to workspace root (tests run from bin directory)
        Day.Run("../../../../y2025/day_9", "input.txt");
    }
}
