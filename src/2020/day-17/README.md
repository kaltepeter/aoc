# Day 17

abc
def
ghi

jkl
mno
pqr

stu
vwx
yzA

j neighbors = abdekmnstvw
n neighbors = abcdefghijklmopqrstuvwxyzA

```
Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


```

0,0,0
0,0,-1
0,0,1
0,1,0
0,-1,0
0,-1,0

-1,-1,-1
0,0,0
1,1,1

```javascript
[
  [-1, -1, -1],
  [0, 0, 0],
  [1, 1, 1],
][(-1, -1, -1)];
```

[1,2,3]
pos 1: one of three vals

[0, [1,2,3], [2,3,4]]
[1, [1,2,3], [2,3,4]]
[2, [1,2,3], [2,3,4]]

pos 2: one of three vals

[[0,1,2], 1, [2,3,4]]
[[0,1,2], 2, [2,3,4]]
[[0,1,2], 3, [2,3,4]]

pos 3: one of three vals

[[0,1,2], [1,2,3], 2]
[[0,1,2], [1,2,3], 3]
[[0,1,2], [1,2,3], 4]

return if pos 1 = -1, all combos of other 2 possible values

1. Find all active cubes for a slice
2. For each active cube find all neighbors
3. Create a set of all neighbors of active cubes
4. Loop through set of all neighbors of active cubes
5. Calculate immediate neighbors and get the active cubes of the set.
6. split lists and set vals

Run Cycles

1. start with a slice, calc dimension
