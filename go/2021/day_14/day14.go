package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"strings"
)

type Polymer struct {
	Template           string
	PairInsertionRules map[string]string
}

type CountMap struct {
	char  string
	count int
}

type CharCounts struct {
	total       int
	mostCommon  CountMap
	leastCommon CountMap
}

func CountChars(s string) CharCounts {
	charCounts := CharCounts{total: len(s)}
	counts := map[rune]int{}
	least, most := rune(s[0]), rune(s[0])
	for _, c := range s {
		counts[c] += 1
		if counts[c] > counts[most] {
			most = c
		}
		if counts[c] < counts[least] {
			least = c
		}
	}
	charCounts.mostCommon = CountMap{string(most), counts[most]}
	charCounts.leastCommon = CountMap{string(least), counts[least]}
	return charCounts
}

func ProcessInput(inputData *[]string) *Polymer {
	polymer := Polymer{Template: (*inputData)[0], PairInsertionRules: map[string]string{}}
	instructions := (*inputData)[2:]
	for _, instruction := range instructions {
		rule := strings.Split(instruction, " -> ")
		pair, insertion := strings.Trim(rule[0], " \n"), strings.Trim(rule[1], " \n")
		polymer.PairInsertionRules[pair] = fmt.Sprintf("%s%s%s", string(pair[0]), insertion, string(pair[1]))
	}
	return &polymer
}

func Part1(pd *Polymer) int {
	str := pd.Template
	newStr := ""
	steps := 10
	for i := 0; i < steps; i++ {
		// take first char
		newStr += string(str[0])
		for idx := 1; idx < len(str); idx++ {
			pair := fmt.Sprintf("%s%s", string(str[idx-1]), string(str[idx]))
			newStr += pd.PairInsertionRules[pair][1:3] // last two chars of pair, they overlap
		}
		str = newStr
		newStr = ""
	}
	counts := CountChars(str)
	return counts.mostCommon.count - counts.leastCommon.count
}

func main() {
	input := filepath.Join("2021", "day_14", "raw-input.txt")
	inputData := util.ParseInput(input)
	polymerData := ProcessInput(&inputData)
	p1Result := Part1(polymerData)
	fmt.Printf("Part I: most common element minus least common element = %v\n", p1Result) // 2988
}
