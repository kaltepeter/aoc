# Day 17

## Bitwise

```python
print(f"{(0b0011110 << 3 & 127):07b}") # 1110000
print(f"{ 0b0011110 << 3:07b}") # 11110000
print(f"{ 0b0011110 << 2:07b}") # 1111000
print(f"{ 0b0011110 << 1:07b}") # 0111100
```

```text
0011110 #3
0000000 #2
0000000 #1
0000000 #0
```

```text
0000000 #3
0011110 #2
0000000 #1
0000000 #0

0001000
0011100
0001000
0000000
0011110
0000000
0000000
```

## moving rocks attempt 1

The following approach doesn't work because rows can merge. If the rows couldn't intersect it works great.

```python
# move 4 down 1
start, end = (3,1)
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
arr[start-1:start-1+end], arr[start: start+end] = arr[start:start+end],arr[start-1:start-1+end]
arr # [1, 2, 4, 3, 5, 6, 7, 8, 9, 10]

# move 6,7,8 down 1, 5 becomes pos 7
# [1, 2, 3, 4, 6, 7, 8, 5, 9, 10]
start,end = (5,3)
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
arr[start-1:start-1+end], arr[start: start+end] = arr[start:start+end],arr[start-1:start-1+end]
arr # [1, 2, 3, 4, 6, 5, 6, 7, 9, 10]

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
arr, rock, tail = arr[:start-1], arr[start:start+end], arr[start-1:start] + arr[start+end:]
arr = arr + rock + tail
arr # [1, 2, 3, 4, 6, 5, 6, 7, 9, 10]

## final
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
start, end = (3,1)
arr, rock, tail = arr[:start-1], arr[start:start+end], arr[start-1:start] + arr[start+end:]
arr = arr + rock + tail
arr # [1, 2, 4, 3, 5, 6, 7, 8, 9, 10]

start, end = (5,3)
arr, rock, tail = arr[:start-1], arr[start:start+end], arr[start-1:start] + arr[start+end:]
arr = arr + rock + tail
arr # [1, 2, 4, 3, 6, 7, 8, 5, 9, 10]
```

## Detect intersection

no move

```bash
0000000
0000000
0000000
0000010
0000111
0000010
0001111
```

```python
0b0001111 & 0b0000010 # 2
```

move

```bash
0000000
0000000
0000000
0010000
0111000
0010000
0001111
```

```python
0b0001111 & 0b0010000 # 0
```

do not move

```bash
0000000
0000000
0000000
0000000
0010000
0111000
0011111
```

```python
0b0011111 & 0b01110000 # 16
```

## Merging Rows

Bitwise OR should do it

```bash
0000000
0000000
0000000
0010000
0111000
0010000
0001111
```

```python
0b0001111 | 0b0010000 # 31, 0011111
```

Also, handle left and right collisions:

```python
value=0b0111000
[i for i in range(CHAMBER_WIDTH) if get_normalized_bit(value, i)] # 3,4,5
```

move: D landed: False start: 4 end: 3

```bash
0000000
0000000
0000000
0010000
0010000
1111000
0011100
0001000
0011110
```

apply jet > should skip

get left and right bits

```python
# least significant bit
elbow =  [0b0011100, 0b0000100, 0b0000100]
for row in elbow:
  print(f"index: {(row&-row).bit_length()-1}")

# most significant
elbow =  [0b0011100, 0b0000100, 0b0000100]
for row in elbow:
  print(f"index: {(row).bit_length()-1}")
```
