package util

func ReduceInt(nums []int, f func(int, int) int, start int) int {
	res := start
	for _, v := range nums {
		res = f(res, v)
	}
	return res
}
