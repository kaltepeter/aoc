import fs from 'fs';
import path from 'path';
import { processPassports } from './challenge';
const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const inputs = processPassports(text);

const validPassportsText = fs
  .readFileSync(path.join(__dirname, 'valid-passports.txt'))
  .toString('utf-8');

const validPassportsInputs = processPassports(validPassportsText);

const invalidPassportsText = fs
  .readFileSync(path.join(__dirname, 'invalid-passports.txt'))
  .toString('utf-8');

const invalidPassportsInputs = processPassports(invalidPassportsText);

export { inputs, validPassportsInputs, invalidPassportsInputs };
