package main

import (
	"reflect"
	"testing"
)

func TestGetAllRotations(t *testing.T) {
	coord := &Coord{1, 2, -3}
	got := coord.GetAllRotations()
	want := 24
	if len(got) != want {
		t.Errorf(`GetAllRotations should return %v, got %v`, want, len(got))
	}
}

func TestRotateCoord(t *testing.T) {
	cases := []struct {
		coord  *Coord
		rotate [3]int
		want   *Coord
	}{
		{
			coord:  &Coord{1, 1, 1},
			rotate: [3]int{-1, 0, 0},
			want:   &Coord{0, 1, 1},
		},
		{
			coord:  &Coord{-1, 1, 1},
			rotate: [3]int{-1, 0, 0},
			want:   &Coord{-2, 1, 1},
		},
		{
			coord:  &Coord{1, 5, 1},
			rotate: [3]int{-1, 1, 0},
			want:   &Coord{0, 6, 1},
		},
	}
	for _, c := range cases {
		got := c.coord.RotateCoord(c.rotate[0], c.rotate[1], c.rotate[2])
		want := c.want
		if !reflect.DeepEqual(got, want) {
			t.Errorf(`RotateCoord should return %v, got: %v`, want, got)
		}
	}
}
