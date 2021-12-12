package util

import "testing"

func TestReduceInt(t *testing.T) {
	arr1 := []int{1, 2, 3, 4, 5, 6}
	got := ReduceInt(arr1, Add, 0)
	want := 21
	if got != want {
		t.Errorf(`ReduceInt should return %v, got %v`, want, got)
	}
}

func TestReduceIntWithMultiply(t *testing.T) {
	arr1 := []int{9, 14, 9}
	got := ReduceInt(arr1, Multiply, 1)
	want := 1134
	if got != want {
		t.Errorf(`ReduceInt should return %v, got %v`, want, got)
	}
}

func TestReduceIntWithStart(t *testing.T) {
	arr1 := []int{1, 2, 3, 4, 5, 6}
	got := ReduceInt(arr1, Add, 5)
	want := 26
	if got != want {
		t.Errorf(`ReduceInt should return %v, got %v`, want, got)
	}
}
