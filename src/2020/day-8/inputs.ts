import fs from 'fs';
import path from 'path';
import { ProgramLine } from './challenge';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const processProgram = (t: string): ProgramLine[] =>
  t
    .split('\n\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((v) =>
      v
        .trim()
        .split('\n')
        .map((inst) => {
          const i = inst.split(' ');
          return { command: i[0], value: i[1] } as ProgramLine;
        })
    )
    .flat(1);
const inputs = processProgram(text);

const sampleData = processProgram(sampleDataText);

export { inputs, sampleData };
