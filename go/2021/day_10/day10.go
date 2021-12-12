package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"sort"
	"strings"
)

const (
	OPEN_SQUARE_BRACKET  = '['
	OPEN_PAREN           = '('
	OPEN_GATOR           = '<'
	OPEN_BRACE           = '{'
	CLOSE_SQUARE_BRACKET = ']'
	CLOSE_PAREN          = ')'
	CLOSE_GATOR          = '>'
	CLOSE_BRACE          = '}'
)

var CORRUPT_POINTS map[rune]int = map[rune]int{
	CLOSE_SQUARE_BRACKET: 57,
	CLOSE_PAREN:          3,
	CLOSE_GATOR:          25137,
	CLOSE_BRACE:          1197,
}

var AUTOCOMPLETE_POINTS map[rune]int = map[rune]int{
	CLOSE_SQUARE_BRACKET: 2,
	CLOSE_PAREN:          1,
	CLOSE_GATOR:          4,
	CLOSE_BRACE:          3,
}

func ComputeAutoCompleteScore(s string) int {
	total := 0
	for _, char := range s {
		total = (total * 5) + AUTOCOMPLETE_POINTS[char]
	}
	return total
}

func GetWinningScore(scores []int) int {
	sort.Ints(scores)
	mid := len(scores) / 2
	score := scores[mid:][0]
	return score
}

func MatchCloseTag(openTag rune, closeTag rune) bool {
	switch openTag {
	case OPEN_SQUARE_BRACKET:
		return closeTag == CLOSE_SQUARE_BRACKET
	case OPEN_PAREN:
		return closeTag == CLOSE_PAREN
	case OPEN_GATOR:
		return closeTag == CLOSE_GATOR
	case OPEN_BRACE:
		return closeTag == CLOSE_BRACE
	}
	return false
}

func GetMatchCloseTag(openTag rune) rune {
	switch openTag {
	case OPEN_SQUARE_BRACKET:
		return CLOSE_SQUARE_BRACKET
	case OPEN_PAREN:
		return CLOSE_PAREN
	case OPEN_GATOR:
		return CLOSE_GATOR
	case OPEN_BRACE:
		return CLOSE_BRACE
	}
	return ' '
}

func GetMatchOpenTag(closeTag rune) rune {
	switch closeTag {
	case CLOSE_SQUARE_BRACKET:
		return OPEN_SQUARE_BRACKET
	case CLOSE_PAREN:
		return OPEN_PAREN
	case CLOSE_GATOR:
		return OPEN_GATOR
	case CLOSE_BRACE:
		return OPEN_BRACE
	}
	return ' '
}

func IsOpenTag(s rune) bool {
	return s == OPEN_SQUARE_BRACKET || s == OPEN_PAREN || s == OPEN_GATOR || s == OPEN_BRACE
}

func IsCloseTag(s rune) bool {
	return s == CLOSE_SQUARE_BRACKET || s == CLOSE_PAREN || s == CLOSE_GATOR || s == CLOSE_BRACE
}

func Part1(data []string) int {
	points := 0
	for _, line := range data {
		openTags := []rune{}
		corruptTags := []rune{}
		for _, char := range strings.Trim(line, " \n") {
			if IsOpenTag(char) {
				openTags = append(openTags, char)
			}
			if IsCloseTag(char) {
				if !MatchCloseTag(openTags[len(openTags)-1:][0], char) {
					corruptTags = append(corruptTags, char)
					break
				} else {
					openTags = openTags[:len(openTags)-1]
				}
			}
		}
		for _, char := range corruptTags {
			points += CORRUPT_POINTS[char]
		}

	}
	return points
}

func GetIncompleteLines(data []string) []string {
	corruptedLines := []string{}
	for _, line := range data {
		openTags := []rune{}
		for _, char := range strings.Trim(line, " \n") {
			if IsOpenTag(char) {
				openTags = append(openTags, char)
			}
			if IsCloseTag(char) {
				if !MatchCloseTag(openTags[len(openTags)-1:][0], char) {
					corruptedLines = append(corruptedLines, line)
					break
				} else {
					openTags = openTags[:len(openTags)-1]
				}
			}
		}
	}
	return util.DiffArrays(data, corruptedLines)
}

func Part2(data []string) int {
	points := 0
	incompleteLines := GetIncompleteLines(data)
	linePoints := []int{}
	for _, line := range incompleteLines {
		openTags := []rune{}
		closeTags := []rune{}
		for _, char := range strings.Trim(line, " \n") {
			if IsOpenTag(char) {
				openTags = append(openTags, char)
			}
			if IsCloseTag(char) {
				if !MatchCloseTag(openTags[len(openTags)-1:][0], char) {
					closeTags = append(closeTags, GetMatchOpenTag(char))
					break
				} else {
					openTags = openTags[:len(openTags)-1]
				}
			}
		}

		for i := len(openTags) - 1; i >= 0; i-- {
			closeTags = append(closeTags, GetMatchCloseTag(openTags[i]))
		}

		completeStr := ""
		for _, ct := range closeTags {
			// fmt.Printf("%v", string(ct))
			completeStr += string(ct)
		}
		linePoints = append(linePoints, ComputeAutoCompleteScore(completeStr))
	}

	points += GetWinningScore(linePoints)

	return points
}

func main() {
	input := filepath.Join("2021", "day_10", "raw-input.txt")
	inputData := util.ParseInput(input)
	p1Result := Part1(inputData)
	fmt.Printf("Part I: Score is = %v\n", p1Result) // 392043

	p2Result := Part2(inputData)
	fmt.Printf("Part II: Score is = %v\n", p2Result) // 1605968119
}
