namespace y2025;
using System;
using System.Reflection;

class Program
{
  static void Main(string[] args)
  {
    if (args.Length == 0)
    {
      Console.WriteLine("Usage: dotnet run <day_number>");
      Console.WriteLine("Example: dotnet run 1");
      return;
    }

    if (!int.TryParse(args[0], out int dayNumber))
    {
      Console.WriteLine($"Error: '{args[0]}' is not a valid day number");
      return;
    }

    string dayClassName = $"y2025.day_{dayNumber}.Day";
    Type? dayType = Type.GetType(dayClassName);
    
    if (dayType == null)
    {
      Console.WriteLine($"Error: Day {dayNumber} not found. Looking for class: {dayClassName}");
      return;
    }

    MethodInfo? runMethod = dayType.GetMethod("Run", BindingFlags.Public | BindingFlags.Static);
    if (runMethod == null)
    {
      Console.WriteLine($"Error: Day {dayNumber} does not have a Run method");
      return;
    }

    runMethod.Invoke(null, null);
  }
}
