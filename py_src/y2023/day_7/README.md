# Day 7

'AKQJT98765432'

Cards are assigned a rank

```python
card_values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}
```

```python
'AAAAA' = 5 * 14 = 70
'AAAAK' = 4*14+13 = 69

# 5 of a kind should always win
'KKKKK' = 5* 13 = 65
'AAAAK' = 4 * 14 + 13 = 69

# KK677 should be stronger
'KK677' = 2*13 + 6 + 2* 7 = 46
'KTJJT' = 13 + 2 * 10 + 2 * 11 = 55
```

Hand Ranks:

```python
class HandRank(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 8
    FIVE_OF_A_KIND = 16
```

counting:
total = 0b00001
total = total << 1

five is all counts
4 is most counts
full house is three of a kind + pair
three of a kind is counts
two pair is one pair + one pair
rest are counts

```python
'AAAAA' = 6
'AAAAK' = 5
'23332' = 4
'25333' = 3
'23432' = 2
'A23A4' = 1
'23456' = 0

'23332' = 2*2 + 3*3 = 13
'25333' = 2 + 5 + 3*3 = 16

0b00000 # high card
0b00001 # one pair
0b00011 # two pair
0b00100 # three of a kind
0b00101 # full house
0b01000 # four of a kind
0b10000 # five of a kind

one_pair = 0b00001
one_pair << 1 # 0b00010 or two pair

```

1. for each handset the bits for the rank
1. store the hand rank
1. iterate through the groups and sort
1. calculate totals
