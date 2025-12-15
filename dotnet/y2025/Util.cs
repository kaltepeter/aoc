using System.Data;
using Microsoft.VisualBasic.FileIO;

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
}