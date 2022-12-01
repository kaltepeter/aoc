package util

import (
	"bufio"
	"log"
	"os"
	"regexp"
	"strconv"
)

// https://gobyexample.com/reading-files
func check(e error) {
	if e != nil {
		log.Fatal(e)
	}
}

func ParseInput(filePath string) []string {
	file, err := os.Open(filePath)
	check(err)
	defer file.Close()

	var data []string
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		data = append(data, scanner.Text())
	}

	if scanner.Err() == bufio.ErrTooLong {
		log.Fatal(scanner.Err())
	}
	return data
}

func SplitInputByEmptyLines(filePath string) [][]string {
	file, err := os.Open(filePath)
	check(err)
	defer file.Close()

	var data [][]string
	scanner := bufio.NewScanner(file)

	subGroup := []string{}

	for scanner.Scan() {
		line := scanner.Text()

		re := regexp.MustCompile(`^\s*$`)
		if re.MatchString(line) {
			data = append(data, subGroup)
			subGroup = []string{}
		} else {
			subGroup = append(subGroup, line)
		}
	}

	data = append(data, subGroup)

	if scanner.Err() == bufio.ErrTooLong {
		log.Fatal(scanner.Err())
	}

	return data
}

func ParseInputToIntegers(filePath string) []int64 {
	file, err := os.Open(filePath)
	check(err)
	defer file.Close()

	var data []int64
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		lineVal, err := strconv.ParseInt(line, 0, 64)
		check(err)
		data = append(data, lineVal)
	}

	if scanner.Err() == bufio.ErrTooLong {
		log.Fatal(scanner.Err())
	}
	return data
}
