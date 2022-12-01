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

func TestComputeAutoCompleteScore(t *testing.T) {
	got := ComputeAutoCompleteScore("])}>")
	want := 294
	if got != want {
		t.Errorf(`ComputeAutoCompleteScore should return %d for score, got %d`, want, got)
	}
}

func TestGetWinningScore(t *testing.T) {
	got := GetWinningScore([]int{288957, 5566, 1480781, 995444, 294})
	want := 288957
	if got != want {
		t.Errorf(`ComputeAutoCompleteScore should return %d for score, got %d`, want, got)
	}
}

func TestExamplePartI(t *testing.T) {
	input := setupTests()
	got := Part1(input)
	want := 26397
	if got != want {
		t.Errorf(`Part I should return %d for score, got %d`, want, got)
	}
}

func TestExamplePartII(t *testing.T) {
	input := setupTests()
	got := Part2(input)
	want := 288957
	if got != want {
		t.Errorf(`Part II should return %d for score, got %d`, want, got)
	}
}
