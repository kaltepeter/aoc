package main

import (
	"ka/m/util"
	"path/filepath"
	"reflect"
	"testing"
)

func setupTests() [][]int {
	inputExample := filepath.Join("example.txt")
	inputData := util.ParseInput(inputExample)
	return ProcessInput(inputData)
}

func TestExampleGetLowPoints(t *testing.T) {
	input := setupTests()
	got := GetLowPoints(input)
	want := [][2]int{{0, 1}, {0, 9}, {2, 2}, {4, 6}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`GetLowPoints should return %v for risk, got %v`, want, got)
	}
}

func TestExamplePartI(t *testing.T) {
	input := setupTests()
	got := Part1(input)
	want := 15
	if got != want {
		t.Errorf(`Part I should return %d for risk, got %d`, want, got)
	}
}

func TestExamplePartII(t *testing.T) {
	input := setupTests()
	got := Part2(input)
	want := 1134
	if got != want {
		t.Errorf(`Part II should return %d for risk, got %d`, want, got)
	}
}
