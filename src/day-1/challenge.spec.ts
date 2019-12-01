import { fuelCounterUpper, fuelRequired } from './challenge';
import { inputs } from './inputs';

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

  describe.each([...inputs.slice(0, 3)])('value of fuelRequired(%i)', value => {
    test(`returns ${fuelRequired(value)}`, () => {
      expect(fuelRequired(value)).toBe(fuelRequired(value));
    });
  });
});

describe('1: total', () => {
  test('total fuel required', () => {
    const total = fuelCounterUpper([12, 14, 1969, 100756]);
    expect(total).toBe(34241);
  });

  test('total from example', () => {
    const total = fuelCounterUpper([...inputs]);
    expect(total).toBeGreaterThan(3317666);
  });
});
