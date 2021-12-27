package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
)

type Rule struct {
	Pair1, Pair2 string
	NewChar      string
}

type Polymer struct {
	Template           string
	PairInsertionRules map[string]Rule
}

type CharCount = map[string]int

func MakeCharCount(str string) CharCount {
	charCount := CharCount{}
	for _, char := range str {
		charCount[string(char)] += 1
	}
	return charCount
}

func MostAndLeast(cc *CharCount) (int, int) {
	most, least := 0, 0
	for _, count := range *cc {
		if count > most {
			most = count
		}
		if count < least || least == 0 {
			least = count
		}
	}
	return most, least
}

type CacheStep struct {
	Pairs  map[string]int
	Counts CharCount
}
type Cache = map[int]CacheStep

func ProcessInput(inputData *[]string) *Polymer {
	polymer := Polymer{Template: (*inputData)[0], PairInsertionRules: map[string]Rule{}}
	instructions := (*inputData)[2:]
	for _, instruction := range instructions {
		var in, out string
		fmt.Sscanf(instruction, "%s -> %s", &in, &out)
		polymer.PairInsertionRules[in] = Rule{
			Pair1:   string(in[0]) + out,
			Pair2:   out + string(in[1]),
			NewChar: out,
		}
	}
	return &polymer
}

// brute force, large string
func Part1(pd *Polymer) int {
	str := pd.Template
	newStr := ""
	steps := 10
	for i := 0; i < steps; i++ {
		// take first char
		newStr += string(str[0])
		for idx := 1; idx < len(str); idx++ {
			pair := string(str[idx-1]) + string(str[idx])
			newStr += pd.PairInsertionRules[pair].NewChar + string(str[idx]) // last two chars of pair, they overlap
		}
		str = newStr
		newStr = ""
	}
	cc := MakeCharCount(str)
	mostCommon, leastCommon := MostAndLeast(&cc)
	return mostCommon - leastCommon
}

func Part2(pd *Polymer) int {
	cache := Cache{0: CacheStep{Pairs: map[string]int{}, Counts: map[string]int{}}}
	for i := 0; i < len(pd.Template)-1; i++ {
		pair := pd.Template[i : i+2]
		cache[0].Pairs[pair]++
	}

	for i := 0; i < len(pd.Template); i++ {
		cache[0].Counts[string(pd.Template[i])]++
	}

	steps := 40
	for i := 1; i < steps+1; i++ {
		prevCounts := cache[i-1].Counts
		cache[i] = CacheStep{Pairs: map[string]int{}, Counts: prevCounts}
		pairs := cache[i-1].Pairs
		for p, count := range pairs {
			r := pd.PairInsertionRules[p]
			cache[i].Pairs[r.Pair1] += count
			cache[i].Pairs[r.Pair2] += count
			cache[i].Counts[r.NewChar] += count
		}
	}
	c := cache[steps-1].Counts
	mostCommon, leastCommon := MostAndLeast(&c)
	return mostCommon - leastCommon
}

func main() {
	input := filepath.Join("2021", "day_14", "raw-input.txt")
	inputData := util.ParseInput(input)
	polymerData := ProcessInput(&inputData)
	p1Result := Part1(polymerData)
	fmt.Printf("Part I: most common element minus least common element = %v\n", p1Result) // 2988

	p2Result := Part2(polymerData)
	fmt.Printf("Part II: most common element minus least common element = %v\n", p2Result) // 3572761917024
}
