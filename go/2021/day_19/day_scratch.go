package main

type IntAdjList struct {
	Pos     int
	AdjList [][]int
}

func NewIntAdjList(coord int, other [][]int) (c IntAdjList) {
	c.Pos = coord
	c.AdjList = append(c.AdjList, other...)
	return
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
