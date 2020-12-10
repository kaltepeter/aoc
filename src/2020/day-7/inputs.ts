import fs from 'fs';
import path from 'path';
import { Rule } from './challenge';
const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const processGroups = (t: string) =>
  t
    .split('\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((rule) => rule.split(' bags contain '))
    .map((rules) => [rules[0], rules[1].trim().replace('.', '')] as Rule);

const inputs = processGroups(text);

const sampleData = processGroups(sampleDataText);

export { inputs, sampleData };
