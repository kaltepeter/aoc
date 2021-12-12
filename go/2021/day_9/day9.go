package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"sort"
)

func ProcessInput(data []string) [][]int {
	smokeMap := [][]int{}
	for _, line := range data {
		row := util.StringToListOfIntWithSeparator(line, "")
		smokeMap = append(smokeMap, row)
	}
	return smokeMap
}

func AddRisk(acc int, v int) int {
	return acc + (v + 1)
}

func GetLowPoints(data [][]int) [][2]int {
	lowPoints := [][2]int{}
	for rIdx, row := range data {
		for cIdx, cell := range row {
			if cell == 9 {
				continue
			}
			if cIdx > 0 && row[cIdx-1] <= cell {
				continue
			}

			if cIdx < len(row)-1 && row[cIdx+1] <= cell {
				continue
			}

			if rIdx > 0 {
				prevRow := data[rIdx-1]
				if prevRow[cIdx] <= cell {
					continue
				}
			}

			if rIdx < len(data)-1 {
				nextRow := data[rIdx+1]
				if nextRow[cIdx] <= cell {
					continue
				}
			}

			lowPoints = append(lowPoints, [2]int{rIdx, cIdx})
		}
	}
	return lowPoints
}

func GetBasin(data [][]int, point [2]int, foundCoords *[][2]int) int {
	basinCount := 0
	x, y := point[0], point[1]
	cell := data[x][y]
	if y > 0 {
		left := data[x][y-1]
		lCoord := [2]int{x, y - 1}
		coordFound := util.ArrayContainsCoord(foundCoords, lCoord)
		if left > cell && left != 9 && !coordFound {
			*foundCoords = append(*foundCoords, lCoord)
			basinCount += 1
			basinCount += GetBasin(data, lCoord, foundCoords)
		}
	}
	if y < len(data[x])-1 {
		right := data[x][y+1]
		rCoord := [2]int{x, y + 1}
		coordFound := util.ArrayContainsCoord(foundCoords, rCoord)
		if right > cell && right != 9 && !coordFound {
			*foundCoords = append(*foundCoords, rCoord)
			basinCount += 1
			basinCount += GetBasin(data, rCoord, foundCoords)
		}
	}
	if x > 0 {
		up := data[x-1][y]
		uCoord := [2]int{x - 1, y}
		coordFound := util.ArrayContainsCoord(foundCoords, uCoord)
		if up > cell && up != 9 && !coordFound {
			*foundCoords = append(*foundCoords, uCoord)
			basinCount += 1
			basinCount += GetBasin(data, uCoord, foundCoords)
		}
	}
	if x < len(data)-1 {
		down := data[x+1][y]
		dCoord := [2]int{x + 1, y}
		coordFound := util.ArrayContainsCoord(foundCoords, dCoord)
		if down > cell && down != 9 && !coordFound {
			*foundCoords = append(*foundCoords, dCoord)
			basinCount += 1
			basinCount += GetBasin(data, dCoord, foundCoords)
		}
	}
	return basinCount
}

func Part1(data [][]int) int {
	lowPoints := []int{}
	lowPointPos := GetLowPoints(data)
	for _, coord := range lowPointPos {
		x, y := coord[0], coord[1]
		lowPoints = append(lowPoints, data[x][y])
	}
	return util.ReduceInt(lowPoints, AddRisk, 0)
}

func Part2(data [][]int) int {
	basins := []int{}
	lowPointPos := GetLowPoints(data)
	foundCoords := [][2]int{}
	for _, coord := range lowPointPos {
		basinSize := GetBasin(data, coord, &foundCoords)
		foundCoords = append(foundCoords, coord)
		basinSize += 1
		// fmt.Printf("Coord: %v foundCoords: %v basinSize: %v\n", coord, foundCoords, basinSize)
		basins = append(basins, basinSize)
	}
	// fmt.Printf("count of low points: %v basinMap: %v\n", len(lowPointPos), basins)
	sort.Ints(basins)
	// fmt.Println(basins, basins[len(basins)-3:])
	return util.ReduceInt(basins[len(basins)-3:], util.Multiply, 1)
}

func main() {
	input := filepath.Join("2021", "day_9", "raw-input.txt")
	inputData := util.ParseInput(input)
	smokeData := ProcessInput(inputData)
	p1Result := Part1(smokeData)
	fmt.Printf("Part I: Risk is = %v\n", p1Result) // 629 too low, 1763 too high, 633

	p2Result := Part2(smokeData)
	fmt.Printf("Part II: Risk is = %v\n", p2Result)

}
