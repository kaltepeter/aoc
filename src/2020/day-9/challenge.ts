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
  data.forEach((d, idx) => {
    const validNums = getValidNumbers(d, prevVals);
    if (validNums.length === 0) {
      invalidNums.push(d);
    }
    prevVals = [...prevVals.slice(1), d];
  });
  return invalidNums;
};

export { findInvalidNumber, getValidNumbers };
