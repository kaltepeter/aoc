package main

import (
	"container/heap"
	"fmt"
	"ka/m/util"
	"math"
	"path/filepath"
)

// https://pkg.go.dev/container/heap#example-package-PriorityQueue
// https://skarlso.github.io/2021/12/15/aoc-day15/
// https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-using-priority_queue-stl/
// https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Practical_optimizations_and_infinite_graphs
// https://www.redblobgames.com/pathfinding/a-star/introduction.html
// https://www.redblobgames.com/pathfinding/a-star/implementation.html
type Item struct {
	value util.Coord
	dist  int
	index int
}

type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].dist < pq[j].dist
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	item.index = -1
	*pq = old[0 : n-1]
	return item
}

func ProcessInput(data *[]string) [][]int {
	riskData := [][]int{}
	for _, line := range *data {
		riskData = append(riskData, util.StringToListOfIntWithSeparator(line, ""))
	}
	return riskData
}

func GetNeighbors(point util.Coord, maxX int, maxY int) []util.Coord {
	neighbors := []util.Coord{}
	x, y := point[0], point[1]
	if x > 0 {
		neighbors = append(neighbors, util.Coord{x - 1, y})
	}
	if x < maxX-1 {
		neighbors = append(neighbors, util.Coord{x + 1, y})
	}
	if y > 0 {
		neighbors = append(neighbors, util.Coord{x, y - 1})
	}
	if y < maxY-1 {
		neighbors = append(neighbors, util.Coord{x, y + 1})
	}
	return neighbors
}

// basic and slow
func Part1(data *[][]int) int {
	maxX := len((*data)[0])
	maxY := len(*data)
	start := util.Coord{0, 0}
	endNode := util.Coord{maxX - 1, maxY - 1}

	total := 0
	distance := map[util.Coord]int{
		start: 0,
	}
	visited := map[util.Coord]bool{}

	current := start

	for {
		for _, n := range GetNeighbors(current, maxX, maxY) {
			if visited[n] {
				continue
			}
			x, y := n[0], n[1]
			newDistance := distance[current] + (*data)[y][x]
			if _, ok := distance[n]; !ok {
				distance[n] = newDistance
			} else if newDistance < distance[n] {
				distance[n] = newDistance
			}
		}

		visited[current] = true

		if visited[endNode] {
			total = distance[endNode]
			break
		}

		minDist := math.MaxInt
		current = util.Coord{maxX, maxY}
		for p, v := range distance {
			if !visited[p] && v < minDist {
				minDist = v
				current = p
			}
		}
	}

	return total
}

func CalcValueForExpandedGrid(data *[][]int, point util.Coord) int {
	rows := len(*data)
	cols := len((*data)[0])
	y := point[1] % rows
	x := point[0] % cols
	val := (*data)[y][x]
	val += point[1]/rows + point[0]/cols
	if val > 9 {
		val -= 9
	}
	return val
}

func Part2(data *[][]int) int {
	maxX := len((*data)[0]) * 5
	maxY := len(*data) * 5
	start := util.Coord{0, 0}
	end := util.Coord{maxX - 1, maxY - 1}
	pq := make(PriorityQueue, 0)
	heap.Init(&pq)
	heap.Push(&pq, &Item{
		value: start,
		dist:  0,
	})
	distance := map[util.Coord]int{
		start: 0,
	}
	cameFrom := map[util.Coord]util.Coord{
		start: start,
	}

	for pq.Len() > 0 {
		current := heap.Pop(&pq).(*Item) // u

		if current.value == end {
			break
		}

		for _, n := range GetNeighbors(current.value, maxX, maxY) {
			val := CalcValueForExpandedGrid(data, n)
			newDistance := distance[current.value] + val
			if v, ok := distance[n]; !ok || newDistance < v {
				cameFrom[n] = current.value
				distance[n] = newDistance
				heap.Push(&pq, &Item{
					value: n,
					dist:  newDistance,
				})
			}
		}
	}

	var total int
	current := end
	for current != start {
		val := CalcValueForExpandedGrid(data, current)
		total += val
		current = cameFrom[current]
	}

	return total
}

func main() {
	input := filepath.Join("2021", "day_15", "raw-input.txt")
	inputData := util.ParseInput(input)
	riskData := ProcessInput(&inputData)
	p1Result := Part1(&riskData)
	fmt.Printf("Part I: the lowest risk path level is = %v\n", p1Result) // 562
	if p1Result != 562 {
		panic("FAILED on Part I")
	}

	p2Result := Part2(&riskData)
	fmt.Printf("Part II: the lowest risk path level is = %v\n", p2Result) // 2874
	if p2Result != 2874 {
		panic("FAILED on Part II")
	}
}
