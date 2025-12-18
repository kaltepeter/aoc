using System.Collections.Generic;
using System.Linq;

public class UnionFind<T> where T : IEquatable<T>
{
    private Dictionary<T, T> parent = new();
    private Dictionary<T, int> size = new();
    private static readonly EqualityComparer<T> comparer = EqualityComparer<T>.Default;

    public static bool Equals(T a, T b) => comparer.Equals(a, b);

    public void MakeSet(T p) {
        parent[p] = p;
        size[p] = 1;
    }

    public T Find(T p) {
        if (!comparer.Equals(parent[p], p)) {
            parent[p] = Find(parent[p]); // Path compression
        }
        return parent[p];
    }

    public void Union(T a, T b)
    {
        var rootA = Find(a);
        var rootB = Find(b);
        if (comparer.Equals(rootA, rootB)) {
            return; // Already in same component
        }

        if (size[rootA] < size[rootB]) {
            (rootA, rootB) = (rootB, rootA);
        }

        parent[rootB] = rootA;
        size[rootA] += size[rootB];
    }

    public int GetSize(T p) => size[Find(p)];

    public IEnumerable<T> GetRoots() => parent.Keys.Where(p => comparer.Equals(parent[p], p));

    public IEnumerable<T> GetAllNodes() => parent.Keys;

    public IEnumerable<KeyValuePair<T, T>> GetParentRelationships() => parent;

    public IEnumerable<KeyValuePair<T, int>> GetRootSizes()
    {
        foreach (var root in GetRoots())
        {
            yield return new KeyValuePair<T, int>(root, size[root]);
        }
    }

    public override string ToString() => $"UnionFind({string.Join(", ", GetRootSizes().Select(p => $"{p.Key}: {p.Value}"))})";

    public Dictionary<T, int> GetSizes() => size;
}