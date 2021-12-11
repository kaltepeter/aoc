package util

import (
	"reflect"
	"testing"
)

func TestToListOfInt(t *testing.T) {
	input := []string{"7", "34", "23"}
	got := ToListOfInt(input)
	want := []int{7, 34, 23}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`ToListOfInt should return %#v, got %#v`, want, got)
	}
}

func TestStringToListOfInt(t *testing.T) {
	input := "7,4,9,5,11,17"
	got := StringToListOfInt(input)
	want := []int{7, 4, 9, 5, 11, 17}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`StringToListOfInt should return %#v, got %#v`, want, got)
	}
}

func TestStringToListOfString(t *testing.T) {
	input := "7,4,9,5,11,17"
	got := StringToListOfString(input)
	want := []string{"7", "4", "9", "5", "11", "17"}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`StringToListOfInt should return %#v, got %#v`, want, got)
	}
}

func TestStringToListOfIntWithSeparator(t *testing.T) {
	input := "22 13 17 11  0 \n"
	got := StringToListOfIntWithSeparator(input, ` +`)
	want := []int{22, 13, 17, 11, 0}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`StringToListOfIntWithSeparator should return %#v, got %#v`, want, got)
	}
}

func TestStringToListOfStringWithSeparator(t *testing.T) {
	input := "22 X 13 17 11 y  0 \n"
	got := StringToListOfStringWithSeparator(input, ` +`)
	want := []string{"22", "X", "13", "17", "11", "y", "0"}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`StringToListOfStringWithSeparator should return %#v, got %#v`, want, got)
	}
}

func TestHasAllChars(t *testing.T) {
	cases := []struct {
		arg1     string
		arg2     string
		exact    bool
		expected bool
	}{
		{
			arg1:     "cefabd",
			arg2:     "eafb",
			exact:    false,
			expected: true,
		},
		{

			arg1:     "gcdfa",
			arg2:     "dab",
			exact:    false,
			expected: false,
		},
		{
			arg1:     "cefabd",
			arg2:     "eafb",
			exact:    true,
			expected: false,
		},
		{
			arg1:     "ab",
			arg2:     "ba",
			exact:    true,
			expected: true,
		},
	}

	for _, c := range cases {
		got := HasAllChars(c.arg1, c.arg2, c.exact)

		if got != c.expected {
			t.Errorf("Expected HasAllChars(%v, %v, %v) to return %v, got %v", c.arg1, c.arg2, c.exact, c.expected, got)
		}
	}
}
