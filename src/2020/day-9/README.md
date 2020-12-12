# Day 9

```text
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
```

preamble:

```text
35
20
15
25
47
```

numbers:

```text
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
```

40 - 47 = -7 // NOPE
40 - 25 = 15 // YES
40 - 15 = 25 // YES
40 - 20 = 20 // YES
40 - 35 = 5 // NOPE

62 - 40 = 22 // NOPE
62 - 47 = 5 // does prevNumbers have 5?
62 - 25 = 37 // does previous list have 37?
62 - 15 = 47 // YES, is valid

// next
55 - 62 = -7 // NOPE
55 - 40 = 15 // YES

IF cur === prev: NOPE
IF cur - prev < 0: NOPE
IF cur - prev IN prevNums: YES

// SORT list and split to optimize ???
ex. 62, [20, 15, 25, 47, 40]
[15, 20, 25, 40, 47] (take half?)
