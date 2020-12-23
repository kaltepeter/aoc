import fs from 'fs';
import path from 'path';
import { IDockData } from './challenge';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const readData = (t: string): number[][] =>
  t
    .split('\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((l) => l.split(',').map((v) => +v));

const inputs = readData(text);
const sample = readData(sampleDataText);

export { inputs, sample };
