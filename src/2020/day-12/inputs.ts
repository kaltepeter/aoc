import fs from 'fs';
import path from 'path';
import { Action, Instructions } from './challenge';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const processInstructions = (t: string): Instructions =>
  t
    .split('\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((inst) => {
      const [a, ...i] = inst;
      return [a, +i.join('')] as [Action, number];
    });

const inputs = processInstructions(text);
const sample = processInstructions(sampleDataText);

export { inputs, sample };
