using y2025.util;

namespace y2025.unit;

public class UtilTests
{
    [Theory]
    [InlineData(1, 1, 1)] // Range 0-1 has 2 items
    [InlineData(0, 1, 2)] // Range 0-1 has 2 items
    [InlineData(1, 10, 10)] // Range 1-10 has 10 items
    [InlineData(10, 1, 10)] // backwards range 10-1 has 10 items
    [InlineData(4848455367, 4848568745, 113379)] // Range 4848455367-4848568745 has 113379 items
    public void Test_Range(long start, long end, long expected)
    {
        var result = Util.Range(start, end);
        Assert.Equal(expected, result.Count());
    }

    public static IEnumerable<object[]> CalculateEuclideanDistanceTestData()
    {
        // Diagonal movement: equal distance in all three dimensions
        yield return new object[] { (0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 1.7320508075688772 };
        
        // Only X difference: distance along X axis
        yield return new object[] { (0.0, 0.0, 0.0), (3.0, 0.0, 0.0), 3.0 };
        
        // All zeros - zero distance
        yield return new object[] { (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 0.0 };
        
        // Only X difference: unit distance along X axis
        yield return new object[] { (1.0, 1.0, 1.0), (2.0, 1.0, 1.0), 1.0 };
        
        // Negative coordinates: diagonal movement from negative to positive
        yield return new object[] { (-1.0, -1.0, -1.0), (2.0, 2.0, 2.0), 5.196152422706632 };
        
        // Only X difference: larger distance along X axis
        yield return new object[] { (0.0, 0.0, 0.0), (5.0, 0.0, 0.0), 5.0 };
        
        // Only Y difference: distance along Y axis
        yield return new object[] { (0.0, 0.0, 0.0), (0.0, 5.0, 0.0), 5.0 };
        
        // Only Z difference: distance along Z axis
        yield return new object[] { (0.0, 0.0, 0.0), (0.0, 0.0, 7.0), 7.0 };
    }

    [Theory]
    [MemberData(nameof(CalculateEuclideanDistanceTestData))]
    public void Test_CalculateEuclideanDistanceThreeDimensional((double x, double y, double z) p1, (double x, double y, double z) p2, double expected)
    {
        var point1 = new Point(p1);
        var point2 = new Point(p2);
        var result = Util.CalculateEuclideanDistanceThreeDimensional(point1, point2);
        Assert.Equal(expected, result);
    }
}