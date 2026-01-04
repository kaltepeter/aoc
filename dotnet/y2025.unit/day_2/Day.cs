namespace y2025.unit.day_2;
using y2025.day_2;

public class Day2Tests
{
    string inputPath = "../../../../y2025.unit/day_2";

    [Fact]
    public void Test_ProcessInput()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var result = Day.ProcessInput(inputPath, "example.txt");
        Assert.Equal(11, result.Count);
        Assert.Equal((11, 22), result[0]);
        Assert.Equal((95, 115), result[1]);
    }

    [Fact]
    public void Test_Part1()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
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

    [Theory]
    [InlineData(1, false)]
    [InlineData(11, true)]
    [InlineData(12, false)]
    [InlineData(22, true)]
    [InlineData(99, true)]
    [InlineData(111, true)]
    [InlineData(123, false)]
    [InlineData(115, false)]
    [InlineData(1112, false)]
    [InlineData(1001, false)]
    [InlineData(10000, false)]
    [InlineData(11112222, false)]
    [InlineData(1188511885, true)]
    [InlineData(12341234, true)]
    [InlineData(123123123, true)]
    [InlineData(123456789, false)]
    [InlineData(1212121212, true)]
    [InlineData(1111111, true)]
    [InlineData(1698522, false)]
    [InlineData(123412356, false)]
    [InlineData(824824824, true)]
    [InlineData(2121212121, true)]
    [InlineData(2121212123, false)]
    [InlineData(504504, true)]
    [InlineData(505050, true)]
    public void Test_IsInvalidNumberPart2(long number, bool expected)
    {
        bool result = Day.IsInvalidNumberPart2(number);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(4174379265, result);
    }

    [Fact]
    public void Debug_Day2_Run()
    {
        // Skip unless debugger is attached (allows debugging via code lens)
        if (!System.Diagnostics.Debugger.IsAttached)
        {
            Assert.Skip("Skipped unless debugger is attached. Use debug code lens to run.");
        }
        
        // Use this to debug Day2.Run() - set breakpoints and run with debugger
        // Pass path relative to workspace root (tests run from bin directory)
        Day.Run("../../../../y2025/day_2", "range.txt");
    }
}  