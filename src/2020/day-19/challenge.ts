import {
  all,
  any,
  ap,
  curry,
  curryN,
  equals,
  flatten,
  map,
  mapAccum,
  unless,
  when,
  zip,
  __,
} from 'ramda';

export interface IMonsterMessages {
  rules: Map<number, string | number[][]>;
  messages: string[];
}

export type Rule = (v: string) => RuleResult;
export type Rules = Map<number, Rule>;
export type RuleResult = [boolean, string];

// subRule: '4 4' or '3 4 5'
const parseSubRuleString = (subRule: string): number[] =>
  subRule.split(/\s/).map((v) => +v);
const ruleLookup = curry((rId: number, rList: Rules) => rList.get(rId));
const genEqualRule = curry((subRule: string, msg: string) => {
  if (msg.length < subRule.length) {
    return [false, ''] as RuleResult;
  }
  const m = msg.slice(0, subRule.length);
  const res = equals(subRule, m);
  return [res, msg.slice(subRule.length)];
});
const genSubRule = curry((sRuleList: number[], rList: Rules, msg: string) => {
  if (msg.length < sRuleList.length) {
    return [false, ''] as RuleResult;
  }
  const processSubRule = map<any, RuleResult>(
    ([fn, v]) => fn(rList)(v),
    zip(map(ruleLookup, sRuleList), msg.split(''))
  );
  const res = all((r) => r[0] === true, processSubRule);
  return [res, msg.slice(sRuleList.length)] as RuleResult;
});
const genRule = curry((sRuleList: number[][], rList: Rules, msg: string) => {
  const processRule = map((sRule) => genSubRule(sRule, rList, msg), sRuleList);
  const valid = processRule.filter((r) => r[0] === true);
  if (valid.length > 0) {
    return valid[0];
  } else {
    return [false, ''];
  }
});

const createRules = (rawRules: Map<number, string | number[][]>) => {
  const rules = new Map<number, any>();
  for (let [ruleId, subRules] of rawRules) {
    if (typeof subRules === 'string') {
      rules.set(ruleId, genEqualRule(subRules));
    } else {
      const rule = genRule(subRules)(rules); // TODO: need to combine rules as or
      rules.set(ruleId, rule);
    }
  }
  return rules;
};

const processRules = (
  rules: Map<number, any>,
  ruleToProcess: number[],
  msg: string
) => {
  let m = msg.slice(0);
  let res = false;
  for (let n of ruleToProcess) {
    [res, m] = rules.get(n)(m);
    console.log(
      '🚀 ~ file: challenge.ts ~ line 57 ~ processRules ~ res',
      n,
      res,
      m
    );
  }
  return res;
};

export {
  createRules,
  ruleLookup,
  genRule,
  genSubRule,
  genEqualRule,
  processRules,
};
