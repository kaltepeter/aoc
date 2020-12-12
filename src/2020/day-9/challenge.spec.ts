import { findInvalidNumber, getValidNumbers } from './challenge';
import { inputs, sample } from './inputs';

describe(`day 9: Encoding Error`, () => {
  test(`should process numbers`, () => {
    expect(sample).toEqual({
      data: [
        40,
        62,
        55,
        65,
        95,
        102,
        117,
        150,
        182,
        127,
        219,
        299,
        277,
        309,
        576,
      ],
      preamble: [35, 20, 15, 25, 47],
    });
  });

  test(`findInvalidNumber(data)`, () => {
    expect(findInvalidNumber(sample)).toEqual([127]);
  });

  test(`findInvalidNumber(data)`, () => {
    expect(findInvalidNumber(inputs)).toEqual([138879426]);
  });

  describe.each([
    [40, [35, 20, 15, 25, 47], [15, 20, 25]],
    [62, [20, 15, 25, 47, 40], [15, 47]],
    [55, [15, 25, 47, 40, 62], [15, 40]],
    [65, [25, 47, 40, 62, 55], [25, 40]],
    [95, [47, 40, 62, 55, 65], [40, 55]],
    [102, [40, 62, 55, 65, 95], [40, 62]],
    [117, [62, 55, 65, 95, 102], [55, 62]],
    [150, [55, 65, 95, 102, 117], [55, 95]],
    [182, [65, 95, 102, 117, 150], [117, 65]],
    [127, [95, 102, 117, 150, 182], []],
  ])(
    `getValidNumbers(%i, %p)`,
    (num: number, list: number[], expectedValid: number[]) => {
      test(`should return ${expectedValid}`, () => {
        expect(getValidNumbers(num, list).sort()).toEqual([...expectedValid]);
      });
    }
  );
});
