package util

import (
	"testing"
)

func TestMultiply(t *testing.T) {
	got := Multiply(3, 3)
	want := 9
	if got != want {
		t.Errorf(`Multiply should return %v, got %v`, want, got)
	}
}

func TestMAdd(t *testing.T) {
	got := Add(3, 3)
	want := 6
	if got != want {
		t.Errorf(`Add should return %v, got %v`, want, got)
	}
}
