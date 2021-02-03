import { readFileSync } from 'fs';
import { countMessagesMatchingRule, parseRulesAndMessages } from './solution';

export function readFileIntoGroups(path: string) {
  return readFileSync(path, 'utf-8').split('\n\n').filter(Boolean);
}

describe(`solution`, () => {
  it(`should work`, () => {
    const input = readFileIntoGroups(`${__dirname}/raw-input.txt`);
    expect(countMessagesMatchingRule(parseRulesAndMessages(input))).toEqual(
      226
    );
  });

  describe('Part II', () => {
    it('Example', () => {
      const input = readFileIntoGroups(`${__dirname}/raw-input.txt`);
      expect(countMessagesMatchingRule(parseRulesAndMessages(input))).toEqual(
        226
      );
    });

    const updateRules = (rules: string[]) =>
      rules.map((rule) => {
        if (rule.startsWith('8: ')) {
          return '8: 42 | 42 8';
        }
        if (rule.startsWith('11: ')) {
          return '11: 42 31 | 42 11 31';
        }
        return rule;
      });

    it('Example (Updated Rules)', () => {
      const input = readFileIntoGroups(`${__dirname}/raw-input.txt`);
      expect(
        countMessagesMatchingRule(parseRulesAndMessages(input, updateRules))
      ).toEqual(355);
    });
  });
});
