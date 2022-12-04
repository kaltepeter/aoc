package main

import (
	"ka/m/util"
	"path/filepath"
	"reflect"
	"testing"
)

func setupTests(filePath string) Game {
	inputExample := filepath.Join(filePath)
	inputData := util.ParseInput(inputExample)
	game := ProcessInput(&inputData)
	return game
}

func TestProcessInput(t *testing.T) {
	inputExample := filepath.Join("example.txt")
	inputData := util.ParseInput(inputExample)

	type args struct {
		data *[]string
	}
	tests := []struct {
		name     string
		args     args
		wantGame Game
	}{
		{name: "should return the game setup with players",
			args: args{
				data: &inputData,
			},
			wantGame: Game{dieRollCount: 1, players: []Player{{name: "Player 1", score: 0, position: 4}, {name: "Player 2", score: 0, position: 8}}},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			gotGame := ProcessInput(tt.args.data)

			if !reflect.DeepEqual(gotGame, tt.wantGame) {
				t.Errorf("ProcessInput() = %v, want %v", gotGame, tt.wantGame)
			}
		})
	}
}

func TestIsGameWon(t *testing.T) {

	type args struct {
		data        *Game
		targetScore int
	}
	tests := []struct {
		name       string
		args       args
		want       bool
		wantWinner Player
	}{
		{name: "should return true if player is over 1000",
			args: args{
				data:        &Game{dieRollCount: 993, players: []Player{{name: "Player 1", score: 1000, position: 10}, {name: "Player 2", score: 745, position: 3}}},
				targetScore: 1000,
			},
			want:       true,
			wantWinner: Player{name: "Player 1", score: 1000, position: 10},
		},
		{name: "should return true if player is over 21",
			args: args{
				data:        &Game{dieRollCount: 21, players: []Player{{name: "Player 1", score: 26, position: 6}, {name: "Player 2", score: 16, position: 7}}},
				targetScore: 21,
			},
			want:       true,
			wantWinner: Player{name: "Player 1", score: 26, position: 6},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			gotIsWon, gotWinner := IsGameWon(tt.args.data, tt.args.targetScore)

			if gotIsWon != tt.want {
				t.Errorf("IsGameWon() = %v, want %v", gotIsWon, tt.want)
			}

			if !reflect.DeepEqual(gotWinner, tt.wantWinner) {
				t.Errorf("IsGameWon() = %v, want %v", gotIsWon, tt.want)
			}
		})
	}
}

func TestRollDice(t *testing.T) {

	type args struct {
		rollCount int
	}
	tests := []struct {
		name      string
		args      args
		wantValue int
		wantErr   error
	}{
		{
			name: "should return 1",
			args: args{
				rollCount: 1,
			},
			wantValue: 1,
		},
		{
			name: "should return 100",
			args: args{
				rollCount: 100,
			},
			wantValue: 100,
		},
		{
			name: "should return 1",
			args: args{
				rollCount: 101,
			},
			wantValue: 1,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			gotValue, _ := RollDice(tt.args.rollCount)

			if !reflect.DeepEqual(gotValue, tt.wantValue) {
				t.Errorf("RollDice() = %v, want %v", gotValue, tt.wantValue)
			}
		})
	}
}

func TestTakeTurn(t *testing.T) {

	type args struct {
		rollCount        int
		startingPosition int
	}
	tests := []struct {
		name         string
		args         args
		wantPosition int
		wantCount    int
	}{
		{
			name: "should return 10",
			args: args{
				startingPosition: 4,
				rollCount:        1,
			},
			wantPosition: 10,
			wantCount:    4,
		},
		{
			name: "should return 1",
			args: args{
				startingPosition: 8,
				rollCount:        4,
			},
			wantPosition: 3,
			wantCount:    7,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			gotValue, gotCount := TakeTurn(tt.args.startingPosition, tt.args.rollCount)

			if !reflect.DeepEqual(gotValue, tt.wantPosition) {
				t.Errorf("TakeTurn() = %v, want %v", gotValue, tt.wantPosition)
			}

			if gotCount != tt.wantCount {
				t.Errorf("TakeTurn() newRollCount = %v, want %v", gotCount, tt.wantCount)
			}
		})
	}
}

func TestCalcLoserScore(t *testing.T) {
	got := CalcLoserScore(&Game{dieRollCount: 994, players: []Player{{name: "Player 1", score: 1000, position: 10}, {name: "Player 2", score: 745, position: 3}}})
	want := 739785
	if got != want {
		t.Errorf(`CalcLoserScore should return %v, got %v`, want, got)
	}
}

func TestPartI(t *testing.T) {
	input := setupTests("example.txt")
	got := Part1(input)
	want := 739785
	if got != want {
		t.Errorf(`Part I should return %v, got %v`, want, got)
	}
}

func SkipTestPartII(t *testing.T) {
	input := setupTests("example.txt")
	got := Part2(input)
	want := int64(444356092776315)
	if got != want {
		t.Errorf(`Part II should return %v, got %v`, want, got)
	}
}
