package main

import (
	"fmt"
	"ka/m/util"
	"net/http"
	_ "net/http/pprof"
	"path/filepath"
)

type processedFish struct {
	fish         []int8
	newFishCount int
}

type fishcounter [9]int

const NEW_FISH = 8
const OLD_FISH_NEW_CYCLE = 6

func ProcessFishTimers(fishes []int8) processedFish {
	newFish := 0

	for idx, fishTimer := range fishes {
		if fishTimer == 0 {
			fishes[idx] = 6
			newFish += 1
		} else {
			fishes[idx] -= 1
		}
	}
	return processedFish{fish: fishes, newFishCount: newFish}
}

func ProcessFishTimersII(fishes []int) fishcounter {
	updatedFish := fishcounter{}
	copy(updatedFish[:], fishes)
	for idx, count := range fishes {
		if idx == 0 {
			updatedFish[OLD_FISH_NEW_CYCLE] += count
			updatedFish[NEW_FISH] += count
			updatedFish[idx] -= count
		} else {
			updatedFish[idx-1] += count
			updatedFish[idx] -= count

		}
	}
	return updatedFish
}

func countFish(fishes fishcounter) int {
	total := 0
	for _, fish := range fishes {
		total += int(fish)
	}
	return total
}

func Part1(data []int, days int) int {
	go func() {
		_ = http.ListenAndServe("0.0.0.0:8081", nil)
	}()
	fishes := fishcounter{}
	for _, fishTimer := range data {
		fishes[fishTimer] += 1
	}

	fmt.Println(countFish(fishes))

	for day := 0; day < days; day++ {
		fishes = ProcessFishTimersII(fishes[:])
		// fishes[NEW_FISH] += newFishCount
		// fmt.Printf("day: %v fish:  %v\n", day, fishes)
		// fishes = result
		// 	results := []int8{}
		// 	results = append(results, result.fish...)
		// 	if result.newFishCount > 0 {
		// 		for i := 0; i < result.newFishCount; i++ {
		// 			results = append(results, 8)
		// 		}
		// 	}
		// 	fishes = results
	}
	return countFish(fishes)
}

func main() {
	input := filepath.Join("2021", "day_6", "raw-input.txt")
	inputData := util.ParseInput(input)
	listOfInts := util.StringToListOfInt(inputData[0])
	p1Result := Part1(listOfInts, 80) // 345793
	fmt.Printf("Part I: Number of fish %d\n", p1Result)

	p2Result := Part1(listOfInts, 256) // 1572643095893
	fmt.Printf("Part II: Number of fish %d\n", p2Result)
}
