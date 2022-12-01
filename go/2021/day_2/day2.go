package main

import (
	"fmt"
	"ka/m/util"
	"log"
	"path/filepath"
	"strconv"
	s "strings"
)

type coord struct {
	direction string
	amount    int
}

func part_1(inputData []string) {
	pos := 0
	depth := 0

	for _, inst := range inputData {
		vals := s.Split(inst, " ")
		dir := vals[0]
		amt, err := strconv.ParseInt(vals[1], 0, 0)
		if err != nil {
			log.Fatal(err)
		}

		coordVal := coord{direction: dir, amount: int(amt)}

		// process
		switch coordVal.direction {
		case "up":
			depth -= coordVal.amount
		case "down":
			depth += coordVal.amount
		case "forward":
			pos += coordVal.amount
		}
	}

	fmt.Printf("Part I: The position is: %d and the depth is %d\n", pos, depth)
	fmt.Println("Part I: The value is: ", pos*depth)
}

func part_2(inputData []string) {
	pos := 0
	depth := 0
	aim := 0

	for _, inst := range inputData {
		vals := s.Split(inst, " ")
		dir := vals[0]
		amt, err := strconv.ParseInt(vals[1], 0, 0)
		if err != nil {
			log.Fatal(err)
		}

		coordVal := coord{direction: dir, amount: int(amt)}

		// process
		switch coordVal.direction {
		case "up":
			aim -= coordVal.amount
		case "down":
			aim += coordVal.amount
		case "forward":
			pos += coordVal.amount
			depth += aim * coordVal.amount
		}
	}

	fmt.Printf("Part II: The position is: %d and the depth is %d\n", pos, depth)
	fmt.Println("Part II: The value is: ", pos*depth)
}

func main() {
	input := filepath.Join("2021", "day_2", "raw-input.txt")
	inputData := util.ParseInput(input)
	inputExample := filepath.Join("2021", "day_2", "example.txt")
	inputDataExample := util.ParseInput(inputExample)
	part_1(inputData)
	part_2(inputData)
	fmt.Println("Example")
	part_2(inputDataExample)
}
