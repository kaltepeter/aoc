# Day 20

OFF/LOW = 0
ON/HIGH = 1

FLIP FLOP (initial 0) output

| STATE | RECEIVE LOW | RECEIVE HIGH | OUTPUT |
| ----: | ----------: | -----------: | -----: |
|     0 |           1 |         None |   HIGH |
|     1 |           0 |         None |    LOW |

CONJUNCTION (initial 0) output

| STATE | ALL LOW | ALL HIGH | OUTPUT |
| ----: | ------: | -------: | -----: |
|   [0] |    HIGH |      LOW |   HIGH |
|   [1] |    HIGH |      LOW |    LOW |
|  [01] |    HIGH |      LOW |   HIGH |
|  [11] |    HIGH |      LOW |    LOW |

```python
val = 0 # 0
val ^= 0b1 # 1
val ^= 0b1 # 0


# conjunction
val = 0b0 # 0
val = (val << 1) | 1 # 01
val = (val << 1) | 1 # 011
val = (val << 1) | 0 # 0110
val = (val << 1) | 0 # 01100
val = (val << 1) | 1 # 011001
```
