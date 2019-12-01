import { fuelRequired } from './day_1';

describe('1: fuelRequired', () => {
  describe.each([
    [12, 2],
    [14, 2],
    [1969, 654],
    [100756, 33583]
  ])('fuelRequired(%i)', (value, expected) => {
    test(`returns ${expected}`, () => {
      expect(fuelRequired(value)).toBe(expected);
    });
  });
});
