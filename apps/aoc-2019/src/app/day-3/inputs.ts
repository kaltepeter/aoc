import fs from 'fs';
import path from 'path';

const text = fs
  .readFileSync(path.join(__dirname, '..', 'day-3', 'raw-input.txt'))
  .toString('utf8');

const inputs = text
  .split(',')
  .filter((val: string) => !(val.trim() === ''))
  .map((val: string) => +val.trim());
export { inputs };
