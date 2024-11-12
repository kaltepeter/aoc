const getTimes = (timeList: string) => timeList.split(',').map((v) => +v);
const getValidTimes = (timeList: string) =>
  timeList.split(',').map((v) => (v === 'x' ? 1 : +v));

const findEarliestBusTime = ([startTime, t]: string[]) => {
  const times = getTimes(t);
  let curTime = +startTime;
  let nextBus = 0;
  const validTimes: number[] = times.filter((v) => !Number.isNaN(v));
  do {
    curTime += 1;
    for (const b of validTimes) {
      if (curTime % b === 0) {
        // console.log('found: ', b, curTime);
        nextBus = b;
        break;
      }
    }
  } while (nextBus === 0);
  // console.log(curTime - +startTime, nextBus);
  return (curTime - +startTime) * nextBus;
};

// https://www.geeksforgeeks.org/using-chinese-remainder-theorem-combine-modular-equations/
// rosetta code, chinese remainder theorem
export const crt = (num: number[], rem: number[]) => {
  let sum = 0;
  const prod = num.reduce((a, c) => a * c, 1);

  for (let i = 0; i < num.length; i++) {
    const [ni, ri] = [num[i], rem[i]];
    const p = Math.floor(prod / ni);
    sum += ri * p * mulInv(p, ni);
  }
  return sum % prod;
};

const mulInv = (a: number, b: number) => {
  const b0 = b;
  let [x0, x1] = [0, 1];

  if (b === 1) {
    return 1;
  }
  while (a > 1) {
    const q = Math.floor(a / b);
    [a, b] = [b, a % b];
    [x0, x1] = [x1 - q * x0, x0];
  }
  if (x1 < 0) {
    x1 += b0;
  }
  return x1;
};

const validateOutput = (num: number, list: number[]) => {
  let isValid = true;
  list.forEach((n, idx) => {
    if ((num + idx) % n !== 0) {
      console.log(
        '🚀 ~ file: challenge.ts ~ line 60 ~ list.forEach ~ num',
        idx,
        n
      );
      isValid = false;
    }
  });
  return isValid;
};

// cheated cuz math sucks
const findBusTimes = (data: string) => {
  const busses: [number, number][] = data
    .split(',')
    .map(
      (bus, offset) =>
        (bus === 'x' ? [1, offset] : [Number(bus), offset]) as [number, number]
    )
    .sort((a, z) => a[0] - z[0]); // Makes it a littttle bit faster

  let sum = 0;
  let product = 1;

  for (const [bus, offset] of busses) {
    while ((sum + offset) % bus !== 0) {
      sum += product;
    }

    product *= bus;
  }

  return sum;
};

const getTableOfBusses = ([_startTime, t]: string[]) => {
  const validTimes: number[] = getValidTimes(t);
  const remainders: number[] = new Array(validTimes.length)
    .fill(1)
    .map((_n, idx) => validTimes.length - idx);
  // console.log(new Array(validTimes.length).fill(1).map((v, i) => i));
  const res = crt(validTimes, remainders);
  return res - validTimes.length;
};

export {
  findEarliestBusTime,
  getTableOfBusses,
  validateOutput,
  getValidTimes,
  findBusTimes,
};
