package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
)

func ProcessInput(data *[][]string) [][]string {
	imageData := [][]string{}
	// for _, line := range *data {
	// 	imageData = append(imageData, util.StringToListOfIntWithSeparator(line, ""))
	// }
	return imageData
}

func Part1(data *[][]string) int {
	return 0
}

func Part2(data *[][]string) int {
	return 0
}

func main() {
	input := filepath.Join("2021", "day_20", "raw-input.txt")
	inputData := util.SplitInputByEmptyLines(input)
	imageData := ProcessInput(&inputData)
	p1Result := Part1(&imageData)
	fmt.Printf("Part I: the number of lit pixels is = %v\n", p1Result)
	if p1Result != 562 {
		panic("FAILED on Part I")
	}

	p2Result := Part2(&imageData)
	fmt.Printf("Part II: the lowest risk path level is = %v\n", p2Result)
	if p2Result != 2874 {
		panic("FAILED on Part II")
	}
}
