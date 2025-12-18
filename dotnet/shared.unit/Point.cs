namespace shared.unit;
using shared;

public class PointTests
{
    [Fact]
    public void Test_Equals()
    {
        Assert.True(new Point(1, 2, 3).Equals(new Point(1, 2, 3)));
        Assert.False(new Point(1, 2, 3).Equals(new Point(1, 2, 4)));
    }

    [Fact]
    public void Test_EqualityOperator_SameValues()
    {
        var p1 = new Point(52, 470, 668);
        var p2 = new Point(52, 470, 668);
        Assert.True(p1 == p2);
        Assert.False(p1 != p2);
    }

    [Fact]
    public void Test_EqualityOperator_DifferentValues()
    {
        var p1 = new Point(1, 2, 3);
        var p2 = new Point(1, 2, 4);
        Assert.False(p1 == p2);
        Assert.True(p1 != p2);
    }

    [Fact]
    public void Test_EqualityOperator_AllCoordinatesDifferent()
    {
        var p1 = new Point(52, 470, 668);
        var p2 = new Point(117, 168, 530);
        Assert.False(p1 == p2);
        Assert.True(p1 != p2);
    }

    [Fact]
    public void Test_EqualityOperator_WithTupleDestructuring()
    {
        var tuple1 = (new Point(52, 470, 668), new Point(117, 168, 530));
        var tuple2 = (new Point(52, 470, 668), new Point(52, 470, 668));
        
        // Same point comparison
        Assert.True(tuple2.Item1 == tuple2.Item2);
        
        // Different point comparison
        Assert.False(tuple1.Item1 == tuple1.Item2);
    }
}