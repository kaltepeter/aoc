import { fuelRequired } from './day_1';

describe('1: fuelRequired', () => {
  test('should return 2 when 12 is passed', () => {
    expect(fuelRequired(12)).toBe(2);
  });
});
