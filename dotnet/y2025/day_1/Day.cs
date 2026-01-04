using System.Diagnostics;

namespace y2025.day_1;

public static class Day
{
  public static List<int> ProcessInput(string path, string filename)
  {
    List<int> result = [];
    try
    {
      using (StreamReader sr = new StreamReader(Path.Join(path, filename)))
      {
        string? line;
        while ((line = sr.ReadLine()) != null)
        {
          if (line.StartsWith("L"))
          {
            result.Add(-int.Parse(line.Substring(1)));
          }
          else if (line.StartsWith("R"))
          {
            result.Add(int.Parse(line.Substring(1)));
          }
        }
      }
    }
    catch (Exception ex)
    {
      Console.WriteLine(ex.Message);
    }

    return result;
  }

  public static int Part1(List<int> turns)
  {
    int current = 50;
    int count = 0;

    foreach (int item in turns)
    {
      current = (current + item) % 100;
      if (current == 0) {
        count += 1;

      }
    }

    return count;
  }

  public static int Part2(int start, List<int> turns)
  {
    int current = start;
    int count = 0;

    foreach (int turn in turns)
    {
      var (full_turns, rem) = Math.DivRem(turn, Math.Sign(turn) * 100);
      count += (int)full_turns;

      if (turn < 0) {
        if (current != 0 && current + rem <= 0) {
          count += 1;
        }
      } else {
        if (current + rem >= 100) {
          count += 1;
        }
      }

      current = ((current + turn) % 100 + 100) % 100;
    }

    return count;
  }

  public static void Run()
  {
    // Path is relative to workspace root
    List<int> input = ProcessInput("dotnet/y2025/day_1", "input.txt");
    
    int part1Result = Part1(input);
    Console.WriteLine($"Part I: {part1Result}");
    Debug.Assert(part1Result < 2222);
    Debug.Assert(part1Result == 1132);

    int part2Result = Part2(50, input);
    Console.WriteLine($"Part II: {part2Result}");
    Debug.Assert(part2Result == 6623);
  }
}