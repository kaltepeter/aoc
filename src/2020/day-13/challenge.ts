const getTimes = (timeList: string) => timeList.split(',').map((v) => +v);

const findEarliestBusTime = ([startTime, t]: string[]) => {
  const times = getTimes(t);
  let curTime = +startTime;
  let nextBus = 0;
  const validTimes: number[] = times.filter((v) => !Number.isNaN(v));
  console.log(startTime, times);
  do {
    curTime += 1;
    for (const b of validTimes) {
      if (curTime % b === 0) {
        console.log('found: ', b, curTime);
        nextBus = b;
        break;
      }
    }
  } while (nextBus === 0);
  console.log(curTime - +startTime, nextBus);
  return (curTime - +startTime) * nextBus;
};

export { findEarliestBusTime };
