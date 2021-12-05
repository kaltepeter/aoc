package util

import (
	"regexp"
	"strconv"
	"strings"
)

const DEFAULT_SEP = ","

func ToListOfInt(data []string) []int {
	nums := []int{}
	for _, n := range data {
		num, _ := strconv.Atoi(n)
		nums = append(nums, num)
	}
	return nums
}

func StringToListOfInt(s string) []int {
	data := strings.Split(s, DEFAULT_SEP)
	return ToListOfInt(data)
}

func StringToListOfIntWithSeparator(s string, sep string) []int {
	regexDelim := regexp.MustCompile(sep)
	data := regexDelim.Split(strings.Trim(s, " \n"), -1)
	return ToListOfInt(data)
}

func StringToListOfString(s string) []string {
	data := strings.Split(s, DEFAULT_SEP)
	return data
}

func StringToListOfStringWithSeparator(s string, sep string) []string {
	regexDelim := regexp.MustCompile(sep)
	data := regexDelim.Split(strings.Trim(s, " \n"), -1)
	return data
}
