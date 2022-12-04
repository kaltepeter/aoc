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

type Result struct {
	turns  []int
	s1, s2 int
}

/*                      (0, 1, 2) 3 4 5 6 7 8 9 */
var multiplier = []int64{0, 0, 0, 1, 3, 6, 7, 6, 3, 1}

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

func IsGameWon(game *Game, targetScore int) (isWon bool, winner Player) {
	for _, player := range game.players {
		if player.score >= targetScore {
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

func scores(p1, p2 int, turns []int) (s1 int, s2 int) {
	var score = []int{10, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	for i := range turns {
		switch i % 2 {
		case 0: //p1
			p1 = (p1 + turns[i]) % 10
			s1 += score[p1]
		case 1: //p2
			p2 = (p2 + turns[i]) % 10
			s2 += score[p2]
		}
	}
	return s1, s2
}

func genGames(p1, p2 int) chan Result {
	c := make(chan Result)

	var gen func(in []int)
	gen = func(in []int) {
		for i := 3; i <= 9; i++ {
			next := make([]int, len(in)+1)
			copy(next, in)
			next[len(in)] = i
			s1, s2 := scores(p1, p2, next)
			if s1 >= 21 || s2 >= 21 {
				c <- Result{next, s1, s2}
			} else {
				gen(next)
			}
		}
		if in == nil {
			close(c)
		}
	}
	go gen(nil)
	return c
}

func Part1(game Game) int {
	for dieRollCount := game.dieRollCount; dieRollCount < 3000; dieRollCount++ {
		for i, player := range game.players {
			newPos, newCount := TakeTurn(player.position, game.dieRollCount)
			game.players[i].position = newPos
			game.players[i].score += newPos
			dieRollCount = newCount
			game.dieRollCount = dieRollCount
			isWon, _ := IsGameWon(&game, 1000)
			// fmt.Printf("player: %v score: %v pos: %v isWon: %v newPos: %v newCount: %v\n", game.players[i].name, game.players[i].score, game.players[i].position, isWon, newPos, newCount)
			if isWon {
				return CalcLoserScore(&game)
			}
		}
	}
	return CalcLoserScore(&game)
}

func countGames(turns []int) int64 {
	var out int64 = 1
	for _, i := range turns {
		out *= multiplier[i]
	}
	return out
}

func Part2(game Game) int64 {
	// My approach wouldn't work for part II, followed https://www.youtube.com/watch?v=omj84PgE-Mc for the solution
	wins := []int64{0, 0}
	fmt.Println("Play for p1: ", game.players[0].position, " p2: ", game.players[1].position)
	games := genGames(game.players[0].position, game.players[1].position)
	last := 0
	winnerCount := int64(0)

	for {
		result, ok := <-games
		if !ok {
			break
		}
		if result.s1 > result.s2 {
			wins[0] += countGames(result.turns)
		} else {
			wins[1] += countGames(result.turns)
		}
		if last != result.turns[0] {
			last = result.turns[0]
			// fmt.Print(">", result)
		}

		if wins[0] > wins[1] {
			// fmt.Println(wins[0], "( >", wins[1], ")")
			winnerCount = wins[0]
		} else {
			// fmt.Println(wins[1], "( >", wins[0], ")")
			winnerCount = wins[1]
		}
	}
	return winnerCount
}

func main() {
	input := filepath.Join("2021", "day_21", "raw-input.txt")
	inputData := util.ParseInput(input)
	game := ProcessInput(&inputData)
	fmt.Println(game)

	p1Result := Part1(game)
	fmt.Printf("Part I: the losing player result is = %v\n", p1Result)
	if p1Result != 805932 {
		panic("FAILED on Part I")
	}

	exampleInput := filepath.Join("2021", "day_21", "example.txt")
	exampleInputData := util.ParseInput(exampleInput)
	exampleData := ProcessInput(&exampleInputData)

	p2ExampleResult := Part2(exampleData)
	fmt.Printf("Part II example: the winning player wins in %v universes\n", p2ExampleResult)
	if p2ExampleResult != int64(444356092776315) {
		panic("FAILED on Part II")
	}

	game = ProcessInput(&inputData)
	fmt.Println(game)

	p2Result := Part2(game)
	fmt.Printf("Part II: the winning player wins in %v universes\n", p2Result)
	if p2Result != int64(133029050096658) {
		panic("FAILED on Part II")
	}
}
