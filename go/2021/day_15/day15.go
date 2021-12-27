package main

import (
	"fmt"
	"ka/m/util"
	"math"
	"path/filepath"
)

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

func Part1(data *[][]int) int {
	maxX := len((*data)[0])
	maxY := len(*data)
	total := 0
	distance := map[util.Coord]int{}
	visited := map[util.Coord]bool{}
	distance[util.Coord{0, 0}] = 0

	current := util.Coord{0, 0}
	endNode := util.Coord{maxX - 1, maxY - 1}

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

func Part2(data *[][]int) int {
	maxX := len((*data)[0]) * 5
	maxY := len(*data) * 5
	total := 0
	distance := map[util.Coord]int{}
	visited := map[util.Coord]bool{}
	distance[util.Coord{0, 0}] = 0

	current := util.Coord{0, 0}
	endNode := util.Coord{maxX - 1, maxY - 1}

	for {
		for _, n := range GetNeighbors(current, maxX, maxY) {
			if visited[n] {
				continue
			}

			rows := len(*data)
			cols := len((*data)[0])
			y := n[1] % rows
			x := n[0] % cols
			val := (*data)[y][x]
			val += n[1]/rows + n[0]/cols
			if val > 9 {
				val -= 9
			}

			newDistance := distance[current] + val
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

func main() {
	input := filepath.Join("2021", "day_15", "raw-input.txt")
	inputData := util.ParseInput(input)
	riskData := ProcessInput(&inputData)
	p1Result := Part1(&riskData)
	fmt.Printf("Part I: the lowest risk path level is = %v\n", p1Result) // 562

	p2Result := Part2(&riskData)
	fmt.Printf("Part II: the lowest risk path level is = %v\n", p2Result)
}
