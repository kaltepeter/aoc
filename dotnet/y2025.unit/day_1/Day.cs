namespace y2025.unit.day_1;
using y2025.day_1;

public class Day1Tests
{
    string path = "../../../../y2025/day_1";

    [Fact]
    public void Test_ProcessInput()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var result = Day.ProcessInput(path, "example.txt");
        Assert.Equal(new List<int> { -68, -30, 48, -5, 60, -55, -1, -99, 14, -82 }, result);
    }

    [Fact]
    public void Test_Part1()
    {
        var input = Day.ProcessInput(path, "example.txt");
        var result = Day.Part1(input);
        Assert.Equal(3, result);
    }

    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(path, "example.txt");
        var result = Day.Part2(input);
        // Update expected value when Part2 is implemented
        Assert.Equal(0, result);
    }
}
