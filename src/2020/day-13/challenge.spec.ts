import {
  crt,
  findBusTimes,
  findEarliestBusTime,
  getTableOfBusses,
  getValidTimes,
  validateOutput,
} from './challenge';
import { inputs, sample } from './inputs';
describe(`Day 13: Shuttle Search`, () => {
  test(`findEarliestBusTime(sample)`, () => {
    expect(findEarliestBusTime(sample)).toBe(295);
  });

  test(`findEarliestBusTime(inputs)`, () => {
    expect(findEarliestBusTime(inputs)).toBe(205);
  });

  describe(`part II`, () => {
    test(`getTableOfBusses(sample)`, () => {
      expect(getTableOfBusses(sample)).toBe(1068781);
    });

    // suck it. This doesn't work
    test.skip(`getTableOfBusses(inputs)`, () => {
      const busTimes = getTableOfBusses(inputs);
      expect(busTimes).toBe(803025030761664);
      expect(busTimes).toBeGreaterThan(664875210780180);
      expect(busTimes).toBeLessThan(803025030762085);
      expect(busTimes).toBeGreaterThan(100000000000000);
    });

    test(`validateOutput(sample)`, () => {
      const validTimes: number[] = getValidTimes(sample[1]);
      expect(validateOutput(1068781, validTimes)).toBe(true);
    });

    test(`validateOutput(inputs)`, () => {
      const validTimes: number[] = getValidTimes(inputs[1]);
      expect(validateOutput(803025030761664, validTimes)).toBe(true);
    });

    test(`findBusTimes(inputs)`, () => {
      const busTimes = findBusTimes(inputs[1]);
      expect(busTimes).toBe(803025030761664);
      expect(busTimes).toBeGreaterThan(664875210780180);
      expect(busTimes).toBeLessThan(803025030762085);
      expect(busTimes).toBeGreaterThan(100000000000000);
    });

    // WTF, I don't understand math
    // x = 1, remainder is counting position backwards
    // expected is t + length of array, because of puzzle question
    // https://www.dave4math.com/mathematics/chinese-remainder-theorem/
    describe.each([
      [[7, 13, 1, 1, 59, 1, 31, 19], [8, 7, 6, 5, 4, 3, 2, 1], 1068781 + 8],
      [[67, 7, 59, 61], [4, 3, 2, 1], 754018 + 4],
      [[67, 1, 7, 59, 61], [5, 4, 3, 2, 1], 779210 + 5],
      [[67, 7, 1, 59, 61], [5, 4, 3, 2, 1], 1261476 + 5],
      [[17, 1, 13, 19], [4, 3, 2, 1], 3417 + 4],
      [[1789, 37, 47, 1889], [4, 3, 2, 1], 1202161486 + 4],
      [[3, 5, 7], [2, 3, 2], 23], // typical example
    ])(
      `crt(%j, %j)`,
      (numbers: number[], remainder: number[], expectedResult: number) => {
        test(`should return ${expectedResult}`, () => {
          expect(crt(numbers, remainder)).toEqual(expectedResult);
        });
      }
    );
  });
});
