import {
  findAdapterListByPossibleCount,
  getAdapterHash,
  getBuiltInDeviceJoltage,
  getCombinations,
  getDeltasOfAdapters,
  getRangeOfJoltage,
  IAdapterHash,
  removeOptionFromAdapterList,
  validateAdapterChain,
} from './challenge';
import { inputs, sample, sample2 } from './inputs';

describe(`day 10: Adapter Array`, () => {
  test(`get adapter list`, () => {
    expect(sample.length).toBe(11);
  });

  describe.each([
    [0, [1]],
    [4, [1, 5, 6, 7]],
  ])(
    `getRangeOfJoltage(%i, sample)`,
    (num: number, expectedValid: number[]) => {
      test(`should return ${expectedValid.toString()}`, () => {
        expect(getRangeOfJoltage(num, sample).sort()).toEqual([
          ...expectedValid,
        ]);
      });
    }
  );

  test(`getAdapterHash()`, () => {
    expect(getAdapterHash(sample)['4']).toEqual([5, 1, 7, 6]);
    expect(getAdapterHash(sample)['7']).toEqual([10, 5, 6, 4]);
  });

  test(`getBuiltInDeviceJoltage(sample)`, () => {
    expect(getBuiltInDeviceJoltage(sample)).toBe(22);
  });

  describe.each([
    [sample, { '1': 7, '3': 5 }, 35],
    [sample2, { '1': 22, '3': 10 }, 220],
    [inputs, { '1': 65, '3': 34 }, 2210],
  ])(
    `getDeltasOfAdapters(${JSON.stringify('%j')})`,
    (
      adapters: number[],
      expectedDeltas: { [key: string]: number },
      joltage: number
    ) => {
      test(`should return ${JSON.stringify(expectedDeltas)}`, () => {
        expect(getDeltasOfAdapters(adapters)).toEqual(expectedDeltas);
      });

      test(`should return ${joltage}`, () => {
        expect(
          getDeltasOfAdapters(adapters)['1'] * getDeltasOfAdapters(adapters)[3]
        ).toBe(joltage);
      });
    }
  );

  describe.each([
    [sample, []],
    [sample2, []],
    [inputs, []],
  ])(
    `validateAdapterChain(${JSON.stringify('%j')})`,
    (adapters: number[], expectedValid: number[]) => {
      test(`should return ${expectedValid.toString()}`, () => {
        expect(validateAdapterChain(adapters)).toEqual([...expectedValid]);
      });
    }
  );

  describe.each([
    [
      getAdapterHash(sample),
      1,
      {
        '1': [4],
        '19': [16],
      },
    ],
    [getAdapterHash(sample2), 1, {}],
    [
      getAdapterHash(sample),
      3,
      {
        '5': [7, 6, 4],
        '6': [5, 7, 4],
        '10': [11, 7, 12],
        '12': [10, 15, 11],
      },
    ],
  ])(
    `findAdapterListByPossibleCount(${JSON.stringify('%j')}, %d)`,
    (
      adapterHash: IAdapterHash,
      count: number,
      expectedPartialHash: IAdapterHash
    ) => {
      test(`should return ${JSON.stringify(expectedPartialHash)}`, () => {
        expect(findAdapterListByPossibleCount(adapterHash, count)).toEqual(
          expectedPartialHash
        );
      });
    }
  );

  test(`findAdapterListByPossibleCount(sample, 1)`, () => {
    const adapterHash = getAdapterHash(sample);
    expect(findAdapterListByPossibleCount(adapterHash, 1)).toEqual({
      '1': [4],
      '19': [16],
    });
  });

  test(`removeOptionFromAdapterList(sample2, 49)`, () => {
    const adapterHash = removeOptionFromAdapterList(
      getAdapterHash(sample2),
      49
    );
    const expectedAdapterHash = {
      '1': [4, 2, 3],
      '2': [1, 4, 3],
      '3': [1, 4, 2],
      '4': [1, 7, 2, 3],
      '7': [8, 9, 4, 10],
      '8': [11, 7, 9, 10],
      '9': [11, 8, 7, 10],
      '10': [11, 8, 7, 9],
      '11': [14, 8, 9, 10],
      '14': [11, 17],
      '17': [18, 14, 20, 19],
      '18': [20, 19, 17],
      '19': [18, 20, 17],
      '20': [18, 23, 19, 17],
      '23': [20, 24, 25],
      '24': [23, 25],
      '25': [28, 24, 23],
      '28': [31, 25],
      '31': [28, 33, 32, 34],
      '32': [33, 31, 35, 34],
      '33': [31, 32, 35, 34],
      '34': [33, 31, 32, 35],
      '35': [33, 38, 32, 34],
      '38': [39, 35],
      '39': [42, 38],
      '42': [45, 39],
      '45': [42, 46, 48, 47],
      '46': [48, 47, 45],
      '47': [46, 48, 45],
      '48': [46, 47, 45],
      '49': [46, 48, 47],
    };
    expect(adapterHash).toEqual(expectedAdapterHash);
  });

  describe(`part II`, () => {
    test(`getCombinations(sample)`, () => {
      expect(getCombinations(sample)).toBe(8);
    });

    test(`getCombinations(sample2)`, () => {
      expect(getCombinations(sample2)).toBe(19208);
    });

    test(`getCombinations(inputs)`, () => {
      expect(getCombinations(inputs)).toBe(7086739046912);
    });
  });
});
