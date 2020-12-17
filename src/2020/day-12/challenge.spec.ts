import { mergeDeepRight } from 'ramda';
import {
  calcDirs,
  calcShipPath,
  Direction,
  getManhattanDistance,
  getWayPoints,
  IShipCoords,
  rotateWaypoint,
} from './challenge';
import { inputs, sample } from './inputs';

const getCoords = (coords: Partial<IShipCoords>) =>
  mergeDeepRight(
    {
      waypoint: { x: 10, y: -4 },
      ship: { x: 100, y: -10 },
      dir: Direction.E,
    },
    coords
  );

describe(`day 12: Rain Risk`, () => {
  test(`calcShipPath(sample)`, () => {
    expect(calcShipPath(sample)).toEqual({
      N: -3,
      S: 11,
      E: 17,
      W: 0,
      L: 0,
      R: 0,
      F: 0,
    });
  });

  test(`getManhattanDistance()`, () => {
    expect(
      getManhattanDistance({
        N: 0,
        S: 8,
        E: 17,
        W: 0,
        L: 0,
        R: 0,
        F: 0,
      })
    ).toBe(25);
  });

  describe.each([
    [Direction.E, 90, Direction.S],
    [Direction['E'], 90, Direction.S],
    [Direction.S, 90, Direction.W],
    [Direction.W, 90, Direction.N],
    [Direction.S, -90, Direction.E],
  ])(
    `getAdjacentSeats(%i, %j)`,
    (startDir: Direction, value: number, expectedDir: Direction) => {
      test(`should return ${expectedDir}`, () => {
        expect(calcDirs(startDir, value)).toEqual(expectedDir);
      });
    }
  );

  test(`calcShipPath(sample)`, () => {
    const iVal = calcShipPath(sample);
    expect(getManhattanDistance(iVal)).toBe(25);
  });

  test(`calcShipPath(input)`, () => {
    const iVal = calcShipPath(inputs);
    expect(getManhattanDistance(iVal)).toBe(1007);
  });

  describe(`part II`, () => {
    // test(`getWayPoints(sample)`, () => {
    //   const iVal = getWayPoints(sample);
    //   expect(iVal).toBe(286);
    // });

    test(`getWayPoints(inputs)`, () => {
      const iVal = getWayPoints(inputs);
      expect(iVal).toBeGreaterThan(34176);
      expect(iVal).toBeLessThan(155558); // 1st: > 34176, 2: < 155558
      expect(iVal).toBe(41212); // 1st: > 34176, 2: < 155558
    });

    describe.each([
      [
        getCoords({ waypoint: { x: 10, y: -4 } }),
        1,
        'R',
        {
          waypoint: { x: 4, y: 10 },
          ship: { x: 100, y: -10 },
          dir: Direction.S,
        },
      ],
      [
        getCoords({ waypoint: { x: 4, y: 10 }, dir: Direction.S }),
        1,
        'R',
        {
          waypoint: { x: -10, y: 4 },
          ship: { x: 100, y: -10 },
          dir: Direction.W,
        },
      ],
      [
        getCoords({ waypoint: { x: 10, y: -4 } }),
        2,
        'R',
        {
          waypoint: { x: -10, y: 4 },
          ship: { x: 100, y: -10 },
          dir: Direction.W,
        },
      ],
      [
        getCoords({ waypoint: { x: 10, y: -4 } }),
        4,
        'R',
        {
          waypoint: { x: 10, y: -4 },
          ship: { x: 100, y: -10 },
          dir: Direction.E,
        },
      ],
      // LEFT
      [
        getCoords({ waypoint: { x: 10, y: -4 } }),
        1,
        'L',
        {
          waypoint: { x: -4, y: -10 },
          ship: { x: 100, y: -10 },
          dir: Direction.N,
        },
      ],
      [
        getCoords({ waypoint: { x: -4, y: -10 }, dir: Direction.N }),
        1,
        'L',
        {
          waypoint: { x: -10, y: 4 },
          ship: { x: 100, y: -10 },
          dir: Direction.W,
        },
      ],
      [
        getCoords({ waypoint: { x: 10, y: -4 } }),
        2,
        'L',
        {
          waypoint: { x: -10, y: 4 },
          ship: { x: 100, y: -10 },
          dir: Direction.W,
        },
      ],
      [
        getCoords({ waypoint: { x: 10, y: -4 } }),
        4,
        'L',
        {
          waypoint: { x: 10, y: -4 },
          ship: { x: 100, y: -10 },
          dir: Direction.E,
        },
      ],
    ])(
      `rotateWaypoint(%j, %i, %s)`,
      (
        shipCoords: IShipCoords,
        count: number,
        rotDir: string,
        expectedCoords: IShipCoords
      ) => {
        test(`should return ${JSON.stringify(expectedCoords.waypoint)}`, () => {
          expect(
            rotateWaypoint(shipCoords, count, rotDir as 'R' | 'L')
          ).toEqual(expectedCoords);
        });
      }
    );
  });
});
