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

https://www.youtube.com/watch?v=ndAfWKmKF34

- Use binary: 1st bit is alive or dead, next bits are neighbor values
- Start with active cells, for each active set true and set neighbor count +1
- use pos as map lookup key

parallel? the run could divide and conquer

http://www.jagregory.com/abrash-black-book/#bringing-in-the-right-brain

11001
11110 // &
11000

01
10

point = x,y,z

cube state = cs[z][x][y], z is the slice

starting with 2d --> convert to 3d

string[x][y] = string[z][x][y]

z starts as zero in docs, but could be 1, the pos offset would be z - 1 or 0 for previous state

mask : 1110
val : 0
increment neighbor

1 << 0

getBitMask

getLastBitSet(v)
num.toString(2).padStart(36, '0');

get first bit
get last bit set
build a mask for this

if v = 1110, mask is 1110
if v = 0 mask is 0
if v = 1 mask is 0
if v is 111111, mask is 111110

prevent changing first bit and all left shift
