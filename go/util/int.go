package util

func Add(acc int, v int) int {
	return acc + v
}

func Multiply(acc int, v int) int {
	return acc * v
}

func Sum(nums []int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}

func GaussSum(num int) int {
	return (num * (num + 1)) / 2
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
