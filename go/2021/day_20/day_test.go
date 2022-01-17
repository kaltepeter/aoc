package main

import (
	"ka/m/util"
	"path/filepath"
	"testing"
)

func setupTests(filePath string) [][]string {
	inputExample := filepath.Join(filePath)
	inputData := util.SplitInputByEmptyLines(inputExample)
	imageData := ProcessInput(&inputData)
	return imageData
}

func TestPartI(t *testing.T) {
	input := setupTests("example.txt")
	got := Part1(&input)
	want := 35
	if got != want {
		t.Errorf(`Part I should return %v, got %v`, want, got)
	}
}

func SkipTestPartII(t *testing.T) {
	input := setupTests("example.txt")
	got := Part2(&input)
	want := 315
	if got != want {
		t.Errorf(`Part II should return %v, got %v`, want, got)
	}
}
