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

func TestPart2(t *testing.T) {
	input := setupTests("example.txt")
	got := Part2(input)
	want := 2188189693529
	if got != want {
		t.Errorf(`Part II should return %v for result of most common minus least common elements, got %v`, want, got)
	}
}

func TestMakeCharCount(t *testing.T) {
	got := MakeCharCount("NCNBCHB")
	want := CharCount{"N": 2, "C": 2, "B": 2, "H": 1}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`MakeCharCount should return %v, got %v`, want, got)
	}
}

func TestMostAndLeast(t *testing.T) {
	charCount := CharCount{"B": 1749, "C": 298, "H": 161, "N": 865}
	gotMost, gotLeast := MostAndLeast(&charCount)
	wantMost := 1749
	wantLeast := 161
	if gotMost != wantMost {
		t.Errorf(`TestMostAndLeast should return %v for most, got %v`, wantMost, gotMost)
	}
	if gotLeast != wantLeast {
		t.Errorf(`TestMostAndLeast should return %v for least, got %v`, wantLeast, gotLeast)
	}
}
