using System.Data;
using Microsoft.VisualBasic.FileIO;
using Shared;

namespace y2025.util;

public static class Util
{
    public static IEnumerable<long> Range(long start, long end)
    {
        if (start <= end)
        {
            for (long i = start; i <= end; i++)
            {
                yield return i;
            }
        }
        else
        {
            for (long i = start; i >= end; i--)
            {
                yield return i;
            }
        }

    }

    public static IEnumerable<string> ReadLines(StreamReader reader)
    {
        string? line;
        while ((line = reader.ReadLine()) != null)
        {
            yield return line;
        }
    }

    public static double CalculateEuclideanDistanceThreeDimensional(Point p1, Point p2)
    {
        return Math.Sqrt(
                Math.Pow(p2.X - p1.X, 2) +
                Math.Pow(p2.Y - p1.Y, 2) +
                Math.Pow(p2.Z - p1.Z, 2)
        );
    }
}