using System.Diagnostics;

namespace y2025.day_12;

using System.Data;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;
using ExCSS;
using y2025.util;
using System.Drawing;
using System.Drawing.Drawing2D;
using MathNet.Numerics.LinearAlgebra;
using System.Text;


public struct Region {
    public int width { get; set; }

    public int height { get; set; }

    public List<int> counts { get; set; }

    public Matrix<Single> matrix { get; set; }

    public Region(int width, int height, List<int> counts) {
        this.width = width;
        this.height = height;
        this.counts = counts;
        matrix = Matrix<Single>.Build.Dense(width, height);
    }

    public int Size() {
        return width * height;
    }

    public override string ToString()
    {
        var sb = new StringBuilder();
        sb.Append($"width: {width, 2}\t");
        sb.Append($"height: {height, 2}\t");
        sb.Append($"size: {Size(), 4}\t");
        sb.Append($"counts: {string.Join(", ", counts)}\t");
        return sb.ToString();
    }
}


public struct Result {
    public List<Matrix<Single>> Shapes { get; set; }

    public List<Region> Regions { get; set; }

    public Result() {
        Shapes = [];
        Regions = [];
    }

    public override string ToString()
    {
        return $"Shapes: {Shapes.Count}, Regions: {Regions.Count}";
    }
}

public static class Day
{
    public static Result ProcessInput(string path, string filename)
    {
        Result result = new Result();
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            var groupedInput = Util.ReadLines(sr)
                .Aggregate(new List<List<string>>(), (acc, line) => {
                    if (Regex.Match(line, @"^\d+").Success) {
                        acc.Add(new List<string>());
                    }
                    if (!string.IsNullOrEmpty(line) && !Regex.Match(line, @"^\d+:").Success) {
                        if (char.IsDigit(line[0])) {
                            acc.Last().AddRange(line.Split(": "));
                        } else {
                            acc.Last().Add(line);
                        }
                    }
                    return acc;
                })
                .ToList();

            groupedInput.ForEach(group => {
                if (char.IsDigit(group.First()[0])) {
                    var size = group.First().Split("x").Select(int.Parse);
                    var width = size.First();
                    var height = size.Last();
                    var counts = group.Last().Split(" ").Select(int.Parse).ToList();
                    result.Regions.Add(new Region(width, height, counts));
                } else {
                    List<System.Drawing.Point> shape = group.SelectMany((line, rowIndex) => 
                        line.Select((ch, colIndex) => (ch, colIndex))
                            .Where(x => x.ch == '#')
                            .Select(x => new System.Drawing.Point(rowIndex, x.colIndex))
                    ).ToList();
                    var matrix = Matrix<Single>.Build.Dense(3, 3);
                    shape.ForEach(point => matrix[point.X, point.Y] = 1);
                    result.Shapes.Add(matrix);
                }
            });
        }
        return result;
    }

    public static Matrix<Single> RotateShape(Matrix<Single> shape) {
        return Matrix<Single>.Build.Dense(3, 3, (r, c) => shape[2 - c, r]);
    }

    public static long Part1(Result input)
    {
        int count = 0;
        foreach (var region in input.Regions) {
            var shapeSpace = region.counts.Select((count, index) =>
                (count, input.Shapes[index].ColumnSums().Sum()))
                .Select(value => value.Item1 * value.Item2).Sum();

            if (shapeSpace <= region.Size()) {
                count += 1;
            }
        }
        return count;
    }

    public static List<Region> GetRegionsToPack(Result input) {
        var regionsToPack = new List<Region>();
        foreach (var region in input.Regions) {
            int regionSplit = region.matrix.ColumnCount / 2;
            var (darkCount, lightCount) = (region.matrix.ColumnCount - regionSplit, regionSplit);
            var (targetDarkCount, targetLightCount) = (darkCount * region.matrix.RowCount, lightCount * region.matrix.RowCount);

            var (darkShapeSpace, lightShapeSpace) = (0, 0);
            for (var i = 0; i < input.Shapes.Count; i++) {
                var targetCount = region.counts[i];
                var shape = input.Shapes[i];
                
                if (targetCount == 0) {
                    continue;
                }

                int shapeSpace = (int)shape.ColumnSums().Sum();
                int shapeSplit = shapeSpace / 2;
                var (shapeDarkCount, shapeLightCount) = (shapeSpace - shapeSplit, shapeSplit);
                var (shapeTargetDarkCount, shapeTargetLightCount) = (shapeDarkCount * targetCount, shapeLightCount * targetCount);
                darkShapeSpace += shapeTargetDarkCount;
                lightShapeSpace += shapeTargetLightCount;
            }

            if (darkShapeSpace <= targetDarkCount && lightShapeSpace <= targetLightCount && 
                lightShapeSpace <= targetDarkCount && darkShapeSpace <= targetLightCount
            ) {
                regionsToPack.Add(region);
            }
        }
        return regionsToPack;
    }

    public static long Part1_Checkerboard(Result input)
    {
        return GetRegionsToPack(input).Count;
    }

    public static void Run(string inputPath = "dotnet/y2025/day_12", string inputFilename = "input.txt")
    {
        var input = ProcessInput(inputPath, inputFilename);

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result == 414);

        long coloringResult = Part1_Checkerboard(input);
        Console.WriteLine($"Part II: {coloringResult}");
        Debug.Assert(coloringResult == 414);
    }
}
