import { inputs, sample } from './inputs';
import {
  calcStarLabels,
  getInputForAMillionCups,
  playCups,
  playCupsPartII,
} from './challenge';
import { LinkedList } from '../../model/linked-list';

describe(`Day 23: Crab Cups`, () => {
  it(`should should play cups for sample, 10 moves`, () => {
    expect(playCups([...sample])).toBe('92658374');
  });

  it(`should should play cups for sample, 100 moves`, () => {
    const res = playCups([...sample], 100);
    expect(res).toBe('67384529');
  });

  it(`should should play cups for input, 100 moves`, () => {
    const res = playCups([...inputs], 100);
    expect(res).not.toBe('78542396'); // too high
    expect(res).toBe('45983627');
  });

  describe(`part II`, () => {
    it(`getInputForAMillionCups(inputs)`, () => {
      expect(getInputForAMillionCups([...inputs]).length).toBe(1000000);
    });

    it(`should calculate results of star labels`, () => {
      expect(calcStarLabels([934001, 159792])).toBe(149245887792);
    });

    describe.each([
      [[934001, 159792], 149245887792],
      [[931248, 119281], 111080192688],
    ])(`calcStarLabels(%a)`, (inputArr: number[], expectedValue: number) => {
      it(`should return ${expectedValue}`, () => {
        expect(calcStarLabels(inputArr)).toBe(expectedValue);
      });
    });

    describe(`playCupsPartII`, () => {
      it(`should should play cups for sample, 100 moves`, () => {
        const result = playCupsPartII(sample, 100);
        expect(result).toEqual([6, 7]);
      });

      it(`should should play cups for inputs, 100 moves`, () => {
        const result = playCupsPartII(inputs, 100);
        expect(result).toEqual([4, 5]);
      });
    });
  });
});
