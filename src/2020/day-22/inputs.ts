import fs from 'fs';
import path from 'path';
import { Player } from './player';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const infiniteGameText = fs
  .readFileSync(path.join(__dirname, 'infinite-game.txt'))
  .toString('utf-8');

const readData = (t: string): Array<[string, number[]]> =>
  t
    .split('\n\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((val) => {
      const [name, cards] = val.split(':');
      return [
        name,
        cards
          .trim()
          .split('\n')
          .map((c) => +c),
      ];
    });

const inputs = readData(text);
const sample = readData(sampleDataText);
const infiniteGame = readData(infiniteGameText);

export { inputs, sample, infiniteGame };
