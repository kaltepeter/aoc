package util

import (
	"reflect"
	"testing"
)

func TestDiffArrays(t *testing.T) {
	cases := []struct {
		arg1     []string
		arg2     []string
		expected []string
	}{
		{
			arg1:     []string{"c", "e", "f", "a", "b", "d"},
			arg2:     []string{"e", "f", "a", "b"},
			expected: []string{"c", "d"},
		},
		{

			arg1:     []string{"a", "b"},
			arg2:     []string{"e", "a", "f", "b"},
			expected: []string{"e", "f"},
		},
	}

	for _, c := range cases {
		got := DiffArrays(c.arg1, c.arg2)

		if !reflect.DeepEqual(got, c.expected) {
			t.Errorf("Expected DiffArrays(%v, %v) to return %v, got %v", c.arg1, c.arg2, c.expected, got)
		}
	}
}

func TestDiffArraysShouldReturnEmpty(t *testing.T) {
	arr1 := []string{"a", "b"}
	arr2 := []string{"b", "a"}
	got := DiffArrays(arr1, arr2)
	want := []string{}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`DiffArrays should return %v, got %v`, want, got)
	}
}

func TestDiffArraysShouldReturnDelta(t *testing.T) {
	arr1 := []string{"a", "b"}
	arr2 := []string{"b", "a", "d"}
	got := DiffArrays(arr1, arr2)
	want := []string{"d"}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`DiffArrays should return delta %v, got %v`, want, got)
	}
}

func TestArrayContainsCoordIsTrue(t *testing.T) {
	arr := [][2]int{{0, 0}, {2, 3}, {4, 5}}
	got := ArrayContainsCoord(&arr, [2]int{4, 5})
	want := true
	if got != want {
		t.Errorf("ArrayContainsCoord should return %v, got %v", want, got)
	}
}

func TestArrayContainsCoordIsFalse(t *testing.T) {
	arr := [][2]int{{0, 0}, {2, 3}, {4, 5}}
	got := ArrayContainsCoord(&arr, [2]int{3, 6})
	want := false
	if got != want {
		t.Errorf("ArrayContainsCoord should return %v, got %v", want, got)
	}
}

func TestArrayContainsStringIsTrue(t *testing.T) {
	arr := []string{"h", "hello", "bye", "hi"}
	got := ArrayContainsString(&arr, "hi")
	want := true
	if got != want {
		t.Errorf("ArrayContainsString should return %v, got %v", want, got)
	}
}

func TestArrayContainsStringIsFalse(t *testing.T) {
	arr := []string{"h", "hello", "bye", "hi"}
	got := ArrayContainsString(&arr, "hola")
	want := false
	if got != want {
		t.Errorf("ArrayContainsString should return %v, got %v", want, got)
	}
}
