package main

import (
	"ka/m/util"
	"path/filepath"
	"testing"
)

func setupTests(filePath string) *Origami {
	inputExample := filepath.Join(filePath)
	inputData := util.ParseInput(inputExample)
	origamiData := ProcessInput(&inputData, '#', '.')
	return &origamiData
}

func TestPartI(t *testing.T) {
	input := setupTests("example.txt")
	got := Part1(input)
	want := 17
	if got != want {
		t.Errorf(`Part I should return %v for count of visible dots, got %v`, want, got)
	}
}

// #.##..#..#.
// #...#......
// ......#...#
// #...#......
// .#.#..#.###
// ...........
// ...........
