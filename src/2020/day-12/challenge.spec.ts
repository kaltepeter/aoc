import {
  calcDirs,
  calcShipPath,
  Direction,
  getManhattanDistance,
} from './challenge';
import { inputs, sample } from './inputs';
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
});
