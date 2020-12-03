import fs from 'fs';
import path from 'path';
const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const inputs: (string | number)[][] = text
  .split('\n')
  // empty converts to 0 so drop
  .filter((val: string) => !(val.trim() === ''))
  .map((val: string) => {
    const v = val.split(' ');
    const [min, max] = v[0].split('-');
    return [+min, +max, v[1].replace(':', ''), v[2]];
  });

export { inputs };
