import fs from 'fs';
import path from 'path';
import { IRule, ITicketData, RuleRange } from './challenge';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const processRules = (ruleList: string): IRule[] =>
  ruleList.split('\n').map((r) => {
    const [key, v] = r.split(':');
    const valList: RuleRange[] = v
      .split(' or ')
      .map(
        (rangeStr) => rangeStr.split('-').map((i) => +i.trim()) as RuleRange
      );
    return {
      [key]: valList,
    };
  });

const processTickets = (tList: string) =>
  tList
    .split(':')[1]
    .split('\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((l) => l.split(',').map((v) => +v));

const processGroups = (i: string) => i.split('\n\n');

const readData = (t: string): ITicketData => {
  const [rList, ticket, nearbyTicketList] = processGroups(t);
  return {
    rules: processRules(rList),
    ticket: processTickets(ticket)[0],
    nearbyTickets: processTickets(nearbyTicketList),
  };
};

const inputs = readData(text);
const sample = readData(sampleDataText);

export { inputs, sample };
