namespace y2025.unit.day_10;
using y2025.day_10;
using static y2025.day_10.Day;
using System.Diagnostics;
using System.Text.Json;

public class Day10Tests
{
    string inputPath = "../../../../y2025.unit/day_10";

    [Fact]
    public void Test_ProcessInput()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var results = Day.ProcessInput(inputPath, "example.txt");
        Assert.Equal(3, results.Count);
        Assert.Equal(".##.", results[0].Pattern);
        Assert.Equal(new List<int> { 3 }, results[0].Buttons.First().Positions);
        Assert.Equal(6, results[0].Buttons.Count());
        Assert.Equal(2, results[0].Buttons.Last().Positions.Count());
        Assert.Equal(new List<int> { 3, 5, 4, 7 }, results[0].Joltages);
    }

    [Theory]
    [InlineData(".##.", 0b0110)]
    [InlineData("..#.", 0b0010)]
    [InlineData("#..#", 0b1001)]
    [InlineData("####", 0b1111)]
    public void TestResult_GetLights(string pattern, int expected) {
        var result = new Result { Pattern = pattern };
        Assert.Equal(expected, result.GetLights());
    }

    [Theory]
    [InlineData(".##.", new int[] { 1, 2 })]
    [InlineData("..#.", new int[] { 2 })]
    [InlineData("#..#", new int[] { 0, 3 })]
    [InlineData("####", new int[] { 0, 1, 2, 3 })]
    public void TestResult_GetLightPositions(string pattern, int[] expected) {
        var result = new Result { Pattern = pattern };
        Assert.Equal(expected.ToList(), result.GetLightPositions());
    }

    [Theory]
    [InlineData(new int[] { 1, 2 }, 4,0b0110)]
    [InlineData(new int[] { 2 }, 4, 0b0010)]
    [InlineData(new int[] { 0, 3 }, 4, 0b1001)]
    [InlineData(new int[] { 0, 1, 2, 3 }, 4, 0b1111)]
    public void TestButton_CalculateButtonMask(int[] positions, int length, int expected) {
        var button = new Button { Positions = positions.ToList() };
        Assert.Equal(expected, Button.CalculateButtonMask(button.Positions, length));
    }

    [Fact]
    public void TestResult_FilteredButtons() {
        var results = Day.ProcessInput(inputPath, "example.txt");
        Assert.Equal(5, results[0].FilteredButtons().Count());
        Assert.Equal(3, results[1].FilteredButtons().Count());
        Assert.Equal(4, results[2].FilteredButtons().Count());
    }
    
    [Fact]
    public void Test_Part1()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");

        var result = Day.Part1(input);
        Assert.Equal(7, result);
    }


    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(0, result);
    }

    [Fact]
    public void Debug_Day10_Run()
    {
        // Skip unless debugger is attached (allows debugging via code lens)
        if (!System.Diagnostics.Debugger.IsAttached)
        {
            Assert.Skip("Skipped unless debugger is attached. Use debug code lens to run.");
        }

        // Use this to debug Day2.Run() - set breakpoints and run with debugger
        // Pass path relative to workspace root (tests run from bin directory)
        Day.Run("../../../../y2025/day_10", "input.txt");
    }
}
