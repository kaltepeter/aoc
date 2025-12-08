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
}