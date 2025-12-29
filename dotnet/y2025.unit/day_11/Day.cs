namespace y2025.unit.day_11;
using y2025.day_11;
using static y2025.day_11.Day;
using System.Text.Json;
using System.Diagnostics;

public class Day11Tests
{
    string inputPath = "../../../../y2025.unit/day_11";

    [Fact]
    public void Test_ProcessInput()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var results = Day.ProcessInput(inputPath, "example.txt");
        Debug.WriteLine(JsonSerializer.Serialize(results));
        Assert.Equal(10, results.Count);
        Assert.Equal(new List<string> { "bbb", "ccc" }, results["you"]);
        Assert.Equal(new List<string> { "out" }, results["eee"]);
    }
    
    [Fact]
    public void Test_Part1()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");

        var result = Day.Part1(input);
        Assert.Equal(5, result);
    }


    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(0, result);
    }

    [Fact]
    public void Debug_Day11_Run()
    {
        // Skip unless debugger is attached (allows debugging via code lens)
        if (!System.Diagnostics.Debugger.IsAttached)
        {
            Assert.Skip("Skipped unless debugger is attached. Use debug code lens to run.");
        }

        // Use this to debug Day2.Run() - set breakpoints and run with debugger
        // Pass path relative to workspace root (tests run from bin directory)
        Day.Run("../../../../y2025/day_11", "input.txt");
    }
}
