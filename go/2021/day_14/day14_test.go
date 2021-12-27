package main

import (
	"ka/m/util"
	"path/filepath"
	"reflect"
	"testing"
)

func setupTests(filePath string) *Polymer {
	inputExample := filepath.Join(filePath)
	inputData := util.ParseInput(inputExample)
	polymerData := ProcessInput(&inputData)
	return polymerData
}

func TestPartI(t *testing.T) {
	input := setupTests("example.txt")
	got := Part1(input)
	want := 1588
	if got != want {
		t.Errorf(`Part I should return %v for result of most common minus least common elements, got %v`, want, got)
	}
}

func TestCharCounts(t *testing.T) {
	got := CountChars("NBBBCNCCNBBNBNBBCHBHHBCHB")
	want := CharCounts{total: 25, mostCommon: CountMap{"B", 11}, leastCommon: CountMap{"H", 4}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`CountChars should return CharCounts %v, got %v`, want, got)
	}
}
