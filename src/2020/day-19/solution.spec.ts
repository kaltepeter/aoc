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
});
