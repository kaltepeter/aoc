package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"strconv"
)

type card [][]string

type bingogames struct {
	numbers []string
	cards   []card
}

const MARKER = "X"

func GetGameData(data []string) bingogames {
	cards := []card{}
	nums := util.StringToListOfString(data[0])
	var cardData card = card{}
	cardInput := data[2:]
	for idx, line := range cardInput {
		if len(line) == 0 {
			cards = append(cards, cardData)
			cardData = card{}
		} else {
			chars := util.StringToListOfStringWithSeparator(line, " +")
			cardData = append(cardData, chars)
		}
		// capture last line
		if idx >= len(cardInput)-1 {
			cards = append(cards, cardData)
			cardData = card{}
		}
	}
	bingoGame := bingogames{
		numbers: nums,
		cards:   cards,
	}
	return bingoGame
}

func MarkBoards(gameData *bingogames, num string) {
	for _, board := range gameData.cards {
		for _, row := range board {
			for cellIdx, cell := range row {
				if cell == num {
					row[cellIdx] = MARKER
				}
			}
		}
	}
}

func CheckBoard(board card) bool {
	found := false
	rowMax := len(board[0])
	colMax := len(board)
	colMap := map[int]int{}
	for _, row := range board {
		var rowCount int = 0
		for idx, cell := range row {
			if cell == MARKER {
				colMap[idx] += 1
				rowCount += 1
			}
		}
		if rowCount >= rowMax {
			rowCount = 0
			found = true
			break
		}
	}
	for _, v := range colMap {
		if v >= colMax {
			found = true
			break
		}
	}
	return found
}

func CheckForWinners(cards []card) int {
	for boardIdx, board := range cards {
		isWon := CheckBoard(board)
		if isWon {
			return boardIdx
		}
	}
	return -1
}

func CollectAllWinners(cards []card, prevWinners []int) []int {
	winners := prevWinners
	for boardIdx, board := range cards {
		var found bool = false
		for _, w := range winners {
			if boardIdx == w {
				found = true
				break
			}
		}
		if !found {
			isWon := CheckBoard(board)
			if isWon {
				winners = append(winners, boardIdx)
			}
		}
	}
	return winners
}

func HandleWinner(board card, num string) int {
	var total int
	for _, row := range board {
		for _, cell := range row {
			v, _ := strconv.ParseInt(cell, 10, 0)
			total += int(v)
		}
	}
	calledNum, _ := strconv.ParseInt(num, 10, 0)
	return total * int(calledNum)
}

func Part1(gameData bingogames) int {
	for _, num := range gameData.numbers[0:] {
		MarkBoards(&gameData, num)
		winningBoard := CheckForWinners(gameData.cards)
		if winningBoard > 0 {
			fmt.Printf("Found a winner. Board index %d\n", winningBoard)
			return HandleWinner(gameData.cards[winningBoard], num)
		}
	}
	return -1
}

func Part2(gameData bingogames) int {
	lastWinner := -1
	lastCalledWinner := ""
	winners := []int{}
	winnersCache := map[string]int{}

	for _, num := range gameData.numbers[0:] {
		MarkBoards(&gameData, num)
		prevNum := len(winners)
		winners = CollectAllWinners(gameData.cards, winners)

		if len(winners) > prevNum {
			lastWinner = winners[len(winners)-1]
			lastCalledWinner = num
			res := HandleWinner(gameData.cards[lastWinner], num)
			winnersCache[lastCalledWinner] = res
		}
	}
	fmt.Printf("Last winner is %d. Called with %v\n", lastWinner, lastCalledWinner)
	return winnersCache[lastCalledWinner]
}

func main() {
	input := filepath.Join("2021", "day_4", "raw-input.txt")
	inputData := util.ParseInput(input)
	bingoGames := GetGameData(inputData)
	p1Result := Part1(bingoGames)
	fmt.Printf("Part I: Winning number is %d\n", p1Result)

	p2Result := Part2(bingoGames)
	fmt.Printf("Part II: Winning number is %d\n", p2Result)
}
