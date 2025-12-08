namespace y2025;
using System;
using System.Diagnostics;
using System.Linq;
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

    // Find Run method - handle optional parameters by getting all overloads
    MethodInfo? runMethod = dayType.GetMethod("Run", BindingFlags.Public | BindingFlags.Static);
    if (runMethod == null)
    {
      Console.WriteLine($"Error: Day {dayNumber} does not have a Run method");
      return;
    }

    // Get parameter info to check if all parameters are optional
    var parameters = runMethod.GetParameters();
    if (parameters.Length > 0)
    {
      // Check if all parameters have default values (are optional)
      bool allOptional = parameters.All(p => p.HasDefaultValue);
      if (!allOptional)
      {
        Console.WriteLine($"Error: Day {dayNumber}.Run() requires parameters but none provided");
        return;
      }
      // Invoke with default values for all optional parameters
      var defaultValues = parameters.Select(p => p.DefaultValue ?? Type.Missing).ToArray();
      runMethod.Invoke(null, defaultValues);
    }
    else
    {
      // No parameters, invoke directly
      runMethod.Invoke(null, null);
    }
  }
}
