import fs from 'fs';
import path from 'path';
import { match } from 'ramda';
const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const processGroups = (t: string) =>
  t
    .split('\n\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((v) =>
      v
        .split('\n')
        .filter((val: string) => match(/^[a-zA-Z]+$/, val).length > 0)
        .map((p) => p.split(''))
    );

const inputs = processGroups(text);

const sampleData = processGroups(sampleDataText);

export { inputs, sampleData };
