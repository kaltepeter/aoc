package main

import (
	"ka/m/linear"
	"ka/m/util"
	"path/filepath"
	"reflect"
	"testing"

	"gonum.org/v1/gonum/mat"
)

func setupTests(filePath string) []Scanner {
	inputExample := filepath.Join(filePath)
	inputData := util.ParseInput(inputExample)
	scannerData := ProcessInput(&inputData)
	return scannerData
}

func TestProcessInput(t *testing.T) {
	input := setupTests("example.txt")
	got := len(input)
	want := 5
	if got != want {
		t.Errorf(`ProcessInput should return %v items, got: %v`, want, got)
	}

	gotBeaconCount := len(input[0].Beacons)
	wantBeaconCount := 25
	if gotBeaconCount != wantBeaconCount {
		t.Errorf(`ProcessInput should return %v beacons for scanner 0, got: %v`, wantBeaconCount, gotBeaconCount)
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

func TestGetAllRotations(t *testing.T) {
	coord := &Coord{1, 2, -3}
	got := coord.GetAllRotations()
	want := 24
	if len(got) != want {
		t.Errorf(`GetAllRotations should return %v, got %v`, want, len(got))
	}
}

func TestCalcL2Norm(t *testing.T) {
	got := CalcL2Norm([3]int{25, 2, 5})
	got2 := CalcL2Norm([3]int{2, -25, 5})
	want := 25.573423705088842
	if got != want {
		t.Errorf(`CalcL2Norm() = %v, got %v`, want, got)
	}
	if got2 != want {
		t.Errorf(`CalcL2Norm() = %v, got %v`, want, got2)
	}
	pos := []float64{float64(2), float64(-25), float64(5)}
	vect := mat.NewVecDense(3, pos)
	if got != mat.Norm(vect, 2) {
		t.Errorf(`CalcL2Norm() = %v, got %v`, got, mat.Norm(vect, 2))
	}
}

func TestCalcSquaredNorm(t *testing.T) {
	got := CalcSquaredNorm([3]float64{25, 2, 5})
	got2 := CalcSquaredNorm([3]float64{2, -25, 5})
	want := float64(654)
	if got != want {
		t.Errorf(`CalcSquaredNorm() = %v, got %v`, want, got)
	}
	if got2 != want {
		t.Errorf(`CalcSquaredNorm() = %v, got %v`, want, got)
	}
}

func TestPartI(t *testing.T) {
	input := setupTests("example.txt")
	scanners := ProcessScanners(input)
	got := Part1(scanners)
	want := 79
	if got != want {
		t.Errorf(`Part I should return %v, got %v`, want, got)
	}
}

func TestPartII(t *testing.T) {
	input := setupTests("example.txt")
	scanners := ProcessScanners(input)
	got := Part2(scanners)
	want := 3621
	if got != want {
		t.Errorf(`Part II should return %v, got %v`, want, got)
	}
}

func TestScanner_FindCommonBeacons(t *testing.T) {
	input := setupTests("example.txt")
	s0 := input[0]
	s0.SetBeaconDist()

	s1 := input[1]
	s1.SetBeaconDist()

	s3 := input[3]
	s3.SetBeaconDist()

	type args struct {
		s2 *Scanner
	}
	tests := []struct {
		name   string
		fields *Scanner
		args   args
		want   int
	}{
		{
			name:   "s0,s1: Should return 12 matching Coords",
			fields: &s0,
			args:   args{s2: &s1},
			want:   12,
		},
		{
			name:   "s1,s3: Should return 12 matching Coords",
			fields: &s1,
			args:   args{s2: &s3},
			want:   12,
		},
		{
			name:   "s0,s3: Should return 0 matching Coords",
			fields: &s0,
			args:   args{s2: &s3},
			want:   0,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			s := &Scanner{
				Name:       tt.fields.Name,
				Pos:        tt.fields.Pos,
				Beacons:    tt.fields.Beacons,
				BeaconDist: tt.fields.BeaconDist,
			}
			if got := len(s.FindCommonBeacons(tt.args.s2)); got != tt.want {
				t.Errorf("Scanner.FindCommonBeacons() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestScanner_Translate(t *testing.T) {
	input := setupTests("example.txt")
	s0 := input[0]
	s0.SetBeaconDist()

	s1 := input[1]
	s1.SetBeaconDist()

	type args struct {
		s2            *Scanner
		matchedCoords [][2]Coord
	}
	tests := []struct {
		name   string
		fields *Scanner
		args   args
		want   Coord
	}{
		{
			name:   "Should return correct position",
			fields: &s0,
			args: args{
				s2: &s1,
				matchedCoords: [][2]Coord{
					{{553, 889, -390}, {-485, -357, 347}},
					{{515, 917, -361}, {-447, -329, 318}},
					{{686, 422, 578}, {-618, -824, -621}},
					{{-460, 603, -452}, {528, -643, 409}},
					{{413, 935, -424}, {-345, -311, 381}},
					{{-476, 619, 847}, {544, -627, -890}},
					{{-355, 545, -477}, {423, -701, 434}},
					{{-391, 539, -444}, {459, -707, 401}},
					{{605, 423, 415}, {-537, -823, -458}},
					{{-322, 571, 750}, {390, -675, -793}},
					{{729, 430, 532}, {-661, -816, -575}},
					{{-336, 658, 858}, {404, -588, -901}},
				},
			},
			want: Coord{X: 68, Y: -1246, Z: -43}, // 68,-1246,-43
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// s := tt.args.s2
			if got := tt.args.s2.Translate(tt.fields, tt.args.matchedCoords); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Scanner.Translate() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestUmeyama(t *testing.T) {
	t.Skip("Skip for now")
	aCoords := [][]float64{
		{23, 178},
		{66, 173},
		{88, 187},
		{119, 202},
		{122, 229},
		{170, 232},
		{179, 199},
	}
	bCoords := [][]float64{
		{232, 38},
		{208, 32},
		{181, 31},
		{155, 45},
		{142, 33},
		{121, 59},
		{139, 69},
	}

	wantRotation := [][]float64{
		{-0.81034281, 0.58595608},
		{-0.58595608, -0.81034281},
	}

	wantScale := 1.46166131

	wantTranslation := []float64{271.3345951, 396.07800317}

	gotRotation, gotScale, gotTranslation := linear.Umeyama(aCoords, bCoords)

	if !reflect.DeepEqual(gotRotation, wantRotation) {
		t.Errorf("Umeyama() gotRotation = %v, want %v", gotRotation, wantRotation)
	}
	if gotScale != wantScale {
		t.Errorf("Umeyama() gotScale = %v, want %v", gotScale, wantScale)
	}
	if !reflect.DeepEqual(gotTranslation, wantTranslation) {
		t.Errorf("Umeyama() gotTranslation = %v, want %v", gotTranslation, wantTranslation)
	}
}

func TestBeacon_TranslatePosition(t *testing.T) {
	type fields struct {
		Pos Coord
	}
	type args struct {
		R *mat.Dense
		c float64
		t *mat.Dense
	}

	argV := args{
		R: mat.NewDense(3, 3, []float64{-1.0000000000000002, -6.938893903907228e-18, -6.505213034913027e-17, -6.938893903907228e-18, 1, 0, 6.765421556309548e-17, -1.3877787807814457e-16, -1}),
		c: 0.9999999999999998,
		t: mat.NewDense(3, 1, []float64{68.00000000000001, -1246, -42.99999999999996}),
	}

	tests := []struct {
		name   string
		fields fields
		args   args
		want   Coord
	}{
		{
			name: "rotates coord",
			fields: fields{
				Pos: Coord{
					X: 686,
					Y: 422,
					Z: 578,
				},
			},
			args: argV,
			want: Coord{X: -618, Y: -824, Z: -621},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			coord := &Beacon{
				Pos: tt.fields.Pos,
			}
			coord.TranslatePosition(tt.args.R, tt.args.c, tt.args.t)
			if !reflect.DeepEqual(coord.Pos, tt.want) {
				t.Errorf(`coord.TranslatePosition failed expected Coord %v, got %v`, tt.want, coord.Pos)
			}
		})
	}
}
