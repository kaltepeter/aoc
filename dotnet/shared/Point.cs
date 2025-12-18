using System.Text.Json;
using System.Text.Json.Serialization;

[JsonConverter(typeof(PointJsonConverter))]
public struct Point : IEquatable<Point>, IComparable<Point>
{
    public double X { get; set; }
    public double Y { get; set; }
    public double Z { get; set; }
    public Point(double x, double y, double z)
    {
        X = x;
        Y = y;
        Z = z;
    }
    
    public Point((double x, double y, double z) tuple)
    {
        X = tuple.x;
        Y = tuple.y;
        Z = tuple.z;
    }
    
    public bool Equals(Point other)
    {
        return X == other.X && Y == other.Y && Z == other.Z;
    }
    
    public override bool Equals(object? obj)
    {
        return obj is Point other && Equals(other);
    }
    
    public override int GetHashCode()
    {
        return HashCode.Combine(X, Y, Z);
    }
    
    public override string ToString()
    {
        return $"{X},{Y},{Z}";
    }
    
    public static bool operator ==(Point left, Point right)
    {
        return left.X == right.X && left.Y == right.Y && left.Z == right.Z;
    }
    
    public static bool operator !=(Point left, Point right)
    {
        return !(left == right);
    }
    
    public int CompareTo(Point other)
    {
        // Lexicographic comparison: X, then Y, then Z
        int xComparison = X.CompareTo(other.X);
        if (xComparison != 0) return xComparison;
        
        int yComparison = Y.CompareTo(other.Y);
        if (yComparison != 0) return yComparison;
        
        return Z.CompareTo(other.Z);
    }
    
    public static bool operator <(Point left, Point right)
    {
        return left.CompareTo(right) < 0;
    }
    
    public static bool operator >(Point left, Point right)
    {
        return left.CompareTo(right) > 0;
    }
    
    public static bool operator <=(Point left, Point right)
    {
        return left.CompareTo(right) <= 0;
    }
    
    public static bool operator >=(Point left, Point right)
    {
        return left.CompareTo(right) >= 0;
    }
}

public class PointJsonConverter : JsonConverter<Point>
{
    public override Point Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        var str = reader.GetString();
        if (string.IsNullOrEmpty(str))
            throw new JsonException("Invalid Point string");
        
        var parts = str.Split(',');
        if (parts.Length != 3)
            throw new JsonException("Point must have 3 coordinates");
        
        return new Point(double.Parse(parts[0]), double.Parse(parts[1]), double.Parse(parts[2]));
    }

    public override void Write(Utf8JsonWriter writer, Point value, JsonSerializerOptions options)
    {
        writer.WriteStringValue($"{value.X},{value.Y},{value.Z}");
    }

    public override Point ReadAsPropertyName(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        return Read(ref reader, typeToConvert, options);
    }

    public override void WriteAsPropertyName(Utf8JsonWriter writer, Point value, JsonSerializerOptions options)
    {
        writer.WritePropertyName($"{value.X},{value.Y},{value.Z}");
    }
}   