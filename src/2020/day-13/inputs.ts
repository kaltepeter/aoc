import fs from 'fs';
import path from 'path';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const processBusTimes = (t: string) =>
  t.split('\n').filter((val: string) => !(val.trim() === ''));

const inputs = processBusTimes(text);
const sample = processBusTimes(sampleDataText);

export { inputs, sample };
