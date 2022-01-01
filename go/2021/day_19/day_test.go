package main

import (
	"ka/m/util"
	"path/filepath"
	"testing"
)

func setupTests(filePath string) [][]int {
	inputExample := filepath.Join(filePath)
	inputData := util.ParseInput(inputExample)
	riskData := ProcessInput(&inputData)
	return riskData
}

func TestPartI(t *testing.T) {
	input := setupTests("example.txt")
	got := Part1(&input)
	want := 40
	if got != want {
		t.Errorf(`Part I should return %v, got %v`, want, got)
	}
}

func TestPartII(t *testing.T) {
	input := setupTests("example.txt")
	got := Part2(&input)
	want := 315
	if got != want {
		t.Errorf(`Part II should return %v, got %v`, want, got)
	}
}
