import fs from 'fs';
import path from 'path';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const sampleData2Text = fs
  .readFileSync(path.join(__dirname, 'sample-data-2.txt'))
  .toString('utf-8');

const processAdapterList = (t: string): number[] =>
  t
    .split('\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((v) => +v);

const inputs = processAdapterList(text);
const sample = processAdapterList(sampleDataText);
const sample2 = processAdapterList(sampleData2Text);
export { inputs, sample, sample2 };
