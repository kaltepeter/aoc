# Packet Decoder

1. Convert Hexadecimal to Binary

```txt
0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111
```

```txt
D2FE28
  D  2   F    E   2  8
1101 10 1111 1110 10 1000
110 100 10111 11110 00101 000
VVV TTT AAAAA BBBBB CCCCC
```

`VVV` packet version, 6

`TTT` type id, 4

`AAAAA` packet version, 0111

`BBBBB` packet version, 1110

`CCCCC` packet version, 0101

`---` empty zeros

## Basic Process

`100010100000000001001010100000000001101010000000000000101111010001111000`

`100`: version 4

`010`: type 2

`1`: length type

`00000000001`: packet count of 1

`rp=001010100000000001101010000000000000101111010001111000`

`001`: version 1

`010`: type 2

`1`: length type

`00000000001`: packet count of 1

`rp=101010000000000000101111010001111000`

`101`: version 5

`010`: type 2

`0`: length type

`000000000001011`: count of 11 bytes

`rp=11010001111`

`110` : version 6

`100`: type 4

`01111` -> `1111`: last packet of F

```text
bits Bits
b = bits.subpacket
for len(rp) > 0; p
  take first 6 bits and get version, type
  if type is 4 process the literal
    p.subpacket = value
  if type is not 4 apply operator rules and return remaining bits
    p.subpacket = value
    rp = remaining bits
    b = p.subpacket
```

start with bits, perform one round
feed into recursion ^^

## Child Packets

`620080001611562C8802118E34`

`01100010000000001000000000000000000101100001000101010110001011001000100000000010000100011000111000110100`

`011`: version 3, `000`: typeId 0, `1`: length type, `00000000010` 2 packets

`rp=00000000000000000101100001000101010110001011001000100000000010000100011000111000110100, rc=2`

`000`: version 0, `000`: typeId: 0, `0`: length type, `000000000010110` 22 bits
`rp=0001000101010110001011, rc=1`

`001`: version 1, `000` : typeId: 0, `1`: length type, `00000000010` 2 packets

`rp=000100011000111000110100`
