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
}

type Board [][]string

const (
	CHAR  = "#"
	EMPTY = "."
)

func (b *Board) String() {
	for _, row := range *b {
		for _, col := range row {
			if len(col) == 0 {
				fmt.Print(EMPTY)
			} else {
				fmt.Printf("%s", col)
			}
		}
		fmt.Printf("\n")
	}
}

func (b *Board) CountCells() int {
	count := 0
	for _, row := range *b {
		for _, col := range row {
			if col == CHAR {
				count += 1
			}
		}
	}
	return count
}

func (b *Board) CollectCoord() []util.Coord {
	coords := []util.Coord{}
	for y, row := range *b {
		for x, col := range row {
			if col == CHAR {
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

func ProcessInput(data *[]string) Origami {
	origami := Origami{Coords: []util.Coord{}, Instructions: []OrigamiInstruction{}}
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
	// setup board
	board := Board{}
	for i := 0; i < data.MaxY+1; i++ {
		board = append(board, make([]string, data.MaxX+1))
	}
	for _, coord := range data.Coords {
		x, y := coord[0], coord[1]
		board[y][x] = CHAR
	}
	// fmt.Printf("board: %v, %v maxX: %v maxY: %v count: %v\n", len(board[0]), len(board), data.MaxX, data.MaxY, board.CountCells())

	coords := data.Coords
	max := 1
	// max := len(data.Instructions)
	maxX := data.MaxX
	maxY := data.MaxY
	for i := 0; i < max; i++ {
		instruction := data.Instructions[i]
		fmt.Println("max: ", maxX, maxY)

		if instruction.dir == "y" {
			fmt.Println("Fold UP")
			// fold up
			for _, coord := range coords {
				x, y := coord[0], coord[1]
				if y > instruction.amount {
					board[maxY-y][x] = CHAR
				}
			}
			// board = board[0:instruction.amount][:]
			board = board.Copy(maxX, instruction.amount)
			maxY = maxY / 2
			// fmt.Printf("board: %v, %v maxX: %v maxY: %v count: %v\n", len(board[0]), len(board), maxX, maxY, board.CountCells())

		} else {
			fmt.Println("Fold LEFT")
			// fold left
			for _, coord := range coords {
				x, y := coord[0], coord[1]
				if x > instruction.amount {
					board[y][maxX-x] = CHAR
				}

			}
			// board = board[:][0:instruction.amount]
			board = board.Copy(instruction.amount, maxY)
			maxX = maxX / 2

			// fmt.Printf("board: %v, %v maxX: %v maxY: %v count: %v\n", len(board[0]), len(board), maxX, maxY, board.CountCells())

		}
		coords = board.CollectCoord()
	}
	// board.String()
	return board.CountCells()
}

func main() {
	input := filepath.Join("2021", "day_13", "raw-input.txt")
	inputData := util.ParseInput(input)
	origamiData := ProcessInput(&inputData)
	p1Result := Part1(&origamiData)
	fmt.Printf("Part I: count of dots visible is = %v\n", p1Result) // 852 too high, 640 too low == 706
}
