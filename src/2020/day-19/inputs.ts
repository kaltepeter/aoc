import fs from 'fs';
import path from 'path';
import { keys } from 'ramda';
import { IMonsterMessages } from './challenge';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const readData = (t: string) =>
  t
    .split('\n')
    .filter((val: string) => !(val.trim() === ''))
    .reduce<IMonsterMessages>(
      (acc, v) => {
        if (v.match(/^\d+:.*/)) {
          const ruleParts = v.split(':');
          const key = +ruleParts[0];
          const value = ruleParts[1].trim().replace(/"/g, '');
          if (value.match(/[a-z]/i)) {
            acc.rules.set(key, value.trim());
          } else {
            acc.rules.set(
              key,
              value.split('|').map((val) =>
                val
                  .trim()
                  .split(' ')
                  .map((n) => +n)
              )
            );
          }
        } else {
          acc.messages.push(v.trim());
        }
        return acc;
      },
      { rules: new Map<number, string | number[][]>(), messages: [] }
    );

const readData2 = (t: string) =>
  t
    .split('\n')
    .filter((val: string) => !(val.trim() === ''))
    .reduce<any>(
      (acc, v) => {
        if (v.match(/^\d+:.*/)) {
          const ruleParts = v.split(':');
          const key = +ruleParts[0];
          const value = ruleParts[1].trim().replace(/"/g, '');
          if (value.match(/[a-z]/i)) {
            acc.rules.set(key, value.trim());
          } else {
            acc.rules.set(key, value.trim());
          }
        } else {
          acc.messages.push(v.trim());
        }
        return acc;
      },
      { rules: new Map<number, string>(), messages: [] }
    );

const inputs = readData2(text);
const sample = readData(sampleDataText);
const sample2 = readData2(sampleDataText);

export { inputs, sample, sample2 };
