# approach

NORTH (0, -1) 90º [(-1, 0), (1, 0)] 180º [(0, 1)]
EAST (1, 0) 90º [(0, -1), (0, 1)] 180º [(-1, 0)]
SOUTH (0, 1) 90º [(-1, 0), (1, 0)] 180º [(0, -1)]
WEST (-1, 0) 90º [(0, 1), (0, -1)] 180º [(1, 0)]

180º flips sign for non-zero value
90º swaps x,y and can be either sign

90º = 1001 cost
180º = 2001 cost (2 90º turns and move)

start == end = 0
vector = endx - startx, endy - starty

if vector == direction: cost 1
