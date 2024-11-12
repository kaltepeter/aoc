import {
  calcCoordsForActiveCubes,
  calcCoordsForActiveCubes4D,
  calcNextGeneration,
  calcPocketDimension,
  calcPocketDimensionFast,
  calcPocketDimensionFast4D,
  getCurrentCube,
  getLastSetBit,
  getMaskForValue,
  getNeighborCount,
  getPermutationsOfCoords,
  getPermutationsOfCoordsFor4D,
  isEmpty,
  point,
  point4d,
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

  test.skip(`calcPocketDimension(sample)`, () => {
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
  });

  describe.each([
    [1, 11],
    [2, 21],
    [6, 112],
  ])(
    `calcPocketDimensionFast(sample, %i)`,
    (value: number, expectedResult: number) => {
      test(`should return ${expectedResult}`, () => {
        const res = calcPocketDimensionFast(sample, value);
        const nextGen = calcNextGeneration(res);
        expect(nextGen.size).toBe(expectedResult);
      });
    }
  );

  // too slow to run
  test.skip(`calcPocketDimension(inputs)`, () => {
    expect(calcPocketDimension(inputs).length).toBe(112);
  });

  test(`calcPocketDimensionFast(inputs, 6)`, () => {
    const res = calcPocketDimensionFast(inputs, 6);
    const nextGen = calcNextGeneration(res);
    expect(nextGen.size).not.toBe(64);
    expect(nextGen.size).toBe(276); // 1278ms to run
  });

  describe(`Part II`, () => {
    test(`getPermutationsOfCoordsFor4D([0,1,2,3])`, () => {
      const pos = [0, 1, 2, 3] as point4d;
      const res = getPermutationsOfCoordsFor4D(pos);
      expect(res.length).toBe(80);
      expect(res).toEqual(
        jasmine.arrayContaining([
          [-1, 0, 1, 2],
          [0, 1, 1, 2],
          [0, 2, 2, 3],
          [0, 1, 3, 4],
        ])
      );
      expect(res.indexOf(pos)).toBe(-1);
    });

    test(`calcCoordsForActiveCubes4D([[sample]])`, () => {
      expect(calcCoordsForActiveCubes4D([[sample]])).toEqual([
        [0, 1, 0, 0],
        [1, 2, 0, 0],
        [2, 0, 0, 0],
        [2, 1, 0, 0],
        [2, 2, 0, 0],
      ]);
    });

    test(`calcCoordsForActiveCubes4D([[[], sample, []]])`, () => {
      expect(calcCoordsForActiveCubes4D([[[], sample, []]])).toEqual([
        [0, 1, 0, 1],
        [1, 2, 0, 1],
        [2, 0, 0, 1],
        [2, 1, 0, 1],
        [2, 2, 0, 1],
      ]);
    });

    describe.each([
      [6, 848], // 26675 ms
    ])(
      `calcPocketDimensionFast4D(sample, %i)`,
      (value: number, expectedResult: number) => {
        test(`should return ${expectedResult}`, () => {
          const res = calcPocketDimensionFast4D(sample, value);
          const nextGen = calcNextGeneration(res);
          expect(nextGen.size).toBe(expectedResult);
        });
      }
    );

    test.skip(`calcPocketDimensionFast4D(inputs, 6)`, () => {
      const res = calcPocketDimensionFast4D(inputs, 6);
      const nextGen = calcNextGeneration(res);
      expect(nextGen.size).toBe(2136); // 70,323 ms
    });
  });
});
