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
		t.Errorf(`Part I should return %v for least risk, got %v`, want, got)
	}
}
