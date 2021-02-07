import fs from 'fs';
import path from 'path';

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const readData = (t: string): string[][] =>
  t
    .split('\n\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((v) => v.split(':'))
    .map(([tile, board]) => [tile.replace(/Tile /, ''), board.trim()]);

const inputs = readData(text);
const sample = readData(sampleDataText);

export { inputs, sample };
