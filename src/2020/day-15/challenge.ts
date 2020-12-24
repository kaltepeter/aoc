const playGame = (start: number[]): number => {
  const turns = [...start];
  const spokenValues: { [key: string]: number[] } = {};
  start.forEach((v, idx) => {
    spokenValues[v] = spokenValues[v] ? [...spokenValues[v], idx] : [idx];
  });
  // let lastNum = start[start.length - 1];
  for (let i = start.length; i < 2020; i++) {
    let lastNum = turns.slice(-1)[0];
    const lastNumPositions = spokenValues[lastNum] ? spokenValues[lastNum] : [];
    const lastTwoNums =
      lastNumPositions.length > 1 ? lastNumPositions.slice(-2) : -1;
    if (lastTwoNums !== -1) {
      lastNum = lastTwoNums[1] - lastTwoNums[0];
    } else {
      lastNum = 0;
    }
    spokenValues[lastNum] = spokenValues[lastNum]
      ? [...spokenValues[lastNum], i]
      : [i];
    turns.push(lastNum);
  }
  return turns.slice(-1)[0];
};

export { playGame };
