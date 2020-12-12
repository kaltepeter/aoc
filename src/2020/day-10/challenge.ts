import { difference, fromPairs, gte, lte } from 'ramda';

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

const printChain = (adapters: number[]) => {
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
  fromPairs(Object.entries(adapterHash).filter(([k, v]) => v.length === count));

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
};
