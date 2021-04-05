# distance

N: 0, E: 10, S: 0, W: 0

N: 3, E: 10, S: 0, W: 0
N: 3, E: 17, S: 0, W: 0
N: 0, E: 17, S: 8, W: 0

N 3 - 11 = -8 = 8

E 17

         N
      W -|- E
         S

        360
         0
    270 -|- 90
        180

E = 90 E
L90 = 0 N
L180 = 180 S
L180 = 180 N
R270 = 270 W
R270 = 180 S

180 - 270 = -90 (90)
270 + 270 = 540 - 360 (180)
0 - 270 = -270 - 360 = -90 (90)

PART II

two points

ship and waypoint

directions move waypoint relative to ship
forward moves toward waypoint
rotation rotates the waypoint relative to ship

10,-4 (E,N)
R90
4,10 (E,S)

R90
-10,4 (W,S)

R90
-4,-10 (W,N)

R90
10,-4 (E,N)

// LEFT

10,-4 (E,N)
L90
-4,-10 (W,N)

L90
-10,4 (W,S)

L90
4,10 (E,S)

L90
10,-4 (E,N)
