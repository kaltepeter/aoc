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

	cases := []struct {
		input    string
		expected string
	}{
		{
			input:    input[0],
			expected: "110100101111111000101000",
		},
		{
			input:    input[1],
			expected: "00111000000000000110111101000101001010010001001000000000",
		},
		{
			input:    input[2],
			expected: "11101110000000001101010000001100100000100011000001100000",
		},
		{
			input:    input[3],
			expected: "100010100000000001001010100000000001101010000000000000101111010001111000",
		},
		{
			input:    input[4],
			expected: "01100010000000001000000000000000000101100001000101010110001011001000100000000010000100011000111000110100",
		},
	}
	for _, c := range cases {
		got := ProcessInput(c.input)
		want := c.expected
		if got != want {
			t.Errorf(`ProcessInput should return %s for %v, got %v`, want, c.input, got)
		}
	}
}

func TestReadBits(t *testing.T) {

	cases := []struct {
		input    string
		start    int
		count    int
		expected int64
	}{
		{
			input:    "110100101111111000101000",
			start:    0,
			count:    3,
			expected: 6,
		},
		{
			input:    "110100101111111000101000",
			start:    3,
			count:    3,
			expected: 4,
		},
		{
			input:    "011111100101",
			start:    0,
			count:    12,
			expected: 2021,
		},
	}
	for _, c := range cases {
		got, _, err := ReadBits(c.input, c.start, c.count)
		if err != nil {
			t.Errorf(`Failed to read bits`)
		}
		want := c.expected
		if got != want {
			t.Errorf(`ReadBits should return %d for %v, got %v`, want, c.input, got)
		}
	}
}

func TestReadNumber(t *testing.T) {
	got, gotCount := ReadNumber("110100101111111000101000", 6)
	want := int64(2021)
	wantCount := 15
	if got != want || gotCount != wantCount {
		t.Errorf(`ReadNumber should return %v %v, got %v, %v`, want, wantCount, got, gotCount)
	}
}

func TestSumVersions(t *testing.T) {
	packets := Operator{
		Version:  1,
		TypeId:   6,
		Value:    0,
		LengthId: 0,
		Length:   27,
		Packets: []interface{}{
			Literal{
				Version: 6,
				TypeId:  4,
				Value:   10,
			},
			Literal{
				Version: 2,
				TypeId:  4,
				Value:   20,
			},
		},
	}
	got := SumVersions(packets)
	want := int64(9)
	if got != want {
		t.Errorf(`SumVersions should return %v, got %v`, want, got)
	}
}

func TestReadPacket(t *testing.T) {
	cases := []struct {
		input     string
		want      interface{}
		wantCount int
	}{
		{
			input: "110100101111111000101000",
			want: Literal{
				Version: 6,
				TypeId:  4,
				Value:   2021,
			},
			wantCount: 21,
		},
		{
			input: "00111000000000000110111101000101001010010001001000000000",
			want: Operator{
				Version:  1,
				TypeId:   6,
				Value:    0,
				LengthId: 0,
				Length:   27,
				Packets: []interface{}{
					Literal{
						Version: 6,
						TypeId:  4,
						Value:   10,
					},
					Literal{
						Version: 2,
						TypeId:  4,
						Value:   20,
					},
				},
			},
			wantCount: 49,
		},
		{
			input: "11101110000000001101010000001100100000100011000001100000",
			want: Operator{
				Version:  7,
				TypeId:   3,
				Value:    0,
				LengthId: 1,
				Length:   3,
				Packets: []interface{}{
					Literal{
						Version: 2,
						TypeId:  4,
						Value:   1,
					},
					Literal{
						Version: 4,
						TypeId:  4,
						Value:   2,
					},
					Literal{
						Version: 1,
						TypeId:  4,
						Value:   3,
					},
				},
			},
			wantCount: 51,
		},
	}

	for _, c := range cases {
		got, gotC := ReadPacket(c.input, 0)
		if !reflect.DeepEqual(got, c.want) || gotC != c.wantCount {
			t.Errorf(`ReadLiteral should return (%v %v), got (%v, %v).`, c.want, c.wantCount, got, gotC)
		}
	}
}

func TestPartI(t *testing.T) {
	input := setupTests("example.txt")

	cases := []struct {
		input    string
		expected int
	}{
		{
			input:    input[3],
			expected: 16,
		},
		{
			input:    input[4],
			expected: 12,
		},
		{
			input:    input[5],
			expected: 23,
		},
		{
			input:    input[6],
			expected: 31,
		},
	}
	for _, c := range cases {
		bitData := ProcessInput(c.input)

		got := Part1(bitData)
		want := c.expected
		if got != want {
			t.Errorf(`Part I should return %d for %v, got %v`, want, c.input, got)
		}
	}
}

func TestPartII(t *testing.T) {
	input := setupTests("example.txt")

	cases := []struct {
		input    string
		expected int
	}{
		{
			input:    input[7],
			expected: 3,
		},
		{
			input:    input[8],
			expected: 54,
		},
		{
			input:    input[9],
			expected: 7,
		},
		{
			input:    input[10],
			expected: 9,
		},
		{
			input:    input[11],
			expected: 1,
		},
		{
			input:    input[12],
			expected: 0,
		},
		{
			input:    input[13],
			expected: 0,
		},
		{
			input:    input[14],
			expected: 1,
		},
	}
	for _, c := range cases {
		bitData := ProcessInput(c.input)

		got, err := Part2(bitData)
		if err != nil {
			t.Errorf(`Part 2 failed. %v`, err)
		}
		want := c.expected
		if got != want {
			t.Errorf(`Part II should return %d for %v, got %v`, want, c.input, got)
		}
	}
}
