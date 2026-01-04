namespace y2025.unit.day_1;
using y2025.day_1;

public class Day1Tests
{
    string path = "../../../../y2025.unit/day_1";

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
    public void Test_Part2_Large_Rotation()
    {
        var result = Day.Part2(50, [1000]);
        Assert.Equal(10, result);
    }

    [Fact]
    public void Test_Part2_Backward_Rotation()
    {
        var result = Day.Part2(50, [-68]);
        Assert.Equal(1, result);
    }

    [Fact]
    public void Test_Part2_Backward_Rotation_To_Zero()
    {
        var result = Day.Part2(0, [-5]);
        Assert.Equal(0, result);
    }

    [Fact]
    public void Test_Part2_Forward_Rotation()
    {
        var result = Day.Part2(95, [60]);
        Assert.Equal(1, result);
    }

    [Fact]
    public void Test_Part2_Forward_Rotation_To_Zero()
    {
        var result = Day.Part2(52, [48]);
        Assert.Equal(1, result);
    }

    [Fact]
    public void Test_Part2_Forward_End_Zero_Without_Passing_Zero()
    {
        var result = Day.Part2(55, [-55]);
        Assert.Equal(1, result);
    }

    [Fact]
    public void Test_Part2_Forward_Should_Pass_Zero_Once()
    {
        var result = Day.Part2(50, [150]);
        Assert.Equal(2, result);
    }

    [Fact]
    public void Test_Part2_Backward_Should_Pass_Zero_Once()
    {
        var result = Day.Part2(50, [-150]);
        Assert.Equal(2, result);
    }

    [Fact]
    public void Test_Part2_Large_Forward_Rotation_Ending_At_Zero()
    {
        var result = Day.Part2(50, [250]);
        Assert.Equal(3, result);
    }

    [Fact]
    public void Test_Part2_Large_Backward_Rotation_Ending_At_Zero()
    {
        var result = Day.Part2(50, [-250]);
        Assert.Equal(3, result);
    }

    [Fact]
    public void Test_Part2_Ends_On_One_Hundred()
    {
        var result = Day.Part2(0, [100]);
        Assert.Equal(1, result);
    }

    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(path, "example.txt");
        var result = Day.Part2(50, input);
        Assert.Equal(6, result);
    }
}
