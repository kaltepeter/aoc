import { join } from 'path';
import { any, gte, lte, pluck, transpose } from 'ramda';
import { writeToLog } from 'util/debug';

const LOG_FILE = join(__dirname, 'challenge.log');

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
  [key: string]: ((value: number) => boolean)[];
}

const getRangeFunc =
  (range: RuleRange): ((value: number) => boolean) =>
  (value) =>
    // console.log(`value: ${value}, r: ${range}`, (gte(value, range[0]) && lte(value,range[1])))
    gte(value, range[0]) && lte(value, range[1]);
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
  rules: IRuleSet,
  returnValid: boolean = false
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
    if (isValidForRule === returnValid) {
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
    .map((v) => pluck('invalid', v))
    .flat(1)
    .filter((v) => v.size > 0)
    .flatMap((v) => Array.from(v.values()));
  return invalidVals;
};

const getValidTickets = (ticketList: ITicketData): ITicketData => {
  const rules = processRules(ticketList.rules);
  const tix = [...ticketList.nearbyTickets, ticketList.ticket];
  const validTickets: number[][] = tix
    .map((t) => {
      const ticketVals = t.map((ticket) => validateEntry(ticket, rules));
      const countTicketVals = ticketVals.map((tv) => getTicketResults(tv));
      const invalidVals = pluck('invalid', Object.values(countTicketVals))
        .flat(1)
        .filter((v) => v.size > 0);
      if (invalidVals.length === 0) {
        return t;
      }
    })
    // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
    .filter<NonNullable<number[]>>(Boolean as any);

  return { ...ticketList, nearbyTickets: validTickets };
};

const validateColumn = (values: number[], rules: IRuleSet): Set<string> => {
  const results = new Set<string>();
  Object.entries(rules).forEach(([k, v]) => {
    let validCount = 0;
    for (const val of values) {
      const vResults = v.map((rule) => rule(val));
      const isValidForRule = any((x) => x === true, vResults);
      if (!isValidForRule) {
        break;
      }
      validCount += 1;
      if (validCount === values.length) {
        results.add(k);
      }
    }
  });
  return results;
};

const getTicketFieldList = (
  rules: IRuleSet,
  ticketFieldValues: number[][]
): Set<string>[] => {
  writeToLog(
    LOG_FILE,
    `process fieldCount: ${ticketFieldValues.length}, itemCount: ${ticketFieldValues[0].length}`
  );
  const possibleVals = ticketFieldValues.map((cols: number[]) =>
    validateColumn(cols, rules)
  );
  // console.log("🚀 ~ file: challenge.ts ~ line 162 ~ getTicketFieldList ~ possibleVals", possibleVals.sort((a,b) => a.size - b.size))
  return possibleVals;
};

const processTickets = (ticketList: ITicketData): Record<string, number> => {
  const rules = processRules(ticketList.rules);
  const fieldValues = transpose(ticketList.nearbyTickets);
  const list = getTicketFieldList(rules, fieldValues);
  const fieldList: Record<string, number> = {};
  do {
    for (let i = 0; i < list.length; i++) {
      if (list[i].size === 1) {
        const field = Array.from(list[i])[0];
        fieldList[field] = i;
        list[i].delete(field);
        list.filter((x) => x.has(field)).map((x) => x.delete(field));
      }
    }
  } while (Object.keys(fieldList).length < fieldValues.length);
  return fieldList;
};

const getDepartureFieldsResult = (
  fieldList: Record<string, number>,
  ticketList: ITicketData
) =>
  // console.log(ticketList)
  Object.entries(fieldList)
    .filter(([k, _v]) => k.startsWith('departure'))
    .map(([_k, v]) => ticketList.ticket[v])
    .reduce((acc, v) => (acc *= v), 1);
export {
  getInvalidTicketValues,
  processRules,
  getErrorRate,
  getValidTickets,
  getTicketFieldList,
  processTickets,
  validateColumn,
  getDepartureFieldsResult,
};
