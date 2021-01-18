import {
  calcCoordsForActiveCubes,
  calcNextGeneration,
  calcPocketDimension,
  calcPocketDimensionFast,
  countResults,
  Flags,
  getCurrentCube,
  getLastSetBit,
  getMaskForValue,
  getNeighborCount,
  getPermutationsOfCoords,
  isEmpty,
  point,
  runCycle,
  States,
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
    const pos = [0, 1, 2] as point;
    const res = getPermutationsOfCoords(pos);
    expect(res.length).toBe(26);
    expect(res).toEqual(
      jasmine.arrayContaining([
        [-1, 0, 1],
        [0, 1, 1],
        [0, 2, 2],
        [0, 1, 3],
      ])
    );
    expect(res.indexOf(pos)).toBe(-1);
  });

  test(`calcCoordsForActiveCubes([sample])`, () => {
    expect(calcCoordsForActiveCubes([sample])).toEqual([
      [0, 1, 0],
      [1, 2, 0],
      [2, 0, 0],
      [2, 1, 0],
      [2, 2, 0],
    ]);
  });

  test(`calcCoordsForActiveCubes([[], sample, []])`, () => {
    expect(calcCoordsForActiveCubes([[], sample, []])).toEqual([
      [0, 1, 1],
      [1, 2, 1],
      [2, 0, 1],
      [2, 1, 1],
      [2, 2, 1],
    ]);
  });

  describe.each([
    [0b0, 0],
    [0b1100, 2],
    [0b1101, 2],
    [0b0001, 0],
  ])(`getNeighborCount(%i)`, (value: number, expectedResult: number) => {
    test(`should return ${expectedResult}`, () => {
      expect(getNeighborCount(value)).toBe(expectedResult);
    });
  });

  describe.each([
    [0b0, -1],
    [0b100, 2],
    [0b1100, 3],
    [0b1101, 3],
    [0b0001, 0],
  ])(`getLastSetBit(%i)`, (value: number, expectedResult: number) => {
    test(`should return ${expectedResult}`, () => {
      expect(getLastSetBit(value)).toBe(expectedResult);
    });
  });

  describe.each([
    [0b0, 0b0],
    [0b1, 0b0],
    [0b11110, 0b11110],
    [0b0001, 0b0],
    [0b0011, 0b10],
    // [0b101, 0b10], // no gaps
    [0b1111, 0b1110],
  ])(`getMaskForValue(%i)`, (value: number, expectedResult: number) => {
    test(`should return ${expectedResult.toString(2)}`, () => {
      expect(getMaskForValue(value)).toBe(expectedResult);
    });
  });

  describe.each([
    [0b0, true],
    [0b1100, false],
    [0b1101, false],
    [0b0001, false],
  ])(`isEmpty(%i)`, (value: number, expectedResult: boolean) => {
    test(`should return ${expectedResult}`, () => {
      expect(isEmpty(value)).toBe(expectedResult);
    });
  });

  describe.each([
    [[sample], [0, 1, 0] as point, States.ACTIVE],
    [[sample], [0, 1, 1] as point, States.INACTIVE],
    [[[], sample, []], [0, 1, 0] as point, States.INACTIVE],
    [[[], sample, []], [0, 1, 1] as point, States.ACTIVE],
    [[[], sample, []], [0, 1, 2] as point, States.INACTIVE],
    [[[], sample, []], [0, 1, 3] as point, States.INACTIVE],
  ])(
    `getCurrentCube(%j, %j)`,
    (value: string[][][], pos: point, expectedResult: States) => {
      test(`should return ${expectedResult}`, () => {
        expect(getCurrentCube(value, pos)).toBe(expectedResult);
      });
    }
  );

  test(`calcPocketDimension(sample)`, () => {
    expect(calcPocketDimension(sample).length).toBe(112);
  });

  test(`calcPocketDimensionFast(sample)`, () => {
    const res = calcPocketDimensionFast(sample);

    expect(res.get('0,1,1')).toEqual(0b11);
    expect(res.get('1,2,1')).toEqual(0b1111);
    expect(res.get('2,1,1')).toEqual(0b1111);
    expect(res.get('3,1,1')).toEqual(0b1110);
    const firstGen = calcNextGeneration(res);
    expect(firstGen.has('0,1,1')).toBe(false);
    expect(firstGen.has('2,0,1')).toBe(false);
    expect(firstGen.get('1,2,1')).toEqual(0b1);
    expect(firstGen.get('2,1,1')).toEqual(0b1);
    expect(firstGen.get('3,1,1')).toEqual(0b1);
    expect(firstGen.size).toBe(11);

    // expect(calcPocketDimensionFast(sample)).toBe(112); // 6 iterations
  });

  test.skip(`calcPocketDimension(inputs)`, () => {
    expect(calcPocketDimension(inputs).length).toBe(112);
  });
});
