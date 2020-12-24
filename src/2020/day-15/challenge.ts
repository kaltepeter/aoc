import { getHeapStatistics } from 'v8';

const updateSpokenValue = (pos: number, prevPos: number[] = []) => {
  let retVal = prevPos;
  // housekeeping, went from 12-15s to 1.5-3s for 300000 iterations (.slice(-2))
  if (prevPos.length > 1) {
    retVal = [...retVal.slice(-2), pos];
  } else if (prevPos.length > 0) {
    retVal = [...prevPos, pos];
  } else {
    retVal = [pos];
  }
  return retVal;
};

const playGame = (start: number[], iterationCount: number = 2020): number => {
  let lastTurn = start[-1];
  const spokenValues = new Map<number, number[]>();
  start.forEach((v, idx) => {
    spokenValues.set(v, updateSpokenValue(idx, spokenValues.get(v)));
  });
  const startLen = start.length;
  for (let i = startLen; i < iterationCount; i++) {
    if (!spokenValues.has(lastTurn)) {
      spokenValues.set(lastTurn, []);
    }
    const prevVal = spokenValues.get(lastTurn) || [];
    if (prevVal.length > 1) {
      const lastTwoNums = updateSpokenValue(i, prevVal);
      lastTurn = lastTwoNums[1] - lastTwoNums[0];
    } else {
      lastTurn = 0;
    }

    spokenValues.set(
      lastTurn,
      updateSpokenValue(i, spokenValues.get(lastTurn))
    );
    // console.log(`it: ${i}`);
  }
  // console.log(Object.keys(spokenValues).length)
  // console.log(getHeapStatistics())
  return lastTurn;
};

const testIt = (iterationCount: number) => {
  let count = 0;
  for (let i = 6; i < iterationCount; i++) {
    count = i;
  }
  return count;
};

export { playGame };
