package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
)

type Coord struct {
	X int
	Y int
	Z int
}

func (c Coord) String() string {
	return fmt.Sprintf("[%d,%d,%d]", c.X, c.Y, c.Z)
}

type Scanner struct {
	Name    int // `default:"27"`
	Pos     Coord
	Beacons []Beacon
}

func NewScanner() *Scanner {
	return &Scanner{
		Name:    -1,
		Beacons: []Beacon{},
	}
}

func (s Scanner) String() string {
	return fmt.Sprintf("[Scanner %d] Pos: %s %d Beacons", s.Name, s.Pos.String(), len(s.Beacons))
}

func (s *Scanner) Exists() bool {
	exists := false
	if s.Name != -1 && len(s.Beacons) > 0 {
		exists = true
	}
	return exists
}

type Beacon struct {
	Pos Coord
}

func (b Beacon) String() string {
	return fmt.Sprintf("%v", b.Pos)
}

type ScannerData struct {
	Scanners []Scanner
	Beacons  []Beacon
}

func (sd *ScannerData) String() string {
	return fmt.Sprintf("Scanners: %v, Beacons: %v", sd.Scanners, sd.Beacons)
}

const (
	MAX_DISTANCE = 1000
)

func ProcessInput(data *[]string) []Scanner {
	scannerData := []Scanner{}
	isCoordRegex := regexp.MustCompile(`^\d|-`)
	var scanner Scanner
	var beacons []Beacon
	for _, line := range *data {
		if strings.Contains(line, "---") {
			name := -1
			fmt.Sscanf(line, "--- scanner %d ---", &name)
			scanner = *NewScanner()
			beacons = []Beacon{}
			scanner.Name = name
		} else if isCoordRegex.MatchString(line) {
			coords := strings.Split(line, ",")
			x, _ := strconv.ParseInt(coords[0], 10, 64)
			y, _ := strconv.ParseInt(coords[1], 10, 64)
			z, _ := strconv.ParseInt(coords[2], 10, 64)
			beacons = append(beacons, Beacon{
				Pos: Coord{
					X: int(x),
					Y: int(y),
					Z: int(z),
				},
			})
		} else if line == "" {
			scanner.Beacons = beacons
			scannerData = append(scannerData, scanner)
		}
	}
	return scannerData
}

func Part1(data *[]Scanner) int {
	for _, s := range *data {
		fmt.Println(s)
	}
	return 0
}

func Part2(data *[]Scanner) int {
	return 0
}

func main() {
	input := filepath.Join("2021", "day_19", "raw-input.txt")
	inputData := util.ParseInput(input)
	riskData := ProcessInput(&inputData)
	p1Result := Part1(&riskData)
	fmt.Printf("Part I: the number of beacons is = %v\n", p1Result)
	if p1Result != 562 {
		panic("FAILED on Part I")
	}

	p2Result := Part2(&riskData)
	fmt.Printf("Part II: the lowest risk path level is = %v\n", p2Result)
	if p2Result != 2874 {
		panic("FAILED on Part II")
	}
}
