package util

func ReduceInt(nums []int, f func(int, int) int, start int) int {
	res := start
	for _, v := range nums {
		res = f(res, v)
	}
	return res
}

type Coord [2]int

type Point struct {
	X int
	Y int
}
