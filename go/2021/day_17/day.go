package main

import (
	"fmt"
	"ka/m/util"
	"math"
	"path/filepath"
)

type TargetArea struct {
	MinX int
	MaxX int
	MinY int
	MaxY int
}

const (
	PROBE       = "#"
	START       = "S"
	TARGET_AREA = "T"
	EMPTY       = "."
)

// func PrintView(p util.Point, ta TargetArea) {
// 	viewMaxY := int(math.Abs(float64(ta.MaxY)))
// 	viewMinY := int(math.Abs(float64(ta.MinY)))
// 	viewMaxX := int(math.Abs(float64(ta.MaxX)))
// 	viewMinX := int(math.Abs(float64(ta.MinX)))
// 	maxY := viewMinY + viewMaxY
// 	maxX := viewMinX + viewMaxX
// 	view := make([][]string, maxY)
// 	for idx, _ := range view {
// 		r := make([]string, maxX)
// 		for cIdx := range r {
// 			r[cIdx] = EMPTY
// 		}
// 		view[idx] = r
// 	}
// 	view[p.Y][p.X] = PROBE
// 	for y := viewMinY; y < int(viewMaxY); y++ {
// 		for x := viewMinX; x < int(viewMaxX); x++ {
// 			view[y][x] = TARGET_AREA
// 		}
// 	}
// 	for _, row := range view {
// 		fmt.Println(strings.Join(row, ""))
// 	}
// }

func ProcessInput(data *string) TargetArea {
	var minX, maxX, minY, maxY int
	fmt.Sscanf(*data, "target area: x=%d..%d, y=%d..%d", &minX, &maxX, &minY, &maxY)
	return TargetArea{
		MinX: minX,
		MaxX: maxX,
		MinY: minY,
		MaxY: maxY,
	}
}

func Step(p *util.Point, xV int, yV int) (int, int) {
	p.X += xV
	p.Y += yV
	if xV > 0 {
		xV -= 1
	} else if xV < 0 {
		xV += 1
	}
	yV -= 1
	return xV, yV
}

func Part1(data *TargetArea) int {
	biggestY := int(math.Abs(float64(data.MaxY)))
	if int(math.Abs(float64(data.MinY))) > biggestY {
		biggestY = int(math.Abs(float64(data.MinY)))
	}
	x := biggestY - 1
	y := biggestY
	return x * y / 2 // triangle number
}

func Part2(data *TargetArea) int {
	return 0
}

func main() {
	input := filepath.Join("2021", "day_17", "raw-input.txt")
	inputData := util.ParseInput(input)
	targetArea := ProcessInput(&inputData[0])
	p1Result := Part1(&targetArea)
	fmt.Printf("Part I: the highest y value is = %v\n", p1Result)
	if p1Result != 4753 {
		panic("FAILED on Part I")
	}

	p2Result := Part2(&targetArea)
	fmt.Printf("Part II: the lowest risk path level is = %v\n", p2Result)
	if p2Result != 2874 {
		panic("FAILED on Part II")
	}
}
