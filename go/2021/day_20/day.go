package main

import (
	"fmt"
	"image"
	"image/color"
	"image/draw"
	"ka/m/util"
	"path/filepath"
	"strings"

	"gonum.org/v1/gonum/mat"
)

type PixelChar int

const (
	DarkPixel PixelChar = iota
	LightPixel
)

func (char PixelChar) String() string {
	chars := [...]string{
		".",
		"#",
	}

	return chars[char]
}

type ImageProcessor struct {
	EnhancementAlgorithm string
	InputImage           []string
	ImageMat             *mat.Dense
	Off                  PixelChar
	On                   PixelChar
}

func CalcPixelDigit(s *mat.Dense) (val int) {
	bits := 0b000000000
	r, c := s.Dims()
	for i := 0; i < r; i++ {
		for j := 0; j < c; j++ {
			bits = bits<<1 | int(s.At(i, j))
		}
	}
	// fmt.Printf("bits: %09b %v\n", bits, bits)
	val = bits
	return
}

func matPrint(X mat.Matrix) {
	fa := mat.Formatted(X, mat.Prefix(""), mat.Squeeze())
	fmt.Printf("%v\n\n", fa)
}

func printImage(ip *ImageProcessor) {
	height, width := ip.ImageMat.Dims()
	// matPrint(ip.ImageMat)
	im := image.NewGray(image.Rectangle{Max: image.Point{X: width, Y: height}})
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			pixel := ip.ImageMat.At(y, x)
			var gray uint8
			switch pixel {
			case float64(LightPixel):
				gray = 255
			case float64(DarkPixel):
				gray = 0
			}
			im.SetGray(x, y, color.Gray{Y: 255 - gray})
		}
	}
	pi := image.NewPaletted(im.Bounds(), []color.Color{
		color.Gray{Y: 255},
		color.Gray{Y: 160},
		color.Gray{Y: 70},
		color.Gray{Y: 35},
		color.Gray{Y: 0},
	})

	draw.FloydSteinberg.Draw(pi, im.Bounds(), im, image.ZP)
	shade := []string{" ", "░", "▒", "▓", "█"}
	for i, p := range pi.Pix {
		fmt.Print(shade[p])
		if (i+1)%width == 0 {
			fmt.Print("\n")
		}
	}
}

func GetPixelCharFromByte(char byte) (pc PixelChar) {
	switch string(char) {
	case LightPixel.String():
		pc = LightPixel
	case DarkPixel.String():
		pc = DarkPixel
	}
	return
}

func ProcessInput(data [][]string, padding int) (ip ImageProcessor) {
	ip.EnhancementAlgorithm = data[0][0]
	ip.InputImage = data[1]
	rows, cols := len(data[1])+(padding*2), len(data[1][0])+(padding*2)

	paddingRow := make([]float64, cols)
	// ip.Off = GetPixelCharFromByte(ip.EnhancementAlgorithm[0])
	if GetPixelCharFromByte(ip.EnhancementAlgorithm[0]) == LightPixel {
		ip.Off = LightPixel
		ip.On = DarkPixel
	} else {
		ip.Off = DarkPixel
		ip.On = LightPixel
	}
	// ip.On = GetPixelCharFromByte(ip.EnhancementAlgorithm[511])
	for i := 0; i < len(paddingRow); i++ {
		paddingRow[i] = float64(ip.Off)
	}
	// padding for the image view, space is infinite
	imageData := []float64{}
	for i := 0; i < padding; i++ {
		imageData = append(imageData, paddingRow...)
	}
	for _, v := range data[1] {
		for i := 0; i < cols; i++ {
			val := fmt.Sprintf("%v%v%v", strings.Repeat(ip.Off.String(), padding), v, strings.Repeat(ip.Off.String(), padding)) // add padding for the image view
			char := val[i]
			pixelChar := GetPixelCharFromByte(char)
			imageData = append(imageData, float64(pixelChar))
		}
	}
	for i := 0; i < padding; i++ {
		imageData = append(imageData, paddingRow...)
	}
	ip.ImageMat = mat.NewDense(rows, cols, imageData)

	return
}

func GetNeighborsAndCell(m *mat.Dense, coord [2]int) (s mat.Matrix) {
	rows, cols := m.Dims()
	startI := 0
	startJ := 0
	endI := rows
	endJ := cols
	i, j := coord[0], coord[1]

	if i > 0 {
		startI = i - 1
	} else if i == 0 {
		startI = i
	}
	if i < rows-1 {
		endI = i + 2
	}
	if j > 0 {
		startJ = j - 1
	} else if j == 0 {
		startJ = j
	}
	if j < cols-1 {
		endJ = j + 2
	}
	s = m.Slice(startI, endI, startJ, endJ)
	return
}

func ProcessImage(ip *ImageProcessor, padding int) {
	rows, cols := ip.ImageMat.Dims()
	// padding ensures neighborcells always returns 9 digits
	var newImage mat.Dense
	newImage.CloneFrom(ip.ImageMat)
	for i := 0; i < rows; i++ {
		for j := 0; j < cols; j++ {
			// fmt.Printf("i,j: %v,%v pixel: %v\n", i, j, pixel)
			s := GetNeighborsAndCell(ip.ImageMat, [2]int{i, j})
			enhancementIndex := CalcPixelDigit(s.(*mat.Dense))
			pixelChar := GetPixelCharFromByte(ip.EnhancementAlgorithm[enhancementIndex])
			newImage.Set(i, j, float64(pixelChar))
		}
	}
	ip.ImageMat = &newImage
}

func Part1(ip *ImageProcessor, padding int, rounds int) int {
	for i := 0; i < rounds; i++ {
		ProcessImage(ip, padding)
	}
	printImage(ip)
	return int(mat.Sum(ip.ImageMat))
}

func Part2(ip *ImageProcessor) int {
	return 0
}

func main() {
	input := filepath.Join("2021", "day_20", "raw-input.txt")
	inputData := util.SplitInputByEmptyLines(input)
	padding := 1
	imageData := ProcessInput(inputData, padding)
	p1Result := Part1(&imageData, padding, 2)
	fmt.Printf("Part I: the number of lit pixels is = %v\n", p1Result)
	if p1Result <= 5245 {
		panic("FAILED on Part I")
	}

	p2Result := Part2(&imageData)
	fmt.Printf("Part II: the lowest risk path level is = %v\n", p2Result)
	if p2Result != 2874 {
		panic("FAILED on Part II")
	}
}
