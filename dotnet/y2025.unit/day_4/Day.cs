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

    [Theory]
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

    public static IEnumerable<object[]> Test_RemoveRollsData() {
       yield return new object[] { new List<(int, int)> { (0, 2), (0, 3), (0, 5), (0, 6), (0, 8) }, "..xx.xx@x.", 0 };
       yield return new object[] { new List<(int, int)> { (1, 0) }, "x@@.@.@.@@", 1 };
   }

    [Theory]
    [MemberData(nameof(Test_RemoveRollsData))]
    public void Test_RemoveRolls(List<(int, int)> rollsToRemove, string expectedRow, int expectedRowIndex)
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.RemoveRolls(input, rollsToRemove);
        Assert.Equal(expectedRow, result[expectedRowIndex]);
    }

    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(43, result);
    }

}