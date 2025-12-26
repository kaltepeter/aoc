namespace y2025.unit.day_10;
using y2025.day_10;
using static y2025.day_10.Day;
using System.Diagnostics;
using System.Text.Json;
using MathNet.Numerics.LinearAlgebra;

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
        Assert.Equal(
            new Dictionary<int, int> { 
                { 0, 3 }, { 1, 5 }, { 2, 4 }, { 3, 7 } 
            }, results[0].Joltages);
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

    [Fact(Skip = "Not used")]
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
    public void Test_IsJoltagesFound() {
        var targetJoltages = new Dictionary<int, int> { { 0, 3 }, { 1, 5 }, { 2, 4 }, { 3, 7 } };
        var joltages = new Dictionary<int, int> { { 0, 3 }, { 1, 5 }, { 2, 4 }, { 3, 7 } };
        Assert.True(Day.IsJoltagesFound(targetJoltages, joltages));
    }

    [Fact]
    public void Test_IsJoltagesFound_False() {
        var targetJoltages = new Dictionary<int, int> { { 0, 3 }, { 1, 5 }, { 2, 4 }, { 3, 7 } };
        var joltages = new Dictionary<int, int> { { 0, 0 }, { 1, 5 }, { 2, 4 }, { 3, 7 } };
        Assert.False(Day.IsJoltagesFound(targetJoltages, joltages));
    }

    [Fact(Skip = "Not used")]
    public void Test_ClickButton() {
        var targetJoltages = new Dictionary<int, int> { { 0, 3 }, { 1, 5 }, { 2, 4 }, { 3, 7 } };
        var joltages = new Dictionary<int, int> { { 0, 0 }, { 1, 0 }, { 2, 0 }, { 3, 0 } };
        var button = new Button { Positions = new List<int> { 0, 1 } };
        var buttonsInCommon = new List<Button> { 
            new Button {
            Positions = new List<int> { 0, 2 }
            }, 
            new Button {
                Positions = new List<int> { 1, 3 }
            }
        };
        var (newJoltages, clicks) = Day.ClickButton(targetJoltages, joltages, buttonsInCommon, button);
        Assert.Equal(3, clicks);
        Assert.Equal(new Dictionary<int, int> { { 0, 3 }, { 1, 5 }, { 2, 1 }, { 3, 3 } }, newJoltages);
    }

    // [Fact]
    // public void Test_ClickButton_TooHigh() {
    //     var targetJoltages = new Dictionary<int, int> { { 0, 3 }, { 1, 5 }, { 2, 4 }, { 3, 7 } };
    //     var joltages = new Dictionary<int, int> { { 0, 3 }, { 1, 3 }, { 2, 0 }, { 3, 0 } };
    //     var button = new Button { Positions = new List<int> { 0, 2 } };
    //     var (newJoltages, clicks) = Day.ClickButton(targetJoltages, joltages, button);
    //     Assert.Equal(joltages, newJoltages);
    //     Assert.Equal(0, clicks);
    // }

    [Fact]
    public void Test_GaussianElimination() {
        var input = Day.ProcessInput(inputPath, "example.txt");
        foreach (var result in input) {
            var matrix = result.ToAugmentedMatrix();
            Day.GaussianEliminationRREF(matrix);
        }
        // Assert.Equal(matrix.ToString(), new Matrix<double>(3, 3, new double[] { 1, 2, 3, 0, 1, 2, 0, 0, 1 }).ToString());
    }

    [Fact]
    public void Test_GetBoundsForIndependentVar() {
        var matrix = Matrix<double>.Build.Dense(3, 5, new double[] { 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, -1, 0, 6, -1, 5 });
        var (lower, upper) = Day.GetBoundsForIndependentVar(matrix, 3, 3);
        Assert.Equal(1, lower);
        Assert.Equal(6, upper);

        var input = Day.ProcessInput(inputPath, "example.txt");
        matrix = input[0].ToAugmentedMatrix();
        
        
        (lower, upper) = Day.GetBoundsForIndependentVar(matrix, 3, 4);
        Assert.Equal(0, lower);
        Assert.Equal(4, upper);

        (lower, upper) = Day.GetBoundsForIndependentVar(matrix, 5, 4);
        Assert.Equal(0, lower);
        Assert.Equal(3, upper);
    }

    [Fact]
    public void Test_ComputeDependentVariables() {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var matrix = input[0].ToAugmentedMatrix();
        var (transformedMatrix, independentVariables, dependentVariables) = Day.GaussianEliminationRREF(matrix);
        var dependentValues = Day.ComputeDependentVariables(transformedMatrix, dependentVariables, independentVariables, new int[] { 1, 0 });
        Assert.Equal(new double[] {1, 5, 0, 3}, dependentValues);
    }

    [Fact]
    public void Test_FindMinClicks() {
        var input = Day.ProcessInput(inputPath, "sample.txt");
        var results = new List<int>();
        for (int i = 0; i < input.Count; i++) {
            var result = input[i];
            var matrix = result.ToAugmentedMatrix();
            var (transformedMatrix, independentVariables, dependentVariables) = Day.GaussianEliminationRREF(matrix);
               Debug.WriteLine($"Dependent Variables: {string.Join(",", dependentVariables)}");
            Debug.WriteLine($"Independent Variables: {string.Join(",", independentVariables)}");
            Debug.WriteLine(transformedMatrix.ToString());
            var assignment = new int[independentVariables.Count];
            var maxBound = transformedMatrix.Column(transformedMatrix.ColumnCount - 1)
                .Select(value => Math.Abs((int)Math.Round(value)))
                .Max();
            var lowestClicks = Day.FindMinClicks(transformedMatrix, independentVariables, dependentVariables, maxBound, 0, assignment);
            results.Add(lowestClicks);
        }
        Assert.Equal(new List<int> { 79, 61, 74 }, results);
    }

    [Fact]
    public void Test_Part2()
    {
        var input = Day.ProcessInput(inputPath, "example.txt");
        var result = Day.Part2(input);
        Assert.Equal(33, result);
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
