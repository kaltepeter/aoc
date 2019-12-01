import { from, of } from 'rxjs';
import { flatMap, map, reduce, tap, toArray } from 'rxjs/operators';
import {
  doubleCheckedFuelCounterUpper$,
  fuelCounterUpper,
  fuelNeededForMass,
  totalFuelNeededByMass$
} from './challenge';
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

describe('1.2: totalFuelNeededByMass$', () => {
  describe.each([
    [14, 2],
    [1969, 966],
    [100756, 50346],
    [4, 0]
  ])('totalFuelNeededByMass$(%i)', (value, expected) => {
    test(`returns ${expected}`, async () => {
      expect.assertions(1);
      const val$ = await totalFuelNeededByMass$(value).toPromise();
      expect(val$).toBe(expected);
    });
  });
});

describe('1.2: total for modules', () => {
  test('total fuel required for [14,1969,100756] is 51314', async () => {
    expect.assertions(1);
    const val$ = await doubleCheckedFuelCounterUpper$([
      14,
      1969,
      100756
    ]).toPromise();
    expect(val$).toBe(51314);
  });

  test('total from example', async () => {
    expect.assertions(1);
    const val$ = await doubleCheckedFuelCounterUpper$([...inputs]).toPromise();
    expect(val$).toBe(4973628);
  });
});
