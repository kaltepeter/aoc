package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"strconv"
)

type result struct {
	zero int
	one  int
}

const (
	zero string = "0"
	one  string = "1"
)

func Filter(vs []string, pos int, criteria string, f func(string, int, string) bool) []string {
	filtered := make([]string, 0)
	for _, v := range vs {
		if f(v, pos, criteria) {
			filtered = append(filtered, v)
		}
	}
	return filtered
}

func countVals(diagnostic []string) []result {
	results := make([]result, len(diagnostic[0]))
	for _, item := range diagnostic {
		for idx, char := range item {
			var zeros int
			var ones int
			previousVal := results[idx]
			zeros = previousVal.zero
			ones = previousVal.one

			switch string(char) {
			case zero:
				zeros += 1
			case one:
				ones += 1
			}
			results[idx] = result{zero: zeros, one: ones}
		}
	}
	return results
}

func Part1(diagnostic []string) (int64, int64, error) {
	var gamma string
	var epsilon string

	results := countVals(diagnostic)

	for _, counts := range results {
		if counts.zero > counts.one {
			gamma += zero
			epsilon += one
		} else {
			gamma += one
			epsilon += zero
		}
	}
	gammaNum, _ := strconv.ParseInt(gamma, 2, 0)
	epsilonNum, _ := strconv.ParseInt(epsilon, 2, 0)
	return gammaNum, epsilonNum, nil
}

func CalcResult(num1 int64, num2 int64) int64 {
	return num1 * num2
}

func ProcessOxygenGeneratorRating(counts result) string {
	var searchVal string
	switch {
	case counts.zero > counts.one:
		searchVal = zero
	case counts.one > counts.zero:
		searchVal = one
	case counts.zero == counts.one:
		searchVal = one
	}
	return searchVal
}

func ProcessCo2ScrubberRating(counts result) string {
	var searchVal string
	switch {
	case counts.zero > counts.one:
		searchVal = one
	case counts.one > counts.zero:
		searchVal = zero
	case counts.zero == counts.one:
		searchVal = zero
	}
	return searchVal
}

func FindRating(diagnostic []string, processFunc func(counts result) string) int64 {
	candidates := diagnostic[0:]
	for digitIdx := 0; digitIdx < len(diagnostic[0]); digitIdx++ {
		results := countVals(candidates)
		if len(candidates) == 1 {
			break
		}
		searchVal := processFunc(results[digitIdx])
		candidates = Filter(candidates, digitIdx, searchVal, func(digits string, pos int, criteria string) bool {
			return string(digits[pos]) == criteria
		})
	}
	rating, _ := strconv.ParseInt(candidates[0], 2, 0)
	return rating
}

func main() {
	input := filepath.Join("2021", "day_3", "raw-input.txt")
	inputData := util.ParseInput(input)
	p1Gamma, p1Epsilon, _ := Part1(inputData)
	fmt.Printf("Part I: Gamma: %d Epsilon %d Power Consumption %d\n", p1Gamma, p1Epsilon, CalcResult(p1Gamma, p1Epsilon))

	p2OxygenGeneratorRating := FindRating(inputData, ProcessOxygenGeneratorRating)
	p2Co2ScrubberRating := FindRating(inputData, ProcessCo2ScrubberRating)
	fmt.Printf("Part II: Oxygen Generator Rating: %d, CO2 Scrubber Rating: %d, Life Support Rating: %d \n", p2OxygenGeneratorRating, p2Co2ScrubberRating, CalcResult(p2OxygenGeneratorRating, p2Co2ScrubberRating))
}
