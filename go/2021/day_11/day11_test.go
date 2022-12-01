package main

import (
	"ka/m/util"
	"path/filepath"
	"reflect"
	"testing"
)

func setupTests() [10][10]int {
	inputExample := filepath.Join("example.txt")
	inputData := util.ParseInput(inputExample)
	octopusMap := ProcessInput(inputData)
	return octopusMap
}

func TestStep(t *testing.T) {
	input := setupTests()

	cases := []struct {
		row             int
		steps           int
		expected        [10]int
		flashesExpected int
	}{
		{
			row:             0,
			steps:           1,
			expected:        [10]int{6, 5, 9, 4, 2, 5, 4, 3, 3, 4},
			flashesExpected: 0,
		},
		{
			row:             0,
			steps:           2,
			expected:        [10]int{8, 8, 0, 7, 4, 7, 6, 5, 5, 5},
			flashesExpected: 35,
		},
	}

	for _, c := range cases {
		dataForRun := input
		got, gotFlashes := Step(&dataForRun)

		for i := 1; i < c.steps; i++ {
			got, gotFlashes = Step(&dataForRun)
		}

		if !reflect.DeepEqual(got[0], c.expected) {
			t.Errorf(`Step() should return %v for row %v after %v steps, got %v`, c.expected, c.row, c.steps, got[0])
		}

		if gotFlashes != c.flashesExpected {
			t.Errorf(`Step() should return %v for flashes afer %v steps, got %v`, c.flashesExpected, c.steps, gotFlashes)
		}
	}
}

func TestGetNeighbors(t *testing.T) {
	got := GetNeighbors([2]int{0, 2}, 5, 5)
	want := [][2]int{{0, 1}, {0, 3}, {1, 1}, {1, 2}, {1, 3}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`GetNeighbors() should be %v, got %v`, want, got)
	}
}

func TestExamplePartI(t *testing.T) {
	input := setupTests()
	got := Part1(input)
	want := 1656
	if got != want {
		t.Errorf(`Part I should return %d for count of octopus flashes, got %d`, want, got)
	}
}

func TestExamplePartII(t *testing.T) {
	input := setupTests()
	got := Part2(input)
	want := 195
	if got != want {
		t.Errorf(`Part II should return %d for step that all octopus flashed, got %d`, want, got)
	}
}
