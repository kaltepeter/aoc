import { join } from 'path';
import { writeToLog } from 'util/debug';

const LOG_FILE = join(__dirname, 'challenge.log');
export interface IDockData {
  mask: string;
  memory: Array<{ loc: string; value: number }>;
}

const getMask = (m: string, prevVal: bigint): string => {
  const mask = m.split('');
  const prevB = convertToBinaryString(prevVal);
  const maskVal = prevB.split('');
  mask.forEach((maskBit, pos) => {
    const prevBit = prevB.substr(pos, 1);
    if (maskBit === 'X') {
      // get the bit of current val
      maskVal[pos] = prevBit;
    } else {
      maskVal[pos] = maskBit;
    }
  });
  // console.log(`mask: ${m}, maskVal: ${maskVal.join('')}, ${prevB}`);
  return maskVal.join('');
};

const convertToBinaryString = (num: bigint) =>
  num.toString(2).padStart(36, '0');

const getSumOfProgram = (memory: { [key: string]: bigint }): bigint =>
  Object.values(memory).reduce((acc, v) => {
    return (acc += v);
  }, BigInt(0));

const setBit = (n: bigint, bitIndex: bigint): bigint => {
  const bitMask = BigInt(1) << bitIndex;
  return n | bitMask;
};

const clearBit = (n: bigint, bitIndex: bigint): bigint => {
  const bitMask = ~(BigInt(1) << bitIndex);
  return n & bitMask;
};

const processDockingData = (data: IDockData[]) => {
  const programMemory: { [key: string]: bigint } = {};
  data.map((d) => {
    const mVal = getMask(d.mask, BigInt(0));
    d.memory.map(({ loc, value }) => {
      let res = BigInt(value) | BigInt(parseInt(mVal, 2));
      d.mask
        .split('')
        .reverse()
        .forEach((v, idx) => {
          if (v === '0') {
            res = clearBit(res, BigInt(idx));
          }
        });
      programMemory[loc] = res;
    });
  });
  return Number(getSumOfProgram(programMemory).valueOf());
};

const getMaskFromSeed = (address: string, mask: string): string => {
  const maskVal = address.split('');
  mask.split('').forEach((maskBit, pos) => {
    if (maskBit === '0') {
      maskVal[pos] = address[pos];
    } else {
      maskVal[pos] = maskBit;
    }
  });
  // console.log(`mask: ${m}, maskVal: ${maskVal.join('')}, ${prevB}`);
  return maskVal.join('');
};

// missing combos
const getMasksFromMaskString = (mask: string): Set<string> => {
  const masks: Set<string> = new Set();
  const xPos: number[] = mask
    .split('')
    .map((v, i) => {
      if (v === 'X') {
        return +i;
      }
    })
    .filter(Boolean as any);
  const xPosReversed = xPos.slice().reverse();
  const startM = mask.replace(/X/g, '0');
  masks.add(startM);
  let newM = startM;
  for (const i of xPos) {
    newM = startM.slice(0, i) + '1' + startM.slice(i + 1, startM.length);
    masks.add(newM);

    let newJM = newM;
    for (const j of xPosReversed) {
      if (j === i) {
        continue;
      }
      newJM = newM.slice(0, j) + '1' + newM.slice(j + 1, newM.length);
      masks.add(newJM);
    }
  }
  const ones = mask.replace(/X/g, '1');
  masks.add(ones);
  writeToLog(
    LOG_FILE,
    `${mask} : masks.size: ${masks.size} #getMasksFromMaskString`
  );
  return masks;
};

// https://dev.to/thibpat/comment/19729
const combinations = (n: number) => {
  const max = 2 ** n;
  const result = [];
  for (let i = 0; i < max; i++) {
    result.push(i.toString(2).padStart(n, '0'));
  }
  return result;
};

const programMemoryToString = (programMemory: { [key: string]: bigint }) =>
  JSON.stringify(
    programMemory,
    (key, value) => (typeof value === 'bigint' ? value.toString() : value) // return everything else unchanged
  );

const decodeDockDataV2 = (data: IDockData[]) => {
  writeToLog(LOG_FILE, `***** items: ${data.length} ******\n`);
  const programMemory: { [key: string]: bigint } = {};
  data.map((d) => {
    d.memory.map(({ loc, value }) => {
      const mVal = BigInt(loc);
      const binaryAddress = convertToBinaryString(mVal);
      writeToLog(LOG_FILE, `${binaryAddress} : loc: ${loc} #loc`);
      writeToLog(LOG_FILE, `${d.mask} : #d.mask`);

      const mask = getMaskFromSeed(binaryAddress, d.mask);
      const combos = combinations(
        mask.split('').filter((v) => v === 'X').length
      );
      writeToLog(LOG_FILE, `${mask} : #mask, ${combos.length} #combos`);
      const mList = getMasksFromMaskString(mask);
      const maskList = Array.from(mList).sort();

      combos.forEach((combo, idx) => {
        let xPos = 0;
        const a = mask.split('').map((v, i) => {
          if (v === 'X') {
            return combo[xPos++];
          }
          return +v | +mask;
        });
        programMemory[a.join('')] = BigInt(value);
      });
      writeToLog(LOG_FILE, programMemoryToString(programMemory));
    });
  });
  // console.log(programMemory);
  return Number(getSumOfProgram(programMemory).valueOf());
};

export {
  processDockingData,
  getSumOfProgram,
  convertToBinaryString,
  getMasksFromMaskString,
  decodeDockDataV2,
  getMaskFromSeed,
};
