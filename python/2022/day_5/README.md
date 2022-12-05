# Day 5

## Data

Stack

Stack = List[str] in reverse order, top is position 0
Stacks = List[Stack]
move tuple (count, from, to)
Move = Tuple[int, int, int]
Moves = List[Move]

## Calc

get_top_of_stacks -> string of top boxes after moves

## Func/Approach

1. process input into Stacks and moves
1. loop through the list of moves and execute each move
1. collect the top of each stack as output
