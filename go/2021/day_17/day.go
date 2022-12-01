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

func Part2(data *TargetArea) (validCount int) {
	// quadratic, solve for drag
	minX := math.Ceil((math.Sqrt(float64(1+data.MinX*8)) - 1) / 2)
	for iY := data.MinY - 1; iY <= -data.MinY; iY++ {
		for iX := int(minX); iX <= data.MaxX; iX++ {
			p := util.Point{X: 0, Y: 0}
			dX, dY := int(iX), int(iY)
			for p.X <= data.MaxX && p.Y >= data.MinY {
				dX, dY = Step(&p, dX, dY)
				if p.X >= data.MinX && p.X <= data.MaxX && p.Y >= data.MinY && p.Y <= data.MaxY {
					validCount++
					break
				}
			}
		}
	}
	return validCount
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
	fmt.Printf("Part II: the total possible velocity combinations = %v\n", p2Result)
	if p2Result != 1546 {
		panic("FAILED on Part II")
	}
}
