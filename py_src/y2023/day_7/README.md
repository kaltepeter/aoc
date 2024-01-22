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

1. for each hand, set the bits for the rank
1. store the hand rank
1. iterate through the groups and sort
1. calculate totals

## Part II

{'T': 1, '5': 3, 'J': 1}
hand: ('T55J5', 684) total: 4

1. ignore J, calculate totals
1. if total == FOUR_OF_A_KIND and J = 1: total = FIVE_OF_A_KIND

```python
class HandRank(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 8
    FIVE_OF_A_KIND = 16

0b00000 # high card
0b00001 # one pair
0b00011 # two pair
0b00100 # three of a kind
0b00101 # full house
0b01000 # four of a kind
0b10000 # five of a kind
```

(3333J) 1 J + 4 of a kind = 5 of a kind (8 = 16)
(3334J) 1 J + 3 of a kind = 4 of a kind (4 = 8)
(3344J) 1 J + 2 pair = full house (2 = 5)
(3345J) 1 J + 1 pair = 3 of a kind (1 = 4)
(3456J) 1 J + high card = 1 pair (0 = 1)

(333JJ) 2 J + 3 of a kind = 5 of a kind (4 = 16)
(334JJ) 2 J + 1 pair = 4 of a kind (1 = 8)
(345JJ) 2 J + high card = 3 of a kind (0 = 4)

(33JJJ) 3 J + 1 pair = 5 of a kind (1 = 16)
(34JJJ) 3 J + high card = 4 of a kind (0 = 8)

(3JJJJ) 4 J + high card = 5 of a kind (0 = 16)

(JJJJJ) 5 J = 5 of a kind (0 = 16)

wild_cards = found_cards['J']

```python
0b000001 # high card
0b000010 # one pair
0b000110 # two pair
0b001000 # three of a kind
0b001010 # full house
0b010000 # four of a kind
0b100000 # five of a kind

class HandRank(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 4
    THREE_OF_A_KIND = 8
    FULL_HOUSE = 10
    FOUR_OF_A_KIND = 16
    FIVE_OF_A_KIND = 32
```
