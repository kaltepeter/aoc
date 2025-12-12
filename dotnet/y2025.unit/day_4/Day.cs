namespace y2025.unit.day_4;
using y2025.day_4;

public class Day4Tests
{
    string inputPath = "../../../../y2025.unit/day_4";

    [Fact]
    public void Test_ProcessInput()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var result = Day.ProcessInput(inputPath, "example.txt");
        Assert.Equal(10, result.Count);
        Assert.Equal("..@@.@@@@.", result[0]);
    }

//     public static IEnumerable<object[]> Test_GetNeighborPositionsData() {
//        yield return new object[] { (0, 0), new List<char> { '.', '@', '@' } };
//    }

    [Theory]
    // [MemberData(nameof(Test_GetNeighborPositionsData))]
    [InlineData(new object[] {0, 0}, 2)]
    [InlineData(new object[] {9, 9}, 2)]
    [InlineData(new object[] {4, 4}, 8)]
    [InlineData(new object[] {0, 2}, 3)]
    public void Test_GetNeighborPositions(object[] position, int expected)
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.GetNeighborPaperRolls(input, ((int)position[0], (int)position[1]));
        Assert.Equal(expected, result.Count);
    }

    [Fact]
    public void Test_Part1()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part1(input);
        Assert.Equal(13, result);
    }

    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(0, result);
    }

}