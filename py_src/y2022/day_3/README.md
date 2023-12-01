# Day 3

## Data

rucksack -> {compartment 1: str, compartment 2: str, common items: []}
priority -> a-z: 1-26, A-Z: 27 - 52
rucksacks -> List[rucksack]

## Calculations

split the string in half
the sum of priorities of common items

## functions/approach

1. process input into list of rucksacks
1. find the common items and set them on each rucksack
1. calculate the sum of priorities

## Notes

```python3
import string


lower_letters = string.ascii_lowercase[:26]
upper_letters = string.ascii_uppercase[:26]
letters = upper_letters + lower_letters
priorities = [i for i in range(1, 52 + 1)]

print(priorities)
print(lower_letters)
print(upper_letters)

for let in letters:
    letter = ord(let)
    print(f"char of ASCII {let} is {letter}")
```

```bash
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ

char of ASCII A is 65
char of ASCII B is 66
char of ASCII C is 67
char of ASCII D is 68
char of ASCII E is 69
char of ASCII F is 70
char of ASCII G is 71
char of ASCII H is 72
char of ASCII I is 73
char of ASCII J is 74
char of ASCII K is 75
char of ASCII L is 76
char of ASCII M is 77
char of ASCII N is 78
char of ASCII O is 79
char of ASCII P is 80
char of ASCII Q is 81
char of ASCII R is 82
char of ASCII S is 83
char of ASCII T is 84
char of ASCII U is 85
char of ASCII V is 86
char of ASCII W is 87
char of ASCII X is 88
char of ASCII Y is 89
char of ASCII Z is 90
char of ASCII a is 97
char of ASCII b is 98
char of ASCII c is 99
char of ASCII d is 100
char of ASCII e is 101
char of ASCII f is 102
char of ASCII g is 103
char of ASCII h is 104
char of ASCII i is 105
char of ASCII j is 106
char of ASCII k is 107
char of ASCII l is 108
char of ASCII m is 109
char of ASCII n is 110
char of ASCII o is 111
char of ASCII p is 112
char of ASCII q is 113
char of ASCII r is 114
char of ASCII s is 115
char of ASCII t is 116
char of ASCII u is 117
char of ASCII v is 118
char of ASCII w is 119
char of ASCII x is 120
char of ASCII y is 121
char of ASCII z is 122
```
