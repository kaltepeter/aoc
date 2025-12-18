namespace shared.unit;
using shared;

public class UnionFindTests
{

    private UnionFind<int> uf;

    public UnionFindTests()
    {
        uf = new UnionFind<int>();
        uf.MakeSet(1);
        uf.MakeSet(2);
        uf.MakeSet(3);
        uf.MakeSet(4);
        uf.MakeSet(5);
    }

    [Fact]
    public void Test_Equals()
    {
        Assert.True(UnionFind<int>.Equals(1, 1));
        Assert.False(UnionFind<int>.Equals(1, 2));
        Assert.True(UnionFind<int>.Equals(new Point(1, 2, 3), new Point(1, 2, 3)));
        Assert.False(UnionFind<int>.Equals(new Point(1, 2, 3), new Point(1, 2, 4)));
    }

    [Fact]
    public void Test_MakeSet()
    {
        // Find should throw KeyNotFoundException if the key doesn't exist
        Assert.Throws<KeyNotFoundException>(() => uf.Find(6));
        
        uf.MakeSet(6);
        Assert.Equal(6, uf.Find(6));
        Assert.Equal(1, uf.GetSize(6));
    }

    [Fact]
    public void Test_Find()
    {
        var rootA = uf.Find(1);
        Assert.Equal(1, rootA);

        uf.Union(1, 2);

        rootA = uf.Find(1);
        Assert.Equal(1, rootA);

        var rootB = uf.Find(2);
        Assert.Equal(1, rootB);

        var rootC = uf.Find(3);
        Assert.Equal(3, rootC);
        
    }
    
    [Fact]
    public void Test_Union()
    {
        var a = 1;
        var b = 2;
        var c = 3;
        Assert.Equal(1, uf.GetSize(a));
        Assert.Equal(1, uf.GetSize(b));
        uf.Union(a, b);
        Assert.Equal(2, uf.GetSize(a));
        Assert.Equal(2, uf.GetSize(b));

        uf.Union(a, c);
        Assert.Equal(3, uf.GetSize(a));
        Assert.Equal(3, uf.GetSize(c));

        // Assert.Equal(3, uf.GetCount());
    }

    [Fact]
    public void Test_GetSize()
    {
        uf.Union(1, 2);
        Assert.Equal(2, uf.GetSize(1));

        Assert.Equal(1, uf.GetSize(3));
    }

    [Fact]
    public void Test_ToString()
    {
        Assert.Equal("UnionFind(1: 1, 2: 1, 3: 1, 4: 1, 5: 1)", uf.ToString());
        uf.Union(1, 2);
        // After union, only roots are shown (2 is no longer a root)
        Assert.Equal("UnionFind(1: 2, 3: 1, 4: 1, 5: 1)", uf.ToString());
    }

    [Fact]
    public void Test_GetSizes()
    {
        // GetSizes returns all entries (including non-roots)
        Assert.Equal(new Dictionary<int, int> { { 1, 1 }, { 2, 1 }, { 3, 1 }, { 4, 1 }, { 5, 1 } }, uf.GetSizes());
        uf.Union(1, 2);
        Assert.Equal(new Dictionary<int, int> { { 1, 2 }, { 2, 1 }, { 3, 1 }, { 4, 1 }, { 5, 1 } }, uf.GetSizes());
    }

    [Fact]
    public void Test_GetRootSizes()
    {
        // GetRootSizes returns only roots
        var rootSizes = uf.GetRootSizes().ToDictionary(kvp => kvp.Key, kvp => kvp.Value);
        Assert.Equal(new Dictionary<int, int> { { 1, 1 }, { 2, 1 }, { 3, 1 }, { 4, 1 }, { 5, 1 } }, rootSizes);
        
        uf.Union(1, 2);
        var rootSizesAfter = uf.GetRootSizes().ToDictionary(kvp => kvp.Key, kvp => kvp.Value);
        // After union, 2 is no longer a root
        Assert.Equal(new Dictionary<int, int> { { 1, 2 }, { 3, 1 }, { 4, 1 }, { 5, 1 } }, rootSizesAfter);
    }

    // [Fact]
    // public void Test_GetRoots()
    // {
    //     var points = uf.GetRoots();
    //     uf.Union(1, 2);
    //     uf.Union(2, 3);
    //     Assert.Equal(3, points.Count());
    //     Assert.Contains(1, points);
    //     Assert.DoesNotContain(2, points);
    //     Assert.DoesNotContain(3, points);
    //     Assert.Contains(4, points);
    //     Assert.Contains(5, points);
    // }

    // [Fact]
    // public void Test_GetChildren()
    // {
    //     // Create a component: 1-2-3 (root is 1)
    //     uf.Union(1, 2);
    //     uf.Union(2, 3);
        
    //     // GetChildren should return all points in the component (including the root)
    //     var children = uf.GetChildren(1).ToList();
    //     Assert.Equal(3, children.Count());
    //     Assert.Contains(1, children);
    //     Assert.Contains(2, children);
    //     Assert.Contains(3, children);
        
    //     // GetChildren should work from any point in the component
    //     var childrenFrom2 = uf.GetChildren(2).ToList();
    //     Assert.Equal(3, childrenFrom2.Count());
    //     Assert.Contains(1, childrenFrom2);
    //     Assert.Contains(2, childrenFrom2);
    //     Assert.Contains(3, childrenFrom2);
        
    //     // Single point component
    //     var childrenOf4 = uf.GetChildren(4).ToList();
    //     Assert.Single(childrenOf4);
    //     Assert.Contains(4, childrenOf4);
        
    //     // Multiple separate components
    //     uf.Union(4, 5);
    //     var childrenOf4AfterUnion = uf.GetChildren(4).ToList();
    //     Assert.Equal(2, childrenOf4AfterUnion.Count());
    //     Assert.Contains(4, childrenOf4AfterUnion);
    //     Assert.Contains(5, childrenOf4AfterUnion);
        
    //     // Component 1-2-3 should still be separate
    //     var childrenOf1After = uf.GetChildren(1).ToList();
    //     Assert.Equal(3, childrenOf1After.Count());
    //     Assert.DoesNotContain(4, childrenOf1After);
    //     Assert.DoesNotContain(5, childrenOf1After);
    // }

    // [Fact]
    // public void Test_IsRoot()
    // {
    //     Assert.True(uf.IsRoot(1));
    //     Assert.True(uf.IsRoot(2));
    //     Assert.True(uf.IsRoot(3));
    //     Assert.True(uf.IsRoot(4));
    //     Assert.True(uf.IsRoot(5));

    //     uf.Union(1, 2);
    //     Assert.True(uf.IsRoot(1));
    //     Assert.False(uf.IsRoot(2));
    //     Assert.True(uf.IsRoot(3));
    //     Assert.True(uf.IsRoot(4));
    //     Assert.True(uf.IsRoot(5));
    // }
    
}