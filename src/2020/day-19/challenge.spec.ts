import {
  createRules,
  genRule,
  ruleLookup,
  Rules,
  genSubRule,
  RuleResult,
  genEqualRule,
  processRules,
} from './challenge';
import { sample, inputs } from './inputs';

const testRules: Rules = new Map();
testRules.set(4, genEqualRule('a'));
testRules.set(5, genEqualRule('b'));

describe(`Day 19: Monster Messages`, () => {
  it(`should process data`, () => {
    expect(sample.rules.size).toBe(6);
    expect(sample.messages.length).toBe(5);
    // inputs
    expect(inputs.rules.size).toBe(129);
    expect(inputs.messages.length).toBe(468);
  });

  it(`ruleLookup(4)()`, () => {
    expect(ruleLookup(4)(testRules)('a')).toEqual([true, '']);
    expect(ruleLookup(4)(testRules)('aa')).toEqual([true, 'a']);
    expect(ruleLookup(4)(testRules)('b')).toEqual([false, '']);
  });

  describe(`genSubRule(4)()`, () => {
    it(`should return false if less chars than subRule`, () => {
      expect(genSubRule([4, 4])(testRules)('a')).toEqual([false, '']);
    });

    it(`should return true if each char matches`, () => {
      expect(genSubRule([4, 4])(testRules)('aa')).toEqual([true, '']);
      expect(genSubRule([4, 4])(testRules)('bb')).toEqual([false, '']);
    });

    it(`should handle extra chars`, () => {
      expect(genSubRule([4, 4])(testRules)('aaa')).toEqual([true, 'a']);
    });
  });

  describe.each([
    [
      [
        [4, 4],
        [5, 5],
      ],
      'ab',
      [false, ''] as RuleResult,
    ],
    [
      [
        [4, 4],
        [5, 5],
      ],
      'aa',
      [true, ''] as RuleResult,
    ],
    [
      [
        [4, 4],
        [5, 5],
      ],
      'aaab',
      [true, 'ab'] as RuleResult,
    ],
    [
      [
        [4, 4],
        [5, 5],
      ],
      'bb',
      [true, ''] as RuleResult,
    ],
    [
      [
        [4, 4],
        [5, 5],
      ],
      'a',
      [false, ''] as RuleResult,
    ],
  ])(
    `genRule(%j)(testRules)(%s)`,
    (value: number[][], msg: string, expectedResult: RuleResult) => {
      test(`should return ${expectedResult}`, () => {
        expect(genRule(value)(testRules)(msg)).toEqual(expectedResult);
      });
    }
  );

  it(`genRule(3)()`, () => {
    expect(genRule([[3]])(testRules)).toEqual(jasmine.any(Function));
  });

  describe(`createRules()`, () => {
    let rules;
    beforeEach(() => {
      rules = createRules(sample.rules);
    });

    describe(`rule.get(0)`, () => {
      it.each([
        // ['ababbb', [true, ''] as RuleResult],
        ['ab', [false, ''] as RuleResult],
        ['bb', [false, ''] as RuleResult],
      ])(`(%s) should equal(%j)`, (msg: string, expectedResult: RuleResult) => {
        expect(rules.get(0)(msg)).toEqual(expectedResult);
      });
    });

    describe(`rule.get(1)`, () => {
      it.each([
        // ['aaab', [true, ''] as RuleResult],
        // ['babbb', [true, 'b'] as RuleResult],
        ['aabb', [false, ''] as RuleResult],
        ['aa', [false, ''] as RuleResult],
      ])(`(%s) should equal(%j)`, (msg: string, expectedResult: RuleResult) => {
        expect(rules.get(1)(msg)).toEqual(expectedResult);
      });
    });

    describe(`rule.get(2)`, () => {
      it.each([
        ['a', [false, ''] as RuleResult],
        ['aa', [true, ''] as RuleResult],
        ['bb', [true, ''] as RuleResult],
        ['ab', [false, ''] as RuleResult],
        ['aaa', [true, 'a'] as RuleResult],
      ])(`(%s) should equal(%j)`, (msg: string, expectedResult: RuleResult) => {
        expect(rules.get(2)(msg)).toEqual(expectedResult);
      });
    });

    describe(`rule.get(3)`, () => {
      it.each([
        ['ab', [true, ''] as RuleResult],
        ['aa', [false, ''] as RuleResult],
        ['ba', [true, ''] as RuleResult],
        ['bb', [false, ''] as RuleResult],
        ['aba', [true, 'a'] as RuleResult],
      ])(`(%s) should equal(%j)`, (msg: string, expectedResult: RuleResult) => {
        expect(rules.get(3)(msg)).toEqual(expectedResult);
      });
    });

    describe(`rule.get(4)`, () => {
      it.each([
        ['a', [true, ''] as RuleResult],
        ['b', [false, ''] as RuleResult],
        ['aa', [true, 'a'] as RuleResult],
        ['aba', [true, 'ba'] as RuleResult],
      ])(`(%s) should equal(%j)`, (msg: string, expectedResult: RuleResult) => {
        expect(rules.get(4)(msg)).toEqual(expectedResult);
      });
    });

    describe(`rule.get(5)`, () => {
      it.each([
        ['b', [true, ''] as RuleResult],
        ['a', [false, ''] as RuleResult],
        ['bb', [true, 'b'] as RuleResult],
      ])(`(%s) should equal(%j)`, (msg: string, expectedResult: RuleResult) => {
        expect(rules.get(5)(msg)).toEqual(expectedResult);
      });
    });
  });

  it.skip(`processRules()`, () => {
    const rules = createRules(sample.rules);
    expect(processRules(rules, [4, 1, 5], 'ababbb')).toBe(true);
  });
});
