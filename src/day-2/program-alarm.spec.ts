import { EMPTY } from 'rxjs';
import {
  execGravityAssistProgram,
  execOp,
  fns,
  getOpFn
} from './program-alarm';

describe.skip('2: program alarm', () => {
  describe.each([
    [
      [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
      [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    ]
    // [
    //   [1, 0, 0, 0, 99],
    //   [2, 0, 0, 0, 99]
    // ],
    // [
    //   [2, 3, 0, 3, 99],
    //   [2, 3, 0, 6, 99]
    // ],
    // [
    //   [2, 4, 4, 5, 99],
    //   [2, 4, 4, 5, 99, 9801]
    // ],
    // [
    //   [1, 1, 1, 4, 99, 5, 6, 0, 99],
    //   [30, 1, 1, 4, 2, 5, 6, 0, 99]
    // ]
  ])('execGravityAssistProgram(%a)', (value: number[], expected: number[]) => {
    test(`returns ${expected}`, async () => {
      expect.assertions(1);
      const val$ = await execGravityAssistProgram(value).toPromise();
      expect(val$).toBe(expected);
    });
  });
});

describe('2: opcode', () => {
  let program: number[];

  beforeEach(() => {
    program = [1, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50];
  });

  describe.each`
    value | expected
    ${1}  | ${fns.add}
    ${2}  | ${fns.multiply}
    ${99} | ${fns.exit}
  `('getOpFn($value)', ({ value, expected }) => {
    test(`returns ${expected}`, () => {
      expect(getOpFn(value)).toBe(expected);
    });
  });

  test('add', () => {
    expect(fns.add(1, 3)).toBe(4);
  });

  test('multiply', () => {
    expect(fns.multiply(1, 3)).toBe(3);
  });
  test('exit', () => {
    expect(fns.exit(1, 3)).toBe(null);
  });
  test('error', () => {
    expect(getOpFn(1202)).toThrow(`unknown op code '1202'`);
  });

  describe.each`
    value               | expected
    ${[1, 9, 10, 3]}    | ${70}
    ${[2, 3, 11, 0]}    | ${3500}
    ${[99, 30, 40, 50]} | ${null}
  `('execOp($value)', ({ value, expected }) => {
    test(`returns ${expected}`, () => {
      expect(execOp(value, [...program])).toBe(expected);
    });
  });
});
