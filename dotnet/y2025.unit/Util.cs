using y2025.util;

namespace y2025.unit;

public class UtilTests
{
    [Theory]
    [InlineData(1, 10, 10)]
    [InlineData(4848455367, 4848568745, 113378)]
    public void Test_Range(long start, long count, long expected)
    {
        var result = Util.Range(start, count);
        Assert.Equal(expected, result.Count());
    }
}