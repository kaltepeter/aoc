import {
  convertToBinaryString,
  decodeDockDataV2,
  getMaskFromSeed,
  getMasksFromMaskString,
  processDockingData,
} from './challenge';
import { inputs, sample, sample2 } from './inputs';

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

  describe(`Part II`, () => {
    test(`bitmath test`, () => {
      const val = 0b00100;
      const mask = 0b00100;
      expect(val).toBe(4);
      expect(val | mask).toBe(4);
      expect(val & mask).toBe(4);
      expect(val ^ mask).toBe(0);
      expect(~val).toBe(-5);
    });

    test(`decodeDockDataV2(sample2)`, () => {
      expect(decodeDockDataV2(sample2)).toBe(208);
    });

    test(`decodeDockDataV2(inputs)`, () => {
      const res = decodeDockDataV2(inputs);
      expect(res).toBeGreaterThan(583466388456);
      expect(res).toBe(3296185383161);
    });

    test(`getMasksFromMaskString('000000000000000000000000000000X1101X)`, () => {
      const result = getMasksFromMaskString(
        '000000000000000000000000000000X1101X'
      );
      expect(result.size).toBe(4);

      expect(result).toContain('000000000000000000000000000000011010');
      expect(result).toContain('000000000000000000000000000000011011');
      expect(result).toContain('000000000000000000000000000000111011');
      expect(result).toContain('000000000000000000000000000000111010');
    });

    test(`getMasksFromMaskString('00000000000000000000000000000001X0XX)`, () => {
      const result = getMasksFromMaskString(
        '00000000000000000000000000000001X0XX'
      );
      expect(result).toContain('000000000000000000000000000000010000');
      expect(result).toContain('000000000000000000000000000000010001');
      expect(result).toContain('000000000000000000000000000000010010');
      expect(result).toContain('000000000000000000000000000000010011');
      expect(result).toContain('000000000000000000000000000000011000');
      expect(result).toContain('000000000000000000000000000000011001');
      expect(result).toContain('000000000000000000000000000000011010');
      expect(result).toContain('000000000000000000000000000000011011');
      expect(result.size).toBe(8);
    });

    test(`getMasksFromMaskString('00000000000000000000000000X00001X0XX)`, () => {
      const result = getMasksFromMaskString(
        '00000000000000000000000000X00001X0XX'
      );
      expect(result.size).toBe(12);
    });

    describe.each([
      [
        '000000000000000000000000000000101010',
        '000000000000000000000000000000X1001X',
        '000000000000000000000000000000X1101X',
      ],
      [
        '000000000000000000000000000000011010',
        '00000000000000000000000000000000X0XX',
        '00000000000000000000000000000001X0XX',
      ],
    ])(
      `getMaskSeed(%s,%s)`,
      (address: string, mask: string, expectedBinaryString: string) => {
        test(`should return ${expectedBinaryString}`, () => {
          expect(getMaskFromSeed(address, mask)).toBe(expectedBinaryString);
        });
      }
    );
  });
});
