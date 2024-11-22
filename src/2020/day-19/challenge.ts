import { fromPairs } from 'ramda';

export interface IMonsterMessages {
  rules: Map<number, string | number[][]>;
  messages: string[];
}

export type Rule = (v: string) => RuleResult;
export type Rules = Map<number, Rule>;
export type RuleResult = [boolean, string];

const createRulesV2 = (rawRules: Map<number, string>) => {
  const stringRules = fromPairs(
    [...rawRules.entries()].filter(([_, rule]) => rule.match(/[a-z]/i))
  );
  const newRules = new Map(rawRules);
  for (const [k, v] of rawRules) {
    if (v.includes('|')) {
      const r = v.replace(/([\d\s]*)?[|]+([\d\s]*)?/g, '(?:$1|$2)?');
      newRules.set(k, r);
    }
  }
  let pRules;
  do {
    for (const [rId, r] of newRules) {
      let rule = r;
      Object.entries(stringRules).forEach(([_k, v]) => {
        rule = rule.replace(/${k}/g, v);
      });
      if (!rule.match(/\d/)) {
        rule = rule.replace(/ /g, '');
      } else {
        const nums = rule.match(/(\d+)/g);
        nums?.forEach((n) => {
          const nr = newRules.get(+n);
          if (!nr?.match(/\d/)) {
            rule = rule.replace(n, `${nr?.replace(/ /g, '')}`);
          }
        });
      }
      newRules.set(rId, rule);
    }
    pRules = Array.from(newRules.values()).filter(
      (v) => v.match(/\d/) || v.match(/ /)
    );
  } while (pRules.length > 0);

  return newRules;
};

const processRules = (
  rules: Map<number, string>,
  ruleToProcess: number,
  msgs: string[]
) => {
  const messageResults: boolean[] = msgs.map((msg) => {
    const m = msg.trim();
    const rule = rules.get(ruleToProcess);
    if (!rule) {
      return false;
    }
    const r = new RegExp(`^${rule}$`, 'g');
    const messageReplaced = r.exec(m);
    return messageReplaced !== null;
  });
  const res = messageResults.filter((m) => m === true);

  return res;
};

export { createRulesV2, processRules };
