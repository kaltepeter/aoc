# Day 21

<https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21>

<https://www.cuemath.com/algebra/perfect-squares/>

~perfect square~: A perfect square is a number that can be expressed as the product of an integer by itself or as the second exponent of an integer. For example, 25 is a perfect square because it is the product of integer 5 by itself, 5 × 5 = 25. However, 21 is not a perfect square number because it cannot be expressed as the product of two same integers.

~perfect cube~: A perfect cube is a number that is obtained by multiplying the same integer three times. For example, multiplying the number 4 three times results in 64. Therefore, 64 is a perfect cube. Therefore, perfect cube = number × number × number. The cube root of 64 is 4. A number is said to be a perfect cube if it can be decomposed into a product of the same three numbers.

<https://en.wikipedia.org/wiki/Quadratic_equation>

~quadratic equation~: In algebra, a quadratic equation (from Latin quadratus 'square') is any equation that can be rearranged in standard form as[1]

`ax^2 + bx + c = 0`

where x represents an unknown value, and a, b, and c represent known numbers, where a ≠ 0. (If a = 0 and b ≠ 0 then the equation is linear, not quadratic.) The numbers a, b, and c are the coefficients of the equation and may be distinguished by respectively calling them, the quadratic coefficient, the linear coefficient and the constant coefficient or free term.[2]

The values of x that satisfy the equation are called solutions of the equation, and roots or zeros of the expression on its left-hand side. A quadratic equation has at most two solutions. If there is only one solution, one says that it is a double root. If all the coefficients are real numbers, there are either two real solutions, or a single real double root, or two complex solutions that are complex conjugates of each other. A quadratic equation always has two roots, if complex roots are included; and a double root is counted for two. A quadratic equation can be factored into an equivalent equation[3]

~parity~: odd or even are opposite parities

## Wrap Around Grid

11 x 11

```txt
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
```

0 == -11
11 == 1

x % 11

---

12 % 11 = 1
22 % 11 = 0
-22 % 11 = 0
-21 % 11 = 1
-3 % 11 = 8

<https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21>

<https://www.reddit.com/r/adventofcode/comments/18o4y0m/2023_day_21_part_2_algebraic_solution_using_only/>

<https://www.youtube.com/watch?v=9UOMZSL0JTg&t=459s>
