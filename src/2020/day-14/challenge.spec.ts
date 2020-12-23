import { convertToBinaryString, processDockingData } from './challenge';
import { inputs, sample } from './inputs';

describe(`Day 14: Docking Data`, () => {
  test(`processDockData`, () => {
    expect(sample.length).toBe(1);
  });
  test(`processDockData inputs`, () => {
    expect(inputs.length).toBe(100);
  });

  test(`processDockData(sample)`, () => {
    expect(processDockingData(sample)).toBe(165);
  });

  test(`processDockData(inputs)`, () => {
    expect(processDockingData(inputs)).toBeGreaterThan(48478083036);
    expect(processDockingData(inputs)).toBeGreaterThan(230437326099);
    expect(processDockingData(inputs)).toBeGreaterThan(338927164419);
    expect(processDockingData(inputs)).not.toBe(14866570214947);
    expect(processDockingData(inputs)).toBe(14862056079561);
  });

  describe.each([
    [30, 1073741824, '000001000000000000000000000000000000'],
    [31, 2147483648, '000010000000000000000000000000000000'],
    [32, 4294967296, '000100000000000000000000000000000000'],
    [33, 8589934592, '001000000000000000000000000000000000'],
    [34, 17179869184, '010000000000000000000000000000000000'],
    [35, 34359738368, '100000000000000000000000000000000000'],
    // [36, 68719476736, '1000000000000000000000000000000000000'],
  ])(
    `JS large number math`,
    (pos: number, expectedResult: number, expectedBinaryString: string) => {
      test(`should return ${expectedResult}`, () => {
        // expect(1 << pos).toEqual(expectedResult); // after pos 30 next bit is negative and starts at 1
        expect(Math.pow(2, pos)).toEqual(expectedResult);
      });

      test(`convertToBinaryString(${expectedResult})`, () => {
        expect(expectedBinaryString.length).toBe(36);
        expect(convertToBinaryString(BigInt(expectedResult))).toBe(
          expectedBinaryString
        );
      });

      test(`parseInt`, () => {
        expect(parseInt(expectedBinaryString, 2)).toBe(expectedResult);
      });
    }
  );
});
