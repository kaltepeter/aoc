import { inputs, sample } from './inputs';
import { playCups } from './challenge';

describe(`Day 23: Crab Cups`, () => {
  it(`should should play cups for sample, 10 moves`, () => {
    expect(playCups(sample)).toBe('92658374');
  });

  it(`should should play cups for sample, 100 moves`, () => {
    expect(playCups(sample, 100)).toBe('67384529');
  });

  it(`should should play cups for input, 100 moves`, () => {
    expect(playCups(inputs, 100)).not.toBe('78542396'); // too high
    expect(playCups(inputs, 100)).toBe('45983627');
  });
});
