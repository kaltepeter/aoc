# Day 19

Find all combinations of rotations and directions.

```md
[1,2,-3]

      [1,-1]
        |  |

[2,-2] [-3,3]
| |
[-3,3] [2,-2]

1,2,-3
1,2,3
1,-2,-3
1,-2,3
-1,-3,2
-1,-3,-2
-1,3,2
-1,3,-2

      [2,-2]
        |  |

[1,-1] [-3,3]
| |
[-3,3] [1,-1]

2,1,-3
2,1,3
2,-1,-3
2,-1,3
-2,1,-3
-2,1,3
-2,-1,-3
-2,-1,3

      [3,-3]
        |  |

[1,-1] [2,-2]
| |
[2,-2] [1,-1]

3,1,2
3,1,-2
3,-1,2
3,-1,-2
-3,1,2
-3,1,-2
-3,-1,2
-3,-1,-2
```

## Finding overlapping beacons

- Scanner 0 is always considered 0,0,0. All scanners are relative to this scanner.

  ```md
  # scanner 0

  ...B.
  B....
  ....B
  S....

  # scanner 1

  ...B..
  B....S
  ....B.

  # overlap

  ...B..
  B....S
  ....B.
  S.....
  ```

- Max range `1000`
- Scanners do not know their own position.
- Unknown direction or rotation. 1,1,1 is same as -1,1,1.

To find the patterns, use the deltas between points. Graph distance?

0,4

```
x-618,-824,-621
x-537,-823,-458
x-447,-329,318
x404,-588,-901
x544,-627,-890
x528,-643,409
x-661,-816,-575
x390,-675,-793
x423,-701,434
x-345,-311,381
x459,-707,401
x-485,-357,347

x686,422,578
x605,423,415
x515,917,-361
x-336,658,858
x-476,619,847
x-460,603,-452
x729,430,532
x-322,571,750
x-355,545,-477
x413,935,-424
x-391,539,-444
x553,889,-390
```

x[-485,-357,347] [553,889,-390]
x[-447,-329,318] [515,917,-361]
x[-618,-824,-621] [686,422,578]
x[528,-643,409] [-460,603,-452]
x[-345,-311,381] [413,935,-424]
x[544,-627,-890] [-476,619,847]
x[423,-701,434] [-355,545,-477]
x[459,-707,401] [-391,539,-444]
x[-537,-823,-458] [605,423,415]
x[390,-675,-793] [-322,571,750]
x[-661,-816,-575] [729,430,532]
x[404,-588,-901] [-336,658,858]

## Translate to scanner zero coords

Scanner 0: pos `0,0,0`

```bash
-618,-824,-621
-537,-823,-458
-447,-329,318
404,-588,-901
544,-627,-890
528,-643,409
-661,-816,-575
390,-675,-793
423,-701,434
-345,-311,381
459,-707,401
-485,-357,347
```

Scanner 1: pos `68,-1246,-43`

```bash
686,422,578
605,423,415
515,917,-361
-336,658,858
-476,619,847
-460,603,-452
729,430,532
-322,571,750
-355,545,-477
413,935,-424
-391,539,-444
553,889,-390
```
