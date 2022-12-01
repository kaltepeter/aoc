import fs from 'fs';
import path from 'path';

const text = fs
  .readFileSync(path.join(__dirname, '..', 'day-1', 'raw-input.txt'))
  .toString('utf8');

const inputs = text
  .split('\n')
  // empty converts to 0 so drop
  .filter((val: string) => !(val.trim() === ''))
  .map((val: string) => +val.trim());

export { inputs };
