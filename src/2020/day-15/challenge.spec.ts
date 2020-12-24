import { playGame } from './challenge';
import { inputs, sample } from './inputs';

describe(`Day 15: Rambunctious Recitation`, () => {
  test(`readData()`, () => {
    expect(sample.length).toBe(7);
    expect(sample[0].length).toBe(3);
    expect(inputs.length).toBe(1);
    expect(inputs[0].length).toBe(6);
  });

  describe.each([
    [sample[0], 436],
    [sample[1], 1],
    [sample[2], 10],
    [sample[3], 27],
    [sample[4], 78],
    [sample[5], 438],
    [sample[6], 1836],
  ])(`playGame(%j)`, (startNumbers: number[], expectedResult: number) => {
    test(`should return ${expectedResult}`, () => {
      const game = playGame(startNumbers);
      expect(game).toBe(expectedResult);
    });
  });

  test(`playGame(inputs[0])`, () => {
    const game = playGame(inputs[0]);
    expect(game).toBe(1259);
  });
});
