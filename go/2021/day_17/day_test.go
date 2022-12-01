package main

import (
	"ka/m/util"
	"path/filepath"
	"reflect"
	"testing"
)

func setupTests(filePath string) []string {
	inputExample := filepath.Join(filePath)
	inputData := util.ParseInput(inputExample)
	return inputData
}

func TestProcessInput(t *testing.T) {
	input := setupTests("example.txt")
	got := ProcessInput(&input[0])
	want := TargetArea{
		MinX: 20,
		MaxX: 30,
		MinY: -10,
		MaxY: -5,
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`ProcessInput should return %v, got %v`, want, got)
	}
}

func TestStep(t *testing.T) {
	cases := []struct {
		point            util.Point
		xV               int
		yV               int
		expectedVelocity []int
		expectedPoint    util.Point
	}{
		{
			point: util.Point{
				X: 0,
				Y: 0,
			},
			xV:               7,
			yV:               2,
			expectedVelocity: []int{6, 1},
			expectedPoint: util.Point{
				X: 7,
				Y: 2,
			},
		},
		{
			point: util.Point{
				X: 0,
				Y: 0,
			},
			xV:               6,
			yV:               3,
			expectedVelocity: []int{5, 2},
			expectedPoint: util.Point{
				X: 6,
				Y: 3,
			},
		},
	}

	for _, c := range cases {
		newPoint := &c.point
		wantNewPoint := c.expectedPoint
		got1, got2 := Step(newPoint, c.xV, c.yV)
		want := c.expectedVelocity
		if !reflect.DeepEqual(*newPoint, c.expectedPoint) {
			t.Errorf(`Step failed. Expected %v, got %v`, wantNewPoint, c.point)
		}
		if got1 != want[0] || got2 != want[1] {
			t.Errorf(`Step failed. Expected %v,%v, got %v,%v`, want[0], want[1], got1, got2)
		}
	}
}

func TestPartI(t *testing.T) {
	input := setupTests("example.txt")
	data := ProcessInput(&input[0])
	got := Part1(&data)
	want := 45
	if got != want {
		t.Errorf(`Part I should return %v for highest y, got %v`, want, got)
	}
}

func TestPartII(t *testing.T) {
	input := setupTests("example.txt")
	data := ProcessInput(&input[0])
	got := Part2(&data)
	want := 112
	if got != want {
		t.Errorf(`Part II should return %v for the total possible velocities, got %v`, want, got)
	}
}
