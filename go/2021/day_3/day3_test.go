package main

import (
	"ka/m/util"
	"path/filepath"
	"testing"
)

func setupTests() []string {
	inputExample := filepath.Join("example.txt")
	return util.ParseInput(inputExample)
}

// TestHelloName calls greetings.Hello with a name, checking
// for a valid return value.
func TestPart1(t *testing.T) {
	inputDataExample := setupTests()
	gamma, epsilon, err := Part1(inputDataExample)
	if gamma != 22 {
		t.Errorf(`Gamma should equal 22, got %d`, gamma)
	}
	if epsilon != 9 {
		t.Errorf(`Epsilon should equal 9, got %d`, epsilon)
	}
	if err != nil {
		t.Fatal(`Received error `, err)
	}
}

type CalcResultTestCase struct {
	arg1     float64
	arg2     float64
	expected float64
}

func TestCalcResult(t *testing.T) {
	cases := []struct {
		arg1     int64
		arg2     int64
		expected int64
	}{
		{
			arg1:     22,
			arg2:     9,
			expected: 198,
		},
		{

			arg1:     23,
			arg2:     10,
			expected: 230,
		},
	}

	for _, c := range cases {
		got := CalcResult(c.arg1, c.arg2)

		if got != c.expected {
			t.Errorf("Expected CalcResult(%v, %v), got %v", c.arg1, c.arg2, got)
		}
	}
}

func TestFindOxygenGeneratorRating(t *testing.T) {
	inputDataExample := setupTests()
	oxygenGeneratorRating := FindRating(inputDataExample, ProcessOxygenGeneratorRating)
	if oxygenGeneratorRating != 23 {
		t.Errorf(`Oxygen generator rating should equal 23, got %d`, oxygenGeneratorRating)
	}
}

func TestFindCO2ScrubberRating(t *testing.T) {
	inputDataExample := setupTests()
	co2ScrubberRating := FindRating(inputDataExample, ProcessCo2ScrubberRating)
	if co2ScrubberRating != 10 {
		t.Errorf(`Oxygen generator rating should equal 10, got %d`, co2ScrubberRating)
	}
}
