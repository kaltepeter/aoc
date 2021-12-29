package main

import (
	"ka/m/util"
	"path/filepath"
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

func TestCountPackets(t *testing.T) {
	bits := Bits{
		Packet: Packet{
			Version: 6,
			TypeId:  4,
			Value:   "111011100000000011",
			SubPacket: &Packet{
				Version: 6,
				TypeId:  4,
				Value:   "01010000001",
				SubPacket: &Packet{
					Version: 6,
					TypeId:  4,
					Value:   "10010000010",
					SubPacket: &Packet{
						Version: 6,
						TypeId:  4,
						Value:   "00110000011",
					},
				},
			},
		},
	}
	got := bits.CountSubPackets()
	want := 3
	if got != want {
		t.Errorf(`CountPackets should return %v, got %v`, want, got)
	}
}

func TestSumVersions(t *testing.T) {
	bits := Bits{
		Packet: Packet{
			Version: 4,
			TypeId:  4,
			Value:   "1111",
			SubPacket: &Packet{
				Version: 1,
				TypeId:  4,
				Value:   "1111",
				SubPacket: &Packet{
					Version: 5,
					TypeId:  4,
					Value:   "1111",
					SubPacket: &Packet{
						Version: 6,
						TypeId:  4,
						Value:   "1111",
					},
				},
			},
		},
	}
	got := bits.SumVersions()
	want := 16
	if got != want {
		t.Errorf(`SumVersions should return %v, got %v`, want, got)
	}
}

func TestProcessLiteral(t *testing.T) {
	input := setupTests("example.txt")
	bitData := ProcessInput(input[0])

	bits := Bits{
		Packet: Packet{
			Version: 6,
			TypeId:  4,
		},
	}
	gotRp, got, err := bits.ProcessLiteral(bitData[6:])
	if err != nil {
		t.Errorf(`Failed to convert`)
	}
	want := int64(2021)
	if got != want || gotRp != "000" {
		t.Errorf(`ProcessLiteral should return %v, got %v. RemainingPackets: want: %v, got: %v`, want, got, "", gotRp)
	}
}

func TestProcessOperator(t *testing.T) {
	input := setupTests("example.txt")
	cases := []struct {
		input                        string
		expectedRemainingPackets     string
		expectedRemainingPacketCount int
	}{
		{
			input:                        input[1],
			expectedRemainingPackets:     "110100010100101001000100100",
			expectedRemainingPacketCount: -1,
		},
		{
			input:                        input[2],
			expectedRemainingPackets:     "01010000001100100000100011000001100000",
			expectedRemainingPacketCount: 3,
		},
	}
	for _, c := range cases {
		bits := Bits{
			Packet: Packet{
				Version: 1,
				TypeId:  6,
			},
		}
		bitData := ProcessInput(c.input)[6:]
		got, remainingCount, err := bits.ProcessOperator(bitData)
		if err != nil {
			t.Error(`Failed to process operator. `, err)
		}
		want := c.expectedRemainingPackets
		if got != want {
			t.Errorf(`ProcessOperator should return %v for %v, got %v`, want, bitData, got)
		}
		if remainingCount != c.expectedRemainingPacketCount {
			t.Errorf(`ProcessOperator should return %v for remainingCounts, got %v`, c.expectedRemainingPacketCount, remainingCount)
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
		// {
		// 	input:    input[4],
		// 	expected: 12,
		// },
		// {
		// 	input:    input[5],
		// 	expected: 23,
		// },
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

// func TestPartII(t *testing.T) {
// 	input := setupTests("example.txt")
// 	bitData := ProcessInput(input[0])
// 	got := Part2(bitData)
// 	want := 315
// 	if got != want {
// 		t.Errorf(`Part II should return %v for blah, got %v`, want, got)
// 	}
// }
