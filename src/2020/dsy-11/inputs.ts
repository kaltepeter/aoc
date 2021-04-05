import fs from 'fs';
import path from 'path';
import { Seat, SeatMap } from './challenge';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const sampleDataRound1Text = fs
  .readFileSync(path.join(__dirname, 'sample-data-round1.txt'))
  .toString('utf-8');

const sampleDataPartIIText = fs
  .readFileSync(path.join(__dirname, 'sample-data-partii.txt'))
  .toString('utf-8');

const sampleDataPartIIRound2Text = fs
  .readFileSync(path.join(__dirname, 'sample-data-pt2-round2.txt'))
  .toString('utf-8');

const processSeatMap = (t: string): SeatMap =>
  t
    .split('\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((v) => v.split('') as Seat[]);

const inputs = processSeatMap(text);
const sample = processSeatMap(sampleDataText);
const sampleRound1 = processSeatMap(sampleDataRound1Text);
const samplePartII = processSeatMap(sampleDataPartIIText);
const samplePartIIRound2 = processSeatMap(sampleDataPartIIRound2Text);

export { inputs, sample, sampleRound1, samplePartII, samplePartIIRound2 };
