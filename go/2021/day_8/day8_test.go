package main

import (
	"ka/m/util"
	"path/filepath"
	"testing"
)

func setupTests() []string {
	inputExample := filepath.Join("example.txt")
	inputData := util.ParseInput(inputExample)
	return inputData
}

func TestProcessInput(t *testing.T) {
	input := setupTests()
	got := ProcessInput(input)
	want := 10
	if len(got) != want {
		t.Errorf(`ProcessInput should return %v for count of puzzle inputs, got %v`, want, got)
	}
}

func TestExamplePartI(t *testing.T) {
	input := setupTests()
	listOfDigits := ProcessInput(input)
	got := Part1(listOfDigits)
	want := 26
	if got != want {
		t.Errorf(`Part I should return %d for counts, got %d`, want, got)
	}
}

func TestExamplePartII(t *testing.T) {
	input := setupTests()
	listOfDigits := ProcessInput(input)
	got := Part2(listOfDigits)
	want := 61229
	if got != want {
		t.Errorf(`Part II should return %d for total of all digits, got %d`, want, got)
	}
}
