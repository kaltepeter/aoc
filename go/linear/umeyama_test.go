package linear

import (
	"math"
	"reflect"
	"testing"
)

func TestUmeyama(t *testing.T) {
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
	R, c, ut := Umeyama(aCoords, bCoords)
	var gotR, gott []float32
	for _, v := range R.RawMatrix().Data {
		gotR = append(gotR, float32(v))
	}
	gotc := float32(c)
	for _, v := range ut.RawMatrix().Data {
		gott = append(gott, float32(v))
	}

	wantR := []float32{-0.81034281, 0.58595608,
		-0.58595608, -0.81034281}
	wantc := float32(1.4616613091002035)
	wantt := []float32{271.3345951, 396.07800317}
	if !reflect.DeepEqual(gotR, wantR) {
		t.Errorf(`Umeyama should return %v for R, got %v`, wantR, gotR)
	}
	if gotc != wantc {
		t.Errorf(`Umeyama should return %v for c, got %v`, wantc, gotc)
	}
	if !reflect.DeepEqual(gott, wantt) {
		t.Errorf(`Umeyama should return %v for t, got %v`, wantt, gott)
	}
}

func TestUmeyama3d(t *testing.T) {
	aCoords := [][]float64{
		{-618, -824, -621},
		{-537, -823, -458},
		{-447, -329, 318},
		{404, -588, -901},
		{544, -627, -890},
		{528, -643, 409},
		{-661, -816, -575},
		{390, -675, -793},
		{423, -701, 434},
		{-345, -311, 381},
		{459, -707, 401},
		{-485, -357, 347},
	}
	bCoords := [][]float64{
		{686, 422, 578},
		{605, 423, 415},
		{515, 917, -361},
		{-336, 658, 858},
		{-476, 619, 847},
		{-460, 603, -452},
		{729, 430, 532},
		{-322, 571, 750},
		{-355, 545, -477},
		{413, 935, -424},
		{-391, 539, -444},
		{553, 889, -390},
	}
	_, _, ut := Umeyama(aCoords, bCoords)
	gott := ut.RawMatrix().Data

	wantt := []float64{68, -1246, -43}
	if math.Round(gott[0]) != wantt[0] || math.Round(gott[1]) != wantt[1] || math.Round(gott[2]) != wantt[2] {
		t.Errorf(`Umeyama should return rounded vals %v for t, got %v`, wantt, gott)
	}
}

func TestUmeyama3d2(t *testing.T) {
	aCoords := [][]float64{
		{-618, -824, -621},
		{-537, -823, -458},
		{-447, -329, 318},
		{404, -588, -901},
		{544, -627, -890},
		{528, -643, 409},
		{-661, -816, -575},
		{390, -675, -793},
		{423, -701, 434},
		{-345, -311, 381},
		{459, -707, 401},
		{-485, -357, 347},
	}
	bCoords := [][]float64{
		{459, -707, 401},
		{-739, -1745, 668},
		{-485, -357, 347},
		{432, -2009, 850},
		{528, -643, 409},
		{423, -701, 434},
		{-345, -311, 381},
		{408, -1815, 803},
		{534, -1912, 768},
		{-687, -1600, 576},
		{-447, -329, 318},
		{-635, -1737, 486},
	}
	_, _, ut := Umeyama(aCoords, bCoords)
	gott := ut.RawMatrix().Data

	wantt := []float64{-158, -3129, 1516}
	if math.Round(gott[0]) != wantt[0] || math.Round(gott[1]) != wantt[1] || math.Round(gott[2]) != wantt[2] {
		t.Errorf(`Umeyama should return rounded vals %v for t, got %v`, wantt, gott)
	}
}
