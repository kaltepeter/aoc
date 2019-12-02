import { execGravityAssistProgram } from './program-alarm';

describe('2: program alarm', () => {
  describe.each([
    [
      [1, 0, 0, 0, 99],
      [2, 0, 0, 0, 99]
    ],
    [
      [2, 3, 0, 3, 99],
      [2, 3, 0, 6, 99]
    ],
    [
      [2, 4, 4, 5, 99],
      [2, 4, 4, 5, 99, 9801]
    ],
    [
      [1, 1, 1, 4, 99, 5, 6, 0, 99],
      [30, 1, 1, 4, 2, 5, 6, 0, 99]
    ]
  ])('execGravityAssistProgram(%a)', (value: number[], expected: number[]) => {
    test(`returns ${expected}`, () => {
      expect(execGravityAssistProgram(value)).toBe(expected);
    });
  });
});
