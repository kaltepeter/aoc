package main

import (
	"fmt"
	"image"
	"image/color"
	"image/draw"
	"ka/m/util"
	"path/filepath"
	"strings"
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

func GetPixelCharFromByte(char byte) (pc PixelChar) {
	switch string(char) {
	case LightPixel.String():
		pc = LightPixel
	case DarkPixel.String():
		pc = DarkPixel
	}
	return
}

func ProcessInput(data [][]string) (algo string, img []string) {
	algo = data[0][0]
	img = data[1]
	return
}

func GrowImage(img []string, padding int, defaultChar string) (newImage []string) {
	// r := len(image)
	c := len(img[0])
	newImage = []string{}
	newRow := strings.Repeat(defaultChar, c+(padding*2))
	for i := 0; i < (padding); i++ {
		newImage = append(newImage, newRow)
	}

	for _, imageRow := range img {
		paddedRow := strings.Repeat(defaultChar, padding)
		paddedRow += imageRow
		paddedRow += strings.Repeat(defaultChar, padding)
		newImage = append(newImage, paddedRow)
	}

	for i := 0; i < (padding); i++ {
		newImage = append(newImage, newRow)
	}
	return
}

func GetNeighborsAndCell(img []string, coord [2]int, notFoundVal string) (s [][3]string) {
	rows := len(img)
	cols := len(img[0])

	s = make([][3]string, 3)
	curRow, curCol := 0, 0

	for i := coord[0] - 1; i < coord[0]+2; i++ {
		for j := coord[1] - 1; j < coord[1]+2; j++ {
			if (i < 0 || i > rows-1) || (j < 0 || j > cols-1) {
				s[curRow][curCol] = notFoundVal
			} else {
				s[curRow][curCol] = fmt.Sprintf("%c", img[i][j])
			}

			if curCol >= 2 {
				curCol = 0
			} else {
				curCol++
			}
		}
		curRow++
	}
	return
}

func printImage(img []string) {
	height := len(img)
	width := len(img[0])
	// matPrint(ip.ImageMat)
	im := image.NewGray(image.Rectangle{Max: image.Point{X: width, Y: height}})
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			pixel := img[y][x]
			var gray uint8
			switch GetPixelCharFromByte(pixel) {
			case LightPixel:
				gray = 255
			case DarkPixel:
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

func CalcPixelDigit(cells [][3]string) (val int) {
	bits := 0b000000000
	r := len(cells)
	c := len(cells[0])
	for i := 0; i < r; i++ {
		for j := 0; j < c; j++ {
			b := []byte(cells[i][j])
			val := GetPixelCharFromByte(b[0])
			bits = bits<<1 | int(val)
		}
	}
	val = bits
	return
}

func ProcessImage(algo string, img []string, defaultChar string) (newImage []string) {
	rows := len(img)
	cols := len(img[0])
	for i := 0; i < rows; i++ {
		newRow := ""
		for j := 0; j < cols; j++ {
			neighbors := GetNeighborsAndCell(img, [2]int{i, j}, defaultChar)
			enhancementIndex := CalcPixelDigit(neighbors)
			pixelChar := GetPixelCharFromByte(algo[enhancementIndex])
			newRow += pixelChar.String()
			// newImage.Set(i, j, float64(pixelChar))
			// newImage[i][j] = pixelChar
		}
		newImage = append(newImage, newRow)
	}
	return
}

func CalcLitPixels(img []string) (v int) {
	for _, value := range img {
		v += strings.Count(value, LightPixel.String())
	}
	return
}

func Part1(algo string, img []string, rounds int) (count int) {
	pImage := img
	defaultChar := DarkPixel.String()
	for i := 0; i < rounds; i++ {
		if i%2 != 0 && LightPixel.String() == string(algo[0]) {
			defaultChar = LightPixel.String()
		}
		expImage := GrowImage(pImage, 1, defaultChar)
		pImage = ProcessImage(algo, expImage, defaultChar)
	}
	printImage(pImage)
	fmt.Print("\n\n")
	count = CalcLitPixels(pImage)
	return
}

func main() {
	exampleInput := filepath.Join("2021", "day_20", "example.txt")
	exampleData := util.SplitInputByEmptyLines(exampleInput)
	exampleAlgo, exampleImage := ProcessInput(exampleData)
	exampleResult := Part1(exampleAlgo, exampleImage, 2)
	fmt.Printf("Example: the number of lit pixels is = %v\n\n", exampleResult)
	if exampleResult != 35 {
		panic("FAILED on Example")
	}

	input := filepath.Join("2021", "day_20", "raw-input.txt")
	inputData := util.SplitInputByEmptyLines(input)

	algo, img := ProcessInput(inputData)
	p1Result := Part1(algo, img, 2)
	fmt.Printf("Part I: the number of lit pixels is = %v\n", p1Result)
	if p1Result <= 5245 || p1Result >= 5679 {
		panic("FAILED on Part I")
	}
}
