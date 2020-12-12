import { IXmasData } from './inputs';

const getValidNumbers = (n: number, list: number[]) => {
  const val = list.filter((v) => {
    const num = n - v;
    if (n === v || num < 0) {
      return false;
    } else {
      return list.includes(num);
    }
  });
  return val;
};

const findInvalidNumber = (d: IXmasData): number[] => {
  const { data, preamble } = d;
  let prevVals = [...preamble];
  const invalidNums: number[] = [];
  data.forEach((d) => {
    const validNums = getValidNumbers(d, prevVals);
    if (validNums.length === 0) {
      invalidNums.push(d);
    }
    prevVals = [...prevVals.slice(1), d];
  });
  return invalidNums;
};

const findContiguousSet = (num: number, d: IXmasData): number[] => {
  const data = [...d.preamble, ...d.data];
  let foundSet: number[] = [];
  for (let i = 0; i < data.length; i++) {
    if (foundSet.length > 0) {
      break;
    }
    let sum = data[i];
    for (let n = i + 1; n < data.length; n++) {
      sum += data[n];
      if (sum > num) {
        i++;
        break;
      } else if (sum === num) {
        foundSet = [...data.slice(i, n + 1)];
        break;
      }
    }
  }
  return foundSet;
};

export { findInvalidNumber, getValidNumbers, findContiguousSet };
