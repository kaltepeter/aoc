package day

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
)

func ProcessInput(data *[]string) [][]int {
	riskData := [][]int{}
	for _, line := range *data {
		riskData = append(riskData, util.StringToListOfIntWithSeparator(line, ""))
	}
	return riskData
}

func Part1(data *[][]int) int {
	return 0
}

func Part2(data *[][]int) int {
	return 0
}

func main() {
	input := filepath.Join("2021", "day_xx", "raw-input.txt")
	inputData := util.ParseInput(input)
	riskData := ProcessInput(&inputData)
	p1Result := Part1(&riskData)
	fmt.Printf("Part I: the lowest risk path level is = %v\n", p1Result)
	if p1Result != 562 {
		panic("FAILED on Part I")
	}

	p2Result := Part2(&riskData)
	fmt.Printf("Part II: the lowest risk path level is = %v\n", p2Result)
	if p2Result != 2874 {
		panic("FAILED on Part II")
	}
}
