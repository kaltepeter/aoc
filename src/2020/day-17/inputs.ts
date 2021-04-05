import fs from 'fs';
import path from 'path';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const expectedResultText = fs
  .readFileSync(path.join(__dirname, 'expected-result-cycle1.txt'))
  .toString('utf-8');

const readData = (t: string): string[][] =>
  t
    .split('\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((l) => l.split('').map((v) => v));

const inputs = readData(text);
const sample = readData(sampleDataText);

const expectedResultCycle1 = expectedResultText
  .split('\n\n')
  .map((er) => readData(er));

export { inputs, sample, expectedResultCycle1 };
