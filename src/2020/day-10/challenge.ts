import { difference, findIndex, fromPairs, gte, lte } from 'ramda';

export interface IAdapterHash {
  [key: string]: number[];
}

const getBuiltInDeviceJoltage = (adapters: number[]) =>
  Math.max(...adapters) + 3;

const getRangeOfJoltage = (joltage: number, adapters: number[]): number[] =>
  adapters.filter((v) => v >= joltage - 3 && v <= joltage + 3 && joltage !== v);

const getAdapterHash = (adapters: number[]): IAdapterHash => {
  const trackAdapters: IAdapterHash = {};
  adapters.forEach((a) => {
    const aList = getRangeOfJoltage(a, [...adapters]);
    trackAdapters[a] = aList;
  });
  return trackAdapters;
};

const printChain = (adapters: number[] | string[]) => {
  console.log(adapters.join(' > '));
};

const sortAdapters = (adapters: number[]): number[] =>
  adapters.map((a) => +a).sort((a, b) => a - b);

const validateAdapterChain = (adapters: number[]): number[] => {
  const aList = sortAdapters(adapters);
  const invalid = aList.filter((a, idx) => {
    const prev = idx >= 1 ? aList[idx - 1] : 0;
    const next = idx < aList.length - 1 ? aList[idx + 1] : aList[idx];
    return gte(a, prev - 3) && lte(a, next + 3);
  });
  return difference(aList, invalid);
};

const findAdapterListByPossibleCount = (
  adapterHash: IAdapterHash,
  count: number
) =>
  fromPairs(Object.entries(adapterHash).filter(([_, v]) => v.length === count));

const removeOptionFromAdapterList = (
  adapterHash: IAdapterHash,
  adapterToRemove: number
): IAdapterHash =>
  fromPairs(
    Object.entries(adapterHash).map(([k, v]) => [
      k,
      v.filter((a) => a !== adapterToRemove),
    ])
  );

const printDeltas = (adapters: number[]) => {
  const deviceJoltage = getBuiltInDeviceJoltage(adapters);
  console.log(adapters.length);
  const aList = [...sortAdapters(adapters), deviceJoltage];
  let possibleRemovals: number[] = [];
  printChain(aList);
  const deltaList: number[] = [];
  const listStart = findIndex((n) => gte(n, 3), aList) - 1;
  for (let i = aList.length - 1; i > listStart; i--) {
    const delta = i === 0 ? aList[i] - 0 : aList[i] - aList[i - 1];
    deltaList.push(delta);
    const twoBefore = i >= 2 ? aList[i - 2] : 0;
    const prev = i >= 1 ? aList[i - 1] : 0;
    const cur = aList[i];
    if (cur - twoBefore >= 3) {
      continue;
    } else {
      // console.log(`cur: ${cur}, prev: ${prev}, twoBefore: ${twoBefore}`);
      possibleRemovals = [...possibleRemovals, prev];
    }
  }
  console.log(possibleRemovals);
};

const getCombinations = (adapters: number[]): number | undefined => {
  const deviceJoltage = getBuiltInDeviceJoltage(adapters);
  const aList = [0, ...sortAdapters(adapters), deviceJoltage];
  const counts = new Array(aList.length) as number[];
  counts[0] = 1;

  for (let i = 1; i < aList.length; i++) {
    let backIdx = i;
    const curValue = aList[i];
    counts[i] = 0;

    while (backIdx >= 0 && curValue - aList[backIdx] <= 3) {
      counts[i] += counts[backIdx];
      backIdx--;
    }
  }

  return counts.pop();
};

const getDeltasOfAdapters = (adapters: number[]): { [key: string]: number } => {
  const deltaCounts: { [key: string]: number } = {};
  const deviceJoltage = getBuiltInDeviceJoltage(adapters);
  const aList = [...sortAdapters(adapters), deviceJoltage];
  for (let i = 0; i < aList.length; i++) {
    const delta = i === 0 ? aList[i] - 0 : aList[i] - aList[i - 1];
    if (deltaCounts[delta]) {
      deltaCounts[delta] += 1;
    } else {
      deltaCounts[delta] = 1;
    }
  }

  return deltaCounts;
};

export {
  getBuiltInDeviceJoltage,
  getRangeOfJoltage,
  getAdapterHash,
  getDeltasOfAdapters,
  validateAdapterChain,
  printChain,
  findAdapterListByPossibleCount,
  removeOptionFromAdapterList,
  sortAdapters,
  printDeltas,
  getCombinations,
};
