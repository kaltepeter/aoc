package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"strconv"
	"strings"
)

type puzzleData struct {
	input   []string
	output  []string
	decoder map[string]int
}

func ProcessInput(s []string) []puzzleData {
	listOfPuzzleData := []puzzleData{}
	for _, line := range s {
		io := util.StringToListOfStringWithSeparator(line, `\|`)
		input := util.StringToListOfStringWithSeparator(strings.Trim(io[0], " \n"), ` +`)
		output := util.StringToListOfStringWithSeparator(strings.Trim(io[1], " \n"), ` +`)
		listOfPuzzleData = append(listOfPuzzleData, puzzleData{
			input:   input,
			output:  output,
			decoder: map[string]int{},
		})
	}
	return listOfPuzzleData
}

func Part1(data []puzzleData) int {
	const (
		ONE   = 2
		FOUR  = 4
		SEVEN = 3
		EIGHT = 7
	)
	counts := 0
	for _, line := range data {
		for _, digit := range line.output {
			switch {
			case len(digit) == ONE || len(digit) == FOUR || len(digit) == SEVEN || len(digit) == EIGHT:
				counts += 1
			}
		}
	}
	return counts
}

func FindMissingChar(str string, code string) string {
	missingChar := ""
	chars := strings.Split(code, ``)
	for _, c := range chars {
		if !strings.Contains(str, c) {
			missingChar += c
		}
	}
	return missingChar
}

func Decode(dataOutput []string, decoder map[int]string) (int, error) {
	output := ""
	var err error = nil
	for _, digit := range dataOutput {
		for d, code := range decoder {
			if util.HasAllChars(digit, code, true) {
				output += fmt.Sprint(d)
			}
		}
	}
	if len(output) != 4 {
		err = fmt.Errorf("error. found less than four digits. output: %v data: %v decoder: %v", output, dataOutput, decoder)
	}
	digit, _ := strconv.ParseInt(output, 10, 0)
	return int(digit), err
}

func Part2(data []puzzleData) int {
	codes := []int{}
	for _, line := range data {
		decoder := map[int]string{}
		for _, digit := range line.input {
			switch len(digit) {
			case 2:
				decoder[1] = digit
			case 4:
				decoder[4] = digit
			case 3:
				decoder[7] = digit
			case 7:
				decoder[8] = digit
			}
		}
		for _, digit := range line.input {
			one := FindMissingChar(digit, decoder[1])
			four := FindMissingChar(digit, decoder[4])

			switch len(digit) {
			case 5:
				if len(four) == 2 {
					decoder[2] = digit
				} else if len(one) == 1 {
					decoder[5] = digit
				} else {
					decoder[3] = digit
				}
			case 6:
				if len(one) == 1 {
					decoder[6] = digit
				} else if len(four) == 1 {
					decoder[0] = digit
				} else {
					decoder[9] = digit
				}
			}
		}
		outputCode, err := Decode(line.output, decoder)
		if err != nil {
			panic(err)
		}
		codes = append(codes, outputCode)
	}

	return util.Sum(codes)
}

func main() {
	input := filepath.Join("2021", "day_8", "raw-input.txt")
	inputData := util.ParseInput(input)
	listOfDigits := ProcessInput(inputData)
	p1Result := Part1(listOfDigits)
	fmt.Printf("Part I: Counts of 1, 4, 7, 8 = %v\n", p1Result) // 554

	p2Result := Part2(listOfDigits)
	fmt.Printf("Part II: Counts of sum of all digits = %v\n", p2Result) // 990964
}
