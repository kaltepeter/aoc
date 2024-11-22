type RuleMap = Map<number, MatchRule>;
type MatchRule = (str: string) => string[];
interface IMatchState {
  matched: string;
  rest: string;
}

// How many messages completely match rule 0?
export function countMessagesMatchingRule({
  messages,
  ruleMap,
}: {
  messages: string[];
  ruleMap: RuleMap;
}) {
  // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
  const matchRuleZerro = ruleMap.get(0)!;
  const validMessages = messages.filter((m) => matchRuleZerro(m).includes(m));
  return validMessages.length;
}

export function parseRulesAndMessages(
  groups: string[],
  updateRules?: (rules: string[]) => string[]
) {
  const messages = groups[1].split('\n').filter((v) => Boolean(v));
  let rules = groups[0].split('\n').filter((v) => Boolean(v));
  const ruleMap: RuleMap = new Map();
  const resultMap = new Map<string, string[]>();

  const initRules = () => {
    // this this for part two
    rules = updateRules ? updateRules(rules) : rules;

    rules.forEach((ruleStr) => {
      const [ruleIndexStr, ruleValue] = ruleStr.split(': ');
      const ruleIndex = Number(ruleIndexStr);
      const subRuleOptions = ruleValue
        .split(' | ')
        .map((o) => o.split(' ').map((n) => parseInt(n, 10)));

      const charValue = ruleValue.includes('"')
        ? unquote(ruleValue.trim())
        : undefined;

      const matchCharRule = (str: string): string[] => {
        if (!charValue) {
          throw Error('charValue missing');
        }
        return str.startsWith(charValue) ? [charValue] : [];
      };

      const matchRule = (str: string): string[] => {
        const key = `${ruleIndex}-` + str;

        if (resultMap.has(key)) {
          return resultMap.get(key) || [];
        }

        const matches = subRuleOptions.flatMap((ruleIdSequence) => {
          let matchStates: IMatchState[] = [{ matched: '', rest: str }];

          for (const ruleId of ruleIdSequence) {
            matchStates = matchStates.flatMap(({ matched, rest }) =>
              (getRule(ruleId)?.(rest) ?? []).map((matchedPart) => ({
                matched: matched + matchedPart,
                rest: removeMatchedPart(rest, matchedPart),
              }))
            );
          }

          return matchStates.map((m) => m.matched);
        });

        resultMap.set(key, matches);

        return matches;
      };

      if (charValue) {
        ruleMap.set(ruleIndex, matchCharRule);
      } else {
        ruleMap.set(ruleIndex, matchRule);
      }
    });
  };

  const getRule = (i: number) =>
    // tslint:disable-next-line: no-non-null-assertion
    ruleMap.get(i);

  const removeMatchedPart = (str: string, usedStr: string) =>
    str.replace(usedStr, '');

  initRules();

  return {
    ruleMap,
    messages,
  };
}

function unquote(str: string) {
  return str.replace(/^"/, '').replace(/"$/, '');
}
