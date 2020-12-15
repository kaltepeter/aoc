# day 11

```text
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
```

LLL
LLL
LLL

i - 1, i, i + 1
i - 1, i, i + 1
i - 1, i, i + 1

Part II

Can see 8 occupied seats.

```text
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
```

[0,7], [1,3], [2,1], [4,2], [4,8], [5,4], [7,0], [8,3]

POS: [4,3]

- row 4, can see any spot in row 4, closest wins
- col 3, can see any spot in col 3, +- closest wins
  // cols
  // loop until found
- row - 1, col - 1, in bounds count em
- row + 1, col - 1, in bounds count em
- row - 1, col + 1, in bounds count em
- row + 1, col + 1, in bounds count em

loop three values per row, row - n, col - n, row - n col, row - n, col +1
row, col - n, row col + n
row + n, col - n, row + n col, row + n col + 1

loop through and store positions of found seats

if any visiblly adjacent seat is occupied, empty the seat

```text
 foundSeats {
      rows: {
        '0': [ 7 ],
        '1': [ 3 ],
        '2': [ 1 ],
        '4': [ 2, 8 ],
        '5': [ 4 ],
        '7': [ 0 ],
        '8': [ 3 ]
      },
      cols: {
        '0': [ 7 ],
        '1': [ 2 ],
        '2': [ 4 ],
        '3': [ 1, 8 ],
        '4': [ 5 ],
        '7': [ 0 ],
        '8': [ 4 ]
      }
    }
```
