namespace y2025.unit.day_3;
using y2025.day_3;
using System.Collections.Generic;

public class Day3Tests
{
    string inputPath = "../../../../y2025.unit/day_3";

    [Fact]
    public void Test_ProcessInput()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var result = Day.ProcessInput(inputPath, "example.txt");
        Assert.Equal(4, result.Count);
        Assert.Equal(new List<int> { 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1}, result[0]);
        Assert.Equal(new List<int> { 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9 }, result[1]);
        Assert.Equal(new List<int> { 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8 }, result[2]);
        Assert.Equal(new List<int> { 8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1 }, result[3]);
    }

    [Fact]
    public void Test_Part1()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part1(input);
        Assert.Equal(357, result);
    }

    public static IEnumerable<object[]> GetHighestTwoJoltageTestData()
    {
        // Test case 1
        yield return new object[] 
        { 
            new List<int> { 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1}, 
            new List<int> { 9, 8 }
        };
        
        // Test case 2
        yield return new object[] 
        { 
            new List<int> { 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9 }, 
             new List<int> { 8, 9 }
        };
        
        // Test case 3
        yield return new object[] 
        { 
            new List<int> { 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8 }, 
             new List<int> { 7, 8 }
        };
        
        // Test case 4
        yield return new object[] 
        { 
            new List<int> { 8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1 }, 
             new List<int> { 9, 2 }
        };
    }

    [Theory]
    [MemberData(nameof(GetHighestTwoJoltageTestData))]
    public void Test_GetHighestTwoJoltage(List<int> bank, List<int> expected_results)
    {
        var result = Day.GetHighestTwoJoltage(bank);
        Assert.Equal(expected_results, result);
    }


    [Fact]
    public void Test_GetHighestTwoJoltage_ShouldNotThrow()
    {
        var bank = new List<int> { 8, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 9, 1 };
        var result = Day.GetHighestTwoJoltage(bank);
        Assert.Equal(new List<int> { 9, 1 }, result);
    }


    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(3121910778619, result);
    }
}