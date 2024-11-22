import { LinkedList } from 'model/index';
import { join } from 'path';
import { range } from 'ramda';
import { writeToLog } from 'util/debug';

const LOG_FILE = join(__dirname, 'challenge.log');

const playCups = (cups: string[], maxMoves = 10, returnList = false) => {
  // const highest = Math.max(...cups.map((v) => +v));
  const highest =
    cups.length < 1000000 ? Math.max(...cups.map((v) => +v)) : 1000000;
  // const lowest = Math.min(...cups.map((v) => +v));
  const lowest = 1;
  const list = new LinkedList<string>();
  list.addAllSync(cups);

  // cups.map((v) => list.insertLast(v));
  let currentCup = list.getFirst();
  // run game
  for (let i = 0; i < maxMoves; i++) {
    const nextCup = currentCup?.next ? currentCup.next : list.getFirst();
    if (!nextCup || !nextCup.item) {
      break;
    }
    // get next three cups
    const nextThree: string[] = list.removeFrom(nextCup.item, 3);

    // handle end of list
    if (nextThree.length < 3) {
      while (nextThree.length < 3) {
        const firstItem = list.removeFirst();
        if (firstItem) {
          nextThree.push(firstItem);
        }
      }
    }

    let destCup: number;
    if (currentCup?.item) {
      // get destination cup
      destCup = currentCup.item ? +currentCup.item - 1 : -1;
      do {
        if (nextThree.includes(destCup.toString())) {
          destCup = +destCup - 1;
        } else if (destCup < lowest) {
          destCup = highest;
        }
      } while (nextThree.includes(destCup.toString()) || destCup < lowest);

      writeToLog(
        LOG_FILE,
        `i: ${i}: nextThree: ${nextThree.toString()}, current: ${
          currentCup.item
        }, dest: ${destCup}`
      );

      // place cups
      let targetVal = destCup.toString();
      while (nextThree.length > 0) {
        const val = nextThree.shift();
        if (val) {
          list.insertAfterFirst(targetVal, val);
          targetVal = val;
        }
      }

      currentCup = currentCup.next?.item ? currentCup.next : list.getFirst();
    }
  }
  if (returnList) {
    const res = list.listContents();
    const oneIdx = res.indexOf('1');
    return res.slice(oneIdx + 1, oneIdx + 3);
  } else {
    const res = list.listContents().join('').split('1');
    return `${res[1]}${res[0]}`;
  }
};

// const printV2List = (list: Map<number, number>, start: number) => {
//   let val = list.get(start);
//   if (!val) {
//     throw new Error(`Val not found.`);
//   }
//   const retVal: number[] = [];
//   do {
//     retVal.push(val);
//     val = list.get(val);
//   } while (val && val !== start);
//   return retVal.join('');
// };

const playCupsPartII = (cups: string[], maxMoves = 10) => {
  const highest =
    cups.length < 1000000 ? Math.max(...cups.map((v) => +v)) : 1000000;
  const lowest = 1;
  const listTracker = new Map<number, number>();

  // way simple, efficient linked list, with loop
  cups.forEach((c, idx) => {
    if (idx + 1 < cups.length) {
      listTracker.set(+c, +cups[idx + 1]);
    } else {
      listTracker.set(+c, +cups[0]); // circular
    }
  });

  let currentCup = +cups[0];
  // run game
  for (let i = 0; i < maxMoves; i++) {
    if (!currentCup) {
      throw new Error(`Cup not found.`);
    }

    // get next three cups
    let nextThree: number[] = [];
    let nextCup = listTracker.get(currentCup);
    do {
      if (nextCup) {
        nextThree = [...nextThree, nextCup];
        nextCup = listTracker.get(nextCup);
      }
    } while (nextThree.length < 3);

    // calc destCup
    let destCup: number = +currentCup - 1;
    do {
      if (nextThree.includes(destCup)) {
        destCup = +destCup - 1;
      } else if (destCup < lowest) {
        destCup = highest;
      }
    } while (nextThree.includes(destCup) || destCup < lowest);

    writeToLog(
      LOG_FILE,
      `i: ${i}: nextThree: ${nextThree.toString()}, current: ${currentCup}, dest: ${destCup}`
    );

    // place cups
    const destNextCup = listTracker.get(destCup);
    const lastOfThree = nextThree[nextThree.length - 1];
    const currentNextCup = listTracker.get(lastOfThree);
    if (!destNextCup || !currentNextCup) {
      throw new Error(`Can't find the next cups to update list.`);
    }
    listTracker.set(currentCup, currentNextCup);
    listTracker.set(destCup, nextThree[0]);
    listTracker.set(lastOfThree, destNextCup);

    const targetCup = listTracker.get(currentCup);
    if (targetCup) {
      currentCup = targetCup;
    }
  }

  const firstItem = listTracker.get(1);
  if (!firstItem) {
    throw new Error('first item not found');
  }
  const secondItem = listTracker.get(firstItem);
  return [firstItem, secondItem];
};

const getInputForAMillionCups = (cups: string[]) => {
  const inputNumbers = cups.map((v) => +v);
  const highest = Math.max(...inputNumbers);
  return [...inputNumbers, ...range(+highest + 1, 1000001)];
};

const calcStarLabels = (labels: number[]) =>
  labels.reduce((acc, v) => (acc *= v), 1);

export { calcStarLabels, getInputForAMillionCups, playCups, playCupsPartII };
