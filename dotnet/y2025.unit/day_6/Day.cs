namespace y2025.unit.day_6;
using y2025.day_6;
using static y2025.day_6.Day;

public class Day6Tests
{
    string inputPath = "../../../../y2025.unit/day_6";

    [Fact]
    public void Test_ProcessInput()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var results = Day.ProcessInput(inputPath, "example.txt");
        Assert.Equal(4, results.Count);
        
        var (inputs0, op0) = results[0];
        Assert.Collection(inputs0,
            item => Assert.Equal(123, item),
            item => Assert.Equal(45, item),
            item => Assert.Equal(6, item));
        Assert.Equal(Operation.Multiply, op0);
        
        var (inputs1, op1) = results[1];
        Assert.Collection(inputs1,
            item => Assert.Equal(328, item),
            item => Assert.Equal(64, item),
            item => Assert.Equal(98, item));
        Assert.Equal(Operation.Add, op1);
        
        var (inputs2, op2) = results[2];
        Assert.Collection(inputs2,
            item => Assert.Equal(51, item),
            item => Assert.Equal(387, item),
            item => Assert.Equal(215, item));
        Assert.Equal(Operation.Multiply, op2);
        
        var (inputs3, op3) = results[3];
        Assert.Collection(inputs3,
            item => Assert.Equal(64, item),
            item => Assert.Equal(23, item),
            item => Assert.Equal(314, item));
        Assert.Equal(Operation.Add, op3);
    }

    [Fact]
    public void Test_ProcessInput_Reverse()
    {
        // Path relative to workspace root - tests run from bin directory, so go up to workspace root
        var results = Day.ProcessInputReverse(inputPath, "example.txt");
        Assert.Equal(12, results.Count);
        Assert.Collection(results,
            item => Assert.Equal((4, null), item),
            item => Assert.Equal((431, null), item),
            item => Assert.Equal((623, Operation.Add), item),
            item => Assert.Equal((175, null), item),
            item => Assert.Equal((581, null), item),
            item => Assert.Equal((32, Operation.Multiply), item),
            item => Assert.Equal((8, null), item),
            item => Assert.Equal((248, null), item),
            item => Assert.Equal((369, Operation.Add), item),
            item => Assert.Equal((356, null), item),
            item => Assert.Equal((24, null), item),
            item => Assert.Equal((1, Operation.Multiply), item));
    }

    public static IEnumerable<object?[]> Test_GetValueFromCharData() {
       yield return new object?[] { ' ', null };
       yield return new object?[] { '1', "1"};
       yield return new object?[] { '0', "0" };
       yield return new object?[] { '+', Operation.Add };
       yield return new object?[] { '*', Operation.Multiply };
   }

    [Theory]
    [MemberData(nameof(Test_GetValueFromCharData))]
    public void Test_GetValueFromChar(char c, object? expected)
    {
        var result = Day.GetValueFromChar(c);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Test_Part1()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");

        var result = Day.Part1(input);
        Assert.Equal(4277556, result);
    }


    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInputReverse(inputPath, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(3263827, result);
    }
}