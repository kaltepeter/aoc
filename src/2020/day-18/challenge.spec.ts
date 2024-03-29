import { inputs, sample } from './inputs';
import {
  calcSumOfAnswers,
  processExpression,
  processExpressionV2,
} from './challenge';

describe(`Day 18: Operation Order`, () => {
  it(`should process data`, () => {
    expect(sample.length).toBe(6);
    expect(inputs.length).toBe(381);
  });

  describe.each([
    [sample[0], 71],
    [sample[1], 51],
    [sample[2], 26],
    [sample[3], 437],
    [sample[4], 12240],
    [sample[5], 13632],
  ])(`processExpression(%s)`, (value: string, expectedResult: number) => {
    test(`should return ${expectedResult}`, () => {
      expect(processExpression(value)).toBe(expectedResult);
    });
  });

  describe(`calcSumOfAnswers(sample)`, () => {
    expect(calcSumOfAnswers(sample)).toBe(26457);
  });

  describe(`calcSumOfAnswers(inputs)`, () => {
    expect(calcSumOfAnswers(inputs)).toBe(14208061823964);
  });

  describe(`part II`, () => {
    describe.each([
      [sample[0], 231],
      [sample[1], 51],
      [sample[2], 46],
      [sample[3], 1445],
      [sample[4], 669060],
      [sample[5], 23340],
    ])(`processExpressionV2(%s)`, (value: string, expectedResult: number) => {
      test(`should return ${expectedResult}`, () => {
        expect(processExpressionV2(value)).toBe(expectedResult);
      });
    });

    describe(`calcSumOfAnswers(inputs)`, () => {
      expect(calcSumOfAnswers(inputs, processExpressionV2)).toBe(
        320536571743074
      );
    });
  });
});
