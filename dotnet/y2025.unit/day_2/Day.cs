namespace y2025.unit.day_2;
using y2025.day_2;

public class Day2Tests
{
    string path = "../../../../y2025.unit/day_2";

    [Fact]
    public void Test_ProcessInput()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var result = Day.ProcessInput(path, "example.txt");
        Assert.Equal(11, result.Count);
        Assert.Equal((11, 22), result[0]);
        Assert.Equal((95, 115), result[1]);
    }

    [Fact]
    public void Test_Part1()
    {
        var input = Day.ProcessInput(path, "example.txt");
        var result = Day.Part1(input);
        Assert.Equal(1227775554, result);
    }

    [Theory]
    [InlineData(11, true)]
    [InlineData(22, true)]
    [InlineData(6464, true)]
    [InlineData(123123, true)]
    [InlineData(1188511885, true)]
    [InlineData(222220, false)]
    [InlineData(222224, false)]
    public void Test_IsInvalidNumber(long number, bool expected)
    {
        bool result = Day.IsInvalidNumber(number);
        Assert.Equal(expected, result);
    }

    [Theory]
    [InlineData(101)]
    public void Test_IsInvalidNumber_Odd_Digits(long number)
    {
        Assert.Throws<InvalidOperationException>(() => Day.IsInvalidNumber(number));
    }

    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(path, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(0, result);
    }
}  