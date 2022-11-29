# Solution

## Data

Players: name (1,2), starting position, score
Game: round (1+), players
board: 1-10

## calc

deterministic dice : round % 100 (0 == 100)
winner : player.score >= 1000
answer : loser.score \* rounds
space : position % 10

## func/approach

1. setup game
1. read input, setup players
1. run round
   1. roll dice, move player 1
   1. check winner
   1. roll dice, move player 2
   1. check winner
   1. increase round
1. repeat until won
1. get answer
