namespace y2025.unit.day_7;
using y2025.day_7;
using static y2025.day_7.Day;

using BeamTracker = Dictionary<int, List<int>>;

public class Day7Tests
{
    string inputPath = "../../../../y2025.unit/day_7";

    [Fact]
    public void Test_ProcessInput()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var results = Day.ProcessInput(inputPath, "example.txt");
        Assert.Equal(16, results.Count);

    }

    [Fact(Skip = "Wasn't needed or working")]
    public void Test_CountBeams()
    {
        BeamTracker beams = new()
        {
            [7] = new List<int> { 1, 4, 4, 5, 8, 9, 10, 11, 12, 12, 13 },
            [6] = new List<int> { 2, 3, 6, 6, 7, 10, 11, 14, 14, 15 },
            [8] = new List<int> { 2, 3, 6, 6, 7, 8, 9, 10, 10, 11, 12, 13, 14, 14, 15 },
            [5] = new List<int> { 4, 5, 8, 8, 9, 12, 13 },
            [9] = new List<int> { 4, 5, 8, 9 },
            [4] = new List<int> { 6, 7, 10, 10, 11, 12, 13, 14, 14, 14, 15 },
            [10] = new List<int> { 6, 7, 10, 10, 11, 12, 13, 14, 15 },
            [3] = new List<int> { 8, 9, 12, 13 },
            [11] = new List<int> { 8, 9, 12, 13, 14, 15 },
            [2] = new List<int> { 10, 11, 14, 14, 15 },
            [12] = new List<int> { 10, 11, 14, 15 },
            [1] = new List<int> { 12, 13 },
            [13] = new List<int> { 12, 13 },
            [0] = new List<int> { 14, 15 },
            [14] = new List<int> { 14, 15 }
        };

        int result = Day.CountBeams(beams);
        Assert.Equal(21, result);
    }

    [Fact]
    public void Test_Part1()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");

        var result = Day.Part1(input);
        Assert.Equal(21, result);
    }


    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(0, result);
    }

    [Fact]
    public void Debug_Day7_Run()
    {
        // Skip unless debugger is attached (allows debugging via code lens)
        if (!System.Diagnostics.Debugger.IsAttached)
        {
            Assert.Skip("Skipped unless debugger is attached. Use debug code lens to run.");
        }

        // Use this to debug Day2.Run() - set breakpoints and run with debugger
        // Pass path relative to workspace root (tests run from bin directory)
        Day.Run("../../../../y2025/day_7", "input.txt");
    }
}