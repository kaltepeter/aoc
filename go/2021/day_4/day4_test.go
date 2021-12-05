package main

import (
	"ka/m/util"
	"path/filepath"
	"reflect"
	"testing"
)

func setupTests() bingogames {
	inputExample := filepath.Join("example.txt")
	inputData := util.ParseInput(inputExample)
	return GetGameData(inputData)
}

func TestMarkBoards(t *testing.T) {
	input := []string{"7,4,9,5,11", "", "22 13 17 11  0", " 8  2 23  4 24", "", " 3 15  0  2 22", " 9 18 13 17  5"}
	gameData := GetGameData(input)
	MarkBoards(&gameData, "11")
	got := gameData
	card1 := card{[]string{"22", "13", "17", "X", "0"}, []string{"8", "2", "23", "4", "24"}}
	card2 := card{[]string{"3", "15", "0", "2", "22"}, []string{"9", "18", "13", "17", "5"}}
	want := bingogames{
		numbers: []string{"7", "4", "9", "5", "11"},
		cards:   []card{card1, card2},
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`GetGameData should return cards %v, got %v`, want.cards, got.cards)
	}
}

func TestGetGameData(t *testing.T) {
	input := []string{"7,4,9,5,11", "", "22 13 17 11  0", " 8  2 23  4 24", "", " 3 15  0  2 22", " 9 18 13 17  5"}
	got := GetGameData(input)
	card1 := card{[]string{"22", "13", "17", "11", "0"}, []string{"8", "2", "23", "4", "24"}}
	card2 := card{[]string{"3", "15", "0", "2", "22"}, []string{"9", "18", "13", "17", "5"}}
	want := bingogames{
		numbers: []string{"7", "4", "9", "5", "11"},
		cards:   []card{card1, card2},
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf(`GetGameData should return numbers %v, got %v`, want.numbers, got.numbers)
		t.Errorf(`GetGameData should return cards %v, got %v`, want.cards, got.cards)
	}
}

func TestCheckBoardWhenRowSuccessful(t *testing.T) {
	input := card{[]string{"X", "X", "X", "X", "X"}, []string{"8", "2", "23", "4", "24"}}
	got := CheckBoard(input)
	want := true
	if got != want {
		t.Errorf(`CheckBoard should return %t for card, got %t`, want, got)
	}
}

func TestCheckBoardWhenRowNotSuccessful(t *testing.T) {
	input := card{[]string{"X", "13", "17", "11", "0"}, []string{"8", "X", "X", "X", "X"}}
	got := CheckBoard(input)
	want := false
	if got != want {
		t.Errorf(`CheckBoard should return %t for card, got %t`, want, got)
	}
}

func TestCheckBoardWhenColSuccessful(t *testing.T) {
	input := card{[]string{"22", "13", "X", "11", "0"}, []string{"8", "2", "X", "4", "24"}}
	got := CheckBoard(input)
	want := true
	if got != want {
		t.Errorf(`CheckBoard should return %t for card, got %t`, want, got)
	}
}

func TestCheckBoardWhenColNotSuccessful(t *testing.T) {
	input := card{[]string{"X", "13", "17", "11", "0"}, []string{"8", "2", "X", "4", "24"}}
	got := CheckBoard(input)
	want := false
	if got != want {
		t.Errorf(`CheckBoard should return %t for card, got %t`, want, got)
	}
}

func TestHandleWinner(t *testing.T) {
	input := card{[]string{"22", "13", "X", "11", "0"}, []string{"8", "2", "X", "4", "24"}}
	got := HandleWinner(input, "22")
	want := (22 + 13 + 11 + 8 + 2 + 4 + 24) * 22
	if got != want {
		t.Errorf(`HandleWinner should return %d for card, got %d`, want, got)
	}
}

func TestExamplePartI(t *testing.T) {
	input := setupTests()
	got := Part1(input)
	want := 4512
	if got != want {
		t.Errorf(`Part I should return %d for card, got %d`, want, got)
	}
}

func TestExamplePartII(t *testing.T) {
	input := setupTests()
	got := Part2(input)
	want := 1924
	if got != want {
		t.Errorf(`Part II should return %d for card, got %d`, want, got)
	}
}
