import fs from 'fs';
import path from 'path';

interface IXmasData {
  preamble: number[];
  data: number[];
}

const text = fs
  .readFileSync(path.join(__dirname, 'raw-input.txt'))
  .toString('utf-8');

const sampleDataText = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const processXmasData = (t: string): number[] =>
  t
    .split('\n')
    .filter((val: string) => !(val.trim() === ''))
    .map((v) => +v);

const inputData = processXmasData(text);
const sampleData = processXmasData(sampleDataText);

const getXmasDataFromArray = (
  d: number[],
  preambleSize: number
): IXmasData => ({
  preamble: d.slice(0, preambleSize),
  data: d.slice(preambleSize),
});

const inputs = getXmasDataFromArray(inputData, 25);

const sample = getXmasDataFromArray(sampleData, 5);
export { inputs, sample, IXmasData };
