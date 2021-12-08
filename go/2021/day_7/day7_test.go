package main

import (
	"ka/m/util"
	"path/filepath"
	"testing"
)

func setupTests() []int {
	inputExample := filepath.Join("example.txt")
	inputData := util.ParseInput(inputExample)
	return util.StringToListOfInt(inputData[0])
}

func TestExamplePartI(t *testing.T) {
	input := setupTests()
	got := Part1(input)
	want := 37
	if got != want {
		t.Errorf(`Part I should return %d for number of fuel, got %d`, want, got)
	}
}

func TestExamplePartII(t *testing.T) {
	input := setupTests()
	got := Part2(input)
	want := 168
	if got != want {
		t.Errorf(`Part II should return %d for number of fuel, got %d`, want, got)
	}
}
