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
    let mVal = getMask(d.mask, BigInt(0));
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

export { processDockingData, getSumOfProgram, convertToBinaryString };
