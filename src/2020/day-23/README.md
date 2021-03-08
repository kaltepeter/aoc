# --- Day 23: Crab Cups ---

The small crab challenges you to a game! The crab is going to mix up some cups, and you have to predict where they'll end up.

The cups will be arranged in a circle and labeled clockwise (your puzzle input). For example, if your labeling were `32415`, there would be five cups in the circle; going clockwise around the circle from the first cup, the cups would be labeled `3, 2, 4, 1, 5,` and then back to `3` again.

Before the crab starts, it will designate the first cup in your list as the current cup. The crab is then going to do 100 moves.

Each move, the crab does the following actions:

The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
For example, suppose your cup labeling were 389125467. If the crab were to do merely 10 moves, the following changes would occur:

```
-- move 1 --
cups: (3) 8  9  1  2  5  4  6  7
pick up: 8, 9, 1
destination: 2

-- move 2 --
cups:  3 (2) 8  9  1  5  4  6  7
pick up: 8, 9, 1
destination: 7

-- move 3 --
cups:  3  2 (5) 4  6  7  8  9  1
pick up: 4, 6, 7
destination: 3

-- move 4 --
cups:  7  2  5 (8) 9  1  3  4  6
pick up: 9, 1, 3
destination: 7

-- move 5 --
cups:  3  2  5  8 (4) 6  7  9  1
pick up: 6, 7, 9
destination: 3

-- move 6 --
cups:  9  2  5  8  4 (1) 3  6  7
pick up: 3, 6, 7
destination: 9

-- move 7 --
cups:  7  2  5  8  4  1 (9) 3  6
pick up: 3, 6, 7
destination: 8

-- move 8 --
cups:  8  3  6  7  4  1  9 (2) 5
pick up: 5, 8, 3
destination: 1

-- move 9 --
cups:  7  4  1  5  8  3  9  2 (6)
pick up: 7, 4, 1
destination: 5

-- move 10 --
cups: (5) 7  4  1  8  3  9  2  6
pick up: 7, 4, 1
destination: 3

-- final --
cups:  5 (8) 3  7  4  1  9  2  6
```

In the above example, the cups' values are the labels as they appear moving clockwise around the circle; the current cup is marked with ( ).

After the crab is done, what order will the cups be in? Starting after the cup labeled 1, collect the other cups' labels clockwise into a single string with no extra characters; each number except 1 should appear exactly once. In the above example, after 10 moves, the cups clockwise from 1 are labeled 9, 2, 6, 5, and so on, producing `92658374`. If the crab were to complete all 100 moves, the order after cup 1 would be `67384529`.

Using your labeling, simulate `100` moves. What are the labels on the cups after cup 1?

Your puzzle input is `186524973`.

## --- Part Two ---

Due to what you can only assume is a mistranslation (you're not exactly fluent in Crab), you are quite surprised when the crab starts arranging many cups in a circle on your raft - one million (`1000000`) in total.

Your labeling is still correct for the first few cups; after that, the remaining cups are just numbered in an increasing fashion starting from the number after the highest number in your list and proceeding one by one until one million is reached. (For example, if your labeling were `54321`, the cups would be numbered `5, 4, 3, 2, 1,` and then start counting up from `6` until one million is reached.) In this way, every number from one through one million is used exactly once.

After discovering where you made the mistake in translating Crab Numbers, you realize the small crab isn't going to do merely 100 moves; the crab is going to do ten million (10000000) moves!

The crab is going to hide your stars - one each - under the two cups that will end up immediately clockwise of cup 1. You can have them if you predict what the labels on those cups will be when the crab is finished.

In the above example (`389125467`), this would be `934001` and then `159792`; multiplying these together produces `149245887792`.

Determine which two cups will end up immediately clockwise of cup 1. What do you get if you multiply their labels together?

## Solution Details

Part 1 is easy enough with a linked list.

Part 2 needs performance improvements.

Sample logs from part 2 after it passes the first set of cups.

```bash
i: 278: nextThree: 1111,1112,1113, current: 1110, dest: 1109
i: 279: nextThree: 1115,1116,1117, current: 1114, dest: 1113
i: 280: nextThree: 1119,1120,1121, current: 1118, dest: 1117
i: 281: nextThree: 1123,1124,1125, current: 1122, dest: 1121
i: 282: nextThree: 1127,1128,1129, current: 1126, dest: 1125
i: 283: nextThree: 1131,1132,1133, current: 1130, dest: 1129
i: 284: nextThree: 1135,1136,1137, current: 1134, dest: 1133
i: 285: nextThree: 1139,1140,1141, current: 1138, dest: 1137
i: 286: nextThree: 1143,1144,1145, current: 1142, dest: 1141
i: 287: nextThree: 1147,1148,1149, current: 1146, dest: 1145
i: 288: nextThree: 1151,1152,1153, current: 1150, dest: 1149
i: 289: nextThree: 1155,1156,1157, current: 1154, dest: 1153
i: 290: nextThree: 1159,1160,1161, current: 1158, dest: 1157
i: 291: nextThree: 1163,1164,1165, current: 1162, dest: 1161
i: 292: nextThree: 1167,1168,1169, current: 1166, dest: 1165
i: 293: nextThree: 1171,1172,1173, current: 1170, dest: 1169
i: 294: nextThree: 1175,1176,1177, current: 1174, dest: 1173
i: 295: nextThree: 1179,1180,1181, current: 1178, dest: 1177
i: 296: nextThree: 1183,1184,1185, current: 1182, dest: 1181
i: 297: nextThree: 1187,1188,1189, current: 1186, dest: 1185
i: 298: nextThree: 1191,1192,1193, current: 1190, dest: 1189
i: 299: nextThree: 1195,1196,1197, current: 1194, dest: 1193
```

Possible pattern?

current: `1110`
`1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122` // 1110
`1109, 1111, 1112, 1113, 1110, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122` // 1114
`1109, 1111, 1112, 1113, 1115, 1116, 1117, 1110, 1114, 1118, 1119, 1120, 1121, 1122` // 1118
`1109, 1111, 1112, 1113, 1115, 1116, 1117, 1119, 1120, 1121, 1110, 1114, 1118, 1122` // 1122

https://github.com/oddbytes/adventofcode/blob/master/src/2020/Day%2023/crabCups.ts on the idea of using a set for a linked list is super efficient.

debug is very slow.

```bash
NODE_OPTIONS="--max_old_space_size=8192" npm run start:2020:millions-of-cups
```
