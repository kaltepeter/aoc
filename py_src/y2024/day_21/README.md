# approach

+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
| 0 | A |
+---+---+

    +---+---+
    | ^ | A |

+---+---+---+
| < | v | > |
+---+---+---+

    +---+---+
    | ^ | A |

+---+---+---+
| < | v | > |
+---+---+---+

    +---+---+
    | ^ | A |

+---+---+---+
| < | v | > |
+---+---+---+

`A -> ^, >`
`^ -> v, A`
`v -> ^, >`
`> -> A, v`
`< -> V`

In summary, there are the following keypads:

One directional keypad that you are using.
Two directional keypads that robots are using.
One numeric keypad (on a door) that a robot is using.

029A

```
029A
<A ^A >^^A vvvA
v < < A > > ^ A < A > A v A < ^ A A > A < v A A A > ^ A
<vA <A A >>^A vA A <^A >A <v<A >>^A vA ^A <vA >^A <v<A >^A >A A vA ^A <v<A >A >^A A A vA <^A >A
```

not a real grid

python py_src/y2024/day_21/day.py 4.87s user 0.37s system 99% cpu 5.256 total max RSS 818240
