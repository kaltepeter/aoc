using Shared;

class RenderNetwork
{
    public string ToGraphvizDot(UnionFind<Point> uf)
    {
        var lines = new List<string> { "graph UnionFind {" };
        
        var roots = uf.GetRoots().OrderBy(r => r.ToString()).ToList();
        
        // Collect all points to find min/max for normalization
        var allPoints = uf.GetAllNodes().ToList();
        
        // Find min/max for each coordinate (X, Y, Z) across all points
        if (allPoints.Count > 0)
        {
            var points = allPoints.ToList();
            double minX = points.Min(p => p.X);
            double maxX = points.Max(p => p.X);
            double minY = points.Min(p => p.Y);
            double maxY = points.Max(p => p.Y);
            double minZ = points.Min(p => p.Z);
            double maxZ = points.Max(p => p.Z);
            
            // Add nodes with colors based on their Point coordinates
            foreach (var root in roots)
            {
                var componentNodes = uf.GetAllNodes()
                    .Where(n => UnionFind<Point>.Equals(uf.Find(n), root))
                    .OrderBy(n => n.ToString())
                    .ToList();
                
                foreach (var node in componentNodes)
                {
                    if (node is Point point)
                    {
                        // Normalize X, Y, Z to 0-255 range
                        int r = NormalizeToByte(point.X, minX, maxX);
                        int g = NormalizeToByte(point.Y, minY, maxY);
                        int b = NormalizeToByte(point.Z, minZ, maxZ);
                        
                        // Make it more pastel by mixing with white (lighten)
                        r = (int)(r * 0.6 + 255 * 0.4);
                        g = (int)(g * 0.6 + 255 * 0.4);
                        b = (int)(b * 0.6 + 255 * 0.4);
                        
                        var color = $"#{r:X2}{g:X2}{b:X2}";
                        var nodeLabel = node.ToString()?.Replace("\"", "\\\"") ?? node.ToString() ?? "";
                        lines.Add($"  \"{nodeLabel}\" [shape=circle, style=filled, fillcolor=\"{color}\"];");
                    }
                    else
                    {
                        // Fallback for non-Point types
                        var nodeLabel = node.ToString()?.Replace("\"", "\\\"") ?? node.ToString() ?? "";
                        lines.Add($"  \"{nodeLabel}\" [shape=circle];");
                    }
                }
            }
        }
        else
        {
            // Fallback: use auto-generated colors for non-Point types
            var componentColors = new Dictionary<Point, string>();
            int rootCount = roots.Count;
            for (int i = 0; i < roots.Count; i++)
            {
                var root = roots[i];
                double hue = rootCount == 1 ? 0 : (360.0 * i / rootCount);
                var color = HslToHex(hue, 0.4, 0.95);
                componentColors[root] = color;
            }
            
            foreach (var root in roots)
            {
                var componentNodes = uf.GetAllNodes()
                    .Where(n => UnionFind<Point>.Equals(uf.Find(n), root))
                    .OrderBy(n => n.ToString())
                    .ToList();
                
                var color = componentColors[root];
                foreach (var node in componentNodes)
                {
                    var nodeLabel = node.ToString()?.Replace("\"", "\\\"") ?? node.ToString() ?? "";
                    lines.Add($"  \"{nodeLabel}\" [shape=circle, style=filled, fillcolor=\"{color}\"];");
                }
            }
        }
        
        lines.Add("");
        
        // Add edges (parent -> child connections)
        foreach (var kvp in uf.GetParentRelationships())
        {
            var node = kvp.Key;
            var parentNode = kvp.Value;
            
            if (!UnionFind<Point>.Equals(node, parentNode))
            {
                var nodeLabel = node.ToString()?.Replace("\"", "\\\"") ?? node.ToString() ?? "";
                var parentLabel = parentNode.ToString()?.Replace("\"", "\\\"") ?? parentNode.ToString() ?? "";
                lines.Add($"  \"{parentLabel}\" -- \"{nodeLabel}\";");
            }
        }
        
        lines.Add("}");
        return string.Join("\n", lines);
    }
    
    private int NormalizeToByte(double value, double min, double max)
    {
        if (max == min) return 128; // Gray if all values are the same
        
        // Normalize to 0-1 range, then scale to 0-255
        double normalized = (value - min) / (max - min);
        // Clamp to 0-1 range (handle edge cases)
        normalized = Math.Max(0, Math.Min(1, normalized));
        return (int)Math.Round(normalized * 255);
    }
    
    private string HslToHex(double h, double s, double l)
    {
        // Convert HSL to RGB, then to hex
        // Normalize hue to 0-360
        h = h % 360;
        if (h < 0) h += 360;
        
        double c = (1 - Math.Abs(2 * l - 1)) * s;
        double x = c * (1 - Math.Abs((h / 60) % 2 - 1));
        double m = l - c / 2;
        
        double r = 0, g = 0, b = 0;
        
        if (h < 60)
        {
            r = c; g = x; b = 0;
        }
        else if (h < 120)
        {
            r = x; g = c; b = 0;
        }
        else if (h < 180)
        {
            r = 0; g = c; b = x;
        }
        else if (h < 240)
        {
            r = 0; g = x; b = c;
        }
        else if (h < 300)
        {
            r = x; g = 0; b = c;
        }
        else
        {
            r = c; g = 0; b = x;
        }
        
        int R = (int)Math.Round((r + m) * 255);
        int G = (int)Math.Round((g + m) * 255);
        int B = (int)Math.Round((b + m) * 255);
        
        return $"#{R:X2}{G:X2}{B:X2}";
    }
}