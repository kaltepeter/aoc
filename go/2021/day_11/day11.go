package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
)

const (
	MAX_ENERGY_LEVEL = 9
)

func ProcessInput(data []string) [10][10]int {
	octopus := [10][10]int{}
	for i, row := range data {
		list := util.StringToListOfIntWithSeparator(row, "")
		octos := (*[10]int)(list)
		octopus[i] = *octos
	}
	return octopus
}

func GetNeighbors(coord [2]int, rowCount int, colCount int) [][2]int {
	neighbors := [][2]int{}
	for x := coord[0] - 1; x <= coord[0]+1; x++ {
		if x >= 0 && x < rowCount {
			for y := coord[1] - 1; y <= coord[1]+1; y++ {
				if y >= 0 && y < colCount {
					if x == coord[0] && y == coord[1] {
						continue
					}
					neighbors = append(neighbors, [2]int{x, y})
				}
			}
		}
	}
	return neighbors
}

func FlashCells(data *[10][10]int, flashMap map[[2]int]int, cellsToFlash *util.CoordSet, hasFlashed *util.CoordSet) *util.CoordSet {
	rows := len(data)
	cols := len(data[0])
	for _, coord := range cellsToFlash.Coords() {
		neighborsNotFlashed := [][2]int{}
		neighbors := GetNeighbors(coord, rows, cols)
		for _, n := range neighbors {
			if !hasFlashed.Has(n) {
				neighborsNotFlashed = append(neighborsNotFlashed, n)
			}
		}
		BumpAllNeighbors(flashMap, neighborsNotFlashed, cellsToFlash)
		hasFlashed.Add(coord)
		cellsToFlash.Delete(coord)
	}

	if cellsToFlash.Size() > 0 {
		// recurse
		FlashCells(data, flashMap, cellsToFlash, hasFlashed)
	}
	return cellsToFlash
}

func Step(data *[10][10]int) (*[10][10]int, int) {
	hasFlashed := util.CoordSet{}
	flashMap := map[[2]int]int{}
	// bump all by one
	BumpAllByOne(data)

	cellsToFlash := util.CoordSet{}
	// Store the cells to flash
	for x, row := range data {
		for y, _ := range row {
			coord := [2]int{x, y}
			// initial value
			flashMap[coord] = data[x][y]

			if flashMap[coord] > MAX_ENERGY_LEVEL {
				cellsToFlash.Add(coord)
			}
		}
	}

	// flash cells
	FlashCells(data, flashMap, &cellsToFlash, &hasFlashed)

	// set values
	for k, v := range flashMap {
		data[k[0]][k[1]] = v
	}

	for _, coord := range hasFlashed.Coords() {
		data[coord[0]][coord[1]] = 0
	}

	return data, hasFlashed.Size()
}

func PrintBoard(data [10][10]int) {
	for _, row := range data {
		for _, cell := range row {
			fmt.Print(cell)
		}
		fmt.Println()
	}
}

func BumpAllNeighbors(flashMap map[[2]int]int, neighbors [][2]int, newCellsToFlash *util.CoordSet) {
	for _, coord := range neighbors {
		flashMap[coord] += 1
		if flashMap[coord] > MAX_ENERGY_LEVEL {
			newCellsToFlash.Add(coord)
		}
	}
}

func BumpAllByOne(data *[10][10]int) *[10][10]int {
	for x, row := range data {
		for y, _ := range row {
			data[x][y] += 1
		}
	}
	return data
}

func Part1(data [10][10]int) int {
	flashes := 0
	for i := 1; i <= 100; i++ {
		fmt.Println("STEP ", i)
		_, f := Step(&data)
		PrintBoard(data)
		fmt.Println("")

		flashes += f
	}

	return flashes
}

func main() {
	input := filepath.Join("2021", "day_11", "raw-input.txt")
	inputData := util.ParseInput(input)
	octopusMap := ProcessInput(inputData)
	p1Result := Part1(octopusMap)
	fmt.Printf("Part I: Octopus flashes is = %v\n", p1Result) // 1608
}
