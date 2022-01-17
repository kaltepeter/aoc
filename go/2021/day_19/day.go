package main

import (
	"fmt"
	"ka/m/linear"
	"ka/m/util"
	"math"
	"path/filepath"
	"reflect"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"sync"

	"gonum.org/v1/gonum/mat"
)

type Coord struct {
	X int
	Y int
	Z int
}

type IntAdjList struct {
	Pos     int
	AdjList [][]int
}

func NewIntAdjList(coord int, other [][]int) (c IntAdjList) {
	c.Pos = coord
	c.AdjList = append(c.AdjList, other...)
	return
}

// https://codeburst.io/slice-based-stack-implementation-in-golang-8140603a1dc2
type CoordStack struct {
	items  []Coord
	rwLock sync.RWMutex
}

func (stack *CoordStack) Push(t Coord) {
	if stack.items == nil {
		stack.items = []Coord{}
	}
	stack.rwLock.Lock()
	stack.items = append(stack.items, t)
	stack.rwLock.Unlock()
}

func (stack *CoordStack) Pop() *Coord {
	if len(stack.items) == 0 {
		return nil
	}
	stack.rwLock.Lock()
	item := stack.items[len(stack.items)-1]
	stack.items = stack.items[0 : len(stack.items)-1]
	stack.rwLock.Unlock()
	return &item
}

func (stack *CoordStack) Size() int {
	stack.rwLock.RLock()
	defer stack.rwLock.RUnlock()
	return len(stack.items)
}

func (stack *CoordStack) All() []Coord {
	stack.rwLock.RLock()
	defer stack.rwLock.RUnlock()
	return stack.items
}

func (stack *CoordStack) IsEmpty() bool {
	stack.rwLock.RLock()
	defer stack.rwLock.RUnlock()
	return len(stack.items) == 0
}

type Pair struct {
	Left   *Pair
	Right  *Pair
	Parent *Pair
	Depth  int
	Value  int
}

func (p *Pair) String() string {
	return fmt.Sprintf("Left: %v Right: %v Depth: %d VAlue: %d", p.Left, p.Right, p.Depth, p.Value)
}

func (c Coord) String() string {
	return fmt.Sprintf("[%d,%d,%d]", c.X, c.Y, c.Z)
}

func (c *Coord) RotateCoord(xDir, yDir, zDir int) *Coord {
	return &Coord{
		X: c.X + xDir,
		Y: c.Y + yDir,
		Z: c.Z + zDir,
	}
}

func calcCombos(g *IntAdjList) (cList []Coord) {
	coord := &Coord{
		X: g.Pos,
	}
	p1 := g.AdjList[0]
	p2 := g.AdjList[1]
	coord.Y = p1[0]
	coord.Z = p2[0]
	cList = append(cList, *coord)
	coord.Y = p1[1]
	coord.Z = p2[1]
	cList = append(cList, *coord)
	coord.Y = p1[0]
	coord.Z = p2[1]
	cList = append(cList, *coord)
	coord.Y = p1[1]
	coord.Z = p2[0]
	cList = append(cList, *coord)
	return
}

// Not needed if using the Norm to match coords
func (c *Coord) GetAllRotations() map[Coord]bool {
	coords := map[Coord]bool{}
	pairs := [][]int{{c.X, c.X * -1}, {c.Y, c.Y * -1}, {c.Z, c.Z * -1}}
	for i, c := range pairs {
		pList := [][]int{}
		if i > 0 {
			pList = append(pList, pairs[:i]...)
		}
		if i < len(pairs)-1 {
			pList = append(pList, pairs[i+1:]...)
		}
		cListL := NewIntAdjList(c[0], pList)
		cListR := NewIntAdjList(c[1], pList)
		adjList := calcCombos(&cListL)
		adjList = append(adjList, calcCombos(&cListR)...)
		for _, c := range adjList {
			coords[c] = true
		}
	}

	return coords
}

type Scanner struct {
	Name       int // `default:"27"`
	Pos        Coord
	Beacons    []Beacon
	BeaconDist map[[2]int]float64
}

func CalcL2Norm(vect [3]int) float64 {
	return math.Sqrt(math.Pow(float64(vect[0]), 2) + math.Pow(float64(vect[1]), 2) + math.Pow(float64(vect[2]), 2))
}

func CalcSquaredNorm(vect [3]float64) float64 {
	return math.Pow(float64(vect[0]), 2) + math.Pow(float64(vect[1]), 2) + math.Pow(float64(vect[2]), 2)
}

func (s *Scanner) SetBeaconDist() {
	beaconDist := map[[2]int]float64{}
	for i := 0; i < len(s.Beacons)-1; i++ {
		for j := i + 1; j < len(s.Beacons); j++ {
			// beaconDist = append(beaconDist, Coord{
			//   X:
			// })
			cb := s.Beacons[i]
			curBeacon := [3]float64{float64(cb.Pos.X), float64(cb.Pos.Y), float64(cb.Pos.Z)}
			// curBeacon := [3]float64{math.Abs(float64(cb.Pos.X)), math.Abs(float64(cb.Pos.Y)), math.Abs(float64(cb.Pos.Z))}
			// sort.Float64s(curBeacon[:])
			nb := s.Beacons[j]
			nextBeacon := [3]float64{float64(nb.Pos.X), float64(nb.Pos.Y), float64(nb.Pos.Z)}
			// nextBeacon := [3]float64{math.Abs(float64(nb.Pos.X)), math.Abs(float64(nb.Pos.Y)), math.Abs(float64(nb.Pos.Z))}
			// sort.Float64s(nextBeacon[:])
			curVect := mat.NewVecDense(3, curBeacon[:])
			nextVect := mat.NewVecDense(3, nextBeacon[:])
			distVect := mat.NewVecDense(3, nil)
			distVect.SubVec(curVect, nextVect)
			dist := CalcSquaredNorm([3]float64{distVect.AtVec(0), distVect.AtVec(1), distVect.AtVec(2)})
			// dist := mat.Norm(distVect, 2)
			// dist := mat.Norm(curVect, 2) - mat.Norm(nextVect, 2)
			beaconDist[[2]int{i, j}] = dist
			beaconDist[[2]int{j, i}] = dist
		}
	}
	s.BeaconDist = beaconDist
}

type CoordPair struct {
	Key   [2]int
	Value float64
}

type CoordPairList []CoordPair

func (p CoordPairList) Len() int { return len(p) }
func (p CoordPairList) Swap(i, j int) {
	p[i], p[j] = p[j], p[i]
}
func (p CoordPairList) Less(i, j int) bool {
	return p[i].Value < p[j].Value
}

func (s *Scanner) FindCommonBeacons(s2 *Scanner) (matchedCoords [][2]Coord) {
	// count := 0
	// d1Set := map[float64][][2]int{}
	// d2Set := map[float64][][2]int{}

	d1Sorted := make(CoordPairList, len(s.BeaconDist))
	i := 0
	for k, v := range s.BeaconDist {
		d1Sorted[i] = CoordPair{k, v}
		i++
	}
	sort.Sort(d1Sorted)

	d2Sorted := make(CoordPairList, len(s2.BeaconDist))
	i = 0
	for k, v := range s2.BeaconDist {
		d2Sorted[i] = CoordPair{k, v}
		i++
	}
	sort.Sort(d2Sorted)
	// pList := map[int]int{}

	foundMap := map[int]map[int]int{}

	// get list of overlaps
	for _, cp1 := range d1Sorted {
		for _, cp2 := range d2Sorted {
			d1, d1Key := cp1.Value, cp1.Key
			d2, d2Key := cp2.Value, cp2.Key
			sort.Ints(d1Key[:])
			sort.Ints(d2Key[:])

			// will find 66 combos, 12 choose 2 is 66
			if d1 == d2 {
				if _, hasD1Key0 := foundMap[d1Key[0]]; !hasD1Key0 {
					foundMap[d1Key[0]] = map[int]int{}
				}
				if _, hasD1Key1 := foundMap[d1Key[1]]; !hasD1Key1 {
					foundMap[d1Key[1]] = map[int]int{}
				}
				foundMap[d1Key[0]][d2Key[0]] += 1
				foundMap[d1Key[0]][d2Key[1]] += 1
				foundMap[d1Key[1]][d2Key[0]] += 1
				foundMap[d1Key[1]][d2Key[1]] += 1

				// d1Set[d1] = append(d1Set[d1], d1Key)
				// d2Set[d2] = append(d2Set[d2], d2Key)
				// count++
			}
		}
	}
	for k, v := range foundMap {
		for k2, v2 := range v {
			if v2 > 4 { // should be 44? 66 - 12...
				matchedCoords = append(matchedCoords, [2]Coord{s.Beacons[k].Pos, s2.Beacons[k2].Pos})
			}
		}
	}

	return
}

func (coord *Beacon) TranslatePosition(R *mat.Dense, c float64, t *mat.Dense) {
	// [t + c * R @ coord]
	var cScaleR mat.Dense
	cScaleR.Scale(c, R)
	var newVec mat.VecDense
	b := mat.NewVecDense(3, []float64{float64(coord.Pos.X), float64(coord.Pos.Y), float64(coord.Pos.Z)})
	newVec.MulVec(&cScaleR, b)
	var newPos mat.Dense
	newPos.Add(t, &newVec)
	(*coord).Pos = Coord{X: int(math.Round(newPos.At(0, 0))), Y: int(math.Round(newPos.At(1, 0))), Z: int(math.Round(newPos.At(2, 0)))}
}

func (s *Scanner) Translate(s2 *Scanner, matchedCoords [][2]Coord) (position Coord) {
	leftCoords, rightCoords := [][]float64{}, [][]float64{}
	for _, v := range matchedCoords {
		leftCoords = append(leftCoords, []float64{float64(v[0].X), float64(v[0].Y), float64(v[0].Z)})
		rightCoords = append(rightCoords, []float64{float64(v[1].X), float64(v[1].Y), float64(v[1].Z)})
	}
	// flip right and left, left is destination
	R, c, t := linear.Umeyama(rightCoords, leftCoords)
	for i, coord := range (*s).Beacons {
		coord.TranslatePosition(R, c, t)
		newPos := &coord
		(*s).Beacons[i] = *newPos
	}

	var pos []int
	for _, v := range t.RawMatrix().Data {
		pos = append(pos, int(math.Round(v)))
	}

	position = Coord{X: pos[0], Y: pos[1], Z: pos[2]}
	(*s).Pos = position

	return
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
		} else {
			scanner.Beacons = beacons
			scannerData = append(scannerData, scanner)
		}
	}
	scanner.Beacons = beacons
	scannerData = append(scannerData, scanner)
	return scannerData
}

func ProcessScanners(data []Scanner) []Scanner {
	scanners := data[:]
	for i, _ := range scanners {
		scanners[i].SetBeaconDist()
	}

	known := []Scanner{scanners[0]}
	zeroPos := &Coord{X: 0, Y: 0, Z: 0}

	for len(known) < len(scanners) {
		for i := 0; i < len(known); i++ {
			s := known[i]
			for j := 0; j < len(scanners); j++ {
				p := &scanners[j]
				if !reflect.DeepEqual(p.Pos, *zeroPos) || p.Name == 0 {
					continue
				}
				if p.Name == s.Name {
					continue
				}
				if pairs := p.FindCommonBeacons(&s); len(pairs) == 12 {
					p.Translate(&s, pairs)
					known = append(known, *p)
					break
				}
			}
		}
	}
	return scanners
}

func Part1(scanners []Scanner) int {
	uniqueBeacons := map[Coord]int{}
	for _, s := range scanners {
		for _, b := range s.Beacons {
			uniqueBeacons[b.Pos] += 1
		}
	}

	return len(uniqueBeacons)
}

func Part2(scanners []Scanner) (manhattenDist int) {
	for _, s := range scanners {
		v1 := mat.NewVecDense(3, []float64{float64(s.Pos.X), float64(s.Pos.Y), float64(s.Pos.Z)})
		for _, s2 := range scanners {
			if s.Name == s2.Name {
				continue
			}
			v2 := mat.NewVecDense(3, []float64{float64(s2.Pos.X), float64(s2.Pos.Y), float64(s2.Pos.Z)})
			var res mat.VecDense
			res.SubVec(v2, v1)
			sum := 0
			for _, v := range res.RawVector().Data {
				sum += int(math.Abs(v))
			}
			manhattenDist = int(math.Max(float64(manhattenDist), float64(sum)))
		}
	}

	return
}

func main() {
	input := filepath.Join("2021", "day_19", "raw-input.txt")
	inputData := util.ParseInput(input)
	scannerData := ProcessInput(&inputData)

	// process scanners
	scanners := ProcessScanners(scannerData)

	p1Result := Part1(scanners)
	fmt.Printf("Part I: the number of unique beacons is = %v\n", p1Result)
	if p1Result != 350 {
		panic("FAILED on Part I")
	}

	p2Result := Part2(scanners)
	fmt.Printf("Part II: the largest manhatten distance is = %v\n", p2Result)
	if p2Result != 10895 {
		panic("FAILED on Part II")
	}
}
