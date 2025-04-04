# day 10

```JSON
    '1': [ 4 ],
    '4': [ 5, 1, 7, 6 ],
    '5': [ 7, 6, 4 ],
    '6': [ 5, 7, 4 ],
    '7': [ 10, 5, 6, 4 ],
    '10': [ 11, 7, 12 ],
    '11': [ 10, 12 ],
    '12': [ 10, 15, 11 ],
    '15': [ 16, 12 ],
    '16': [ 15, 19 ],
    '19': [ 16 ]

    '4': [ 5, 7, 6 ],
    '5': [ 7, 6 ],
    '6': [ 5, 7 ],
    '7': [ 10, 5, 6],
    '10': [ 11, 7, 12 ],
    '11': [ 10, 12 ],
    '12': [ 10, 15, 11 ],
    '15': [ 12 ],
    '16': [ 15 ],

    '4': [ 5, 7, 6 ],
    '5': [ 7, 6 ],
    '6': [ 5, 7 ],
    '7': [ 10, 5, 6],
    '10': [ 11, 7,],
    '11': [ 10],
    '12': [ 10, 11 ],

    '4': [ 5, 6 ],
    '5': [ 6 ],
    '6': [ 5],
    '7': [ 5, 6],

```

Single items are easy, one choice:

1 > 4 > x > 16 > 19
1 > 4 > x > 12 > 15 > 16 > 19
1 > 4 > x > 10 > 11 > 12 > 15 > 16 > 19
1 > 4 > x > 7 > 10 > 11 > 12 > 15 > 16 > 19
1 > 4 > x > 5 > 6 > 7 > 10 > 11 > 12 > 15 > 16 > 19
1 > 4 > 5 > 6 > 7 > 10 > 11 > 12 > 15 > 16 > 19

1. Sort list
2. Validate list
3. If VALID:

Part II

```text
(0) > 1 > 4 > 5 > 6 > 7 > 10 > 11 > 12 > 15 > 16 > 19 > (22) # adapters
      1 > 3 > 1 > 1 > 1 >  3 >  1 >  1 >  3 >  1 >  3 >  3 # deltas
```

start at end:

If `list[i-1] >= 3 || list[i] - list[i-2] > 3 : break`
...
else `list = list.splice(i-1, 1)
validateList
...

```text
(0) > 1 > 4 > 5 > 6 > 7 > 10 > _ > 12 > 15 > 16 > 19 > (22) # adapters, remove 11
      1 > 3 > 1 > 1 > 1 >  3 > 1 >  1 >  3 >  1 >  3 >  3 # deltas

(0) > 1 > 4 > 5 > _ > 7 > 10 > _ > 12 > 15 > 16 > 19 > (22) # adapters, remove 6
      1 > 3 > 1 > 1 > 1 >  3 > 1 >  1 >  3 >  1 >  3 >  3 # deltas

(0) > 1 > 4 > _ > _ > 7 > 10 > _ > 12 > 15 > 16 > 19 > (22) # adapters, remove 5
      1 > 3 > 1 > 1 > 1 >  3 > 1 >  1 >  3 >  1 >  3 >  3 # deltas

```

1 for full solution, + (5), (5,6), (5,11), (5,6,11) + (6), (6,11), + (11) = 8 combos

1. get full list of removable numbers
2. create a list of possible removal combos: (5), (5,6),(5,11), (5,6,11), (6), (6,11), (11)
3. add one for full solution
4. answer 8

It's a combination problems, why not working

---

5,
6,
11
5,6
5,11
6,11
5,6,11

Can I take original length minus possible removals and get answer? 11 - 3 = 8

1 > 3 > 4 > 7 > 8 > 9 > 10 > 11 > 14 > 17 > 18 > 19 > 20 > 23 > 24 > 25 > 28 > 31 > 32 > 33 > 34 > 35 > 38 > 39 > 42 > 45 > 46 > 47 > 48 > 49 > 52

48, 47, 46, 34, 33, 32, 24, 19, 18, 10, 9, 8, 3, 2, 1

[1], [2]... = 15
[1,2] [1,3] [1,8] [1,9] [1,10] = 15 - 1 = 14
[1,2,3] [1,3,8] []

DP

(0) > 1 > 3 > 4 > 7 > 8 > 9 > 10 > 11 > 14 > 17 > 18 > 19 > 20 > 23 > 24 > 25 > 28 > 31 > 32 > 33 > 34 > 35 > 38 > 39 > 42 > 45 > 46 > 47 > 48 > 49 > (52)

1 > 1 > 1 > 3 > 1 > 1 > 1 > 1 > 3 > 3 > 1 > 1 > 1 > 3 > 1 > 1 > 3 > 3 > 1 > 1 > 1 > 1 > 3 > 1 > 3 > 3 > 1 > 1 > 1 > 1 > 3

Final Note: DP is the way, became much simpler in the end
