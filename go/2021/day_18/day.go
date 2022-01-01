package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"strconv"
)

type Pair struct {
	Left   interface{}
	Right  interface{}
	Parent *Pair
	Depth  int
}

func (p *Pair) String() string {
	return fmt.Sprintf("[%v,%v]", p.Left, p.Right)
}

func Add(a *Pair, b *Pair) *Pair {
	p := &Pair{
		Parent: nil,
		Depth:  0,
		Left:   a,
		Right:  b,
	}
	a.Parent = p
	b.Parent = p
	incDepth(a)
	incDepth(b)
	reduce(p)
	return p
}

func (p *Pair) CalcMagnitude() int {
	var l, r int
	switch v := p.Left.(type) {
	case *Pair:
		l = v.CalcMagnitude()
	case *Num:
		l = v.Value
	}
	switch v := p.Right.(type) {
	case *Pair:
		r = v.CalcMagnitude()
	case *Num:
		r = v.Value
	}
	return 3*l + 2*r
}

func reduce(p *Pair) *Pair {
	modified := true
	for modified {
		modified = false

		it := flattenPairValues(p)
		for i, v := range it {
			if v.Depth > 4 {
				// explode
				if i > 0 {
					it[i-1].Value += v.Value
				}
				if i < len(it)-2 {
					it[i+2].Value += it[i+1].Value
				}
				parent := v.Parent
				if parent.Parent.Left == parent {
					parent.Parent.Left = &Num{
						Parent: parent.Parent,
						Depth:  parent.Depth,
						Value:  0,
					}
				} else {
					parent.Parent.Right = &Num{
						Parent: parent.Parent,
						Depth:  parent.Depth,
						Value:  0,
					}
				}
				modified = true
				break
			}
		}
		if modified {
			continue
		}
		for _, v := range it {
			if v.Value >= 10 {
				p := &Pair{
					Parent: v.Parent,
					Depth:  v.Depth,
				}
				p.Left = &Num{
					Parent: p,
					Depth:  p.Depth + 1,
					Value:  v.Value / 2,
				}
				p.Right = &Num{
					Parent: p,
					Depth:  p.Depth + 1,
					Value:  (v.Value + 1) / 2,
				}
				if v.Parent.Left == v {
					v.Parent.Left = p
				} else {
					v.Parent.Right = p
				}
				modified = true
				break
			}
		}
	}
	return p
}

func flattenPairValues(p *Pair) []*Num {
	var out []*Num
	switch v := p.Left.(type) {
	case *Num:
		out = append(out, v)
	case *Pair:
		out = append(out, flattenPairValues(v)...)
	}
	switch v := p.Right.(type) {
	case *Num:
		out = append(out, v)
	case *Pair:
		out = append(out, flattenPairValues(v)...)
	}
	return out
}

func incDepth(p *Pair) {
	p.Depth++
	switch p2 := p.Left.(type) {
	case *Pair:
		incDepth(p2)
	case *Num:
		p2.Depth++
	}
	switch p2 := p.Right.(type) {
	case *Pair:
		incDepth(p2)
	case *Num:
		p2.Depth++
	}
}

type Num struct {
	Value  int
	Parent *Pair
	Depth  int
}

func (n *Num) String() string {
	return fmt.Sprintf("%d", n.Value)
}

type Stream struct {
	s   string
	pos int
}

func NewStream(s string) *Stream {
	return &Stream{
		s:   s,
		pos: 0,
	}
}

func (s *Stream) Next() string {
	out := string(s.s[s.pos])
	s.pos++
	return out
}

func NewPair(s string) *Pair {
	o := parseValue(NewStream(s), nil, 0)
	switch v := o.(type) {
	case *Pair:
		return v
	default:
		panic(s)
	}
}

func parseValue(data *Stream, parent *Pair, depth int) interface{} {
	next := data.Next()
	switch next {
	case "[":
		p := &Pair{Parent: parent, Depth: depth}
		p.Left = parseValue(data, p, depth+1)
		data.Next()
		p.Right = parseValue(data, p, depth+1)
		data.Next()
		return p
	default:
		i, _ := strconv.Atoi(next)
		return &Num{
			Value:  i,
			Parent: parent,
			Depth:  depth,
		}
	}
}

func Part1(data []string) int {
	p := NewPair(data[0])
	for i := 1; i < len(data); i++ {
		p = Add(p, NewPair(data[i]))
	}
	return p.CalcMagnitude()
}

func Part2(data []string) (largestMag int) {
	for i := 0; i < len(data); i++ {
		for j := 1; j < len(data); j++ {
			sum1 := Add(NewPair(data[i]), NewPair(data[1]))
			mag1 := sum1.CalcMagnitude()
			if mag1 > largestMag {
				largestMag = mag1
			}
			sum2 := Add(NewPair(data[j]), NewPair(data[i]))
			mag2 := sum2.CalcMagnitude()
			if mag2 > largestMag {
				largestMag = mag2
			}
		}
	}
	return
}

func main() {
	input := filepath.Join("2021", "day_18", "raw-input.txt")
	inputData := util.ParseInput(input)
	// mathHomework := ProcessInput(&inputData)
	p1Result := Part1(inputData)
	fmt.Printf("Part I: the magnitude of the final sum is = %v\n", p1Result)
	if p1Result != 4120 {
		panic("FAILED on Part I")
	}

	p2Result := Part2(inputData)
	fmt.Printf("Part II: the larget pair magnitdue is = %v\n", p2Result)
	if p2Result != 4725 {
		panic("FAILED on Part II")
	}
}
