import fs from 'fs';
import path from 'path';
import { IDockData } from './challenge';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const processDockingData = (t: string): IDockData[] =>
  t
    .split(/^mask/m)
    .filter((val: string) => !(val.trim() === ''))
    .map((l) => {
      const lines = l
        .split('\n')
        .filter((val: string) => !(val.trim() === ''))
        .map((v) => v.split('=').map((m) => m.trim()));
      const [mask, ...memory] = lines;
      const mems = memory.map(([loc, v]) => ({
        loc: loc.replace(/mem\[(.*)\]/, '$1'),
        value: +v,
      }));
      return {
        mask: mask[1],
        memory: [...mems],
      };
    });

const inputs = processDockingData(text);
const sample = processDockingData(sampleDataText);

export { inputs, sample };
