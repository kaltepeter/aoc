package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
)

func Part1(data []int) int {
	result := 0
	resultMap := map[int]int{}
	for i := 0; i < len(data); i++ {
		for _, num := range data {
			resultMap[i] += util.Abs(num - i)
		}
		if resultMap[i] < result || result == 0 {
			result = resultMap[i]
		}
	}

	// fmt.Println(resultMap)
	return result
}

func Part2(data []int) int {
	result := 0
	resultMap := map[int]int{}
	for i := 0; i < len(data); i++ {
		for _, num := range data {
			resultMap[i] += util.GaussSum(util.Abs(num - i))
		}
		if resultMap[i] < result || result == 0 {
			result = resultMap[i]
		}
	}

	return result
}

func main() {
	input := filepath.Join("2021", "day_7", "raw-input.txt")
	inputData := util.ParseInput(input)
	listOfInts := util.StringToListOfInt(inputData[0])
	p1Result := Part1(listOfInts) // 387033 too high, 335271
	fmt.Printf("Part I: Number of fuel %d\n", p1Result)

	p2Result := Part2(listOfInts)
	fmt.Printf("Part II: Number of fuel %d\n", p2Result)
}
