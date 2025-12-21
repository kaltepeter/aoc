using System.Diagnostics;

namespace y2025.day_9;

using System.Data;
using System.Linq;
using y2025.util;
using System.Drawing;

using Result = List<System.Drawing.Point>;
using VectSharp;
using VectSharp.SVG;
using System.Collections.Immutable;

using Rectangles = List<(System.Drawing.Point, System.Drawing.Point, System.Drawing.Point, System.Drawing.Point)>;
using Bounds = (int minX, int maxX, int minY, int maxY);
using Edges = List<(System.Drawing.Point, System.Drawing.Point)>;
using Microsoft.VisualBasic;

public static class Day
{
    public static Result ProcessInput(string path, string filename)
    {
        Result result = [];
        using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
        {
            result = Util.ReadLines(sr)
                .Where(line => !string.IsNullOrWhiteSpace(line))
                .Select(line => line.Split(',').Select(int.Parse).ToArray())
                .Select(parts => new System.Drawing.Point(parts[0], parts[1]))
                .ToList();
        }
        return result;
    }

    public static bool IsDiagonal(System.Drawing.Point p1, System.Drawing.Point p2)
    {
        return p1.X != p2.X && p1.Y != p2.Y;
    }

    /// <summary>
    /// Checks if two points form a 45-degree angle (diagonal line).
    /// For a 45-degree angle, the absolute change in X must equal the absolute change in Y.
    /// </summary>
    public static bool Is45DegreeAngle(System.Drawing.Point p1, System.Drawing.Point p2)
    {
        int deltaX = Math.Abs(p2.X - p1.X);
        int deltaY = Math.Abs(p2.Y - p1.Y);
        return deltaX == deltaY && deltaX > 0; // Must be non-zero and equal
    }

    /// <summary>
    /// Filters a list of coordinates to find points that form a 45-degree angle with a reference point.
    /// </summary>
    public static List<System.Drawing.Point> Find45DegreeCorners(System.Drawing.Point referencePoint, List<System.Drawing.Point> coordinates)
    {
        return coordinates
            .Where(p => Is45DegreeAngle(referencePoint, p))
            .ToList();
    }

    public static long GetManhattanDistance(System.Drawing.Point p1, System.Drawing.Point p2)
    {
        return Math.Abs(p1.X - p2.X) + Math.Abs(p1.Y - p2.Y);
    }

    public static long GetArea(System.Drawing.Point p1, System.Drawing.Point p2)
    {
        long width = Math.Abs((long)p2.X - p1.X) + 1;
        long height = Math.Abs((long)p2.Y - p1.Y) + 1;
        return width * height;
    }

    public static Bounds GetBounds(Result input)
    {
        return (input.Min(p => p.X), input.Max(p => p.X), input.Min(p => p.Y), input.Max(p => p.Y));
    }

    /// <summary>
    /// Coordinate compression (discretization) maps sparse coordinates to dense, contiguous indices.
    /// Useful when you have large coordinate ranges but relatively few unique values.
    /// 
    /// Example: [1, 100, 10000, 1000000] -> [0, 1, 2, 3]
    /// 
    /// This preserves relative ordering and allows using coordinates as array indices.
    /// </summary>
    public static (Dictionary<int, int> xMap, Dictionary<int, int> yMap, Dictionary<int, int> xReverse, Dictionary<int, int> yReverse) CompressCoordinates(Result input)
    {
        // Get all unique X and Y coordinates
        var uniqueX = input.Select(p => p.X).Distinct().OrderBy(x => x).ToList();
        var uniqueY = input.Select(p => p.Y).Distinct().OrderBy(y => y).ToList();

        // Map original coordinates to compressed indices (0, 1, 2, ...)
        var xMap = uniqueX.Select((x, i) => (x, i)).ToDictionary(t => t.x, t => t.i);
        var yMap = uniqueY.Select((y, i) => (y, i)).ToDictionary(t => t.y, t => t.i);

        // Reverse mapping: compressed index -> original coordinate
        var xReverse = xMap.ToDictionary(kvp => kvp.Value, kvp => kvp.Key);
        var yReverse = yMap.ToDictionary(kvp => kvp.Value, kvp => kvp.Key);

        return (xMap, yMap, xReverse, yReverse);
    }

    /// <summary>
    /// Compress a point using coordinate compression maps.
    /// Returns a point with compressed coordinates (0-based indices).
    /// </summary>
    public static System.Drawing.Point CompressPoint(System.Drawing.Point point, Dictionary<int, int> xMap, Dictionary<int, int> yMap)
    {
        return new System.Drawing.Point(xMap[point.X], yMap[point.Y]);
    }

    /// <summary>
    /// Decompress a point back to original coordinates.
    /// </summary>
    public static System.Drawing.Point DecompressPoint(System.Drawing.Point compressedPoint, Dictionary<int, int> xReverse, Dictionary<int, int> yReverse)
    {
        return new System.Drawing.Point(xReverse[compressedPoint.X], yReverse[compressedPoint.Y]);
    }

    public static bool IsPointInBounds(System.Drawing.Point point, Result polygonPoints)
    {
        var (minX, maxX, minY, maxY) = GetBounds(polygonPoints);
        if (point.X < minX || point.X > maxX || point.Y < minY || point.Y > maxY)
        {
            return false;
        }

        // Check if point is on the polygon boundary (exact match with input points)
        if (polygonPoints.Contains(point))
        {
            return true;
        }

        // Use ray casting algorithm to check if point is inside the polygon
        // Cast a ray to the right and count intersections with polygon edges
        int intersections = 0;
        for (int i = 0; i < polygonPoints.Count; i++)
        {
            var p1 = polygonPoints[i];
            var p2 = polygonPoints[(i + 1) % polygonPoints.Count];

            // Check if ray intersects this edge
            if (((p1.Y > point.Y) != (p2.Y > point.Y)) &&
                (point.X < (p2.X - p1.X) * (point.Y - p1.Y) / (double)(p2.Y - p1.Y) + p1.X))
            {
                intersections++;
            }
        }

        // Odd number of intersections means point is inside
        return intersections % 2 == 1;
    }

    public static bool isPointInsidePolygon(List<(System.Drawing.Point, System.Drawing.Point)> edges, System.Drawing.Point point)
    {
        var count = 0;
        foreach (var edge in edges)
        {
            var (p1, p2) = edge;
            if ((point.Y < p1.Y) != (point.Y < p2.Y) && point.X < p1.X + ((point.Y - p1.Y) / (p2.Y - p1.Y)) * (p2.X - p1.X))
            {
                count++;
            }
        }
        return count % 2 == 1;
    }

    public static long Part1(Result input)
    {
        var pointsToCheck = input;

        var areas = pointsToCheck
            .SelectMany((point1, i) => pointsToCheck.Skip(i + 1).Select((point2) => (point1, point2)))
            .Select(pair => (p1: pair.point1, p2: pair.point2, dist: GetManhattanDistance(pair.point1, pair.point2), area: GetArea(pair.point1, pair.point2)))
            .OrderByDescending(a => a.area);

        var (_, _, dist, area) = areas.First();

        return area;
    }

    public static long Part2_SimpleShape(Result input)
    {
        var pointsToCheck = input;

        var areas = pointsToCheck
            .SelectMany((point1, i) => pointsToCheck.Skip(i + 1).Select((point2) => (point1, point2)))
            .Select(pair => (p1: pair.point1, p2: pair.point2, area: GetArea(pair.point1, pair.point2)))
            .Where(pair =>
                IsPointInBounds(new System.Drawing.Point(pair.p2.X, pair.p1.Y), pointsToCheck) &&
                IsPointInBounds(new System.Drawing.Point(pair.p1.X, pair.p2.Y), pointsToCheck) &&
                IsPointInBounds(pair.p1, pointsToCheck) &&
                IsPointInBounds(pair.p2, pointsToCheck)
            )
            .OrderByDescending(a => a.area);

        var (_, _, area) = areas.First();

        return area;
    }

    public static (Edges, System.Drawing.Point) FindPaths(Result halfInputs, Edges edges, System.Drawing.Point startCorner, bool isBottomHalf)
    {
        var (minX, maxX, minY, maxY) = GetBounds(halfInputs);
        Debug.WriteLine($"isBottomHalf: {isBottomHalf} minX: {minX}, maxX: {maxX}, minY: {minY}, maxY: {maxY}");

        // Raycast 1: Vertical raycast (upward for bottom half, downward for top half)
        int furthestYInBounds = startCorner.Y;
        if (isBottomHalf)
        {
            for (int y = startCorner.Y; y <= maxY; y++)
            {
                var testPoint = new System.Drawing.Point(startCorner.X, y);
                if (isPointInsidePolygon(edges, testPoint))
                {
                    furthestYInBounds = y;
                }
                else
                {
                    break;
                }
            }
        }
        else
        {
            // Top half: go downward (decreasing Y)
            for (int y = startCorner.Y; y >= minY; y--)
            {
                var testPoint = new System.Drawing.Point(startCorner.X, y);
                if (isPointInsidePolygon(edges, testPoint))
                {
                    furthestYInBounds = y;
                }
                else
                {
                    break;
                }
            }
        }
        var furthestPointInBounds = new System.Drawing.Point(startCorner.X, furthestYInBounds);

        // Raycast 2: Horizontal raycast leftward (same for both halves)
        int lowestXInBounds = furthestPointInBounds.X;
        for (int x = furthestPointInBounds.X; x >= minX; x--)
        {
            var testPoint = new System.Drawing.Point(x, furthestPointInBounds.Y);
            if (isPointInsidePolygon(edges, testPoint))
            {
                lowestXInBounds = x;
            }
            else
            {
                break;
            }
        }
        var lowestXPointInBounds = new System.Drawing.Point(lowestXInBounds, furthestPointInBounds.Y);
        Debug.WriteLine($"startCorner: {startCorner.X}, {startCorner.Y} furthestPointInBounds: {furthestPointInBounds.X}, {furthestPointInBounds.Y} lowestXPointInBounds: {lowestXPointInBounds.X}, {lowestXPointInBounds.Y}");

        // Find the furthest left point in the input that's within bounds
        var furthestLeftPoint = halfInputs
            .Where(p =>
            {
                if (isBottomHalf)
                {
                    return p.Y <= furthestPointInBounds.Y && p.X <= lowestXPointInBounds.X;
                }
                else
                {
                    return p.Y >= furthestPointInBounds.Y && p.X <= lowestXPointInBounds.X;
                }
            })
            .OrderByDescending(p => p.X)
            .First();
        Debug.WriteLine($"furthestLeftPoint: {furthestLeftPoint.X}, {furthestLeftPoint.Y}");

        var lines = new Edges {
            (startCorner, furthestPointInBounds),
            (furthestPointInBounds, furthestLeftPoint)
        };
        return (lines, furthestLeftPoint);
    }

    public static long ProcessHalf(string halfName, Result half, System.Drawing.Point corner, Result corners, bool isBottomHalf)
    {
        var edges = half.SelectMany((point1, i) => half.Skip(i + 1).Select((point2) => (point1, point2))).ToList();

        var (lines, furthestLeftPoint) = FindPaths(half, edges, corner, isBottomHalf);

        DrawPolygon(halfName, half, corners, [], lines);
        var area = GetArea(corner, furthestLeftPoint);
        Debug.WriteLine($"{halfName} area: {area}");

        return area;
    }

    public static IEnumerable<(System.Drawing.Point, System.Drawing.Point, long)> ProcessRectangle(Result pointsToCheck, int midX, List<System.Drawing.Point> corners)
    {
        Debug.WriteLine($"midX: {midX} corners: {string.Join(", ", corners)}");
        var sortedCorners = corners.OrderBy(p => p.X).ThenBy(p => p.Y).ToList();
        var leftCorner = sortedCorners.First();
        var rightCorner = sortedCorners.Last();
        return pointsToCheck
            // .SelectMany((point1, i) => pointsToCheck.Skip(i + 1).Select((point2) => (point1, point2)))
            .Select((point1, i) => (point1, point2: rightCorner))
            // .Where(pair => pair.point1.X != pair.point2.X && pair.point1.Y != pair.point2.Y)
            .Where(pair => IsDiagonal(pair.point1, pair.point2))
            .Where(pair => pair.point1.X >= leftCorner.X && pair.point2.X <= rightCorner.X)
            .Where(pair =>
                pair.point1.X <= midX && pair.point2.X >= midX ||
                pair.point1.X >= midX && pair.point2.X <= midX
            )
            .Where(pair =>
                IsPointInBounds(new System.Drawing.Point(pair.point2.X, pair.point1.Y), pointsToCheck) &&
                IsPointInBounds(new System.Drawing.Point(pair.point1.X, pair.point2.Y), pointsToCheck) &&
                IsPointInBounds(pair.point1, pointsToCheck) &&
                IsPointInBounds(pair.point2, pointsToCheck)
            )
            .Select(pair => (p1: pair.point1, p2: pair.point2, area: GetArea(pair.point1, pair.point2)))
            .OrderByDescending(a => a.area);
    }

    public static bool IsEdgeInBounds(System.Drawing.Point p1, System.Drawing.Point p2, Result pointsToCheck)
    {
        List<System.Drawing.Point> allEdges = [p1, new System.Drawing.Point(p2.X, p1.Y), p2, new System.Drawing.Point(p1.X, p2.Y)];
        var allPointsInBounds = allEdges.All(e => IsPointInBounds(e, pointsToCheck));

        if (!allPointsInBounds)
        {
            return false;
        }

        var verticalEdges = allEdges.Where(e => e.X == p1.X).OrderBy(e => e.Y).ToList();
        var leftEdge = verticalEdges.First();
        var rightEdge = verticalEdges.Last();

        var leftEdgeInBounds = Enumerable.Range(leftEdge.Y, rightEdge.Y - leftEdge.Y).All(y => IsPointInBounds(new System.Drawing.Point(leftEdge.X, y), pointsToCheck));
        var rightEdgeInBounds = Enumerable.Range(leftEdge.Y, rightEdge.Y - leftEdge.Y).All(y => IsPointInBounds(new System.Drawing.Point(leftEdge.X, y), pointsToCheck));

        return true;
    }

    public static long Part2(Result input)
    {

        // var bottomRightCorner = corners[1];
        var (xMap, yMap, xReverse, yReverse) = CompressCoordinates(input);
        List<System.Drawing.Point> pointsToCheck = input.Select(p => new System.Drawing.Point(xMap[p.X], yMap[p.Y])).ToList();
        // var compressedCorners = corners.Select(p => new System.Drawing.Point(xMap[p.X], yMap[p.Y])).ToList();
        var corners = GetCorners(pointsToCheck);
        corners.OrderBy(p => p.X).ThenBy(p => p.Y);
        var bottomCorners = new[] { corners[0], corners[1] }; // bottomLeft, bottomRight
        var topCorners = new[] { corners[2], corners[3] }; // topRight, topLeft



        var areas = pointsToCheck
            .SelectMany((point1, i) => pointsToCheck.Skip(i + 1).Select((point2) => (p1: point1, p2: point2)))
            .Where(pair => bottomCorners.Contains(pair.p1) || bottomCorners.Contains(pair.p2) || 
                           topCorners.Contains(pair.p1) || topCorners.Contains(pair.p2))
            .Where(pair =>
                IsEdgeInBounds(pair.p1, pair.p2, pointsToCheck)
            )
            .Select(pair => (p1: pair.p1, p2: pair.p2, area: GetArea(pair.p1, pair.p2)))
            .OrderByDescending(a => a.area);

        var (p1, p2, area) = areas.First();

        var decompressedP1 = DecompressPoint(p1, xReverse, yReverse);
        var decompressedP2 = DecompressPoint(p2, xReverse, yReverse);

        // DrawPolygon("bottom-polygon", bottomHalf, [], [
        //     (p1, new System.Drawing.Point(p1.X, p2.Y), p2, new System.Drawing.Point(p2.X, p1.Y))
        // ], []);
        DrawSimplePolygon("bottom-polygon-compressed", pointsToCheck, [
            (p1, new System.Drawing.Point(p1.X, p2.Y), p2, new System.Drawing.Point(p2.X, p1.Y))
        ]);

        return GetArea(decompressedP1, decompressedP2);
    }

    public static long Part2_WIP2(Result input)
    {
        var corners = GetCorners(input);
        corners.OrderBy(p => p.X).ThenBy(p => p.Y);
        var bottomRightCorner = corners[1];
        var bottomLeftCorner = corners[0];
        var topLeftCorner = corners[3];
        var topRightCorner = corners[2];

        int mid = input.Count / 2;
        var bottomHalf = input.ToList()[0..mid];
        var topHalf = input.ToList()[mid..];
        var pointsToCheck = input;


        var topMidX = topLeftCorner.X + (topRightCorner.X - topLeftCorner.X) / 2;
        var bottomMidX = bottomLeftCorner.X + (bottomRightCorner.X - bottomLeftCorner.X) / 2;
        var midX = (topMidX + bottomMidX) / 2;
        Debug.WriteLine($"topMidX: {topMidX} bottomMidX: {bottomMidX} midX: {midX}");

        var edges = pointsToCheck.SelectMany((point1, i) => pointsToCheck.Skip(i + 1).Select((point2) => (point1, point2))).ToList();

        var bottomAreas = ProcessRectangle(bottomHalf, bottomMidX, [bottomRightCorner, bottomLeftCorner]);
        var topAreas = ProcessRectangle(topHalf, topMidX, [topLeftCorner, topRightCorner]);
        var areas = ProcessRectangle(input, midX, corners);

        var (bottomP1, bottomP2, _) = bottomAreas.First();
        Rectangles bottomRectangle = [
            (bottomP1, new System.Drawing.Point(bottomP1.X, bottomP2.Y), bottomP2, new System.Drawing.Point(bottomP2.X, bottomP1.Y))
        ];

        var (topP1, topP2, _) = topAreas.First();
        Rectangles topRectangle = [
            (topP1, new System.Drawing.Point(topP1.X, topP2.Y), topP2, new System.Drawing.Point(topP2.X, topP1.Y))
        ];

        var (p1, p2, area) = areas
            .First();

        Debug.WriteLine($"p1: {p1.X}, {p1.Y} p2: {p2.X}, {p2.Y} area: {area}");
        Debug.WriteLine($"bottom rectangle: {string.Join(", ", bottomRectangle)} points: {bottomP1}, {bottomP2}");
        Debug.WriteLine($"top rectangle: {string.Join(", ", topRectangle)} points: {topP1}, {topP2}");
        DrawPolygon("bottom-polygon", bottomHalf, corners, bottomRectangle, []);
        DrawPolygon("top-polygon", topHalf, corners, topRectangle, []);
        DrawPolygon("combined-polygon", input, corners, [
            (p1, new System.Drawing.Point(p1.X, p2.Y), p2, new System.Drawing.Point(p2.X, p1.Y))
            // (corners[0], corners[1], corners[2], corners[3])
        ], []);

        return area;
    }

    public static long Part2_WIP(Result input)
    {
        var (minX, maxX, minY, maxY) = GetBounds(input);

        var corners = GetCorners(input);
        corners.OrderBy(p => p.X).ThenBy(p => p.Y);

        var topLeftCorner = corners[3];
        var topRightCorner = corners[2];
        var bottomRightCorner = corners[1];
        var bottomLeftCorner = corners[0];

        Debug.WriteLine($"topLeftCorner: {topLeftCorner.X}, {topLeftCorner.Y} topRightCorner: {topRightCorner.X}, {topRightCorner.Y} bottomRightCorner: {bottomRightCorner.X}, {bottomRightCorner.Y} bottomLeftCorner: {bottomLeftCorner.X}, {bottomLeftCorner.Y}");

        var bottomHalf = input.ToList()[0..(input.Count / 2)];
        var topHalf = input.ToList()[(input.Count / 2)..];
        var filteredList = bottomHalf.Where(p => p.X <= bottomRightCorner.X && p.X >= bottomLeftCorner.X).ToList();
        var mid = (bottomRightCorner.X - bottomLeftCorner.X) / 2 + bottomLeftCorner.X;
        Debug.WriteLine($"original count: {input.Count} bottomHalf count: {bottomHalf.Count} filtered count: {filteredList.Count} mid: {mid} bottomLeftCorner: {bottomLeftCorner.X} bottomRightCorner: {bottomRightCorner.X}");
        // var leftSide = filteredList.Where(p => p.X <= mid).ToList();
        // var rightSide = filteredList.Where(p => p.X > mid).ToList();

        // var rightPairs = leftSide.Zip(Enumerable.Repeat(bottomRightCorner, leftSide.Count), (p1, p2) => (p1, p2));
        // var leftPairs = rightSide.Zip(Enumerable.Repeat(bottomLeftCorner, rightSide.Count), (p1, p2) => (p2, p1));
        // Debug.WriteLine($"rightPairs count: {rightPairs.Count()} leftPairs count: {leftPairs.Count()}");

        // Rectangles rightBounds = rightPairs
        //     .Select(pair => (p1: new System.Drawing.Point(pair.p1.X, pair.p2.Y), p2: pair.p2, p3: new System.Drawing.Point(pair.p2.X, pair.p1.Y), p4: pair.p1))
        //     .Where(points => IsPointInBounds(points.p1, bottomHalf) && IsPointInBounds(points.p2, bottomHalf) && IsPointInBounds(points.p3, bottomHalf) && IsPointInBounds(points.p4, bottomHalf))
        //     .ToList();
        // rightBounds.ForEach(p => Debug.WriteLine(string.Join(", ", p)));

        // Rectangles leftBounds = leftPairs
        //     .Select(pair => (p1: new System.Drawing.Point(pair.p1.X, pair.p2.Y), p2: pair.p2, p3: new System.Drawing.Point(pair.p2.X, pair.p1.Y), p4: pair.p1))
        //     .Where(points => IsPointInBounds(points.p1, bottomHalf) && IsPointInBounds(points.p2, bottomHalf) && IsPointInBounds(points.p3, bottomHalf) && IsPointInBounds(points.p4, bottomHalf))
        //     .ToList();
        // leftBounds.ForEach(p => Debug.WriteLine(string.Join(", ", p)));

        // Raycast 1: From bottomRightCorner, go upward (increasing Y) along same X to find furthest Y in bounds
        // Check against full input polygon, not just bottomHalf


        var topHalfArea = ProcessHalf("top-polygon", topHalf, topRightCorner, corners, false);
        var bottomHalfArea = ProcessHalf("bottom-polygon", bottomHalf, bottomRightCorner, corners, true);
        DrawPolygon("combined-polygon", input, corners, [], []);


        return Math.Max(topHalfArea, bottomHalfArea);
    }

    public static List<System.Drawing.Point> GetCorners(Result input)
    {
        List<System.Drawing.Point> corners = new List<System.Drawing.Point>();
        int mid = input.Count / 2 - 1;
        for (int i = mid; i < mid + 4; i++)
        {
            corners.Add(input[i]);
        }

        return corners;
    }

    public static IEnumerable<FormattedText> GetFormattedText(string text, double fontSize = 400)
    {
        return FormattedText.Format(text,
            VectSharp.FontFamily.StandardFontFamilies.Helvetica,
            fontSize);
    }

    public static void DrawSimplePolygon(string documentName, Result input, Rectangles rectangles)
    {
        var (minX, maxX, minY, maxY) = GetBounds(input);
        string documentPath = Path.Combine(Directory.GetCurrentDirectory(), "dotnet", "y2025", "day_9", $"{documentName}.svg");
        Page page = new Page(maxX - minX + 10, maxY - minY + 10);

        VectSharp.Graphics graphics = page.Graphics;
        var start = input.First();
        double lineWidth = .25;
        VectSharp.FontFamily family = VectSharp.FontFamily.ResolveFontFamily(VectSharp.FontFamily.StandardFontFamilies.Helvetica);
        VectSharp.Font font = new VectSharp.Font(family, lineWidth);

        GraphicsPath full = new GraphicsPath();

        full.MoveTo(start.X, start.Y);
        foreach (var point in input.Skip(1))
        {
            full.LineTo(point.X, point.Y);
        }

        full.Close();

        graphics.FillPath(full, Colours.Green);

        foreach (var point in input)
        {
            var text = $"{point.X}, {point.Y}";
            // Draw a small square at each point
            GraphicsPath marker = new GraphicsPath();
            marker.MoveTo(point.X - lineWidth / 2, point.Y - lineWidth / 2);
            marker.LineTo(point.X + lineWidth / 2, point.Y - lineWidth / 2);
            marker.LineTo(point.X + lineWidth / 2, point.Y + lineWidth / 2);
            marker.LineTo(point.X - lineWidth / 2, point.Y + lineWidth / 2);
            // marker.AddText(point.X, point.Y, formattedText.First(), font, TextBaselines.Middle);
            marker.Close();
            graphics.FillPath(marker, Colours.Red);
            var textMetrics = font.MeasureText(text);
            graphics.FillRectangle(point.X + (lineWidth / 2), point.Y - (textMetrics.Height / 2) - (lineWidth / 2), textMetrics.Width + lineWidth, textMetrics.Height + lineWidth, Colours.White);
            graphics.StrokeRectangle(point.X + (lineWidth / 2), point.Y - (textMetrics.Height / 2) - (lineWidth / 2), textMetrics.Width + lineWidth, textMetrics.Height + lineWidth, Colours.Black, lineWidth / 4);
            graphics.FillText(new VectSharp.Point(point.X + lineWidth, point.Y), text, font, Colours.Black, TextBaselines.Middle);
        }

        foreach (var (p1, p2, p3, p4) in rectangles)
        {
            GraphicsPath marker = new GraphicsPath();
            marker.MoveTo(p1.X - lineWidth / 2, p1.Y - lineWidth / 2);
            marker.LineTo(p2.X + lineWidth / 2, p2.Y - lineWidth / 2);
            marker.LineTo(p3.X + lineWidth / 2, p3.Y + lineWidth / 2);
            marker.LineTo(p4.X - lineWidth / 2, p4.Y + lineWidth / 2);
            marker.Close();
            graphics.StrokePath(marker, Colours.Blue, lineWidth);
        }

        try
        {
            page.SaveAsSVG(documentPath);
            Console.WriteLine($"Polygon visualization saved to: {documentPath}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error saving polygon visualization: {ex.Message}");
        }
    }

    public static void DrawPolygon(string documentName, Result input, List<System.Drawing.Point> corners, Rectangles rectangles, List<(System.Drawing.Point, System.Drawing.Point)> lines)
    {
        int padding = 5;
        string documentPath = Path.Combine(Directory.GetCurrentDirectory(), "dotnet", "y2025", "day_9", $"{documentName}.svg");
        // var normalizedPoints = input.Select(point => new System.Drawing.Point(point.X - minX, point.Y - minY)).ToList();
        var normalizedPoints = input.ToList();
        var (minX, maxX, minY, maxY) = GetBounds(input);

        if (normalizedPoints.Count == 0)
        {
            return;
        }

        Page page = new Page(maxX - minX + padding * 2, maxY - minY + padding * 2);
        page.Crop(new VectSharp.Rectangle(minX - padding, minY - padding, maxX - minX + padding * 2, maxY - minY + padding * 2));
        VectSharp.Graphics graphics = page.Graphics;

        double lineWidth = 400;
        var start = normalizedPoints.First();

        GraphicsPath full = new GraphicsPath();

        full.MoveTo(start.X, start.Y);
        foreach (var point in normalizedPoints.Skip(1))
        {
            full.LineTo(point.X, point.Y);
        }

        full.Close();

        // graphics.StrokePath(full, Colours.Red, lineWidth);
        graphics.FillPath(full, Colours.Green);

        // Draw individual point markers to see all points
        // This helps identify if there are interior points not on the boundary
        foreach (var point in normalizedPoints)
        {
            var text = $"{point.X}, {point.Y}";
            // Draw a small square at each point
            GraphicsPath marker = new GraphicsPath();
            marker.MoveTo(point.X - lineWidth / 2, point.Y - lineWidth / 2);
            marker.LineTo(point.X + lineWidth / 2, point.Y - lineWidth / 2);
            marker.LineTo(point.X + lineWidth / 2, point.Y + lineWidth / 2);
            marker.LineTo(point.X - lineWidth / 2, point.Y + lineWidth / 2);
            // marker.AddText(point.X, point.Y, formattedText.First(), font, TextBaselines.Middle);
            marker.Close();
            graphics.FillPath(marker, Colours.Red);
            graphics.FillText(point.X, point.Y, GetFormattedText(text), Colours.Black, TextBaselines.Middle);
        }

        foreach (var point in corners)
        {
            var text = $"{point.X}, {point.Y}";
            GraphicsPath marker = new GraphicsPath();
            marker.MoveTo(point.X - lineWidth / 2, point.Y - lineWidth / 2);
            marker.LineTo(point.X + lineWidth / 2, point.Y - lineWidth / 2);
            marker.LineTo(point.X + lineWidth / 2, point.Y + lineWidth / 2);
            marker.LineTo(point.X - lineWidth / 2, point.Y + lineWidth / 2);
            marker.Close();
            graphics.FillPath(marker, Colours.Blue);
            graphics.FillText(point.X, point.Y, GetFormattedText(text), Colours.Black, TextBaselines.Middle);
        }

        foreach (var line in lines)
        {
            GraphicsPath marker = new GraphicsPath();
            marker.MoveTo(line.Item1.X, line.Item1.Y);
            marker.LineTo(line.Item2.X, line.Item2.Y);
            marker.Close();
            graphics.StrokePath(marker, Colours.Blue, lineWidth);
        }

        foreach (var (p1, p2, p3, p4) in rectangles)
        {
            GraphicsPath marker = new GraphicsPath();
            marker.MoveTo(p1.X - lineWidth / 2, p1.Y - lineWidth / 2);
            marker.LineTo(p2.X + lineWidth / 2, p2.Y - lineWidth / 2);
            marker.LineTo(p3.X + lineWidth / 2, p3.Y + lineWidth / 2);
            marker.LineTo(p4.X - lineWidth / 2, p4.Y + lineWidth / 2);
            marker.Close();
            graphics.StrokePath(marker, Colours.Blue, lineWidth);
        }

        try
        {
            page.SaveAsSVG(documentPath);
            Console.WriteLine($"Polygon visualization saved to: {documentPath}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error saving polygon visualization: {ex.Message}");
        }
    }

    public static void Run(string inputPath = "dotnet/y2025/day_9", string inputFilename = "input.txt")
    {
        var input = ProcessInput(inputPath, inputFilename);

        long part1Result = Part1(input);
        Console.WriteLine($"Part I: {part1Result}");
        Debug.Assert(part1Result > 2147425684);
        Debug.Assert(part1Result == 4735268538);

        try
        {
            var tsstInput = ProcessInput("dotnet/y2025.unit/day_9", "example.txt");
            DrawSimplePolygon("example-polygon", tsstInput, []);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error drawing polygon: {ex.Message}");
        }

        long part2Result = Part2(input);
        Console.WriteLine($"Part II: {part2Result}");
        Debug.Assert(part2Result > 156595054);
        Debug.Assert(part2Result < 1570336549);
        Debug.Assert(part2Result > 1534701749);
        Debug.Assert(part2Result == 1537458069);
    }
}
