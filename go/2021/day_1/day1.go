package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
)

type counts struct {
	increase  int
	descrease int
}

func part_1() {
	input := filepath.Join("2021", "day_1", "raw-input.txt")
	inputData := util.ParseInputToIntegers(input)

	retVal := counts{
		increase:  0,
		descrease: 0,
	}

	for idx, num := range inputData {
		if idx != 0 {
			if num > inputData[idx-1] {
				retVal.increase += 1
			} else {
				retVal.descrease += 1
			}
		}
	}

	fmt.Println("Part I: ", retVal.increase)
}

func sum(array []int64) int64 {
	result := int64(0)
	for _, v := range array {
		result += v
	}
	return result
}

func part_2() {
	input := filepath.Join("2021", "day_1", "raw-input.txt")
	inputData := util.ParseInputToIntegers(input)

	window := 3
	maxRange := len(inputData) - window

	retVal := counts{
		increase:  0,
		descrease: 0,
	}

	var slices []int64

	for idx := range inputData {
		if idx > maxRange {
			break
		}
		slice := inputData[idx : idx+window]
		slices = append(slices, sum(slice))
	}

	for idx, num := range slices {
		if idx != 0 {
			if num > slices[idx-1] {
				retVal.increase += 1
			} else {
				retVal.descrease += 1
			}
		}
	}

	fmt.Println("Part II: ", retVal.increase)
}

func main() {
	part_1()
	part_2()
}
