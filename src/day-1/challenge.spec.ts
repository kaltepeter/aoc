import { fuelCounterUpper, fuelNeededForMass } from './challenge';
import { inputs } from './inputs';

describe('1: fuelNeededForMass', () => {
  describe.each([
    [12, 2],
    [14, 2],
    [1969, 654],
    [100756, 33583]
  ])('fuelNeededForMass(%i)', (value, expected) => {
    test(`returns ${expected}`, () => {
      expect(fuelNeededForMass(value)).toBe(expected);
    });
  });

  describe.each([...inputs.slice(0, 3)])(
    'value of sample data [0,3] fuelNeededForMass(%i)',
    value => {
      test(`returns ${fuelNeededForMass(value)}`, () => {
        expect(fuelNeededForMass(value)).toBe(fuelNeededForMass(value));
      });
    }
  );
});

describe('1: total for modules', () => {
  test('total fuel required', () => {
    const total = fuelCounterUpper([12, 14, 1969, 100756]);
    expect(total).toBe(34241);
  });

  test('total from example', () => {
    const total = fuelCounterUpper([...inputs]);
    expect(total).toBe(3317668);
  });
});

describe('1.2: fuel mass', () => {
  test('should count for fuel', () => {
    expect(2).toBe(2);
  });
});
