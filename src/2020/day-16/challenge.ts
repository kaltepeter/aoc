import {
  all,
  any,
  countBy,
  groupBy,
  gte,
  invert,
  invertObj,
  lte,
  pluck,
  where,
} from 'ramda';

export type RuleRange = [number, number];
export interface IRule {
  [key: string]: RuleRange[];
}
export interface ITicketData {
  rules: IRule[];
  ticket: number[];
  nearbyTickets: number[][];
}

export interface IRuleSet {
  [key: string]: Array<(value: number) => boolean>;
}

const isTicketValid = where({
  ticket: (t: number[]) => {
    console.log(t);
  },
});

const getRangeFunc = (range: RuleRange): ((value: number) => boolean) => {
  return (value) => {
    // console.log(`value: ${value}, r: ${range}`, (gte(value, range[0]) && lte(value,range[1])))
    return gte(value, range[0]) && lte(value, range[1]);
  };
};

const processRules = (rules: IRule[]): IRuleSet => {
  const ruleList = {} as IRuleSet;
  rules.map((r) => {
    Object.entries(r).forEach(([k, v]) => {
      const ranges = v.map((range) => getRangeFunc(range));
      ruleList[k] = ranges;
    });
  });
  return ruleList;
};

const validateEntry = (
  val: number,
  rules: IRuleSet
): Record<string, number[]> => {
  // return invalid entries
  const results: Record<string, number[]> = {};
  Object.entries(rules).forEach(([k, v]) => {
    if (!results[k]) {
      results[k] = [];
    }
    const vResults = v.map((rule) => rule(val));
    const isValidForRule = any((x) => x === true, vResults);
    // console.log("🚀 ~ file: challenge.ts ~ line 50 ~ Object.entries ~ vResults", k, val, vResults, isValidForRule)
    if (isValidForRule === false) {
      results[k] = [...results[k], val];
    }
  });
  return results;
};

const getTicketResults = (
  ticket: Record<string, number[]>
): Record<string, Set<number>> => {
  const ruleCount = Object.keys(ticket).length;
  const vals = Object.values(ticket).flat(1);
  const len = vals.length;
  const valid = new Set<number>();
  const invalid = new Set<number>();

  vals.forEach((v) => {
    if (len === ruleCount) {
      invalid.add(v);
    } else {
      valid.add(v);
    }
  });

  return {
    valid,
    invalid,
  };
};

const getErrorRate = (errorVals: number[]): number =>
  errorVals.reduce((acc, v) => (acc += +v), 0);

const getInvalidTicketValues = (ticketList: ITicketData): number[] => {
  const rules = processRules(ticketList.rules);
  const tix = [...ticketList.nearbyTickets];
  const tVals = tix.map((t) => {
    const ticketVals = t.map((ticket) => validateEntry(ticket, rules));
    const countTicketVals = ticketVals.map((tv) => getTicketResults(tv));
    return countTicketVals;
  });
  const invalidVals = Object.values(tVals)
    .map((v) => {
      return pluck('invalid', v);
    })
    .flat(1)
    .filter((v) => v.size > 0)
    .flatMap((v) => Array.from(v.values()));
  return invalidVals;
};

export { isTicketValid, getInvalidTicketValues, processRules, getErrorRate };
