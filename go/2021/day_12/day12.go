package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"strings"
)

const (
	START = "start"
	END   = "end"
	SEP   = " -> "
)

type Cave struct {
	Key      string
	Big      bool
	Vertices map[string]*Cave
}

func (c *Cave) String() string {
	return fmt.Sprintf("%v", c.Key)
}

func NewCave(key string) *Cave {
	return &Cave{
		Key:      key,
		Big:      !util.IsLowerCase(key),
		Vertices: map[string]*Cave{},
	}
}

type CaveGraph struct {
	Vertices map[string]*Cave
}

func NewCaveGraph() *CaveGraph {
	return &CaveGraph{
		Vertices: map[string]*Cave{},
	}
}

func (c *CaveGraph) String() {
	s := ""
	for key, v := range c.Vertices {
		s += key + " -> "
		near := v.Vertices
		for k, _ := range near {
			s += k + " "
		}
		s += "\n"
	}
	fmt.Println(s)
}

func (c *CaveGraph) AddCave(key string) {
	v := NewCave(key)
	if _, ok := c.Vertices[key]; !ok {
		c.Vertices[key] = v
	}
}

func (c *CaveGraph) AddEdge(k1, k2 string) {
	v1 := c.Vertices[k1]
	v2 := c.Vertices[k2]

	if v1 == nil || v2 == nil {
		panic("not all vertices exist")
	}

	if _, ok := v1.Vertices[v2.Key]; ok {
		return
	}

	v1.Vertices[v2.Key] = v2
	if v1.Key != v2.Key {
		v2.Vertices[v1.Key] = v1
	}

	c.Vertices[v1.Key] = v1
	c.Vertices[v2.Key] = v2
}

type Path struct {
	Path                  []string
	Visited               map[string]int
	VisitedSmallCaveTwice bool
}

func copyMap(a map[string]int) map[string]int {
	out := map[string]int{}
	for k, v := range a {
		out[k] = v
	}
	return out
}

func Traverse(g *CaveGraph) [][]string {
	queue := []Path{{[]string{START}, map[string]int{}, false}}
	paths := [][]string{}

	for len(queue) > 0 {
		cur := queue[0]
		queue = queue[1:]

		cave := g.Vertices[cur.Path[len(cur.Path)-1]]

		if len(cave.Key) == 0 {
			continue
		}

		if cave.Key == END {
			paths = append(paths, cur.Path)
			continue
		}

		newVisited := copyMap(cur.Visited)
		if !cave.Big {
			newVisited[cave.Key] = 1
		}

		for _, otherCave := range cave.Vertices {
			if cur.Visited[otherCave.Key] > 0 {
				continue
			}
			newPath := make([]string, len(cur.Path))
			copy(newPath, cur.Path)
			newPath = append(newPath, otherCave.Key)
			queue = append(queue, Path{newPath, newVisited, false})
		}
	}

	return paths
}

func TraverseSingleSmallCaveTwice(g *CaveGraph) [][]string {
	queue := []Path{{[]string{START}, map[string]int{}, false}}
	paths := [][]string{}

	for len(queue) > 0 {
		cur := queue[0]
		queue = queue[1:]

		cave := g.Vertices[cur.Path[len(cur.Path)-1]]

		if len(cave.Key) == 0 {
			continue
		}

		if cave.Key == END {
			paths = append(paths, cur.Path)
			continue
		}

		newVisited := copyMap(cur.Visited)
		if !cave.Big {
			newVisited[cave.Key] += 1
		}

		for _, otherCave := range cave.Vertices {
			newVisitedCalledTwice := cur.VisitedSmallCaveTwice
			if cur.Visited[otherCave.Key] > 0 {
				if otherCave.Key == START || cur.VisitedSmallCaveTwice {
					continue
				} else {
					newVisitedCalledTwice = true
				}
			}

			newPath := make([]string, len(cur.Path))
			copy(newPath, cur.Path)
			newPath = append(newPath, otherCave.Key)
			queue = append(queue, Path{newPath, newVisited, newVisitedCalledTwice})
		}
	}

	return paths
}

func ProcessInput(data []string) *CaveGraph {
	caveGraph := NewCaveGraph()

	for _, line := range data {
		nodes := strings.Split(line, "-")
		n1, n2 := nodes[0], nodes[1]
		caveGraph.AddCave(n1)
		caveGraph.AddCave(n2)
		caveGraph.AddEdge(n1, n2)
	}
	caveGraph.String()

	return caveGraph
}

func Part1(data *CaveGraph) int {
	paths := Traverse(data)
	// for _, path := range paths {
	// 	fmt.Println(strings.Join(path, SEP))
	// }
	return len(paths)
}

func Part2(data *CaveGraph) int {
	paths := TraverseSingleSmallCaveTwice(data)
	return len(paths)
}

func main() {
	input := filepath.Join("2021", "day_12", "raw-input.txt")
	inputData := util.ParseInput(input)
	caveMap := ProcessInput(inputData)
	p1Result := Part1(caveMap)
	fmt.Printf("Part I: Paths that visit small caves is = %v\n", p1Result) // 4549

	p2Result := Part2(caveMap)
	fmt.Printf("Part II: Paths that visit small caves is = %v\n", p2Result) // 120535
}
