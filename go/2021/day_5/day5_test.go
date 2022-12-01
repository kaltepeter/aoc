package main

import (
	"ka/m/util"
	"path/filepath"
	"reflect"
	"testing"
)

func setupTests() lineInstructions {
	inputExample := filepath.Join("example.txt")
	inputData := util.ParseInput(inputExample)
	return ProcessData(inputData)
}

func TestCalcRangeForHorizontal(t *testing.T) {
	input := []coord{{x: 0, y: 9}, {x: 5, y: 9}}
	got := CalcRange(input[0], input[1], DIR_H)
	want := []coord{{x: 0, y: 9}, {x: 1, y: 9}, {x: 2, y: 9}, {x: 3, y: 9}, {x: 4, y: 9}, {x: 5, y: 9}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`CalcRange(%v, %v) should return coords %v, got %v`, input[0], input[1], want, got)
	}
}

func TestCalcRangeForVertical(t *testing.T) {
	input := []coord{{x: 7, y: 0}, {x: 7, y: 4}}
	got := CalcRange(input[0], input[1], DIR_V)
	want := []coord{{x: 7, y: 0}, {x: 7, y: 1}, {x: 7, y: 2}, {x: 7, y: 3}, {x: 7, y: 4}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`CalcRange(%v, %v) should return coords %v, got %v`, input[0], input[1], want, got)
	}
}

func TestCalcRangeForDiagonal(t *testing.T) {
	cases := []struct {
		arg1     coord
		arg2     coord
		expected []coord
	}{
		{
			arg1:     coord{x: 1, y: 1},
			arg2:     coord{x: 3, y: 3},
			expected: []coord{{x: 1, y: 1}, {x: 2, y: 2}, {x: 3, y: 3}},
		},
		{
			arg1:     coord{x: 9, y: 7},
			arg2:     coord{x: 7, y: 9},
			expected: []coord{{x: 7, y: 9}, {x: 8, y: 8}, {x: 9, y: 7}},
		},
	}

	for _, c := range cases {
		got := CalcRange(c.arg1, c.arg2, DIR_D)

		if !reflect.DeepEqual(got, c.expected) {
			t.Errorf(`CalcRange(%v, %v) should return coords %v, got %v`, c.arg1, c.arg2, c.expected, got)
		}
	}

}

func TestExamplePartI(t *testing.T) {
	input := setupTests()
	got := Part1(input)
	want := 5
	if got != want {
		t.Errorf(`Part I should return %d for dangerous points, got %d`, want, got)
	}
}

func TestExamplePartII(t *testing.T) {
	input := setupTests()
	got := Part2(input)
	want := 12
	if got != want {
		t.Errorf(`Part II should return %d for dangerous points, got %d`, want, got)
	}
}
