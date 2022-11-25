package main

import (
	"ka/m/util"
	"path/filepath"
	"reflect"
	"testing"
)

func setupTests(filePath string) (algo string, image []string) {
	inputExample := filepath.Join(filePath)
	inputData := util.SplitInputByEmptyLines(inputExample)
	algo, image = ProcessInput(inputData)
	return
}

func TestProcessInput(t *testing.T) {
	inputExample := filepath.Join("example.txt")
	inputData := util.SplitInputByEmptyLines(inputExample)

	type args struct {
		data [][]string
	}
	tests := []struct {
		name      string
		args      args
		wantAlgo  string
		wantImage []string
	}{
		{name: "should return algo and image",
			args: args{
				data: inputData,
			},
			wantAlgo:  "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#",
			wantImage: []string{"#..#.", "#....", "##..#", "..#..", "..###"},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			gotAlgo, gotImage := ProcessInput(tt.args.data)

			if gotAlgo != tt.wantAlgo {
				t.Errorf("ProcessInput() = %v, want %v", gotAlgo, tt.wantAlgo)
			}

			if !reflect.DeepEqual(gotImage, tt.wantImage) {
				t.Errorf("ProcessInput() = %v, want %v", gotImage, tt.wantImage)
			}
		})
	}
}

func TestGrowImage(t *testing.T) {
	type args struct {
		m   []string
		num int
	}
	tests := []struct {
		name    string
		args    args
		wantVal []string
	}{
		{
			name: "should return with 2 rows padding",
			args: args{
				m:   []string{"#..#.", "#....", "##..#", "..#..", "..###"},
				num: 2,
			},
			wantVal: []string{".........", ".........", "..#..#...", "..#......", "..##..#..", "....#....", "....###..", ".........", "........."},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if gotVal := GrowImage(tt.args.m, tt.args.num, "."); !reflect.DeepEqual(gotVal, tt.wantVal) {
				t.Errorf("GrowImage() = %v, want %v", gotVal, tt.wantVal)
			}
		})
	}
}

func TestGetNeighborsAndCell(t *testing.T) {
	type args struct {
		m           []string
		coord       [2]int
		defaultChar string
	}
	tests := []struct {
		name    string
		args    args
		wantVal [][3]string
	}{
		{
			name: "should return [[.,.,.], [#,.,.], [.,#,.]]",
			args: args{
				m:           []string{"#..#.", "#....", "##..#", "..#..", "..###"},
				defaultChar: ".",
				coord:       [2]int{2, 2},
			},
			wantVal: [][3]string{{".", ".", "."}, {"#", ".", "."}, {".", "#", "."}},
		},
		{
			name: "should return [[.,#,.], [.,#,.], [.,#,#]]",
			args: args{
				m:           []string{"#..#.", "#....", "##..#", "..#..", "..###"},
				defaultChar: ".",
				coord:       [2]int{1, 0},
			},
			wantVal: [][3]string{{".", "#", "."}, {".", "#", "."}, {".", "#", "#"}},
		},
		{
			name: "should return [[.,.,.], [#,#,.], [.,.,.]]",
			args: args{
				m:           []string{"#..#.", "#....", "##..#", "..#..", "..###"},
				defaultChar: ".",
				coord:       [2]int{4, 4},
			},
			wantVal: [][3]string{{".", ".", "."}, {"#", "#", "."}, {".", ".", "."}},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if gotVal := GetNeighborsAndCell(tt.args.m, tt.args.coord, tt.args.defaultChar); !reflect.DeepEqual(gotVal, tt.wantVal) {
				t.Errorf("GetNeighborsAndCell() = %v, want %v", gotVal, tt.wantVal)
			}
		})
	}
}

func TestProcessImage(t *testing.T) {
	type args struct {
		m    []string
		algo string
	}
	tests := []struct {
		name    string
		args    args
		wantVal []string
	}{
		{
			name: "should return new image",
			args: args{
				m:    []string{"#..#.", "#....", "##..#", "..#..", "..###"},
				algo: "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#",
			},
			wantVal: []string{".##.##.", "#..#.#.", "##.#..#", "####..#", ".#..##.", "..##..#", "...#.#."},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			expImg := GrowImage(tt.args.m, 1, ".")
			if gotVal := ProcessImage(tt.args.algo, expImg, "."); !reflect.DeepEqual(gotVal, tt.wantVal) {
				t.Errorf("ProcessImage() = %v, want %v", gotVal, tt.wantVal)
			}
		})
	}
}

func TestCalcPixelDigit(t *testing.T) {
	type args struct {
		cells [][3]string
	}
	tests := []struct {
		name    string
		args    args
		wantVal int
	}{
		{
			name: "should return 34",
			args: args{
				cells: [][3]string{{".", ".", "."}, {"#", ".", "."}, {".", "#", "."}},
			},
			wantVal: 34,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if gotVal := CalcPixelDigit(tt.args.cells); gotVal != tt.wantVal {
				t.Errorf("CalcPixelDigit() = %v, want %v", gotVal, tt.wantVal)
			}
		})
	}
}

func TestCalcLitPixels(t *testing.T) {
	type args struct {
		image []string
	}
	tests := []struct {
		name    string
		args    args
		wantVal int
	}{
		{
			name: "should return 10",
			args: args{
				image: []string{"#..#.", "#....", "##..#", "..#..", "..###"},
			},
			wantVal: 10,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if gotVal := CalcLitPixels(tt.args.image); gotVal != tt.wantVal {
				t.Errorf("CalcLitPixels() = %v, want %v", gotVal, tt.wantVal)
			}
		})
	}
}

func TestPartI(t *testing.T) {
	algo, image := setupTests("example.txt")
	got := Part1(algo, image, 2)
	want := 35
	if got != want {
		t.Errorf(`Part I should return %v, got %v`, want, got)
	}
}
