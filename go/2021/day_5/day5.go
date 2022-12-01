package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
)

const EMPTY_SPACE = "."
const DIR_H = "horizontal"
const DIR_V = "vertical"
const DIR_D = "diagonal"

type coord struct {
	x int
	y int
}

type pathCoords struct {
	start coord
	end   coord
}

type lineInstructions struct {
	lines []pathCoords
	maxX  int
	maxY  int
}

func ProcessData(data []string) lineInstructions {
	var paths []pathCoords = []pathCoords{}
	maxX := 0
	maxY := 0
	for _, d := range data {
		coords := util.StringToListOfStringWithSeparator(d, ` -> `)
		start := util.StringToListOfInt(coords[0])
		end := util.StringToListOfInt(coords[1])
		switch {
		case start[0] > maxX:
			maxX = start[0]
		case end[0] > maxX:
			maxX = end[0]
		case start[1] > maxY:
			maxY = start[1]
		case end[1] > maxY:
			maxY = end[1]
		}
		paths = append(paths, pathCoords{start: coord{x: start[0], y: start[1]}, end: coord{x: end[0], y: end[1]}})
	}
	return lineInstructions{lines: paths, maxX: maxX + 1, maxY: maxY + 1}
}

func PrintLineMap(data [][]int) {
	for _, row := range data {
		for _, col := range row {
			fmt.Printf("%d", col)
		}
		fmt.Printf("\n")
	}
}

func CalcRange(start coord, end coord, dir string) []coord {
	var coords []coord = []coord{}
	if dir == DIR_H {
		if start.x < end.x {
			for i := start.x; i <= end.x; i++ {
				coords = append(coords, coord{x: i, y: start.y})
			}
		} else {
			for i := end.x; i <= start.x; i++ {
				coords = append(coords, coord{x: i, y: start.y})
			}
		}
	} else if dir == DIR_V {
		if start.y < end.y {
			for i := start.y; i <= end.y; i++ {
				coords = append(coords, coord{x: start.x, y: i})
			}
		} else {
			for i := end.y; i <= start.y; i++ {
				coords = append(coords, coord{x: start.x, y: i})
			}
		}
	} else {
		if start.x < end.x {
			// 1,1 -> 3,3
			for i, j := start.x, start.y; i <= end.x; i = i + 1 {
				if start.y < end.y {
					coords = append(coords, coord{x: i, y: j})
					j += 1
				} else {
					coords = append(coords, coord{x: i, y: j})
					j -= 1
				}
			}
		} else {
			// 9,7 -> 7,9
			for i, j := end.x, end.y; i <= start.x; i = i + 1 {
				if end.y < start.y {
					coords = append(coords, coord{x: i, y: j})
					j += 1
				} else {
					coords = append(coords, coord{x: i, y: j})
					j -= 1
				}
			}
		}

	}
	return coords
}

func Part1(data lineInstructions) int {
	var dangerousPoints int
	var lineMap [][]int = make([][]int, data.maxY)
	for i := range lineMap {
		lineMap[i] = make([]int, data.maxX)
	}

	foundCoords := map[string]int{}

	for _, d := range data.lines {
		var coords []coord
		switch {
		case d.start.x == d.end.x:
			coords = CalcRange(d.start, d.end, DIR_V)
			// fmt.Printf("H: %v coords: %v\n", d, coords)
		case d.start.y == d.end.y:
			coords = CalcRange(d.start, d.end, DIR_H)
			// fmt.Printf("V: %v coords: %v\n", d, coords)
		default:
			// fmt.Printf("Found a diagonal: %v. Skipping\n", d)
		}

		for _, coord := range coords {
			lineMap[coord.y][coord.x] = lineMap[coord.y][coord.x] + 1
			if lineMap[coord.y][coord.x] >= 2 {
				coordKey := fmt.Sprintf("%v,%v", coord.x, coord.y)
				_, coordFound := foundCoords[coordKey]
				if !coordFound {
					dangerousPoints += 1
				}
				foundCoords[coordKey] = lineMap[coord.y][coord.x]

			}
		}
	}
	// fmt.Println(foundCoords)

	fmt.Println("")

	return dangerousPoints
}

func Part2(data lineInstructions) int {
	var dangerousPoints int
	var lineMap [][]int = make([][]int, data.maxY)
	for i := range lineMap {
		lineMap[i] = make([]int, data.maxX)
	}

	foundCoords := map[string]int{}

	for _, d := range data.lines {
		var coords []coord
		switch {
		case d.start.x == d.end.x:
			coords = CalcRange(d.start, d.end, DIR_V)
			// fmt.Printf("H: %v coords: %v\n", d, coords)
		case d.start.y == d.end.y:
			coords = CalcRange(d.start, d.end, DIR_H)
			// fmt.Printf("V: %v coords: %v\n", d, coords)
		default:
			coords = CalcRange(d.start, d.end, DIR_D)
			// fmt.Printf("D: %v coords: %v\n", d, coords)
		}

		for _, coord := range coords {
			lineMap[coord.y][coord.x] = lineMap[coord.y][coord.x] + 1
			if lineMap[coord.y][coord.x] >= 2 {
				coordKey := fmt.Sprintf("%v,%v", coord.x, coord.y)
				_, coordFound := foundCoords[coordKey]
				if !coordFound {
					dangerousPoints += 1
				}
				foundCoords[coordKey] = lineMap[coord.y][coord.x]

			}
		}
	}
	// PrintLineMap(lineMap)

	fmt.Println("")

	return dangerousPoints
}

func main() {
	input := filepath.Join("2021", "day_5", "raw-input.txt")
	inputData := util.ParseInput(input)
	coords := ProcessData(inputData)
	p1Result := Part1(coords)
	// 5678 too high, 305 too low, 5373
	fmt.Printf("Part I: Dangerous points %d\n", p1Result)

	p2Result := Part2(coords)
	fmt.Printf("Part II: Dangerous points %d\n", p2Result)
}
