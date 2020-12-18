import { findEarliestBusTime } from './challenge';
import { inputs, sample } from './inputs';
describe(`Day 13: Shuttle Search`, () => {
  test(`findEarliestBusTime(sample)`, () => {
    expect(findEarliestBusTime(sample)).toBe(295);
  });

  test(`findEarliestBusTime(inputs)`, () => {
    expect(findEarliestBusTime(inputs)).toBe(205);
  });
});
