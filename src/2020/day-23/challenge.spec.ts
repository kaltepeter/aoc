import { inputs, sample } from './inputs';
import { getInputForAMillionCups, playCups } from './challenge';
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

    it.skip(`should should play cups for sample, 10000000 moves`, () => {
      const millionCupsInput = getInputForAMillionCups(sample).map((v) =>
        v.toString()
      );
      // console.log("🚀 ~ file: challenge.spec.ts ~ line 25 ~ it ~ millionCupsInput", millionCupsInput)
      const res = playCups(millionCupsInput, 10, true);
      // expect(playCups(millionCupsInput, 10, true)).toEqual(['934001', '159792']);
    });
  });
});
