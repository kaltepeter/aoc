package main

import (
	"ka/m/util"
	"path/filepath"
	"testing"
)

func setupTests(filePath string) *CaveGraph {
	inputExample := filepath.Join(filePath)
	inputData := util.ParseInput(inputExample)
	caveMap := ProcessInput(inputData)
	return caveMap
}

type caveTraverseTestCase struct {
	inputFile string
	expected  int
}

func TestExamplePartI(t *testing.T) {
	cases := []caveTraverseTestCase{
		{
			inputFile: "example.txt",
			expected:  10,
		},
		{
			inputFile: "example2.txt",
			expected:  19,
		},
		{
			inputFile: "example3.txt",
			expected:  226,
		},
	}
	for _, c := range cases {
		input := setupTests(c.inputFile)
		got := Part1(input)
		want := c.expected
		if got != want {
			t.Errorf(`Part I should return %d for count of cave paths, got %d`, want, got)
		}
	}
}

func TestExamplePartII(t *testing.T) {
	cases := []caveTraverseTestCase{
		{
			inputFile: "example.txt",
			expected:  36,
		},
		{
			inputFile: "example2.txt",
			expected:  103,
		},
		{
			inputFile: "example3.txt",
			expected:  3509,
		},
	}
	for _, c := range cases {
		input := setupTests(c.inputFile)
		got := Part2(input)
		want := c.expected
		if got != want {
			t.Errorf(`Part II should return %d for count of cave paths, got %d`, want, got)
		}
	}
}
