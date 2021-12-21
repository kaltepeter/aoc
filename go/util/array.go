package util

func Filter(vs []string, f func(string) bool) []string {
	filtered := make([]string, 0)
	for _, v := range vs {
		if f(v) {
			filtered = append(filtered, v)
		}
	}
	return filtered
}

func DiffArrays(a1 []string, a2 []string) []string {
	delta := []string{}
	var arr1, arr2 []string
	if len(a1) > len(a2) {
		arr1 = a1
		arr2 = a2
	} else {
		arr1 = a2
		arr2 = a1
	}
	for _, x := range arr1 {
		hasVal := false
		for _, y := range arr2 {
			if x == y {
				hasVal = true
				break
			}
		}
		if !hasVal {
			delta = append(delta, x)
		}
	}
	return delta
}

func ArrayContainsCoord(data *[][2]int, coord [2]int) bool {
	for _, c := range *data {
		if c == coord {
			return true
		}
	}
	return false
}

func ArrayContainsString(data *[]string, v string) bool {
	for _, c := range *data {
		if c == v {
			return true
		}
	}
	return false
}
