## Approach

- https://www.geeksforgeeks.org/collinear-points/
- https://en.wikipedia.org/wiki/Collinearity

### Pairing Points

`(8, 1), (5, 2), (7, 3), (4, 4)`

`((8, 1), (5, 2)), ((5, 2), (7, 3)), ((7, 3), (4, 4))` are in line

`((8, 1), (4, 4))` are not

### Colinearity Three Points

$$\dfrac{b_y-a_y}{b_x-a_x} = \dfrac{c_y-b_y}{c_x-b_x} = 0$$

(4,3), (5, 5)

(3,1), (6,7)

$$1/2(x1(y2 – y3 ) + x2 (y3 – y1 ) + x3 (y1 – y2 ))= 0$$

antinode

`(4,3), (5, 5), (3,1)`

$1/2(4(5 - 1) + 5(1 - 3) + 3(3 - 5)) = 0$

$1/2(4(4) + 5(-2) + 3(-2)) = 0$

$1/2(16 + -10 + -6) = 0$

$1/2(0) = 0$

non-antinode

`(4,3), (5, 5), (2,1)`

$1/2(4(5-1) + 5(1-3) + 2(3-5))$

$1/2(4(4) + 5(-2) + 2(-2)) = 0$

$1/2(16 + -10 + -4) = 0$

$1/2(2) = 1$
