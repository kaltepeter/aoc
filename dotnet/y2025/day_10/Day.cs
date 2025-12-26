using System.Diagnostics;

namespace y2025.day_10;

using System.Data;
using System.Linq;
using System.Runtime.InteropServices.Swift;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using y2025.util;
using MathNet.Numerics.LinearAlgebra;

using Joltage = Dictionary<int, int>;
using ExCSS;

public struct Button
{
    public List<int> Positions { get; set; }
    public int Mask { get; set; }

    public override string ToString()
    {
        return $"B({string.Join(",", Positions), 4} Mask: {Mask, 2})";
    }

    public static int CalculateButtonMask(List<int> button, int length)
    {
        int mask = 0b0;
        int max = button.Max();
        button.ForEach(i =>
        {
            if (i == 0)
            {
                mask |= 1 << (length - 1);
            }
            else
            {
                mask |= 1 << (length - 1 - i);
            }
        });
        return mask;
    }


}

public struct Result
{
    public string Pattern { get; set; }
    public List<Button> Buttons { get; set; }
    public Joltage Joltages { get; set; }

    public int LowestClicks { get; set; }

    public Dictionary<int, List<int>> PositionFrequency { get; set; }

    public override string ToString()
    {
        const int padding = 14;
        var stringBuilder = new StringBuilder();
        stringBuilder.Append($"{Convert.ToString(GetLights(), 2).PadLeft(Pattern.Length, '0'),padding} {Pattern,padding}\t");
        stringBuilder.Append("Pos: ".PadLeft(2) + $"{string.Join(",", GetLightPositions()),padding}\t");
        stringBuilder.Append("Counts: ".PadLeft(2) + $"{Buttons.Count,2} / {FilteredButtons().Count,2},\t");
        // stringBuilder.Append($"Lowest: {LowestClicks,2}");
        stringBuilder.Append($"Joltages: ({Joltages.Values.Count, 2}), min: {Joltages.Values.Min(), 2}, max: {Joltages.Values.Max(), 2}");
        return stringBuilder.ToString();
    }

    public string ToIntString()
    {
        var stringBuilder = new StringBuilder();
        var light = GetLights();
        stringBuilder.Append($"{light,4}\t");
        var buttonValues = FilteredButtons().Select(button => light ^ button.Mask);
        stringBuilder.Append($"{string.Join(",", buttonValues),4}\t");
        return stringBuilder.ToString();
    }

    public int GetLights()
    {
        return Pattern.Aggregate(0, (acc, c) => (acc << 1) | (c == '#' ? 1 : 0));
    }

    public List<int> GetLightPositions()
    {
        return Pattern.Select((c, i) => (c == '#' ? i : -1)).Where(i => i != -1).ToList().OrderBy(i => i).ToList();
    }

    public List<Button> FilteredButtons()
    {
        var joltagePositions = Joltages.Keys.ToHashSet();
        return Buttons.Where(buttonList => buttonList.Positions.ToHashSet().Intersect(joltagePositions).Count() > 0).ToList();
    }

    public Matrix<double> ToAugmentedMatrix() {
        var positions = Joltages.Keys.OrderBy(k => k).ToList();
        var matrix = Matrix<double>.Build.Dense(positions.Count, Buttons.Count + 1);
        for (int row = 0; row < positions.Count; row++) {
            int position = positions[row];
            for (int col = 0; col < Buttons.Count; col++) {
                matrix[row, col] = Buttons[col].Positions.Contains(position) ? 1 : 0;
            }
            matrix[row, Buttons.Count] = Joltages[position];
        }
        return matrix;
    }
}

public static class Day
{
    public static List<List<Button>> CombinationsOfSize(List<Button> items, int k)
    {
        if (k == 0) return new List<List<Button>> { new List<Button>() };
        if (k > items.Count) return new List<List<Button>>();

        var result = new List<List<Button>>();

        // Include first item
        var withFirst = CombinationsOfSize(items.Skip(1).ToList(), k - 1);
        foreach (var combo in withFirst)
        {
            combo.Insert(0, items[0]);
            result.Add(combo);
        }

        // Exclude first item
        var withoutFirst = CombinationsOfSize(items.Skip(1).ToList(), k);
        result.AddRange(withoutFirst);

        return result;
    }

    public static List<Result> ProcessInput(string path, string filename)
    {
        List<Result> results = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            results = Util.ReadLines(sr)
                .Where(line => !string.IsNullOrWhiteSpace(line))
                .Select(line => line
                    .Replace("[", "")
                    .Replace("]", "")
                    .Replace("(", "")
                    .Replace(")", "")
                    .Replace("{", "")
                    .Replace("}", "")
                    .Trim().Split(' '))
                .Select(parts => (Pattern: parts.First(),
                    Buttons: parts.Skip(1).Take(parts.Length - 2).Select(btn => btn.Split(',').Select(int.Parse).ToList()).ToList(),
                    Joltages: parts.Last().Split(',').Select(int.Parse).ToList()))
                .Select(parts => new Result
                {
                    Pattern = parts.Pattern,
                    Buttons = parts.Buttons.Select(btn =>
                        new Button
                        {
                            Positions = btn,
                            Mask = Button.CalculateButtonMask(btn, parts.Pattern.Length)
                        }).ToList(),
                    Joltages = parts.Joltages.Select((joltage, index) => (index, joltage)).ToDictionary(t => t.index, t => t.joltage),
                    LowestClicks = int.MaxValue,
                })
                .ToList();

            // lines.ForEach(line => Debug.WriteLine(line.ToString()));

        }
        return results;
    }

    public static int ClickButton(int light, Button button)
    {
        var mask = button.Mask;
        var val = light ^ mask;
        return val;
    }

    public static int Part1(List<Result> input)
    {
        List<Result> results = input.ToList();
        for (int i = 0; i < input.Count; i++)
        {
            var result = results[i];

            var buttons = result.Buttons;
            var light = result.GetLights();
            if (buttons.Count == 0)
            {
                throw new Exception("No buttons found");
            }

            if (light == 0)
            {
                result.LowestClicks = 0;
                results[i] = result;
                continue;
            }

            var rounds = 1;
            var maxRounds = 1000;
            bool found = false;

            while (!found && rounds < maxRounds) {
                List<List<Button>> combos = CombinationsOfSize(
                    buttons.ToList(), rounds
                );
                foreach (var combo in combos) {
                    var value = combo.Select(button => button.Mask)
                        .Aggregate(light, (acc, mask) => acc ^ mask);
                    
                    if (value == 0) {
                        result.LowestClicks = Math.Min(result.LowestClicks, rounds);
                        results[i] = result;
                        found = true;
                        break;
                    }
                }
                rounds += 1;
            }
        }
        // results.ForEach(result => Debug.WriteLine(result.ToString()));
        return results.Select(result => result.LowestClicks).Sum();
    }

    public static bool IsJoltagesFound(Joltage targetJoltages, Joltage joltages) {
        return joltages.Count == targetJoltages.Count &&
                    joltages.All(kvp => targetJoltages.TryGetValue(kvp.Key, out var val) && val == kvp.Value);
    }

    public static void PrintMatrix(double[,] matrix, string label = "Matrix") {
        int rows = matrix.GetLength(0);
        int cols = matrix.GetLength(1);
        Debug.WriteLine($"{label} ({rows}x{cols}):");
        for (int i = 0; i < rows; i++) {
            var row = new List<string>();
            for (int j = 0; j < cols; j++) {
                row.Add(matrix[i, j].ToString().PadLeft(4));
            }
            // Separate augmented column with |
            if (cols > 1) {
                row.Insert(cols - 1, " |");
            }
            Debug.WriteLine(string.Join(" ", row));
        }
    }

    public static (Matrix<double> matrix, List<int> independentVariables, List<int> dependentVariables) GaussianEliminationRREF(Matrix<double> matrix) {
        var pivot = 0;
        var colIndex = 0;
        var maxColIndex = matrix.ColumnCount - 1;
        var independentVariables = new List<int>();
        var dependentVariables = new List<int>();
        
        while (pivot < matrix.RowCount && colIndex < maxColIndex) {
            var column = matrix.Column(colIndex);
            var (bestRow, bestValue) = column
                .Select((value, index) => (index, value))
                .Where((_, index) => index >= pivot)
                .MaxBy(kvp => Math.Abs(kvp.value));

            if (bestValue == 0) {
                independentVariables.Add(colIndex);
                colIndex++;
                continue;
            }
 
            var row1 = matrix.Row(pivot);
            matrix.SetRow(pivot, matrix.Row(bestRow));
            matrix.SetRow(bestRow, row1);
            dependentVariables.Add(colIndex);

            for (int r = pivot + 1; r < matrix.RowCount; r++) {
                var factor = matrix[r, colIndex] / matrix[pivot, colIndex];
                var newRow = matrix.Row(r).Subtract(factor * matrix.Row(pivot));
                matrix.SetRow(r, newRow);
            }

            
            pivot++;
            colIndex++;
        }

        // Backward pass - eliminate above each pivot
        for (int r = dependentVariables.Count - 1; r >= 0; r--) {
            var pivotCol = dependentVariables[r];
            
            // Eliminate entries ABOVE this pivot (rows 0 to r-1)
            for (int rowAbove = 0; rowAbove < r; rowAbove++) {
                var factor = matrix[rowAbove, pivotCol] / matrix[r, pivotCol];
                var newRow = matrix.Row(rowAbove).Subtract(factor * matrix.Row(r));
                matrix.SetRow(rowAbove, newRow);
            }

            // Normalize pivot row (do this ONCE, outside the inner loop)
            var pivotValue = matrix[r, pivotCol];
            var normalizedRow = matrix.Row(r).Divide(pivotValue);
            matrix.SetRow(r, normalizedRow);
        }

        independentVariables.AddRange(Enumerable.Range(colIndex, maxColIndex - colIndex));
        return (matrix, independentVariables, dependentVariables);
    }

    public static (int lowerBound, int upperBound) GetBoundsForIndependentVar(
        Matrix<double> matrix, int freeCol, int pivotRowCount
    ) {
        var lower = 0;
        var upper = int.MaxValue;
        int lastCol = matrix.ColumnCount - 1;

        for (int row = 0; row < pivotRowCount; row++) {
            double coeff = matrix[row, freeCol];
            double constant = matrix[row, lastCol];

            if (coeff > 0) {
                upper = Math.Min(upper, (int)Math.Floor(constant / coeff));
            } else if (coeff < 0) {
                lower = Math.Max(lower, (int)Math.Ceiling(-constant / Math.Abs(coeff)));
            }

        }

        return (lower, upper);
    }

    public static double[] ComputeDependentVariables(
        Matrix<double> matrix, 
        List<int> dependentCols, 
        List<int> independentCols,
        int[] independentVarAssignment
    ) {
        int lastCol = matrix.ColumnCount - 1;
        var dependentValues = new double[dependentCols.Count];

        for (int row = 0; row < dependentCols.Count; row++) {
            double value = matrix[row, lastCol];

            for (int i = 0; i < independentCols.Count; i++) {
                value -= matrix[row, independentCols[i]] * independentVarAssignment[i];
            }

            dependentValues[row] = value;
        }

        return dependentValues;
    }

    public static int FindMinClicks(
        Matrix<double> matrix,
        List<int> independentCols,
        List<int> dependentCols,
        int maxBound,
        int independentVarIndex,                      // which free var we're assigning
        int[] currentAssignment               // partial assignment so far
    ) {
        if (independentVarIndex == independentCols.Count) {
            var dependentValues = ComputeDependentVariables(matrix, dependentCols, independentCols, currentAssignment);
            
            foreach (var val in dependentValues) {
                double rounded = Math.Round(val);
                if (rounded < 0) {
                    return int.MaxValue;
                }
                if (Math.Abs(val - rounded) > 1e-10) {
                    return int.MaxValue;
                }
            }

            int total = currentAssignment.Sum();
            total += (int)Math.Round(dependentValues.Sum());
            return total;
        }
        
        // var (lower, upper) = GetBoundsForIndependentVar(matrix, independentCols[independentVarIndex], dependentCols.Count);
        var (lower, upper) = (0, maxBound);
        int best = int.MaxValue;

        for (int value = lower; value <= upper; value++) {
            currentAssignment[independentVarIndex] = value;
            var result = FindMinClicks(matrix, independentCols, dependentCols, maxBound, independentVarIndex + 1, currentAssignment);
            best = Math.Min(best, result);
        }

        return best;
    }

    public static int Part2(List<Result> input)
    {
        List<Result> results = input.ToList();

        for (int i = 0; i < results.Count; i++) {
            var result = results[i];
            var matrix = result.ToAugmentedMatrix();
            var (transformedMatrix, independentVariables, dependentVariables) = GaussianEliminationRREF(matrix);
            var assignment = new int[independentVariables.Count];
            var maxBound = transformedMatrix.Column(transformedMatrix.ColumnCount - 1)
                .Select(value => Math.Abs((int)Math.Round(value)))
                .Max();
            var lowestClicks = FindMinClicks(transformedMatrix, independentVariables, dependentVariables, maxBound, 0, assignment);
            if (lowestClicks == int.MaxValue) {
                Console.WriteLine($"No solution found for result {i} with max bound {maxBound}, pattern {result.Pattern}");
                throw new Exception("No solution found");
            }
            if (lowestClicks == 0) {
                throw new Exception("No solution found");
            }
            result.LowestClicks = lowestClicks;
            results[i] = result;
        }
        return results.Select(result => result.LowestClicks).Sum();
    }

    public static (Joltage joltages, int clicks) ClickButton(
        Joltage targetJoltages, 
        Joltage joltages, 
        List<Button> buttonsInCommon, 
        Button button) 
    {
        var newJoltages = new Joltage(joltages);
        var maxClicks = targetJoltages
            .Where(kvp => 
                button.Positions.Contains(kvp.Key))
            .Min(kvp => kvp.Value);

        foreach (var position in button.Positions) {
            if (newJoltages[position] + maxClicks > targetJoltages[position]) {
                return (joltages, 0);
            }
            newJoltages[position] += maxClicks;
        }
        
        return (newJoltages, maxClicks);
    }

    public static int Part2_Original(List<Result> input)
    {
        List<Result> results = input.ToList();

        // build position frequency dictionary
        for (int i = 0; i < results.Count; i++) {
            var result = results[i];
            result.PositionFrequency = result.Buttons.SelectMany(button => button.Positions)
                .GroupBy(position => position)
                .GroupBy(group => group.Count(), group => group.Key)
                .ToDictionary(g => g.Key, g => g.ToList());

            // Debug.WriteLine(JsonSerializer.Serialize(result.PositionFrequency));
            results[i] = result;
        }


        // process results
        for (int i = 0; i < input.Count; i++)
        {
            var result = results[i];

            var nextPositions = result.PositionFrequency.OrderBy(kvp => kvp.Key).ToList();
            var positionsToCheck = new Queue<KeyValuePair<int, List<int>>>(nextPositions);

            Joltage joltages = new Joltage(result.Joltages.ToDictionary(kvp => kvp.Key, _ => 0));

            while (positionsToCheck.Count > 0) {
                bool isFound = IsJoltagesFound(result.Joltages, joltages);

                if (isFound) {
                    break;
                }

                var (frequency, positions) = positionsToCheck.Dequeue();
                var sortedButtons = result.Buttons
                    .Select<Button, (Button button, HashSet<int> intersection)>(button => 
                        (button, button.Positions.ToHashSet().Intersect(positions).ToHashSet()) )
                    .Where(pair =>
                        pair.intersection.Count > 0)
                    .OrderByDescending(pair => pair.intersection.Count)
                    .ToList();

                var completedPositions = new HashSet<int>();
                foreach (var pair in sortedButtons) {
                    var (button, _) = pair;
                    if (completedPositions.Overlaps(button.Positions)) {
                        continue;
                    }

                    completedPositions.UnionWith(button.Positions);

                    var buttonsInCommon = result.Buttons
                        .Where(b => 
                            b.Positions.ToHashSet().Intersect(button.Positions).Count() > 0 &&
                            b.Positions.ToHashSet() != button.Positions.ToHashSet()
                        ).ToList();
                    var (newJoltages, clicks) = ClickButton(result.Joltages, joltages, buttonsInCommon, button);
                    result.LowestClicks = Math.Min(result.LowestClicks, clicks);
                    results[i] = result;
                    joltages = newJoltages;
                    isFound = IsJoltagesFound(result.Joltages, joltages);
                    if (isFound) {
                        break;
                    }
                }
            }
        }

       return results.Select(result => result.LowestClicks).Sum();
    }

    public static void Run(string inputPath = "dotnet/y2025/day_10", string inputFilename = "input.txt")
    {
        var input = ProcessInput(inputPath, inputFilename);

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result == 396);

        long part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
        Debug.Assert(part2Result > 15683);
        Debug.Assert(part2Result == 15688);
    }
}
