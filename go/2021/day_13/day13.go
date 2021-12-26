package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
)

type OrigamiInstruction struct {
	dir    string
	amount int
}

type Origami struct {
	Coords       []util.Coord
	Instructions []OrigamiInstruction
	MaxX         int
	MaxY         int
	Char         rune
	EmptyChar    rune
}

type Board [][]string

func (data *Origami) NewBoard() *Board {
	// setup board
	board := Board{}
	for i := 0; i < data.MaxY+1; i++ {
		board = append(board, make([]string, data.MaxX+1))
	}
	for _, coord := range data.Coords {
		x, y := coord[0], coord[1]
		board[y][x] = string(data.Char)
	}
	return &board
}

func (b *Board) String(emptyChar rune) {
	for _, row := range *b {
		for _, col := range row {
			if len(col) == 0 {
				fmt.Print(string(emptyChar))
			} else {
				fmt.Printf("%s", col)
			}
		}
		fmt.Printf("\n")
	}
}

func (b *Board) CountCells(char rune) int {
	count := 0
	for _, row := range *b {
		for _, col := range row {
			if col == string(char) {
				count += 1
			}
		}
	}
	return count
}

func (b *Board) CollectCoord(char rune) []util.Coord {
	coords := []util.Coord{}
	for y, row := range *b {
		for x, col := range row {
			if col == string(char) {
				coords = append(coords, util.Coord{x, y})
			}
		}
	}
	return coords
}

func (b *Board) Copy(maxX int, maxY int) Board {
	board := Board{}
	oldBoard := *b
	for i := 0; i < maxY+1; i++ {
		curRow := make([]string, maxX+1)
		oldRow := oldBoard[i][:maxX+1]
		copy(curRow, oldRow)
		board = append(board, curRow)
	}

	return board
}

func ProcessInput(data *[]string, char rune, emptyChar rune) Origami {
	origami := Origami{Coords: []util.Coord{}, Instructions: []OrigamiInstruction{}, Char: char, EmptyChar: emptyChar}
	isCoordRegex := regexp.MustCompile(`^\d`)
	isInstructionRegex := regexp.MustCompile(`^fold along`)
	maxX := 0
	maxY := 0
	for _, line := range *data {
		if isCoordRegex.MatchString(line) {
			coord := util.StringToListOfIntWithSeparator(line, ",")
			origami.Coords = append(origami.Coords, util.Coord{coord[0], coord[1]})
		} else if isInstructionRegex.MatchString(line) {
			l := strings.Trim(strings.Replace(line, "fold along ", "", 1), " \n")
			info := strings.Split(l, "=")
			amt, _ := strconv.Atoi(info[1])
			if maxX == 0 && info[0] == "x" {
				maxX = 2 * amt
			}
			if maxY == 0 && info[0] == "y" {
				maxY = 2 * amt
			}
			origami.Instructions = append(origami.Instructions, OrigamiInstruction{dir: info[0], amount: amt})
		}
	}
	origami.MaxX = maxX
	origami.MaxY = maxY
	return origami
}

func Part1(data *Origami) int {
	board := *data.NewBoard()
	coords := data.Coords
	max := 1
	maxX := data.MaxX
	maxY := data.MaxY
	for i := 0; i < max; i++ {
		instruction := data.Instructions[i]

		if instruction.dir == "y" {
			// fold up
			for _, coord := range coords {
				x, y := coord[0], coord[1]
				if y > instruction.amount {
					board[(2*instruction.amount)-y][x] = string(data.Char)
				}
			}
			board = board.Copy(maxX, instruction.amount)
			maxY = maxY / 2
		} else {
			// fold left
			for _, coord := range coords {
				x, y := coord[0], coord[1]
				if x > instruction.amount {
					board[y][(2*instruction.amount)-x] = string(data.Char)
				}

			}
			board = board.Copy(instruction.amount, maxY)
			maxX = maxX / 2
		}
		coords = board.CollectCoord(data.Char)
	}
	// board.String(data.EmptyChar)
	return board.CountCells(data.Char)
}

func Part2(data *Origami) {
	board := *data.NewBoard()
	coords := data.Coords
	max := len(data.Instructions)
	maxX := data.MaxX
	maxY := data.MaxY
	for i := 0; i < max; i++ {
		instruction := data.Instructions[i]

		if instruction.dir == "y" {
			// fold up
			for _, coord := range coords {
				x, y := coord[0], coord[1]
				if y > instruction.amount {
					board[(2*instruction.amount)-y][x] = string(data.Char)
				}
			}
			board = board.Copy(maxX, instruction.amount)
			maxY = maxY / 2
		} else {
			// fold left
			for _, coord := range coords {
				x, y := coord[0], coord[1]
				if x > instruction.amount {
					board[y][(2*instruction.amount)-x] = string(data.Char)
				}

			}
			board = board.Copy(instruction.amount, maxY)
			maxX = maxX / 2
		}
		coords = board.CollectCoord(data.Char)
	}
	board.String(data.EmptyChar)
}

func main() {
	input := filepath.Join("2021", "day_13", "raw-input.txt")
	inputData := util.ParseInput(input)
	origamiData := ProcessInput(&inputData, '#', '.')
	p1Result := Part1(&origamiData)
	fmt.Printf("Part I: count of dots visible is = %v\n", p1Result) // 852 too high, 640 too low == 706

	fmt.Println("Part II: eight digit code is: ")
	origamiData.Char = '█'
	origamiData.EmptyChar = ' '
	Part2(&origamiData) // LRFJBJEH
}
