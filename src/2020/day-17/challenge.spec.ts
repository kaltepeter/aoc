import {
  calcCoordsForActiveCubes,
  calcPocketDimension,
  getPermutationsOfCoords,
  runCycle,
} from './challenge';
import { inputs, sample } from './inputs';

describe(`Day 17: Conway Cubes`, () => {
  test(`process input`, () => {
    expect(sample.length).toBe(3);
    expect(sample[0].length).toBe(3);
  });
  test(`runCycle(sample)`, () => {
    const res = runCycle([
      [0, 1, 0],
      [1, 2, 0],
      [2, 0, 0],
      [2, 1, 0],
      [2, 2, 0],
    ]);
    expect(Array.from(res.activeCubes)).toEqual(
      [
        [1, 0, -1],
        [2, 2, -1],
        [3, 1, -1],
        [1, 0, 0],
        [1, 2, 0],
        [2, 1, 0],
        [2, 2, 0],
        [3, 1, 0],
        [1, 0, 1],
        [2, 2, 1],
        [3, 1, 1],
      ].sort()
    );
  });

  test(`getPermutationsOfCoords([0,1,2])`, () => {
    const res = getPermutationsOfCoords([0, 1, 2]);
    expect(res.length).toBe(26);
  });

  test(`calcCoordsForActiveCubes(sample)`, () => {
    expect(calcCoordsForActiveCubes(sample)).toEqual([
      [0, 1, 0],
      [1, 2, 0],
      [2, 0, 0],
      [2, 1, 0],
      [2, 2, 0],
    ]);
  });

  test(`calcPocketDimension(sample)`, () => {
    expect(calcPocketDimension(sample).length).toBe(112);
  });

  test.skip(`calcPocketDimension(inputs)`, () => {
    expect(calcPocketDimension(inputs).length).toBe(112);
  });
});
