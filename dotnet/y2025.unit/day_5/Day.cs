namespace y2025.unit.day_5;
using y2025.day_5;

public class Day5Tests
{
    string inputPath = "../../../../y2025.unit/day_5";

    [Fact]
    public void Test_ProcessInput()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var (ranges, ids) = Day.ProcessInput(inputPath, "example.txt");
        Assert.Equal(4, ranges.Count);
        Assert.Equal((3, 5), ranges[0]);
        Assert.Equal(6, ids.Count);
    }

    [Fact]
    public void Test_Part1()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part1(input);
        Assert.Equal(3, result);
    }


    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(0, result);
    }
}