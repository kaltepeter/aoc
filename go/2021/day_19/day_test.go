package main

import (
	"ka/m/util"
	"path/filepath"
	"testing"
)

func setupTests(filePath string) []Scanner {
	inputExample := filepath.Join(filePath)
	inputData := util.ParseInput(inputExample)
	scannerData := ProcessInput(&inputData)
	return scannerData
}

func TestProcessInput(t *testing.T) {
	input := setupTests("example.txt")
	got := len(input)
	want := 4
	if got != want {
		t.Errorf(`ProcessInput should return %v items, got: %v`, want, got)
	}

	gotBeaconCount := len(input[0].Beacons)
	wantBeaconCount := 25
	if gotBeaconCount != wantBeaconCount {
		t.Errorf(`ProcessInput should return %v beacons for scanner 0, got: %v`, wantBeaconCount, gotBeaconCount)
	}
}

func TestPartI(t *testing.T) {
	input := setupTests("example.txt")
	got := Part1(&input)
	want := 79
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
