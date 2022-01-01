package main

import (
	"ka/m/util"
	"path/filepath"
	"testing"
)

func setupTests(filePath string) []string {
	inputExample := filepath.Join(filePath)
	inputData := util.ParseInput(inputExample)
	// mathHomework := ProcessInput(&inputData)
	return inputData
}

// func TestProcessInput(t *testing.T) {
// 	input := setupTests("example.txt")
// 	got := input.Left.
// 	want := 10
// 	if got != want {
// 		t.Errorf(`ProcessInput should return %v, got %v`, want, got)
// 	}
// }

func TestAdd(t *testing.T) {
	a := NewPair("[1,2]")
	b := NewPair("[[3,4],5]")
	got := Add(a, b)
	if got.Depth != 0 {
		t.Errorf(`Failed to add pairs. Expected %v, got %v`, 0, got)
	}
	switch gL := got.Left.(type) {
	case *Pair:
		if gL.Depth != 1 {
			t.Errorf(`Failed to add pairs. Expected %v, got %v`, 1, gL.Depth)
		}
	}
	switch gR := got.Right.(type) {
	case *Pair:
		if gR.Depth != 1 {
			t.Errorf(`Failed to add pairs. Expected %v, got %v`, 1, gR.Depth)
		}
	}
}

func TestCalcMagnitude(t *testing.T) {
	p1 := NewPair("[9,1]")
	p2 := NewPair("[1,9]")
	p := Add(p1, p2)
	got := p.CalcMagnitude()
	want := 129
	if got != want {
		t.Errorf(`CalcMagnitude should return %v, got %v`, want, got)
	}
}

func TestPartI(t *testing.T) {
	input := setupTests("example.txt")
	got := Part1(input)
	want := 4140
	if got != want {
		t.Errorf(`Part I should return %v, got %v`, want, got)
	}
}

func TestPartII(t *testing.T) {
	input := setupTests("example.txt")
	got := Part2(input)
	want := 3993
	if got != want {
		t.Errorf(`Part II should return %v, got %v`, want, got)
	}
}
