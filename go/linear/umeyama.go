package linear

// https://zpl.fi/aligning-point-patterns-with-kabsch-umeyama-algorithm/

import (
	"fmt"
	"log"
	"math"

	"gonum.org/v1/gonum/mat"
)

func matPrint(X mat.Matrix) {
	fa := mat.Formatted(X, mat.Prefix(""), mat.Squeeze())
	fmt.Printf("%v\n\n", fa)
}

func flatten(a [][]float64) (flatA []float64) {
	for _, r := range a {
		// for _, c := range r {
		flatA = append(flatA, r...)
		// }
	}
	return
}

func meanAxis0(a *mat.Dense) (m mat.Dense) {
	rows, cols := a.Dims()
	m = *mat.NewDense(1, cols, nil)
	for i := 0; i < cols; i++ {
		row := mat.Sum(a.ColView(i))
		m.SetCol(i, []float64{row / float64(rows)})
	}
	return
}

func subVector(a *mat.Dense, vect *mat.Dense) (m mat.Dense) {
	rows, cols := a.Dims()
	m = *mat.NewDense(rows, cols, nil)
	m.Apply(func(i, j int, v float64) float64 {
		return v - vect.At(0, j)
	}, a)
	return
}

func normAxis1(a *mat.Dense) (m mat.Dense) {
	rows, _ := a.Dims()
	m = *mat.NewDense(1, rows, nil)
	for i := 0; i < rows; i++ {
		c := a.RowView(i)
		v := mat.Norm(c, 2)
		m.SetCol(i, []float64{v})
	}
	return
}

func Umeyama(aCoords [][]float64, bCoords [][]float64) (*mat.Dense, float64, *mat.Dense) {
	rows := len(aCoords)
	cols := len(aCoords[0])
	aMat := mat.NewDense(rows, cols, flatten(aCoords))
	bMat := mat.NewDense(rows, cols, flatten(bCoords))

	EA := meanAxis0(aMat)
	EB := meanAxis0(bMat)

	aSubEA := subVector(aMat, &EA)

	bSubEB := subVector(bMat, &EB)

	aNorm := normAxis1(&aSubEA)

	var aNormSquared mat.Dense
	aNormSquared.Apply(func(i, j int, v float64) float64 {
		return math.Pow(v, 2)
	}, &aNorm)

	VarA := mat.Sum(&aNormSquared) / float64(aNormSquared.RawMatrix().Cols)

	var c1 mat.Dense
	c1.Mul(aSubEA.T(), &bSubEB)

	var H mat.Dense
	H.Apply(func(i, j int, v float64) float64 {
		return v / float64(rows)
	}, &c1)

	var svd mat.SVD
	if ok := svd.Factorize(&H, mat.SVDFull); !ok {
		log.Fatal("failed to factorize A")
	}
	var U mat.Dense
	svd.UTo(&U)

	D := svd.Values(nil)

	var VT, iVT mat.Dense
	svd.VTo(&iVT)
	b := iVT.T()
	VT = *mat.DenseCopyOf(b)

	var lu mat.LU
	lu.Factorize(&U)
	luU := lu.Det()

	lu.Factorize(&VT)
	luVT := lu.Det()
	d := math.Copysign(1, (luU * luVT))

	// var s1 mat.Dense
	baseDiagonal := make([]float64, 0)
	for i := 0; i < cols-1; i++ {
		baseDiagonal = append(baseDiagonal, 1)
	}
	// baseDiag := mat.NewDense(1, 1, []float64{1})
	// baseDiag2 := mat.NewDense(1, diagCount, []float64{float64(diagCount)})

	// s1.Mul(baseDiag, baseDiag2)/
	// cc := s1.RawMatrix().Data
	baseDiagonal = append(baseDiagonal, d)
	S := mat.NewDiagDense(cols, baseDiagonal)

	// R = U @ S @ VT
	var R mat.Dense

	R.Mul(&U, S)
	R.Mul(&R, &VT)

	// c = VarA / np.trace(np.diag(D) @ S)
	var d1 mat.Dense
	d1.Mul(mat.NewDiagDense(cols, D), S)
	c := VarA / d1.Trace()

	// t = EA - c * R @ EB
	// var eaSubC, cMulR, t mat.Dense
	// var rDotEB mat.VecDense
	var cScaleR, t mat.Dense
	cScaleR.Scale(c, &R)
	var newVec mat.VecDense
	newVec.MulVec(&cScaleR, EB.RowView(0))
	t.Sub(EA.RowView(0), &newVec)
	// eaSubC.Apply(func(i, j int, v float64) float64 {
	// 	return v - c
	// }, &EA)
	// cMulR.Scale(c, &R)

	// rDotEB.MulVec(&cMulR, EB.RowView(0))
	// t.Sub(EA.RowView(0), &rDotEB)
	return &R, c, &t
}
