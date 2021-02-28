import { LinkedList, LinkedListItem } from 'model/index';
import { join } from 'path';
import { writeToLog } from 'util/debug';

const LOG_FILE = join(__dirname, 'challenge.log');

const playCups = (input: string, maxMoves = 10) => {
  const cups = input.split('');
  const highest = Math.max(...cups.map((v) => +v));
  const lowest = Math.min(...cups.map((v) => +v));
  const list = new LinkedList<string>();
  cups.map((v) => list.insertLast(v));
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
        `nextThree: ${nextThree}, current: ${currentCup.item}, dest: ${destCup}`
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
  // console.log(list.listContents())
  const res = list.listContents().join('').split('1');
  return `${res[1]}${res[0]}`;
};

export { playCups };
