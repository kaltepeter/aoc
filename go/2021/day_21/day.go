package main

import (
	"errors"
	"fmt"
	"ka/m/util"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
)

type Player struct {
	name     string
	position int
	score    int
}

type Game struct {
	dieRollCount int
	players      []Player
}

func ProcessInput(data *[]string) Game {
	game := Game{dieRollCount: 1}
	for _, line := range *data {
		data := regexp.MustCompile(`starting position:`).Split(line, -1)
		pos, _ := strconv.Atoi(strings.Trim(data[1], " "))
		game.players = append(game.players, Player{name: strings.Trim(data[0], " "), position: pos, score: 0})
	}
	return game
}

func RollDice(rollCount int) (val int, err error) {
	err = nil
	val = 0
	if rollCount < 1 {
		err = errors.New("round must be greater than 1")
	}
	val = rollCount % 100
	if val == 0 {
		val = 100
	}
	return
}

func TakeTurn(startingPosition int, rollCount int) (endPosition int, newRollCount int) {
	endPosition = startingPosition
	movePos := 0
	newRollCount = rollCount
	for i := 0; i < 3; i++ {
		roll, _ := RollDice(newRollCount)
		movePos += roll
		newRollCount++
	}
	newVal := (movePos + endPosition) % 10
	if newVal == 0 {
		newVal = 10
	}
	endPosition = newVal
	return
}

func IsGameWon(game *Game) (isWon bool, winner Player) {
	for _, player := range game.players {
		if player.score >= 1000 {
			isWon = true
			winner = player
		}
	}
	return
}

func CalcLoserScore(game *Game) (score int) {
	for _, player := range game.players {
		if player.score < 1000 {
			score = player.score * (game.dieRollCount - 1)
		}
	}
	return
}

func Part1(game *Game) int {
	for dieRollCount := game.dieRollCount; dieRollCount < 3000; dieRollCount++ {
		for i, player := range game.players {
			newPos, newCount := TakeTurn(player.position, game.dieRollCount)
			game.players[i].position = newPos
			game.players[i].score += newPos
			dieRollCount = newCount
			game.dieRollCount = dieRollCount
			isWon, _ := IsGameWon(game)
			// fmt.Printf("player: %v score: %v pos: %v isWon: %v newPos: %v newCount: %v\n", game.players[i].name, game.players[i].score, game.players[i].position, isWon, newPos, newCount)
			if isWon {
				return CalcLoserScore(game)
			}
		}
	}
	return CalcLoserScore(game)
}

func Part2(data *Game) int {
	return 0
}

func main() {
	input := filepath.Join("2021", "day_21", "raw-input.txt")
	inputData := util.ParseInput(input)
	riskData := ProcessInput(&inputData)
	p1Result := Part1(&riskData)
	fmt.Printf("Part I: the losing player result is = %v\n", p1Result)
	if p1Result != 805932 {
		panic("FAILED on Part I")
	}

	p2Result := Part2(&riskData)
	fmt.Printf("Part II: the lowest risk path level is = %v\n", p2Result)
	if p2Result != 2874 {
		panic("FAILED on Part II")
	}
}
