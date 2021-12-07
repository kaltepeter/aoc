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
	got := Part1(input, 80)
	want := 5934
	if got != want {
		t.Errorf(`Part I should return %d for number of fish, got %d`, want, got)
	}
}

func TestExamplePartII(t *testing.T) {
	input := setupTests()
	got := Part1(input, 256)
	want := 26984457539
	if got != want {
		t.Errorf(`Part I should return %d for number of fish, got %d`, want, got)
	}
}
