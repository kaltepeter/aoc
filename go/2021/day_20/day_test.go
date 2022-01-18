package main

import (
	"ka/m/util"
	"path/filepath"
	"reflect"
	"testing"

	"gonum.org/v1/gonum/mat"
)

func setupTests(filePath string) ImageProcessor {
	inputExample := filepath.Join(filePath)
	inputData := util.SplitInputByEmptyLines(inputExample)
	imageData := ProcessInput(inputData, 5)
	return imageData
}

func TestPartI(t *testing.T) {
	input := setupTests("example.txt")
	got := Part1(&input, 1, 2)
	want := 35
	if got != want {
		t.Errorf(`Part I should return %v, got %v`, want, got)
	}
}

func SkipTestPartII(t *testing.T) {
	input := setupTests("example.txt")
	got := Part2(&input)
	want := 315
	if got != want {
		t.Errorf(`Part II should return %v, got %v`, want, got)
	}
}

func TestProcessInput(t *testing.T) {
	inputExample := filepath.Join("example.txt")
	inputData := util.SplitInputByEmptyLines(inputExample)

	type args struct {
		data [][]string
	}
	tests := []struct {
		name   string
		args   args
		wantIp ImageProcessor
	}{
		{name: "should return ImageProcessor",
			args: args{
				data: inputData,
			},
			wantIp: ImageProcessor{
				EnhancementAlgorithm: "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#",
				InputImage:           []string{"#..#.", "#....", "##..#", "..#..", "..###"},
				ImageMat:             mat.NewDense(15, 15, []float64{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}),
				Off:                  DarkPixel,
				On:                   LightPixel,
			},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if gotIp := ProcessInput(tt.args.data, 5); !reflect.DeepEqual(gotIp, tt.wantIp) {
				t.Errorf("ProcessInput() = %v, want %v", gotIp, tt.wantIp)
			}
		})
	}
}

func TestCalcPixelDigit(t *testing.T) {
	type args struct {
		s *mat.Dense
	}
	tests := []struct {
		name    string
		args    args
		wantVal int
	}{
		{
			name: "should return 34",
			args: args{
				s: mat.NewDense(3, 3, []float64{0, 0, 0, 1, 0, 0, 0, 1, 0}),
			},
			wantVal: 34,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if gotVal := CalcPixelDigit(tt.args.s); gotVal != tt.wantVal {
				t.Errorf("CalcPixelDigit() = %v, want %v", gotVal, tt.wantVal)
			}
		})
	}
}
